#include <Foo.hpp>
#include <cstdlib> // EXIT_SUCCESS
#include <iostream> // std::cout

int foo();

int boo() {
  std::cout << "foo: " << foo() << std::endl;
  return foo();
}
