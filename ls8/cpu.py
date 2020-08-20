"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = True
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.op_size = 0

    def ram_read(self, mar): 
        """
         Memory Address Register (MAR)
         Contains the address that is being read or written to
        """
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        """
        Memory Data Register (MDR)
        Contains the data that was read or the data to write
        """
        self.ram[mar] = mdr
        return self.ram[mar]        

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue
                    
                    val = int(n, 2)
                    self.ram[address] = val

                    address +=1
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

    def run(self):
        """Run the CPU."""

        # https://github.com/rsmecking/Computer-Architecture/blob/master/LS8-spec.md
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000

        SP = 7
        self.reg[SP] = 0xf4
        

        while self.running:
            cmd = self.ram_read(self.pc)
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            
            # Halt the CPU (and exit the emulator).
            if cmd == HLT:
                self.running = False                
                self.op_size = 1
            
            # Print numeric value stored in the given register. 
            # Print to the console the decimal integer value that is stored in the given register.
            elif cmd == PRN:                
                print(self.reg[operand_a])
                self.op_size = 2
                
            # Set the value of a register to an integer.
            elif cmd == LDI:
                self.reg[operand_a] = operand_b
                self.op_size = 3 

            # Multiply the values in two registers together and store the result in registerA.
            elif cmd == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.op_size = 3

            # Push the value in the given register on the stack.
                # Decrement the SP.
                # Copy the value in the given register to the address pointed to by SP.
            elif cmd == PUSH:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.reg[operand_a]
                self.op_size = 2

            # Pop the value at the top of the stack into the given register.
                # Copy the value from the address pointed to by SP to the given register.
                # Increment SP. 
            elif cmd == POP:
                self.reg[operand_a] = self.ram[self.reg[SP]]
                self.reg[SP] += 1
                self.op_size = 2
            
            # Calls a subroutine (function) at the address stored in the register
            elif cmd == CALL:
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                self.pc = self.reg[operand_a]
                
                self.op_size = 0

            # Return from subroutine.
            # Pop the value from the top of the stack and store it in the PC.
            elif cmd == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1
                self.op_size = 0

            # Add the value in two registers and store the result in registerA.
            elif cmd == ADD:
                self.reg[operand_a] += self.reg[operand_b]
                self.op_size = 3

            else:
                print(f"Invalid Instruction: {cmd}")
                running = False

            self.pc += self.op_size

