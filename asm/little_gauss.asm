START:
    LOADI   R0, #1        ; constant 1
    LOADI   R1, #1        ; initialize counter
    LOADI   R2, #0        ; clear accumulator
    LOADI   R3, #100      ; upper limit
LOOP:
    ADD     R2, R2, R1    ; add counter to sum
    ADD     R1, R1, R0    ; increment counter
    SUB     R4, R1, R3    ; compute R1 - R3
    BNE     LOOP          ; if R1 != R3, continue loop
    ADD     R2, R2, R1    ; add final term (100)
DONE:
    HALT
