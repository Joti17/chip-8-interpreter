# CHIP-8-Emulator
A simple **CHIP-8** interpreter written in Python with graphics, input handling and small debugging utilities

CHIP-8 is a small interpreted programming language created in the 1970s for the COSMAC VIP computer to make game development easier.
Because of its small instruction set and simple architecture, CHIP-8 is commonly used as a first emulator project.

This emulator aims to provide clean and understandable implementation of the CHIP-8-virtual machine.

## Features

### Emulator
- Complete CHIP-8 instruction set
- Graphical display (64x32 resolution scaled to 16x)
- Keyboard input mapping
- Sound and delay timers
- ROM loading
- Debugging output for instructions

### Assembler
- Convert CHIP-8 assembly into binary ROM files
- Supports labels and comments

### Disassembler
- Convert CHIP-8 back into the closest guess of the original assembly
- Useful for analysis and debugging

## Requirements
- Python
- pygame 2.1+
```
pip3 install -r requirements.txt
```
## Running the Emulator
Run the Emulator with a CHIP-8 ROM:
```
python3 <filename.py> <rom.rom/rom.ch8/rom.bin> <clock-speed: default=700> <optionally: z for qwerty keymap and y for qwertz keymap>
```
Example ROMs in this repository are:
- Tetris
- Pong

## Running the Assembler
Assemble a CHIP-8 assembly file into a ROM
```
python3 <assembler.py> <source.asm> <output.ch8>
```
Example:
```
python3 assembler/assembler.py src/pong.asm roms/pong.ch8
```
## Running the Disassembler
Disassemble a CHIP-8 ROM into human-readable assembly:
```
python3 <disassembler.py> <input.ch8/rom/bin> <output.asm/S>
```
Example:
```
python3 disassembler/disassemble.py roms/pong.rom roms/pong.asm
```


## CHIP-8 Architecture

The CHIP-8 system contains:

| Component | Description |
|-----------|-------------|
| Memory | 4 KB RAM |
| Registers | 16 8-bit registers (V0–VF) |
| Index Register | 16-bit register `I` |
| Stack | Used for subroutine calls |
| Timers | Delay timer and sound timer |
| Display | 64 × 32 monochrome pixels |
| Input | 16-key hexadecimal keypad |

Programs are typically loaded at starting at memory address:
0x200
0x000-0x1FF are reserved by the interpreter in the case of this emulator only used for fonts
## Keyboard Layout
The Original CHIP-8 used a hexadecimal Keypad:
```
1 2 3 C
4 5 6 D
7 8 9 E
A 0 B F
```
The Keyboard Mapping used by me:
```
1 2 3 4
q w e r
a s d f
y x c v
```
For QWERTY users consider adding z at the end of the execution command to test the emulator

## Instructions

### Instruction Example
A CHIP-8 Instruction is 2 bytes long(16bits).
Example:
```
FX29
```
Meaning:
```
The I register will point to the digit in VX
```
Example:
```
670A # Moves 0x0A into V7
F729
```
Sets I as pointer to the digit 'A'

### List of all Instructions

| Mnemonic | Meaning / Operation | Example | Hexadecimal | Name |
|---|---|---|---|---|
| cls | Clear the Screen | cls | 00E0 | Clear |
| ret | Return from subroutine | ret | 00EE | Return |
| jmp nnn | Jump to address NNN | jmp 0x210 | 1NNN | Jump |
| call nnn | Call subroutine at address NNN | call 0x298 | 2NNN | Call |
| se VX, nn | Skip the following instruction if the value of register VX equals NN | se VA, 0x12 | 3XNN | Skip Equals |
| sne VX, nn | Skip the following instruction if the value of register VX is not equal to NN | sne VE, 0x32 | 4XNN | Skip Not Equals |
| sxey VX, VY | Skip the following instruction if the value of register VX is equal to the value of register VY | sxey V1, VB | 5XY0 | Skip VX Equals VY |
| set VX, nn | Set VX to NN | set VB, 0x2 | 6XNN | Move |
| add VX, NN | Add NN to VX | add VB, 0x79 | 7XNN | Add |
| copy VX, VY | Set VX to the value in VY | copy VA, VE | 8XY0 | Move |
| or VX, VY | Set VX to VX OR VY | or VB, VC | 8XY1 | Bitwise-OR |
| and VX, VY | Set VX to VX AND VY | and VB, VE | 8XY2 | Bitwise-AND |
| xor VX, VY | Set VX to VX XOR VY | xor VA, VA | 8XY3 | Bitwise-XOR |
| addc VX, VX | Add the value of register VY to register VX. Set VF to 01 if a carry occurs. Set VF to 00 if a carry does not occur | addc VA, V1 | 8XY4 | Add with Carry |
| subc VX, VY | Subtract the value of register VY from register VX. Set VF to 00 if a borrow occurs. Set VF to 01 if a borrow does not occur | subc VA, VB | 8XY5 | Subtract with Carry |
| shr VX, VY | Store the value of register VY shifted right one bit in register VX. Set register VF to the least significant bit prior to the shift | shr VA, VB | 8XY6 | Shift Right |
| subn VX, VY | Set register VX to the value of VY minus VX. Set VF to 00 if a borrow occurs. Set VF to 01 if a borrow does not occur | subn V1, V0 | 8XY7 | Reverse Subtract |
| shl VX, VY | Store the value of register VY shifted left one bit in register VX. Set register VF to the most significant bit prior to the shift | shl V0, V1 | 8XYE | Shift Left |
| sre VX, VY | Skip the following instruction if the value of register VX is not equal to the value of register VY | sre V0, V1 | 9XY0 | Skip Register Not Equals |
| si NNN | Store memory address NNN in register I | si 0x999 | ANNN | Set I Memory Address |
| j0 NNN | Jump to address NNN + V0 | j0 0xFFF | BNNN | Jump Zero |
| rnd VX, NN | Set VX to a random number with a mask of NN | rnd V1, 0xFF | CXNN | Random |
| draw VX, VY, N | Draw a sprite at position VX, VY with N bytes of sprite data starting at the address stored in I. Set VF to 01 if any set pixels are changed to unset, and 00 otherwise | draw V1, V2, E | DXYN | Draw |
| sk VX | Skip the following instruction if the key corresponding to the hex value currently stored in register VX is pressed | sk V1 | EX9E | Skip If Key |
| snk VX | Skip the following instruction if the key corresponding to the hex value currently stored in register VX is not pressed | snk V2 | EXA1 | Skip If Not Key |
| sdt VX | Store the current value of the delay timer in register VX | sdt V2 | FX07 | Set Delay VX Delay Timer |
| wk VX | Wait for a keypress and store the result in register VX | wk V1 | FX0A | Wait Key |
| sdr VX | Set the delay timer to the value of register VX | sdr VF | FX15 | Set Delay Timer From Register |
| sst VX | Set the sound timer to the value of register VX | sst V5 | FX18 | Set Sound Timer From Register |
| addi VX | Add the value stored in register VX to register I | addi V1 | FX1E | Add VX to Index |
| getd VX | Set I to the memory address of the sprite data corresponding to the hexadecimal digit stored in register VX | getd V2 | FX29 | Get Digit |
| gbcd VX | Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2 | gbcd V1 | FX33 | Get Binary Coded Decimal |
| dump VX | Store the values of registers V0 to VX inclusive in memory starting at address I. I is set to I + X + 1 after operation | dump V9 | FX55 | Dump Registers to VX |
| fill VX | Fill registers V0 to VX inclusive with the values stored in memory starting at address I. I is set to I + X + 1 after operation | fill V9 | FX65 | Restore Registers to VX |

## Resources
- CHIP-8 Instruction Reference  
  ```
  https://chip-8.github.io/extensions/#chip-8
  ```
- Gemini for debugging
  ```
  https://gemini.google.com/
  ```
- Chat GPT for Project planning
  ```
  https://chat.openai.com/
  ```
- Tests:
  ```
  https://github.com/corax89/chip8-test-rom/
  ```
  ```
  https://github.com/Timendus/chip8-test-suite
  ```
## License
MIT License
