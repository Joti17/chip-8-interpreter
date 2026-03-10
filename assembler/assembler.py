import sys
import os

output_hex = bytearray()
labels = {}
pc = 0x200





    
# Collect Labels
def collect_labels(instructions: list[list[str]]):
    global pc
    pc = 0x200
    for line in instructions:
        if not line: continue
        if len(line) == 1 and line[0].endswith(":"):
            label_name = line[0][:-1]
            labels[label_name] = pc
        elif line[0].lower() == "db":
            # Increment by the number of arguments (bytes) provided
            pc += len(line) - 1
        else:
            pc += 2


def append_opcode(opcode: int):
    """
    Helper function for appending 2byte operands
    """
    global output_hex
    output_hex.append((opcode >> 8) & 0xFF)
    output_hex.append(opcode & 0xFF)

def cls():
    """
    Structure of cls instruction:
    cls - Clears the Screen
    Hexadecimal:
    0x00E0
    """
    global output_hex
    append_opcode(0x00E0)

def ret():
    """
    Structure of ret instruction:
    ret - Returns to last address on call stack
    Hexadecimal:
    0x00EE
    """
    global output_hex
    append_opcode(0x00EE)

def jmp(line: list[str]):
    """
    Structure of jmp instruction:
    jmp nnn - Where nnn is the memory address
    Hexadecimal:
    0x1NNN
    """
    global output_hex
    target = line[1]
    
    # Check, if lavel available
    if target in labels:
        nnn = labels[target]
    else:
        try:
            nnn = int(target, 16) # base 16
        except ValueError:
            print(f"Fehler: Label/Adress '{target}' not found!")
            sys.exit(-1)

    opcode = 0x1000 | (nnn & 0xFFF)
    append_opcode(opcode)



def call(line: list[str]):
    """
    Structure of call instruction:
    call nnn - nnn is memory address where the interpreter will jump to
    the current pc+2 will the pushed on the stack - a 16 element 12bit array
    Hexadecimal:
    0x2NNN
    """
    global output_hex
    target = line[1]
    
    # Check, if lavel available
    if target in labels:
        nnn = labels[target]
    else:
        try:
            nnn = int(target, 0x10) # base 16
        except ValueError:
            print(f"Fehler: Label/Adress '{target}' not found!")
            sys.exit(-1)
    
    opcode = 0x2000 | (nnn & 0xFFF)
    append_opcode(opcode)

def skip_if_equals(line: list[str]):
    """
    Structure of skip == instruction:
    se x, nn - where x is the register VX you want to compare and nn is an immediate value if successful adds 2 to pc
    Hexadecimal:
    0x3XNN
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10)
    nn = int (line[2], 16)

    opcode = 0x3000 | (0x100 * vx) | (nn & 0xFF)
    append_opcode(opcode)

def skip_if_not_equals(line: list[str]):
    """
    structure of skip != instruction:
    sne x, nn - where x is the register VX you want to compare and nn is an immediate value if succressful adds 2 to pc
    Hexadecimal:
    0x4XNN
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 16) & 0xF
    nn = int(line[2], 16) & 0xFF
    opcode = 0x4000 | (vx << 8) | nn
    append_opcode(opcode)

def skip_if_vx_equals_vy(line: list[str]):
    """
    Structure of skip if vx == vy instruction:
    sxey x, y - where x is the register VX and y is the register VY adds 2 to pc if both are equal
    Hexadecimal:
    0x5XY0 
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10)
    vy = int(line[2].strip(",").replace("V", ""), 0x10)
    opcode = 0x5000 | (0x100 * vx) | (0x10 * vy) | 0x00
    append_opcode(opcode)

def set_vx_nn(line: list[str]):
    """
    Structure of vx = nn instruction:
    set x, nn - where x is the register VX and nn is a 1 byte integer
    Hexadecimal:
    0x6XNN 
    """
    global output_hex
    vx = int(line[1].strip(",").upper().replace("V", ""), 0x10) & 0xF
    nn = int(line[2].strip(","), 0x10) & 0xFF
    opcode = 0x6000 | (vx << 8) | (nn & 0xFF)
    append_opcode(opcode)

def add(line: list[str]):
    """
    Structure of vx += nn instruction:
    add x, nn - where nn is the value to add to VX and x is the register VX
    Hexadecimal:
    0x7XNN
    """
    global output_hex
    vx = int(line[1].strip(",").upper().replace("V", ""), 0x10) & 0xF
    nn = int(line[2], 0x10) & 0xFF
    opcode = 0x7000 | (vx << 8) | nn
    append_opcode(opcode)

def copy(line: list[str]):
    """
    Structure of vx = vy instruction:
    copy x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY0
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x8000 | (0x100 * vx) | (0x10 * vy) | 0
    append_opcode(opcode)

def OR(line: list[str]):
    """
    Structure of vx = vx OR vy instruction:
    or x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY1
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x8000 | (0x100 * vx) | (0x10 * vy) | 1
    append_opcode(opcode)

def AND(line: list[str]):
    """
    Structure of vx = vx AND vy instruction:
    and x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY2
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x8000 | (0x100 * vx) | (0x10 * vy) | 2
    append_opcode(opcode)

def XOR(line: list[str]):
    """
    Structure of vx = vx XOR vy instruction:
    xor x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY3
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x8000 | (0x100 * vx) | (0x10 * vy) | 3
    append_opcode(opcode)

def MSB_eight(line: list[str], LSB: int):
    """
    Helper function of 8XY* functions
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x8000 | (0x100 * vx) | (0x10 * vy) | (LSB & 0xF)
    append_opcode(opcode)

def add_carry(line: list[str]):
    """
    Strucutre of vx += vy && carry in VF instruction:
    addc x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY4
    """
    MSB_eight(line, 0x04)

def sub_carry(line: list[str]):
    """
    Structure of vx -= vy && carry in VF instruction:
    subc x, y - where x is Vx and y is VY
    Hexadecimal:
    0x8XY5
    """
    MSB_eight(line, 0x05)

def shift_right(line: list[str]):
    """
    Structure of vx = vy >> 1 && VF = LSB before shift instruction:
    shr x, y - where x is Vx and y is VY
    Hexadecimal:
    0x8XY6
    """
    MSB_eight(line, 0x06)

def sub_reverse(line: list[str]):
    """
    Structure of vx = vy - vx instruction:
    subn x, y - where x is VX and y is VY
    Hexadecimal:
    0x8XY7
    """
    MSB_eight(line, 0x07)

def shift_left(line: list[str]):
    """
    Structure of vx = vy << 1 && VF = MSB before shift instruction:
    shl x, y - where x is Vx and y is VY
    Hexadecimal:
    0x8XYE
    """
    MSB_eight(line, 0x0E)

def skip_if_vx_not_vy(line: list[str]):
    """
    Structure of skip if vx == vy instruction:
    sre x, y - where x is VX and y is VY
    Hexadecimal:
    0x9XY0
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0x9000 | (0x100 * vx) | (0x10 * vy) | 0
    append_opcode(opcode)

def store_nnn_in_i(line: list[str]):
    """
    Structure of I = nnn instruction:
    si nnn - where nnn is 3 nibble memory address
    Hexadecimal:
    0xANNN
    """
    global output_hex
    target = line[1].strip(",")
    
    if target in labels:
        nnn = labels[target]
    else:
        try:
            nnn = int(target, 0)
        except ValueError:
            print(f"Fehler: Label/Adress '{target}' not found!")
            sys.exit(-1)
            
    opcode = 0xA000 | (nnn & 0xFFF)
    append_opcode(opcode)

def jump_tp_nnn_plus_0(line: list[str]):
    """
    Structure of jmp nnn + v0 instruction:
    j0 nnn - where nnn is 3 nibble memory address
    Hexadecimal:
    0xBNNN
    """
    global output_hex
    nnn = int(line[1], 0x10) & 0xFFF
    opcode = 0xB000 | (nnn & 0xFFF)
    append_opcode(opcode)

def x_random(line: list[str]):
    """
    Structure of VX = (rand() & NN) instruction:
    rnd x, nn - where x is VX and nn is 1 byte memory address
    Hexadecimal:
    0xCXNN
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    nn = int(line[2].strip(","), 0x10) & 0xFF
    opcode = 0xC000 | (vx << 8) | nn
    append_opcode(opcode)

def draw(line: list[str]):
    """
    Structure draw is x position is VX and y position is VY height is N, where N=0 at least in my interpreter means 0 height in others it might mean 16 instruction:
    draw x, y, n - where x is VX, y is VY and n is height
    Hexadecimal:
    0xDXYN
    """
    global output_hex
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    vy = int(line[2].strip(",").replace("V", ""), 0x10) & 0xF
    n = int(line[3], 0x10) & 0xF
    opcode = 0xD000 | (vx << 8) | (vy << 4) | n
    append_opcode(opcode)

def MSB_E(line: list[str], LSW: int):
    """
    Helper Function like MSB_eight
    """
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0xE000 | (0x100 * vx) | (LSW & 0xFF)
    append_opcode(opcode)

def skip_if_key(line: list[str]):
    """
    Structure of skip instructiion if key_pressed == VX instruction:
    sk x - where x is VX
    Hexadecimal:
    0xEX9E
    """
    MSB_E(line, 0x9E)

def skip_if_not_key(line: list[str]):
    """
    Structure of skip instruction if key_pressed != VX instruction:
    snk x - where x is VX
    Hexadecimal:
    0xEXA1
    """
    MSB_E(line, 0xA1)

def MSB_F(line: list[str], LSW: int):
    """
    Helper function like MSB_E
    """
    vx = int(line[1].strip(",").replace("V", ""), 0x10) & 0xF
    opcode = 0xF000 | (0x100 * vx) | (LSW & 0xFF)
    append_opcode(opcode)

def store_delay_vx(line: list[str]):
    """
    Structure of vx = DT instruction:
    sdt x - where x is VX
    Hexadecimal:
    0xFX07
    """
    MSB_F(line, 0x07)

def wait_for_key(line: list[str]):
    """
    Structure of wait for key instruction:
    wk x - where is x is register to store result in
    Hexadecimal:
    0xFX0A
    """
    MSB_F(line, 0x0A)

def set_DT(line: list[str]):
    """
    Structure of DT = VX instruction:
    sdr x - where x is VX
    Hexadecimal:
    0xFX15
    """
    MSB_F(line, 0x15)

def set_ST(line: list[str]):
    """
    Structure of ST = VX instruction:
    sst x - where x is VX
    Hexadecimal:
    0xFX18
    """
    MSB_F(line, 0x18)

def add_i(line: list[str]):
    """
    Structure of I += VX instruction:
    addi x - where x is VX, which gets added to I
    Hexadecimal:
    0xFX1E
    """
    MSB_F(line, 0x1E)

def set_I_digit(line: list[str]):
    """
    Structure of I = address of digit in VX instruction:
    getd x - where x is VX, which is the digit to get
    Hexadecimal:
    0xFX29
    """
    MSB_F(line, 0x29)

def get_bcd(line: list[str]):
    """
    Structure of I = 100th place I+1 = 10th place and I+2 = 1st place instruction:
    gbcd x - where x is VX, which will be sliced
    Hexadecimal:
    0xFX33
    """
    MSB_F(line, 0x33)

def dump(line: list[str]):
    """
    Structure of dumping every V from V0:VX instruction:
    dump x - where x is the inclusive limit of dumped registers
    Hexadecimal:
    0xFX55
    """
    MSB_F(line, 0x55)

def fill(line: list[str]):
    """
    Structure of filling every register from V0:VX instrution:
    fill x - where x is the inclusive limit of dumped registers
    Hexadecimal:
    0xFX65
    """
    MSB_F(line, 0x65)

def db(line: list[str]):
    """
    Structure defined byte after instruction:
    db stuff
    """
    global output_hex
    for val in line[1:]:
        clean_val = val.strip(",")
        # Use & 0xFF to ensure it's a single byte
        output_hex.append(int(clean_val, 0x10) & 0xFF)

if __name__ == "__main__":
    argv = sys.argv
    
    if len(argv) == 1:
        print("Correct Usage: python3 <filename.py> <input.asm/S> <output.ch8>")
        sys.exit(-1)
    if len(argv) >= 2:
        file = argv[1]
        if len(argv) >= 3:
            output = argv[2]
        else:
            output = os.path.splitext(file)[0]
    
    with open(file, "r") as f:
        file_content = f.read()
    
    file_content_list = file_content.splitlines()
    file_content_list_worlds = []

    for row in file_content_list:
        # Strip Comments
        clean_row = row.split('#')[0].strip()
        
        if clean_row:
           file_content_list_worlds.append(clean_row.split())

    file_content = file_content_list_worlds.copy()
    
    mem_to_func = {
    "cls": cls,             # 00E0
    "ret": ret,             # 00EE
    "jmp": jmp,             # 1NNN
    "call": call,           # 2NNN
    "j0": jump_tp_nnn_plus_0, # BNNN

    "se": skip_if_equals,    # 3XNN
    "sne": skip_if_not_equals, # 4XNN
    "sxey": skip_if_vx_equals_vy, # 5XY0
    "sre": skip_if_vx_not_vy, # 9XY0
    "sk": skip_if_key,       # EX9E
    "snk": skip_if_not_key,  # EXA1

    "set": set_vx_nn,       # 6XNN
    "add": add,             # 7XNN
    "copy": copy,           # 8XY0
    "or": OR,               # 8XY1
    "and": AND,             # 8XY2
    "xor": XOR,             # 8XY3
    "addc": add_carry,      # 8XY4
    "subc": sub_carry,      # 8XY5
    "shr": shift_right,     # 8XY6
    "subn": sub_reverse,    # 8XY7
    "shl": shift_left,      # 8XYE
    "rnd": x_random,        # CXNN

    "si": store_nnn_in_i,   # ANNN
    "addi": add_i,          # FX1E
    "draw": draw,           # DXYN
    "getd": set_I_digit,    # FX29

    "sdt": store_delay_vx,  # FX07
    "sdr": set_DT,          # FX15
    "sst": set_ST,          # FX18

    "wk": wait_for_key,     # FX0A
    "gbcd": get_bcd,        # FX33
    "dump": dump,           # FX55
    "fill": fill,           # FX65
    "db": db                # Data bytes
}

    # Assembler work
    collect_labels(file_content)
    for line in file_content:
        if not line or line[0].endswith(":"):
            continue

        memonic = line[0].lower()
        if memonic in mem_to_func:
            func = mem_to_func[memonic]
            if func in [cls, ret]:
                func()
            else:
                func(line)
        else:
            print(f"Unknown Instruction: {memonic}")        

    with open(output if output.endswith(".ch8") else output + ".ch8", "wb") as f:
        f.write(output_hex)
    print(f"Successfully assembled: {output}")

