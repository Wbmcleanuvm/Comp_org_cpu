START:
    LOADI R0, 5 #multiply by
    LOADI R1, 0 #min
    LOADI R2, 0 #memory
    LOADI R3, 9
    ADD R4, R0, R0 #start mult
LOOP:
    STORE R4, R1, 0
    ADD R4, R4, R4
    ADDI R1, R1, 1
    ADDI R2, R2, 1     # increment 
    SUB R5, R2, R4     # if sub fails loop ends
    BNE LOOP       
DONE: 
    HALT    

