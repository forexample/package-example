#include <foo/Bar.hpp>
#include <cstdlib> // EXIT_SUCCESS
#include <iostream> // std::cout

int main() {
  std::cout << "Hello, Boo!" << std::endl;
  foo::Bar::say();
  return EXIT_SUCCESS;
}
