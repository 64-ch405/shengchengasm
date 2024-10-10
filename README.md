# shengchengasm.py version 1.0


A script to make versions of exec /bin/elf tiny elf binary assembly source code.
Final binary is 160 to 164 bytes in size with new signature with each generation.
Each generate will also have mutated function inserted.  
By CH405

                  01000011 01001000 00110100 00110000 00110101

# Use:


> localhost $ ./shengchengasm.py  
> [ shengchengasm.py version 1.0 ]  
> File 'shellexec.asm' write success. \o/  
> localhost $ nasm -o shellexec -s shellexec.asm  
> localhost $ chmod +x shellexec  
> localhost $ ./shellexec  
> $ echo $SHELL  
> /bin/sh  
> $  


# Greet:
Thx 0x00000000 for idea. ^^  
Thx Hexrider for more idea. xD  
