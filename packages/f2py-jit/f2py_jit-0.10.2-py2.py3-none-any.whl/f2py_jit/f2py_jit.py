# Part of this code is adapted from numpy.f2py module
# Copyright 2001-2005 Pearu Peterson all rights reserved,
# Pearu Peterson <pearu@cens.ioc.ee>
# Permission to use, modify, and distribute this software is given under the
# terms of the NumPy License, as follows:

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#     * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.

#     * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided
#        with the distribution.

#     * Neither the name of the NumPy Developers nor the names of any
#        contributors may be used to endorse or promote products derived
#        from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
Create python modules from Fortran code just-in-time.

Two main steps: first build, then import the module. This can be done
in a single step using the `jit()` function.

The `modules_dir` directory contains the compiled modules and is
created in the current path (cwd).
"""

from __future__ import division, absolute_import, print_function
import importlib
import hashlib
import json
import sys
import subprocess
import os
import glob
import numpy
import logging

_log = logging.getLogger(__name__)
modules_dir = '.f2py-jit'
# modules_dir = os.path.expanduser('~/.cache/f2py-jit')

__all__ = ['jit', 'compile_module', 'build_module',
           'import_module', 'available_modules', 'clear_modules']


# This is necessary when the f2py-jit is installed as a package it seems
if '' not in sys.path:
    sys.path.insert(0, '')


def create_modules_path():
    """Make sure modules_dir exists and is a package"""
    if not os.path.exists(modules_dir):
        try:
            os.makedirs(modules_dir)
        except FileExistsError:
            # Ignore error if another process has been able to create
            # this in the meantime (yes, it happened!)
            pass
    path = os.path.join(modules_dir, '__init__.py')
    if not os.path.exists(path):
        with open(path, 'w') as _:
            pass
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)

def _f2py(name, src, args):

    # Run f2py
    c = [sys.executable,
         '-c',
         'import numpy.f2py as f2py2e; f2py2e.main()'] + args
    #print('DEBUG:', c)
    output, status = _execute(c)
    if os.path.basename(src).startswith('tmp'):
        artefacts = [src]
    else:
        artefacts = []
    return output, status, artefacts


def _f90wrap(name, src, args):
    # TODO: safer to compile/build in a separate tmp (for *.mod)
    # Set paths
    base = os.path.basename(src)
    obj = os.path.splitext(base)[0] + '.o'  # 'library.o'
    wrap = f'f90wrap_{base}'  # 'f90wrap_library.f90'
    lib = f'lib{base}.a'
    # print('DEBUG:', src, obj, wrap, lib)
    
    # Find constructors
    constructors = []
    with open(src) as fh:
        for line in fh:
            if line.lstrip().lower().startswith('subroutine new_'):
                signature = line.split()[1]
                subroutine = signature.split('(')[0].strip()
                constructors.append(subroutine)

    # Run compilation pipeline
    output = ''
    # TODO: enable flags via args, something is wrong with this
    #['f2py-f90wrap'] + args + ['-I.', wrap, '-L.', f'-l{base}']]:
    for c in [['gfortran', '-c', src],
              ['ar', 'rc', lib, obj],
              ['ranlib', lib],
              ['f90wrap', '-m', name, '-C'] + constructors + ['-D', 'delete', '-M', src],
              ['f2py-f90wrap', '-m', f'_{name}', '-c', '-I.', wrap, '-L.', f'-l{base}']]:
        # '-k', 'kind_map',     -> f90wrap
        # print('DEBUG:', ' '.join(c))
        output, status = _execute(c, append=output)
        if status != 0:
            break

    # Clean up
    artefacts = [obj, wrap, lib]
    return output, status, artefacts


def _require_f90wrap(source):
    for line in source.split('\n'):
        if line.lstrip().lower().startswith('type'):
            return True
    return False


# Adapted from numpy.f2py
def compile_module(source,
                   name,
                   extra_args='',
                   verbose=True,
                   quiet=False,
                   source_fn=None,
                   extension='.f90'):
    """
    Build extension module from a Fortran source string with f2py.

    Parameters
    ----------
    source : str or bytes
        Fortran source of module / subroutine to compile
    name : str, optional
        The name of the compiled python module
    extra_args : str or list, optional
        Additional parameters passed to f2py (Default value = '')
    verbose : bool, optional
        Print f2py output to screen (Default value = True)
    source_fn : str, optional
        Name of the file where the fortran source is written.
        The default is to use a temporary file with the extension
        provided by the `extension` parameter
    extension : {'.f', '.f90'}, optional
        Filename extension if `source_fn` is not provided.
        The extension tells which fortran standard is used.
        The default is `.f`, which implies F77 standard.
    quiet :
         (Default value = False)

    Returns
    -------


    """
    import tempfile

    # Surely quiet means not verbose
    if quiet:
        verbose = False

    # Compile source directly in modules_dir path
    # we get back at cwd where we were at the end of the function
    cwd = os.getcwd()
    create_modules_path()
    os.chdir(os.path.abspath(modules_dir))

    # TODO: we could assume the source is a string, not a file anymore at this stage
    if source_fn is None:
        f, fname = tempfile.mkstemp(suffix=extension)
        # f is a file descriptor so need to close it
        # carefully -- not with .close() directly
        os.close(f)
    else:
        fname = source_fn

    # If source looks like a path but does not exist, exit
    if os.path.splitext(source)[-1] in ['.f90', '.F90'] and not os.path.exists(source):
        raise IOError(f'file {source} does not exist')

    # Input source `src` can be a f90 file or a string containing f90 code
    if os.path.exists(source):
        with open(source) as fh:
            source = fh.read()

    if not isinstance(source, str):
        source = str(source, 'utf-8')

    assert len(source) > 0, 'source is empty'

    if _require_f90wrap(source):
        run_backend = _f90wrap
    else:
        run_backend = _f2py
    
    try:
        with open(fname, 'w') as f:
            f.write(source)
            
        # Assemble f2py arguments
        import shlex
        args = ['-c', '-m', name, f.name]
        if isinstance(extra_args, numpy.compat.basestring):
            is_posix = (os.name == 'posix')
            extra_args = shlex.split(extra_args, posix=is_posix)
        args.extend(extra_args)

        # Build extension
        output, status, artefacts = run_backend(name, f.name, args)

        # Recolorize output
        import re

        class colors:
            """ """
            OK = '\033[92m'
            WARN = '\033[93m'
            FAIL = '\033[91m'
            END = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
        output = re.sub('[eE]rror', colors.UNDERLINE + colors.BOLD +
                        colors.FAIL + 'Error' + colors.END, output)
        output = re.sub('[wW]arning', colors.UNDERLINE + colors.BOLD +
                        colors.WARN + 'warning' + colors.END, output)

        if verbose or (status != 0 and not quiet):
            print(output)
        if status != 0:
            raise RuntimeError('f2py compilation failed')
    finally:
        for fname in artefacts:
            os.remove(fname)

        # Clear the cache every time a new module is compiled
        if sys.version_info[0] > 2:
            importlib.invalidate_caches()

        # Get back where we were
        os.chdir(cwd)

def _execute(c, append=None):
    try:
        output = subprocess.check_output(c, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        status, output = exc.returncode, exc.output
    else:
        status = 0
    try:
        output = output.decode()
    except UnicodeDecodeError:
        pass
    
    if append:
        append += output
        return append, status
    else:
        return output, status


def build_module(source, metadata=None, extra_args='', verbose=False):
    """
    Build a Fortran module from source and return its unique uid,
    which can be used to import the module with `import_module()`

    Parameters
    ----------
    source : str
         Fortran source of module or subroutine to compile
    metadata : dict
         Metadata to identify the module (Default value = None)
    extra_args : str
         Command line arguments passed to `f2py` (Default value = '')
    verbose : bool
         (Default value = False)

    Returns
    -------
    uid : str
         The unique module uid
    """
    # Lock from https://stackoverflow.com/questions/4843359/python-lock-a-file
    import fcntl

    def _lock(fh):
        ''' acquire exclusive lock file access '''
        locked_file_descriptor = open(fh + '.lock', 'w+')
        fcntl.lockf(locked_file_descriptor, fcntl.LOCK_EX)
        return locked_file_descriptor

    def _unlock(locked_file_descriptor):
        ''' release exclusive lock file access '''
        locked_file_descriptor.close()

    # This is a non-pythonic check for list or tuple
    if isinstance(source, list) or isinstance(source, tuple):
        txt = ''
        for path in source:
            with open(path) as fh:
                txt += fh.read()
                txt += '\n'
        source = txt

    # If we pass a file we extract the source from it
    if os.path.exists(source):
        with open(source) as fh:
            source = fh.read()

    # We get the metadata as string and append it to the source
    # to get a unique id of the (source, metadata) via the checksum
    source_metadata = source + str(metadata)
    uid = hashlib.md5(source_metadata.encode('utf-8')).hexdigest()
    import string
    def repl(digit_or_number):
        if digit_or_number in [str(_) for _ in range(0, 10)]:
            return string.ascii_lowercase[int(digit_or_number)]
        else:
            return digit_or_number
    uid = ''.join([repl(x) for x in uid])

    # Check if module has been compiled already
    create_modules_path()
    module_db = os.path.join(modules_dir, uid) + '.json'
    # Wait in case some other process is compiling this very module.
    # Lock the module path, so that we can safely read/write it.
    lock_fd = _lock(module_db)
    try:
        if not os.path.exists(module_db):
            # The module has not been compiled yet, so let's do it and add a metadata file
            compile_module(source, uid, verbose=verbose, extra_args=extra_args)
            with open(module_db, 'w') as fh:
                json.dump(metadata, fh)
        else:
            # The module is already present, we can reuse this uid. We
            # also ensure it is accessible. If not, the f2py-jit database
            # is in an inconsistent state.
            assert uid in available_modules(), f"f2py_jit database may be corrupted, remove folder {modules_dir} and try again"
    except:
        raise
    finally:
        # We always unlock the module at the end
        _unlock(lock_fd)

    return uid


def import_module(path, quiet=False):
    """


    Parameters
    ----------
    name :

    quiet :
         (Default value = False)

    Returns
    -------

    """
    import pkgutil
    try:
        f90 = importlib.import_module(path)
        importlib.invalidate_caches()
        return f90
    except (ImportError, ModuleNotFoundError):
        if not quiet:
            print('problem importing module {}'.format(path))
        raise


def jit(source, flags='', extra_args='', verbose=False, inline=False, skip='', only=''):
    """
    Single-step just-in-time build and import of Fortran
    `source` code, which can be either a path or a string with f90
    code

    Parameters
    ----------
    source :

    flags : str
         (Default value = '')
    extra_args : str
         (Default value = '')
    verbose : bool
         (Default value = False)
    inline : bool
         (Default value = False)

    Returns
    -------
    f90 : module
    """
    from .finline import inline_source
    if inline:
        source = inline_source(source)
    # When flags are passed explicitly, we must blank --opt else we
    # inherit the f2py defaults
    if len(flags) > 0:
        extra_args = '--opt="" --f90flags="{}" {}'.format(flags, extra_args)
    if len(skip) > 0:
        extra_args += 'skip: {} :'.format(skip)
    if len(only) > 0:
        extra_args += 'only: {} :'.format(only)
    uid = build_module(source, extra_args=extra_args, verbose=verbose)
    f90 = import_module(uid)
    return f90


def available_modules():
    """Return a list of available modules"""
    if os.path.exists(modules_dir):
        import pkgutil
        sub_modules = []
        for importer, modname, ispkg in pkgutil.iter_modules([modules_dir]):
            sub_modules.append(modname)
        return sub_modules
    else:
        return []


def clear_modules():
    """Clean modules from cache directory"""
    import shutil

    if os.path.exists(modules_dir):
        shutil.rmtree(modules_dir)
    importlib.invalidate_caches()
