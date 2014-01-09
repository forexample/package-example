#include <iostream> // std::cout
#include <Foo.hpp>

int foo();

int main() {
  std::cout << "foo: " << foo() << std::endl;
  return EXIT_SUCCESS;
}
