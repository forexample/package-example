#!/usr/bin/env python3

import argparse
import glob
import os
import platform
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description="Testing script")
parser.add_argument('--shared', action='store_true', help='Build shared libs')
parser.add_argument(
    '--install-boo', action='store_true', help='Install boo and run'
)
parser.add_argument(
    '--monolithic', action='store_true', help='Build all in one'
)
parser.add_argument(
    '--install-dir', help='Custom install directory'
)
parser.add_argument(
    '--generator', help='CMake generator'
)
cmd_args = parser.parse_args()

cwd = os.getcwd()

def do_call(args):
  oneline = ''
  for i in args:
    oneline += ' "{}"'.format(i)
  print('[{}]>{}'.format(os.getcwd(), oneline))
  try:
    subprocess.check_call(args, env=os.environ)
  except subprocess.CalledProcessError as error:
    print(error)
    print(error.output)
    sys.exit(1)

if os.path.exists('_builds'):
  shutil.rmtree('_builds')

# Warning: do not remove cmd_args.install_dir - it may be system!
if os.path.exists('_install'):
  shutil.rmtree('_install')

if os.name == 'nt':
  do_call(['where', 'cmake'])
else:
  do_call(['which', 'cmake'])

do_call(['cmake', '--version'])

if cmd_args.install_dir:
  install_dir = cmd_args.install_dir
else:
  install_dir = os.path.join(cwd, '_install')

exe_dir = os.path.join(install_dir, 'bin')

if platform.system() == 'Windows' or platform.system().startswith('CYGWIN'):
  # Update PATH for DLL platforms
  windows_path_update = True
else:
  windows_path_update = False

if cmd_args.install_boo:
  # We will install 'boo' executable so it should work without PATH modification
  windows_path_update = False

if not cmd_args.shared:
  # No need to update PATH if libraries are static
  windows_path_update = False

if windows_path_update:
  os.environ['PATH'] = '{};{}'.format(exe_dir, os.environ['PATH'])

if cmd_args.generator == 'MinGW Makefiles':
  os.environ['PATH'] = '{};{}'.format(
      os.environ['MINGW_PATH'], os.environ['PATH']
  )

if cmd_args.generator == 'MSYS Makefiles':
  os.environ['PATH'] = '{};{}'.format(
      os.environ['MSYS_PATH'], os.environ['PATH']
  )

def run_build(projname, buildtype, install, verbose, test):
  os.chdir(cwd)

  print('-' * 80)
  print("+ {} {}".format(projname, buildtype))
  print('-' * 80)

  build_dir = os.path.join('_builds', '{}-{}'.format(projname, buildtype))

  args = [
      'cmake',
      '-H{}'.format(projname),
      '-B{}'.format(build_dir),
      '-DCMAKE_BUILD_TYPE={}'.format(buildtype)
  ]

  if install:
    args += ['-DCMAKE_INSTALL_PREFIX={}'.format(install_dir)]
  else:
    args += ['-DCMAKE_PREFIX_PATH={}'.format(install_dir)]

  if buildtype != 'Release':
    args += ['-DCMAKE_{}_POSTFIX=-{}'.format(buildtype.upper(), buildtype)]

  if verbose:
    args += ['-DCMAKE_VERBOSE_MAKEFILE=ON']

  if cmd_args.shared:
    args += ['-DBUILD_SHARED_LIBS=ON']
  else:
    args += ['-DBUILD_SHARED_LIBS=OFF']

  if cmd_args.generator:
    args += ['-G{}'.format(cmd_args.generator)]

  do_call(args)

  args = ['cmake', '--build', build_dir, '--config', buildtype]
  if install:
    args += ['--target', 'install']
  do_call(args)

  if test:
    os.chdir(build_dir)
    args = ['ctest', '-C', buildtype, '-VV']
    do_call(args)
    os.chdir(cwd)

run_test_after_install = False
if cmd_args.monolithic:
  run_build('.', 'Release', install=True, verbose=True, test=True)
  run_build('.', 'Debug', install=True, verbose=True, test=True)
  run_test_after_install = True
else:
  run_build('Foo', 'Release', install=True, verbose=False, test=False)
  run_build('Foo', 'Debug', install=True, verbose=False, test=False)

  if cmd_args.install_boo:
    run_build('Boo', 'Release', install=True, verbose=True, test=True)
    run_build('Boo', 'Debug', install=True, verbose=True, test=True)
    run_test_after_install = True
  else:
    run_build('Boo', 'Release', install=False, verbose=True, test=True)
    run_build('Boo', 'Debug', install=False, verbose=True, test=True)

if run_test_after_install:
  executables = glob.glob(os.path.join(exe_dir, 'boo*'))

  try:
    # when installed to system
    executables.remove('/usr/bin/bootctl')
  except ValueError:
    pass

  if len(executables) != 2:
    sys.exit('Expected two executables')
  for x in executables:
    do_call([x])
