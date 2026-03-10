import pygame
import sys
import random

pygame.init()
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# new refactor
OFF = BLACK
ON = WHITE
paused = False

"""
Reserved Memory Sections:

    - 0x000-0x1FF # For the font set and interpreter
    - 0x050-0xnnn # For font
"""

"""
Original Keyboard-Layout:

123C
456D
789E
A0BF

My Layout:

1234
qwer
asdf
yxcv

For qwerty users thats:

1234
qwer
asdf
zxcv
"""
"""
KEY_MAP = {
    0x1: 0x02,
    0x2: 0x03,
    0x3: 0x04,
    0xC: 0x05,
    0x4: 0x10,
    0x5: 0x11,
    0x6: 0x12,
    0xD: 0x13,
    0x7: 0x1e,
    0x8: 0x1f,
    0x9: 0x20,
    0xE: 0x21,
    0xA: 0x2C,
    0x0: 0x2D,
    0xB: 0x2E,
    0xF: 0x2F
}
"""
KEY_MAP = {
    0x1: pygame.K_1,
    0x2: pygame.K_2,
    0x3: pygame.K_3,
    0xC: pygame.K_4,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0xD: pygame.K_r,
    0x7: pygame.K_a,
    0x8: pygame.K_s,
    0x9: pygame.K_d,
    0xE: pygame.K_f,
    0xA: pygame.K_y,
    0x0: pygame.K_x,
    0xB: pygame.K_c,
    0xF: pygame.K_v
}
KEY_MAP_QWERTY = {
    0x1: pygame.K_1,
    0x2: pygame.K_2,
    0x3: pygame.K_3,
    0xC: pygame.K_4,
    0x4: pygame.K_q,
    0x5: pygame.K_w,
    0x6: pygame.K_e,
    0xD: pygame.K_r,
    0x7: pygame.K_a,
    0x8: pygame.K_s,
    0x9: pygame.K_d,
    0xE: pygame.K_f,
    0xA: pygame.K_z,
    0x0: pygame.K_x,
    0xB: pygame.K_c,
    0xF: pygame.K_v
}

# The chip-8 has 16-bit operands
# Don't change, hard limit by the CHIP-8 chipset
MEMORY_SIZE = 4096
memory = bytearray(MEMORY_SIZE)
# Graphics memory
# Screen Width is 64 and Height is 32 on CHIP-8
WIDTH, HEIGHT = 64, 32
gfx = bytearray(WIDTH*HEIGHT) # gfx[y][x]
# CHIP-8 Registers - The CHIP-8 has a total of 16 different 8 bit General-Purpose Registers Labeled V0-VF
Vx = [0] * 16
# Index-Register 16 bits large
I = 0 
# Program-Counter 16 bits large
pc = 0x200
# 16 Values each 16 bit 
stack = [0] * 16
# Stack-Pointer - Implemented by being implemented here as an index
sp = 0
# CPU-Clock-Speed
clock_speed = 700
# Sound-Timer if above 0 play beep.wav
ST = 0
BEEP_SOUND = "beep.wav"
pygame.mixer.init()
# Play sound with pygame.mixer.Sound(BEEP_SOUND)

# Delay Timer
DT = 0
# Sound Timer
ST = 0

# Pygame Screen
SCALE = 16 # Every pixel is 16x the normal size

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
chip8_surface = pygame.Surface((WIDTH, HEIGHT))
FONT_PATH = "font.ch8"

    



"""
Chat-GPT Overview:
1. Display / Graphics

00E0 – Clear the screen ✅

DXYN – Draw sprite at (VX, VY) of height N (used for paddles and ball) using I as index ✅

2. Flow Control

1NNN – Jump to address NNN ✅

2NNN – Call subroutine at NNN (used for loops / functions) ✅

00EE – Return from subroutine ✅

3XNN – Skip next instruction if VX == NN (collision detection or input handling) ✅

4XNN – Skip if VX != NN ✅

5XY0 – Skip if VX == VY (rare in Pong, maybe for scoring) ✅

9XY0 – Skip if VX != VY (rare) ✅

3. Registers / Memory

6XNN – Set VX = NN (initialize positions, scores) ✅

7XNN – Add NN to VX (move paddles or ball) ✅

4. Keyboard Input

EX9E – Skip next if key in VX is pressed (for paddle up/down) ✅ 

EXA1 – Skip if key in VX not pressed ✅ 

5. Timers

FX07 – Set VX = delay timer (rare for Pong) ✅ 

FX15 – Set delay timer = VX (rare) ✅ 

FX18 – Set sound timer = VX (rare) ✅ 

6. Index / Memory

ANNN – Set I = NNN (point to sprites for paddles/ball) ✅ 

FX1E – I += VX (rare, depends on implementation) ✅  

FX29 – Point I to sprite for digit in VX (if displaying score as hex digits) ✅  

FX33 – Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2 ✅ 

FX55 – Store V0-VX in memory (if saving state) ✅  

FX65 – Load V0-VX from memory ✅  
"""


def read_program(file: str, offset: int=0x200) -> None:
    """
    Reads Program into Memory wih the default offset of 0x200, which is standart on CHIP-8
    """
    try:
        with open(file, "rb") as f:
            rom_content = bytearray(f.read())
    except Exception as e:
        print(f"Something went wrong!\n{e}")
        return
    global memory
    for i in range(len(rom_content)):
        memory[offset+i] = rom_content[i]

read_program(FONT_PATH, offset=0x050) # Load the font into memory at 0x050

should_draw = True
def read_and_execute_next_operand():
    global pc, memory, should_draw
    pc_incremented = False
    if pc + 1 >= len(memory):
        print(f"Memory at {pc}:{pc+2} has no instructions")
        return

    high, low = memory[pc], memory[pc + 1]
    operand = (high << 8) | low  # Combine two bytes into a single 16-bit word

    print(f"High byte: {hex(high)}, Low byte: {hex(low)}, Operand: {hex(operand)}")

    if operand == 0x00E0:
        cls()
    elif operand >= 0xD000 and operand < 0xE000:
        vx = (operand >> 8) & 0xF
        vy = (operand >> 4) & 0xF
        n = operand & 0xF
        draw(vx, vy, n=n)
        should_draw = True
    elif operand >= 0x1000 and operand < 0x2000:
        mem_address = operand & 0xFFF
        jump(mem_address)
        pc_incremented = True
    elif operand == 0x00EE:
        ret()
        pc_incremented = True
    elif operand >= 0x2000 and operand < 0x3000:
        call(operand & 0xFFF)
        pc_incremented = True
    elif operand >= 0x3000 and operand < 0x4000:
        vx = (operand >> 8) & 0xF
        nn = operand & 0xFF
        skip_if_equals(vx, nn)
    elif operand >= 0x4000 and operand < 0x5000:
        vx = (operand >> 8) & 0xF
        nn = operand & 0xFF
        skip_if_not_equals(vx, nn)
    elif operand >= 0x5000 and operand < 0x6000:
        vx = (operand >> 8) & 0xF
        vy = (operand >> 4) & 0xF
        skip_if_vx_equals_vy(vx, vy) 
    elif operand >= 0x6000 and operand < 0x7000:
        vx = (operand >> 8) & 0xF
        nn = operand & 0xFF 
        move(vx, nn)
    elif operand >= 0x7000 and operand < 0x8000:
        vx = (operand >> 8) & 0xF
        nn = operand & 0xFF
        add(vx, nn)
    elif operand >= 0x8000 and operand < 0x9000:
        LSB = operand & 0xF
        vx = (operand >> 8) & 0xF
        vy = (operand >> 4) & 0xF
        if LSB == 0x0:
            set_vx_to_vy(vx, vy)
        elif LSB == 0x1:
            set_vx_vx_OR_vy(vx, vy)
        elif LSB == 0x2:
            set_vx_vx_AND_vy(vx, vy)
        elif LSB == 0x3:
            set_vx_vx_XOR_vy(vx, vy)
        elif LSB == 0x4:
            add_vy_to_vx(vx, vy)
        elif LSB == 0x5:
            sub_vy_from_vx(vx, vy)
        elif LSB == 0x6:
            shift_right(vx)
        elif LSB == 0x7:
            sub_vx_from_vy(vx, vy)
        elif LSB == 0xE:
            shift_left(vx)
    elif operand >= 0x9000 and operand < 0xA000:
        vx = (operand >> 8) & 0xF
        vy = (operand >> 4) & 0xF
        skip_if_vx_not_equals_vy(vx, vy)
    elif operand >= 0xA000 and operand < 0xB000:
        set_i(operand & 0xFFF)
    elif operand >= 0xB000 and operand < 0xC000:
        jump_plus_v0(operand & 0xFFF)
        pc_incremented = True
    elif operand >= 0xC000 and operand < 0xD000:
        vx = (operand >> 8) & 0xF
        set_vx_random(vx, operand & 0xFF)
    elif operand >= 0xE000 and operand < 0xF000:
        LSB = operand & 0xF
        vx = (operand >> 8) & 0xF
        if LSB == 0xE:
            skip_if_key(vx)
        elif LSB == 0x1:
            skip_if_no_key(vx)
    elif operand >= 0xF000 and operand < 0x10000:
        LB = operand & 0xFF # Least Significant byte
        vx = (operand >> 8) & 0xF
        if LB == 0x07:
            set_vx_to_timer(vx)
        elif LB == 0x0A:
            wait_keypress_and_store(vx)
        elif LB == 0x15:
            set_delay_timer(vx)
        elif LB == 0x18:
            set_sound_timer(vx)
        elif LB == 0x1E:
            add_vx_to_I(vx)
        elif LB == 0x29:
            point_I_to_digit(vx)
        elif LB == 0x33:
            binary_to_bcd(vx)
        elif LB == 0x55:
            store_v0_to_vx(vx)
        elif LB == 0x65:
            restore_v0_to_vx(vx)
            

    if not pc_incremented:
        pc += 2 


# MEMORY OPERATION SECTION
def jump(mem_address: int):
    """
    Equivalent to 1NNN
    """
    global pc
    pc = mem_address

def call(mem_address: int):
    """
    Equivalent to 2NNN or x86 jump instruction
    """
    global stack, sp, pc
    stack[sp] = pc + 2
    sp += 1  
    pc = mem_address

def jump_plus_v0(nnn: int):
    """
    BNNN: Jump to address NNN + V0
    """
    global Vx
    jump(nnn + Vx[0])

def ret():
    """
    Equivalet to 0x00EE or x86 ret instruction
    """
    global stack, sp, pc
    sp -= 1
    pc = stack[sp]
    stack[sp] = 0
    

def skip_if_equals(vx: int, nn: int):
    # 3XNN – Skip next instruction if VX == NN (collision detection or input handling)
    global Vx, pc
    if Vx[vx] == nn:
        pc += 2

def skip_if_not_equals(vx: int, nn: int):
    # 4XNN – Skip if VX != NN
    global Vx, pc
    if Vx[vx] != nn:
        pc += 2



def skip_if_vx_equals_vy(vx: int, vy: int):
    # 5XY0 – Skip if VX == VY (rare in Pong, maybe for scoring)
    global pc, Vx
    if Vx[vx] == Vx[vy]:
        pc += 2

def skip_if_vx_not_equals_vy(vx: int, vy: int):
    """
    9XY0 – Skip if VX != VY (rare)
    """
    global pc, Vx
    if Vx[vx] != Vx[vy]:
        pc += 2

# REGISTER HANDLING
def move(vx: int, nn: int):
    # 6XNN – Set VX = NN (initialize positions, scores)
    # mov vx, nn
    global Vx
    Vx[vx] = nn

def add(vx: int, nn: int):
    # 7XNN – Add NN to VX (move paddles or ball)
    # add vx, nn
    global Vx
    Vx[vx] += nn
    Vx[vx] %= 256

# BIT OPERATIONS
def set_vx_to_vy(vx: int, vy: int):
    """
    8XY0: Set VX to the value in VY
    """
    global Vx
    Vx[vx] = Vx[vy]

def set_vx_vx_OR_vy(vx: int, vy: int):
    """
    8XY1: Set VX to VX OR VY
    """
    global Vx
    Vx[vx] = Vx[vx] | Vx[vy]

def set_vx_vx_AND_vy(vx: int, vy: int):
    """
    8XY2: Set VX to VX AND VY
    """
    global Vx
    Vx[vx] &= Vx[vy]

def set_vx_vx_XOR_vy(vx: int, vy: int):
    """
    8XY3: Set VX to VX XOR VY
    """
    global Vx
    Vx[vx] ^= Vx[vy]

def add_vy_to_vx(vx: int, vy: int):
    """
    8XY4: Add the value of register VY to register VX. Set VF to 01 if a carry occurs. Set VF to 00 if a carry does not occur
    """
    global Vx
    total = Vx[vx] + Vx[vy]
    if total > 0xFF:
        Vx[0xF] = 1
    else:
        Vx[0xF] = 0
    Vx[vx] = total & 0xFF

def sub_vy_from_vx(vx: int, vy: int):
    """
    8XY5: Subtract the value of register VY from register VX. Set VF to 00 if a borrow occurs. Set VF to 01 if a borrow does not occur
    """
    global Vx
    if Vx[vx] >= Vx[vy]:
        Vx[0xF] = 1
        Vx[vx] = Vx[vx] - Vx[vy]
    else:
        Vx[0xF] = 0
        Vx[vx] = (Vx[vx] - Vx[vy]) & 0xFF

def shift_right(vx: int):
    """
    8XY6: Store the value of register VY shifted right one bit in register VX. Set register VF to the least significant bit prior to the shift
    """
    global Vx
    v = Vx[vx] 
    Vx[0xF] = v & 0x1
    Vx[vx] = v >> 1

def sub_vx_from_vy(vx: int, vy: int):
    """
    8XY7: Set register VX to the value of VY minus VX. Set VF to 00 if a borrow occurs. Set VF to 01 if a borrow does not occur
    """
    global Vx
    if Vx[vy] >= Vx[vx]:
        Vx[0xF] = 1          
        Vx[vx] = Vx[vy] - Vx[vx]
    else:
        Vx[0xF] = 0          
        Vx[vx] = (Vx[vy] - Vx[vx]) & 0xFF  

def shift_left(vx: int):
    """
    8XYE: Store the value of register VY shifted left one bit in register VX. Set register VF to the most significant bit prior to the shift
    """
    global Vx
    v = Vx[vx]
    Vx[0xF] = (v >> 7) & 0x1 # most significant bit
    Vx[vx] = (v << 1) & 0xFF

# KEYBOARD INPUT
def skip_if_key(vx: int):
    # EX9E – Skip next if key in VX is pressed (for paddle up/down)
    global Vx, pc, KEY_MAP
    keys = pygame.key.get_pressed()
    if keys[KEY_MAP[Vx[vx]]]:
        pc += 2

def skip_if_no_key(vx: int):
    # EXA1 – Skip if key in VX not pressed
    global Vx, pc, KEY_MAP
    keys = pygame.key.get_pressed()
    if not keys[KEY_MAP[Vx[vx]]]:
        pc += 2

def wait_keypress_and_store(vx: int):
    """
    FX0A: Wait for a keypress and store the result in register VX
    """
    global Vx, KEY_MAP, paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for chip8_key, scancode in KEY_MAP.items():
                    if event.scancode == scancode:
                        Vx[vx] = chip8_key
                        paused = False
                        break
        pygame.time.delay(1)



# RANDOM
def set_vx_random(vx: int, nn: int):
    """
    CXNN: Set VX to a random number with a mask of NN
    """
    global Vx
    Vx[vx] = random.randint(0, 255) & nn

# TIMERS
def set_vx_to_timer(vx: int):
    # FX07 – Set VX = delay timer (rare for Pong)
    global Vx, DT
    Vx[vx] = DT

def set_delay_timer(vx: int):
    # FX15 – Set delay timer = VX (rare)
    global DT, Vx
    DT = Vx[vx]

def set_sound_timer(vx: int):
    # FX18 – Set sound timer = VX (rare)
    global ST, Vx
    ST = Vx[vx]

# Index + Memory
def set_i(nnn: int):
    # ANNN – Set I = NNN (point to sprites for paddles/ball)
    global I
    I = nnn

def add_vx_to_I(vx: int):
    """
    FX1E – I += VX (rare, depends on implementation)
    """
    global Vx, I
    I += Vx[vx]

def point_I_to_digit(vx: int):
    """
    FX29 – Point I to sprite for digit in VX (if displaying score as hex digits) 
    """
    global Vx, I
    offset = 0x050 # normal offset for digits
    # calculation = offset + digit * 5
    digit = Vx[vx] & 0xF
    address = offset + digit * 5
    I = address

def binary_to_bcd(vx: int):
    """
    FX33 – Store the binary-coded decimal equivalent of the value stored in register VX at addresses I, I+1, and I+2 
    """
    global Vx, I, memory
    num = Vx[vx]
    memory[I] = (num // 100)
    memory[I+1] = (num // 10) % 10
    memory[I+2] = num % 10

def store_v0_to_vx(vx: int):
    # FX55 – Store V0-VX in memory (if saving state)
    # Size of register = 1 byte
    global Vx, memory, I
    max = vx
    for reg in range(max + 1):
        memory[I + reg] = Vx[reg]
    I = I + vx + 1

def restore_v0_to_vx(vx: int):
    # FX65 – Load V0-VX from memory
    global Vx, memory, I
    max = vx
    for reg in range(max + 1):
        Vx[reg] = memory[I + reg]
    I = I + vx + 1

# SCREEN
def cls() -> None:
    global gfx
    """
    Equivalent to 0x00E0
    """
    gfx = bytearray(64*32)
    

# DXYN – Draw sprite at (VX, VY) of height N (used for paddles and ball) using I as index
# X meaning accessing V[X], because the position can be an 8 bit number
# Y meaning the same
def draw(vx: int, vy:int, n: int) -> None:
    """
    CHIP-8 DXYN: Draws a sprite from memory[I] at (Vx[vx], Vx[vy]).
    Each sprite row is 8 pixels (1 byte), height = n bytes.
    Pixels are XORed onto gfx (1D array). VF = 1 if any pixels are erased.
    """
    global Vx, gfx, I, memory
    x_start = Vx[vx] % 64
    y_start = Vx[vy] % 32
    VF = 0
    
    for row in range(n):
        sprite_byte = memory[I+row]
        for col in range(8):
            sprite_pixel = (sprite_byte >> (7-col)) & 1
            if sprite_pixel:
                idx = ((y_start + row) % 32) * 64 + ((x_start + col) % 64)
                if gfx[idx] == 1:
                    VF = 1
                gfx[idx] ^= 1

    Vx[0xF] = VF            
    
    

def draw_to_screen_and_scale():
    """
    Draws gfx to the pygame screen, it also scales the surface, because 64x32 is tiny
    """
    global gfx, WHITE, BLACK, chip8_surface, WIDTH, HEIGHT, SCALE
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = WHITE if gfx[y*WIDTH + x] else BLACK
            chip8_surface.set_at((x, y), color)
    scale(SCALE)

def scale(scale: int):
    """
    Scales the pixels by scale onto the pygame screen
    """
    global chip8_surface, WIDTH, HEIGHT, screen
    scaled_surface = pygame.transform.scale(chip8_surface, (WIDTH * SCALE, HEIGHT * SCALE))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()


max_arguments = 4
if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    argv = sys.argv
    if len(argv) == 1:
        print("Correct Usage: \n python3 <filename.py> <rom.rom/rom.ch8> <clock-speed: default=700> <optionally: z for qwerty keymap and y for qwertz keymap>")
        sys.exit(-1)
    if len(argv) > max_arguments:
        print("Too many arguments Correct Usage: \n python3 <filename.py> <rom.rom/rom.ch8> <clock-speed: default=700> <optionally: z for qwerty keymap and y for qwertz keymap>")
        sys.exit(-1)
    if len(argv) >= 2:
        read_program(argv[1])
        if len(argv) >= 3:
            clock_speed = int(argv[2])
            if len(argv) >= 4:
                if argv[3] == "z":
                    KEY_MAP = KEY_MAP_QWERTY
    sound_channel = None
    clock = pygame.time.Clock()
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        #  Every Instruction/Not Time Base - Implemented: ✅ 
        for _ in range(int(clock_speed/60)):
            read_and_execute_next_operand()
            
        # Time Dependant - Implemented: ✅ 
        if DT > 0:
            DT -= 1
        if ST > 0:
            if sound_channel is None or not sound_channel.get_busy():
                sound = pygame.mixer.Sound(BEEP_SOUND)
                sound_channel = sound.play(-1)  # -1 loops it
            ST -= 1
        else:
            if sound_channel is not None:
                sound_channel.stop()
                sound_channel = None

        if should_draw:
            draw_to_screen_and_scale()
            should_draw = False
        clock.tick(FPS)