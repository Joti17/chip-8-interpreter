set VA, 0x02                    # 6a02
set VB, 0x0c                    # 6b0c
set VC, 0x3f                    # 6c3f
set VD, 0x0c                    # 6d0c
si 0x2ea                        # a2ea
draw VA, VB, 0x06               # dab6
draw VC, VD, 0x06               # dcd6
set VE, 0x00                    # 6e00
call 0x2d4                      # 22d4
set V6, 0x03                    # 6603
set V8, 0x02                    # 6802
set V0, 0x60                    # 6060
tds V0                          # f015
sdt V0                          # f007
se V0, 0x00                     # 3000
jmp 0x21a                       # 121a
