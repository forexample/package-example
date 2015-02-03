#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys

def do_call(args):
  oneline = ''
  for i in args:
    oneline += '"{}"'.format(i)
  print('[{}]> {}'.format(os.getcwd(), oneline))
  try:
    subprocess.check_call(args)
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

def run_build(projname, buildtype, install, verbose):
  if buildtype:
    dir_tag = buildtype
  else:
    dir_tag = 'noconfig'
  print('-' * 80)
  print("+ {} {}".format(projname, dir_tag))
  print('-' * 80)
  build_dir = os.path.join('_builds', '{}-{}'.format(projname, dir_tag))
  install_dir = os.path.join('_install')
  args = [
      'cmake',
      '-H{}'.format(projname),
      '-B{}'.format(build_dir),
      '-DCMAKE_INSTALL_PREFIX={}'.format(install_dir)
  ]
  if buildtype:
    args += ['-DCMAKE_BUILD_TYPE={}'.format(buildtype)]
  if verbose:
    args += ['-DCMAKE_VERBOSE_MAKEFILE=ON']
  do_call(args)

  args = ['cmake', '--build', build_dir]
  if buildtype:
    args += ['--config', buildtype]
  if install:
    args += ['--target', 'install']
  do_call(args)

run_build('Foo', 'Release', install=True, verbose=False)
run_build('Foo', 'Debug', install=True, verbose=False)
run_build('Boo', 'Release', install=False, verbose=True)
run_build('Boo', 'Debug', install=False, verbose=True)
run_build('Boo', '', install=False, verbose=True)
