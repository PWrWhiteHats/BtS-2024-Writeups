#include <stdlib.h>
#include <cstddef>
#include <string>
#include <stdio.h>
#include <iostream>

void init(int repeat)
{
  volatile char tab[64];
  if (repeat == 0)
    return;
  else
  {
    for (int i = 0; i < 64; i++)
    {
      tab[i] = i + 0x40;
    }
    init(repeat - 1);
  }
}

__attribute__((constructor)) void foo()
{
  init(120);
}

/*
from pathlib import Path
flag = Path("flag.txt").read_bytes() + b"@"
print(f"{{{",".join(str(i - 0x40) for i in flag)}}}")
*/
int flag_lookup_table[] = {2, 52, 19, 3, 20, 6, 59, 20, 8, 9, 19, 31, 2, 1, 4, 31, 2, 15, 25, 31, 3, 1, 14, 31, 6, 9, 20, 31, 19, 15, 31, 13, 21, 3, 8, 31, 21, 14, 4, 5, 6, 9, 14, 5, 4, 31, 2, 5, 8, 1, 22, 9, 15, 18, 61, 0};

bool check_flag(const char *input, int count = 0)
{
  volatile char tab[64];
  bool eq = input[0] == tab[flag_lookup_table[count]];
  if (flag_lookup_table[count + 1] == 0)
  {
    return eq;
  }
  else
  {
    return check_flag(++input, count + 1) && eq;
  }
}

int main()
{
  puts("Do you know the flag?");
  std::string input;
  std::cin >> input;
  void *store = alloca(0x2d0);
  asm volatile("" : : "r,m"(store) : "memory");
  if (check_flag(input.c_str()))
  {
    puts("Correct Flag");
  }
  else
  {
    puts("Incorrect Flag");
  }
}
