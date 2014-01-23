#!/bin/bash -e

rm -rf _builds
rm -rf _install

CMAKE=cmake

echo "Foo Release"
${CMAKE} -HFoo -B_builds/Foo-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
${CMAKE} --build _builds/Foo-release --target install

echo "Foo Debug"
${CMAKE} -HFoo -B_builds/Foo-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
${CMAKE} --build _builds/Foo-debug --target install

echo "Boo Release"
${CMAKE} -HBoo -B_builds/Boo-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="`pwd`/_install" -DCMAKE_VERBOSE_MAKEFILE=ON
${CMAKE} --build _builds/Boo-release

echo "Boo Debug"
${CMAKE} -HBoo -B_builds/Boo-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="`pwd`/_install" -DCMAKE_VERBOSE_MAKEFILE=ON
${CMAKE} --build _builds/Boo-debug
