#include <unistd.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
// sudo dnf install libseccomp-devel
#include <seccomp.h>


__attribute__((constructor)) void setbufs()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}


void setup_seccomp()
{
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);

    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(creat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(openat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(access), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(readv), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execve), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(execveat), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mkdir), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(mmap), 0);
    seccomp_rule_add(ctx, SCMP_ACT_KILL, SCMP_SYS(pipe), 0);

    seccomp_load(ctx);
}

void execute_code();
void check_flag();

int main()
{
    check_flag();
    execute_code();
}

void execute_code()
{
    void *addr = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    puts("Upload your shellcode.");
    read(0, addr, 4096);
    setup_seccomp();
    ((void (*)())addr)();
}
void check_flag()
{
    int fd = open("flag", O_RDONLY);
    if (fd < 0)
    {
        puts("Flag not found! Please contact admins!");
        exit(EXIT_FAILURE);
    }
}
