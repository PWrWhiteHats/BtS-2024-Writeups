#include <stdlib.h>
#include <unistd.h>
#include <iostream>
#include <string>
#include <algorithm>

struct S
{
  S()
  {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
  }
};

static S init{};

bool contains_unsafe_characters(std::string_view input)
{
  std::string_view unsafe_characters = "&;`|*?([.";
  for (auto c : unsafe_characters)
  {
    if (input.contains(c))
    {
      return true;
    }
  }
  return false;
}

int main()
{
  std::cout << "What file would you like to read?\n";
  system("ls");
  std::cout << "> ";

  std::string input;
  std::cin >> input;

  std::string command{"/bin/cat ./"};
  command += input;

  if (contains_unsafe_characters(input))
  {
    std::cout << "Unsafe characters detected\n";
    return 1;
  }
  else
  {
    system(command.c_str());
  }
  return 0;
}
