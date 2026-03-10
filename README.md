# CHIP-8-Emulator
A simple **CHIP-8** interpreter written in Python with graphics, input handling and small debugging utilities

CHIP-8 is a small interpreted programming language created in the 1970s for the COSMAC VIP computer to make game development easier.
Because of its small instruction set and simple architecture, CHIP-8 is commonly used as a first emulator project.

This emulator aims to provide clean and understandable implementation of the CHIP-8-virtual machine.

## Features
- Complete CHIP-8 instruction set
- Graphical display (64x32 resolution scaled to 16x)
- Keyboard input mapping
- Sound and delay timers
- ROM loading
- Debugging output for instructions

## Requirements
- Python
- pygame 2.1+
```
pip3 install -r requirements.txt
```
## Running the Emulator
Run the Emulator with a CHIP-8 ROM:
```
python3 <filename.py> <rom.rom/rom.ch8/rom.bin> <clock-speed: default=700>
```
Example ROMs in this repository are:
- Tetris
- pong
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
For QWERTY users I'll add an option for more keyboard layouts in the Future

## Instruction Example
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
## License
MIT License
