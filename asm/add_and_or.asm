START:
    LOADI R0, 0xAA      

    AND R3, R0, R1      # check if equal
    BNE DONE            # unsafe, end
    # Safe case: perform OR
    OR R2, R0, R1       # Safe, add
DONE:
    HALT