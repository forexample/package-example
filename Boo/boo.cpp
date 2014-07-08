// #include <Foo.hpp>
#include <cstdlib> // EXIT_SUCCESS
#include <iostream> // std::cout

int foo();

int main() {
  std::cout << "foo: " << foo() << std::endl;
  return EXIT_SUCCESS;
}
