#ifndef FOO_BAR_HPP_
#define FOO_BAR_HPP_

#include <iostream> // std::cout
#include <foo/Baz.hpp>
#include <bar_export.h> // BAR_EXPORT

namespace foo {

class BAR_EXPORT Bar {
 public:
  static void say() {
    Baz::say();
#if (FOO_BAR_DEBUG)
    const char* m = "Bar.hpp (Debug)";
#else
    const char* m = "Bar.hpp (Not debug)";
#endif
    std::cout << m << std::endl;
    cpp_say();
  }

 private:
  static void cpp_say();
};

}

#endif // FOO_BAR_HPP_
