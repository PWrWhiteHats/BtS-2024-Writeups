#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <string>
#include <fcntl.h>

__attribute__((constructor)) void setbufs()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

__attribute__((constructor)) void chroot()
{
    char path[] = "/tmp/chroot_XXXXXX";
    char *new_root = mkdtemp(path);

    if (chroot(new_root) == -1)
    {
        exit(EXIT_FAILURE);
    }
    chdir("/");
}


int main()
{
    puts("Hello World!");
    puts("> ");
    volatile short int a = 0x5fc3;
    volatile short int b = 0xc35f;
    char input[32];
    read(0, input, 0x200);
}
