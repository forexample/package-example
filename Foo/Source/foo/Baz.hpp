#ifndef FOO_BAZ_HPP_
#define FOO_BAZ_HPP_

#include <iostream> // std::cout
#include <foo/BAZ_EXPORT.h>

namespace foo {

class BAZ_EXPORT Baz {
 public:
  static void say() {
#if (FOO_BAZ_DEBUG)
    const char* m = "Baz.hpp (Debug)";
#else
    const char* m = "Baz.hpp (Not debug)";
#endif
    std::cout << m << std::endl;
    cpp_say();
  }

 private:
  static void cpp_say();
};

} // namespace foo

#endif // FOO_BAZ_HPP_
