import sys
def disassemble(lines: bytearray) -> str:
    file = ""
    for i in range(0, len(lines), 2):
        operand = (lines[i] << 8) | lines[i+1]
        if operand == 0x00E0:
            file += "cls\n"
        elif operand >= 0xD000 and operand < 0xE000:
            vx = (operand >> 8) & 0xF
            vy = (operand >> 4) & 0xF
            n = operand & 0xF
            file += f"draw V{hex(vx)}, V{hex(vy)}, {hex(n)}\n"
        elif operand >= 0x1000 and operand < 0x2000:
            mem_address = operand & 0xFFF
            file += f"jmp {hex(mem_address)}\n"
        elif operand == 0x00EE:
            file += f"ret\n"
        elif operand >= 0x2000 and operand < 0x3000:
            nnn = (operand & 0xFFF)
            file += f"call {hex(nnn)}\n"
        elif operand >= 0x3000 and operand < 0x4000:
            vx = (operand >> 8) & 0xF
            nn = operand & 0xFF
            file += f"se V{hex(vx)}, {hex(nn)}\n"
        elif operand >= 0x4000 and operand < 0x5000:
            vx = (operand >> 8) & 0xF
            nn = operand & 0xFF
            file += f"sne V{hex(vx)}, {hex(nn)}\n"
        elif operand >= 0x5000 and operand < 0x6000:
            if (operand & 0xF) == 0:
                vx = (operand >> 8) & 0xF
                vy = (operand >> 4) & 0xF
                file += f"sxey V{hex(vx)}, V{hex(vy)}\n"
            else:
                file += f"db {hex(lines[i])}, {hex(lines[i+1])}\n"
        elif operand >= 0x6000 and operand < 0x7000:
            # set vx, nn
            vx = (operand >> 8) & 0xF
            nn = operand & 0xFF 
            file += f"set V{hex(vx)}, {hex(nn)}\n"
        elif operand >= 0x7000 and operand < 0x8000:
            # add x, nn
            vx = (operand >> 8) & 0xF
            nn = operand & 0xFF
            file += f"add V{hex(vx)}, {hex(nn)}\n"
        elif operand >= 0x8000 and operand < 0x9000:
            LSB = operand & 0xF
            vx = (operand >> 8) & 0xF
            vy = (operand >> 4) & 0xF
            if LSB == 0x0:
                file += f"copy V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x1:
                file += f"or V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x2:
                file += f"and V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x3:
                file += f"xor V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x4:
                file += f"addc V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x5:
                file += f"subc V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x6:
                file += f"shr V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0x7:
                file += f"subn V{hex(vx)}, V{hex(vy)}\n"
            elif LSB == 0xE:
                file += f"shl V{hex(vx)}, V{hex(vy)}\n"
        elif operand >= 0x9000 and operand < 0xA000:
                if (operand & 0xF) == 0:
                    vx = (operand >> 8) & 0xF
                    vy = (operand >> 4) & 0xF
                    file += f"sre V{hex(vx)}, V{hex(vy)}\n"
                else:
                    file += f"db {hex(lines[i])}, {hex(lines[i+1])}\n"
        elif operand >= 0xA000 and operand < 0xB000:
            file += f"si {hex(operand & 0xFFF)}\n"
        elif operand >= 0xB000 and operand < 0xC000:
            file += f"j0 {hex(operand & 0xFFF)}\n"
        elif operand >= 0xC000 and operand < 0xD000:
            vx = (operand >> 8) & 0xF
            file += f"rnd V{hex(vx)}, {hex(operand & 0xFF)}\n"
        elif operand >= 0xE000 and operand < 0xF000:
            LSB = operand & 0xFF
            vx = (operand >> 8) & 0xF
            if LSB == 0x9E:
                file += f"sk V{hex(vx)}\n"
            elif LSB == 0xA1:
                file += f"snk V{hex(vx)}\n"
        elif operand >= 0xF000 and operand < 0x10000:
            LB = operand & 0xFF
            vx = (operand >> 8) & 0xF
            if LB == 0x07:
                file += f"sdt V{hex(vx)}\n"
            elif LB == 0x0A:
                file += f"wk V{hex(vx)}\n"
            elif LB == 0x15:
                file += f"sdr V{hex(vx)}\n"
            elif LB == 0x18:
                file += f"sst V{hex(vx)}\n"
            elif LB == 0x1E:
                file += f"addo V{hex(vx)}\n"
            elif LB == 0x29:
                file += f"getd V{hex(vx)}\n"
            elif LB == 0x33:
                file += f"gbcd V{hex(vx)}\n"
            elif LB == 0x55:
                file += f"dump V{hex(vx)}\n"
            elif LB == 0x65:
                file += f"fill V{hex(vx)}\n"
        else:
            file += f"db {hex(lines[i])}, {hex(lines[i+1])}\n"
    return file

import os
if __name__ == "__main__":
    argv = sys.argv
    if len(argv) == 1:
        print(f"Correct Usage: python3 {argv[0]} <input.rom/ch8/bin> <output.asm/S: defualt=input.asm>")
    if len(argv) >= 2:
        input = argv[1]
        output = os.path.splitext(input)[0]
        if len(argv) >= 3:
            output = argv[2]
    if len(argv) > 4:
        print(f"Correct Usage: python3 {argv[0]} <input.rom/ch8/bin> <output.asm/S: defualt=input.asm>")
        sys.exit(-1)

    with open(input, "rb") as f:
        lines = bytearray(f.read())
    
    file_content = disassemble(lines)
    with open(output, "w") as f:
        f.write(file_content)
    
    print("Disassembly successful")