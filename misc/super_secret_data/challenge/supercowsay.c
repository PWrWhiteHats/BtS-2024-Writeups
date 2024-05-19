#include <unistd.h>
#include <stdlib.h>

int main() {
    setuid(0);
    int result = system("cowsay 'I am a super cow!'");
    if (result == -1) {
        return 1;
    }
    return 0;
}