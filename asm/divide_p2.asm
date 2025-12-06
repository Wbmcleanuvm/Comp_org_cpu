START:
    LOADI R0, 0x1C0
    LOADI R1, 0x0006 
    LUI R1, 0x80 # add shift 

    SHFT R2, R0, R1
    SHFT R3, R2, R1 
    SHFT R4, R3, R1
    SHFT R5, R4, R1
    SHFT R6, R5, R1 
    SHFT R7, R6, R1
DONE:
    HALT

