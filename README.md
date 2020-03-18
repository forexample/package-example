[![Build Status][master]][repo] [![Build status](https://ci.appveyor.com/api/projects/status/oln2ks60gs8fs5ux/branch/master?svg=true)](https://ci.appveyor.com/project/ruslo/package-example/branch/master)

[master]: https://travis-ci.org/forexample/package-example.svg?branch=master
[repo]: https://travis-ci.org/forexample/package-example

### Install Foo

Install project `Foo` in `Debug` and `Release` variants (`Makefile` generator):
``` bash
> cmake -HFoo -B_builds/Foo-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_DEBUG_POSTFIX=d -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
> cmake --build _builds/Foo-debug --target install
...
Install the project...
-- Install configuration: "Debug"
-- Installing: /.../_install/lib/libbard.a
-- Installing: /.../_install/lib/libbazd.a
-- Installing: /.../_install/include/foo
-- Installing: /.../_install/include/foo/Bar.hpp
-- Installing: /.../_install/include/foo/Baz.hpp
-- Installing: /.../_install/include/foo/BAR_EXPORT.h
-- Installing: /.../_install/include/foo/BAZ_EXPORT.h
-- Installing: /.../_install/lib/cmake/Foo/FooConfig.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooConfigVersion.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets-debug.cmake
```

```bash
> cmake -HFoo -B_builds/Foo-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
> cmake --build _builds/Foo-release --target install
...
Install the project...
-- Install configuration: "Release"
-- Installing: /.../_install/lib/libbar.a
-- Installing: /.../_install/lib/libbaz.a
-- Up-to-date: /.../_install/include/foo
-- Up-to-date: /.../_install/include/foo/Bar.hpp
-- Up-to-date: /.../_install/include/foo/Baz.hpp
-- Installing: /.../_install/include/foo/BAR_EXPORT.h
-- Installing: /.../_install/include/foo/BAZ_EXPORT.h
-- Installing: /.../_install/lib/cmake/Foo/FooConfig.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooConfigVersion.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets-release.cmake
```

Note that:
* library target `bar` for different build types has different names: `libbar.a` and `libbard.a`
* header files is equal for both variants
* cmake-config files `FooConfig.cmake`, `FooConfigVersion.cmake` and `FooTargets.cmake` is equal for both variants
* `FooTargets-release.cmake` set `Release` imported target properties, e.g. `IMPORTED_LOCATION_RELEASE`
* `FooTargets-debug.cmake` set `Debug` imported target properties, e.g. `IMPORTED_LOCATION_DEBUG`

Note:
* For `-H` see: https://cgold.readthedocs.io/en/latest/glossary/-H.html

### Boo (use installed Foo)

Easiest way to find and include `FooConfig.cmake` file is to set `CMAKE_INSTALL_PREFIX`:
```bash
> cmake -HBoo -B_builds/Boo -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
```

Also `CMAKE_PREFIX_PATH` and `Foo_DIR` can be used (do not forget to **remove** `_builds/Boo` directory
before every configure):

```bash
> cmake -HBoo -B_builds/Boo -DCMAKE_PREFIX_PATH="`pwd`/_install"
> cmake -HBoo -B_builds/Boo -DFoo_DIR="`pwd`/_install/lib/cmake/Foo"
```

`find_package` config-mode command will include `FooConfig.cmake` file and import new target `Foo::bar`:

```bash
> cat Boo/CMakeLists.txt 
find_package(Foo CONFIG REQUIRED)
add_executable(boo boo.cpp)
target_link_libraries(boo Foo::bar)
```

Note that:
* definition `FOO_BAR_DEBUG` will be added automatically
* include directory for target `Foo::bar` will be added automatically
* in `Debug`-mode macro `FOO_BAR_DEBUG` will be `1` and linker will use `libbard.a` library
* in `Release`-mode macro `FOO_BAR_DEBUG` will be `0` and linker will use `libbar.a` library
* if `find_package` command specify library version then `FooConfigVersion.cmake` module will check compatibility:

```bash
> grep find_package Boo/CMakeLists.txt 
find_package(Foo 2.0 CONFIG REQUIRED)
> cmake -HBoo -B_builds/Boo -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
CMake Error at CMakeLists.txt:8 (find_package):
  Could not find a configuration file for package "Foo" that is compatible
  with requested version "2.0".

The following configuration files were considered but not accepted:

    /.../_install/lib/cmake/Foo/FooConfig.cmake, version: 1.2.3
```

### Script

See `jenkins.py` script for automatic testing + options `--install-boo`/`--shared` and `--monolithic`.

### UML sequence diagram

![uml](https://raw.github.com/forexample/package-example/master/wiki/FindPackage.UML-sequence.png)

### More

* [Package manager](https://github.com/ruslo/hunter)
* [Toolchains](https://github.com/ruslo/polly)
