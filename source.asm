MOV VA, 02        ; 6A02
MOV VB, 0C        ; 6B0C
MOV VC, 3F        ; 6C3F
MOV VD, 0C        ; 6D0C

MOV I, Paddle     ; A2F0
DRW VA, VB, 6     ; DAB6
DRW VC, VD, 6     ; DCD6

MOV VE, 00        ; 6E00
CALL Draw_Score   ; 2248

MOV V6, 03        ; 6603
MOV V8, 02        ; 6802

MOV V0, 60        ; 6060
MOV DT, V0        ; F015

MOV V0, DT        ; F007
SE V0, 00         ; 3000
JP 021A           ; 121A

RND V7, 17        ; C717
ADD V7, 08        ; 7708

MOV V9, FF        ; 69FF
MOV I, Ball       ; A2F6
DRW V6, V7, 1     ; D671

MOV I, Paddle     ; A2F0
DRW VA, VB, 6     ; DAB6
DRW VC, VD, 6     ; DCD6

MOV V0, 01        ; 6001
SKNP V0           ; E0A1
ADD VB, FE        ; 7BFE

MOV V0, 04        ; 6004
SKNP V0           ; E0A1
ADD VB, 02        ; 7B02

MOV V0, 1F        ; 601F
AND VB, V0        ; 8B02
DRW VA, VB, 6     ; DAB6

MOV V0, 0C        ; 600C
SKNP V0           ; E0A1
ADD VD, FE        ; 7DFE

MOV V0, 0D        ; 600D
SKNP V0           ; E0A1
ADD VD, 02        ; 7D02

MOV V0, 1F        ; 601F
AND VD, V0        ; 8D02
DRW VC, VD, 6     ; DCD6

MOV I, Ball       ; A2F6
DRW V6, V7, 1     ; D671

ADD V6, V8        ; 8684
ADD V7, V9        ; 8794

MOV V0, 3F        ; 603F
AND V6, V0        ; 8602

MOV V1, 1F        ; 611F
AND V7, V1        ; 8712

SNE V6, 02        ; 4602
JP 0250           ; 1250

SNE V6, 3F        ; 463F
JP 0260           ; 1260

SNE V7, 1F        ; 471F
MOV V9, FF        ; 69FF

SNE V7, 00        ; 4700
MOV V9, 01        ; 6901

DRW V6, V7, 1     ; D671
JP 022A           ; 122A

MOV V8, 02        ; 6802
MOV V3, 01        ; 6301
MOV V0, V7        ; 8070
SUB V0, VB        ; 80B5
JP 0270           ; 1270

MOV V8, FE        ; 68FE
MOV V3, 0A        ; 630A
MOV V0, V7        ; 8070
SUB V0, VD        ; 80D5

SE VF, 01         ; 3F01
JP 02A0           ; 12A0

MOV V1, 02        ; 6102
SUB V0, V1        ; 8015
SE VF, 01         ; 3F01
JP 0280           ; 1280

SUB V0, V1        ; 8015
SE VF, 01         ; 3F01
JP 0290           ; 1290

SUB V0, V1        ; 8015
SE VF, 01         ; 3F01
JP 0298           ; 1298

MOV V0, 20        ; 6020
MOV ST, V0        ; F018

CALL Draw_Score   ; 2248
ADD VE, V3        ; 8E34
CALL Draw_Score   ; 2248

MOV V6, 3E        ; 663E
SE V3, 01         ; 3301
MOV V6, 03        ; 6603

MOV V8, FE        ; 68FE
SE V3, 01         ; 3301
MOV V8, 02        ; 6802

JP 0216           ; 1216

ADD V9, FF        ; 79FF
SNE V9, FE        ; 49FE
MOV V9, FF        ; 69FF
JP 0290           ; 1290

ADD V9, 01        ; 7901
SNE V9, 02        ; 4902
MOV V9, 01        ; 6901

MOV V0, 04        ; 6004
MOV ST, V0        ; F018

ADD V6, 01        ; 7601
SNE V6, 40        ; 4640
ADD V6, FE        ; 76FE

JP 0268           ; 1268

MOV I, Score      ; A2F8
MOV B, VE         ; FE33
MOV V2, [I]       ; F265
MOV F, V1         ; F129

MOV V4, 14        ; 6414
MOV V5, 00        ; 6500
DRW V4, V5, 5     ; D455

ADD V4, 15        ; 7415
MOV F, V2         ; F229
DRW V4, V5, 5     ; D455

RET               ; 00EE
