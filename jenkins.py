#!/usr/bin/env python3

import argparse
import glob
import os
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser(description="Testing script")
parser.add_argument('--shared', action='store_true', help='Build shared libs')
parser.add_argument(
    '--install-boo', action='store_true', help='Install boo and run'
)
cmd_args = parser.parse_args()

cwd = os.getcwd()
exe_dir = os.path.join(cwd, '_install', 'bin')

if not cmd_args.install_boo and cmd_args.shared:
  # windows and cygwin
  os.environ['PATH'] = '{};{}'.format(exe_dir, os.environ['PATH'])

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

if os.path.exists('_install'):
  shutil.rmtree('_install')

if os.name == 'nt':
  do_call(['where', 'cmake'])
else:
  do_call(['which', 'cmake'])

do_call(['cmake', '--version'])
install_dir = os.path.join('_install')

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
      '-DCMAKE_BUILD_TYPE={}'.format(buildtype),
      '-DCMAKE_INSTALL_PREFIX={}'.format(install_dir)
  ]
  if buildtype != 'Release':
    args += ['-DCMAKE_{}_POSTFIX=-{}'.format(buildtype.upper(), buildtype)]
  if verbose:
    args += ['-DCMAKE_VERBOSE_MAKEFILE=ON']
  if cmd_args.shared:
    args += ['-DBUILD_SHARED_LIBS=ON']
  else:
    args += ['-DBUILD_SHARED_LIBS=OFF']

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

run_build('Foo', 'Release', install=True, verbose=False, test=False)
run_build('Foo', 'Debug', install=True, verbose=False, test=False)

if cmd_args.install_boo:
  run_build('Boo', 'Release', install=True, verbose=True, test=False)
  run_build('Boo', 'Debug', install=True, verbose=True, test=False)
  executables = glob.glob(os.path.join(exe_dir, 'boo*'))
  if len(executables) != 2:
    sys.exit('Expected two executables')
  for x in executables:
    do_call([x])
else:
  run_build('Boo', 'Release', install=False, verbose=True, test=True)
  run_build('Boo', 'Debug', install=False, verbose=True, test=True)
