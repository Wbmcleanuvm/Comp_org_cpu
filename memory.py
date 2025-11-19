"""
We're going with Harvard architecture here. So we'll have two separate
address spaces, one for data and one for instructions. A portion of data
memory is reserved for the stack (addresses between 0xFFFF and 0xFF00).

CS 2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

First released: 2025-11-10
  Revision: 2025-11-11
  - Added `return True` to all write methods and write stubs.
  Revision: 2025-11-12
  - Moved definition of `STACK_BASE` to `constants.py`.
"""

from constants import STACK_BASE, WORD_SIZE, WORD_MASK, STACK_TOP


class Memory:
    """Sparse word-addressable memory for Catamount PU simulation."""

    def __init__(self, default=0):
        self._cells = {}
        self.default = default
        self._write_enable = False

    def _check_addr(self, address):
        # Make sure address is positive, in the desired range,
        if  0 <= address and address < STACK_TOP:
            return True
        else:
            ValueError("Address is negative or out of range.")
        pass

    def write_enable(self, b):
        # Make sure `b` is a Boolean (hint: use `isinstance()).
        if isinstance(b, bool):
            self._write_enable = b
            return
        # If not, raise `TypeError`. If OK, then set
        else:
            TypeError("Write enable flag must be Boolean.")
        # `_write_enable` accordingly. Replace `pass` below.

    def read(self, addr):
        """
        Return 16-bit word from memory (default if never written).
        """
        if self._check_addr(addr):
            return self._cells.get(addr, self.default)
        else:
            return None        

        # Make sure `addr` is OK by calling `_check_addr`. If OK, return value
        # from `_cells` or default if never written. (Hint: use `.get()`.)
        # Replace `pass` below.

    def write(self, addr, value):
        """
        Write 16-bit word to memory, masking to 16 bits.
        """
        # Check to see if `_write_enable` is true. If not, raise `RuntimeError`
        if self._write_enable == True:
             # Otherwise, call `_check_addr()`. If OK, write masked value to the
            if self._check_addr(addr) == True:
                self._cells[addr] = value & 0xFFFF
            # selected address, then turn off `_write_enable` when done. Return
            self.write_enable(False)
        else:
            raise RuntimeError("Write attempted while write enable off.")
        # `True` on success. Replace `pass` below.
        return True

    def hexdump(self, start=0, stop=None, width=8):
        """
        Yield formatted lines showing memory cells in ascending order
        from `start` to the highest initialized address (or `stop` if provided).
        Uninitialized cells display as 0000.
        """
        if not self._cells:
            return  # nothing to show

        highest = max(self._cells)
        end = highest + 1 if stop is None else min(stop, highest + 1)

        for base in range(start, end, width):
            row = []
            for offset in range(width):
                addr = base + offset
                if addr >= end:
                    break
                val = self._cells.get(addr, 0)
                row.append(f"{val:04X}")
            yield f"{base:04X}: {' '.join(row)}"

    def __len__(self):
        return len(self._cells)

    def __contains__(self, addr):
        return addr in self._cells


class DataMemory(Memory):
    """
    Word-addressable memory for data. Reserves a portion for stack use.
    """

    def write(self, addr, value, from_stack=False):
        if addr >= STACK_BASE and not from_stack:
            raise RuntimeError(f"Write to stack region {addr:#06x} disallowed.")
        super().write(addr, value)
        return True


class InstructionMemory(Memory):
    """
    Word-addressable memory for instructions. Load once, then read-only
    thereafter.
    """

    def __init__(self, default=0):
        super().__init__(default)
        self._loading = False  # internal guard flag

    def write(self, addr, value):
        """
        Prevent runtime writes except during program loading.
        """
        if not self._loading:
            raise RuntimeError("Cannot write to instruction memory outside of loader.")
        super().write(addr, value)
        return True

    def load_program(self, words, start_addr=0x0000):
        """
        Load list of 16-bit words into consecutive memory cells.
        """
        self._loading = True
        self._write_enable(self,True)
        # Write each word in `words` to successive addresses in instruction
        # memory. Set `_write_enable` as needed can call parent write with
        wordsLst = list(enumerate(words))
        for i, w in wordsLst:
            super().write(start_addr + i, w)
        # `super().write(start_addr + offset, word)` as needed. Important:
        # Ensure that `_loading` and `_write_enable` are set to `False` when
        # done. (Hint: use `try`/`finally`.) Replace `pass` below.
        self._loading = False
        self._write_enable(self,False)


if __name__ == "__main__":

    # Quick smoke test...
    dm = DataMemory()
    dm.write_enable(True)
    dm.write(0x0000, 0x1234)
    dm.write_enable(True)
    dm.write(0x00F0, 0xABCD)
    dm.write_enable(False)
    for cell in dm.hexdump():
        print(cell)
    print()
    for cell in dm.hexdump(start=0x00F0):
        print(cell)
    print()
