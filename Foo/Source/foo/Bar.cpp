#include <foo/Bar.hpp>

namespace foo {

void Bar::cpp_say() {
#if (FOO_BAR_DEBUG)
  const char* m = "Bar.cpp (Debug)";
#else
  const char* m = "Bar.cpp (Not debug)";
#endif
  std::cout << m << std::endl;
}

} // namespace foo
