Test PR

### Install Foo

Install project `Foo` in `Debug` and `Release` variants:
``` bash
> cmake -HFoo -B_builds/Foo-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
> cmake --build _builds/Foo-debug --target install
...
Install the project...
-- Install configuration: "Debug"
-- Installing: /.../_install/lib/cmake/Foo/FooConfig.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooConfigVersion.cmake
-- Installing: /.../_install/lib/libfood.a
-- Installing: /.../_install/include/Foo.hpp
-- Installing: /.../_install/lib/cmake/Foo/FooTargets.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets-debug.cmake
```

```bash
> cmake -HFoo -B_builds/Foo-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
> cmake --build _builds/Foo-release --target install
...
-- Install configuration: "Release"
-- Installing: /.../_install/lib/cmake/Foo/FooConfig.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooConfigVersion.cmake
-- Installing: /.../_install/lib/libfoo.a
-- Up-to-date: /.../_install/include/Foo.hpp
-- Installing: /.../_install/lib/cmake/Foo/FooTargets.cmake
-- Installing: /.../_install/lib/cmake/Foo/FooTargets-release.cmake
```

Note that:
* target `foo` output has different names: `libfoo.a` and `libfood.a`
* header files is equal for both variants
* cmake-config files `FooConfig.cmake`, `FooConfigVersion.cmake` and `FooTargets.cmake` is equal for both variants
* `FooTargets-release.cmake` set `Release` imported target properties, e.g. `IMPORTED_LOCATION_RELEASE`
* `FooTargets-debug.cmake` set `Debug` imported target properties, e.g. `IMPORTED_LOCATION_DEBUG`
* `FooConfig.cmake` set `IMPORTED_LOCATION` property to value of `IMPORTED_LOCATION_RELEASE` (will be used in cases
when there is no configuration variant at all or variant is differ from `Release`/`Debug`)

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

`find_package` config-mode command will include `FooConfig.cmake` file and import new target `Foo::foo`:

```bash
> cat Boo/CMakeLists.txt 
cmake_minimum_required(VERSION 2.8)
project(Boo)

find_package(Foo CONFIG REQUIRED)

add_executable(boo boo.cpp)
target_link_libraries(boo Foo::foo)
```

Note that:
* definition `FOO_DEBUG` will be added automatically
* include directory for target `Foo::foo` will be added automatically
* in `Debug`-mode macro `FOO_DEBUG` will be `1` and linker will use `libfood.a` library
* in other modes (or without mode) `FOO_DEBUG` will be `0` and linker will use `libfoo.a` library
* if `find_package` command specify library version then `FooConfigVersion.cmake` module will check compatibility:

```bash
> grep find_package Boo/CMakeLists.txt 
find_package(Foo 2.0 CONFIG REQUIRED)
> cmake -HBoo -B_builds/Boo -DCMAKE_INSTALL_PREFIX="`pwd`/_install"
CMake Error at CMakeLists.txt:4 (find_package):
  Could not find a configuration file for package "Foo" that is compatible
  with requested version "2.0".

The following configuration files were considered but not accepted:

    /.../_install/lib/cmake/Foo/FooConfig.cmake, version: 1.2.3
```

### UML sequence diagram

![uml](https://raw.github.com/forexample/package-example/master/wiki/FindPackage.UML-sequence.png)
