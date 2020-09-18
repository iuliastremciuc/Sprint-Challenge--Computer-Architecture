"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.fl = [0] * 8
        self.pc = 0
        self.running = True
        self.SP = 7
        self.reg[self.SP] = 0xF4
    
    def ram_read(self, indx):
        return self.ram[indx]

    def ram_write(self, value, indx):

        self.ram[indx] = value


    def load(self):
        """Load a program into memory."""

        address = 0

       
        print(sys.argv)
        if len(sys.argv) != 2:
            print("usage: ls8.py filename")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    spliting = line.split('#')
                    v = spliting[0].strip()

                    if v == '':
                        continue

                    try:
                        v = int(v, 2)
                    except ValueError:
                        print(f"Invalid number '{v}'")
                        sys.exit(1)

                    self.ram[address] = v
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
      
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            multy = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = multy
        
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[0] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl[1] = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl[2] = 1
           
         
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

        print()
    
    def run(self):
        """Run the CPU."""
        HLT = 0b00000001    # 1
        PRN = 0b01000111    # 71
        LDI = 0b10000010    # 130
        MUL = 0b10100010    # 162
        CMP = 0b10100111    # 167
        JMP = 0b01010100    # 84
        JEQ = 0b01010101    # 85
        JNE = 0b01010110    # 86
       
        while self.running:

            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
        
            if ir == HLT:    # HLT   1
                self.running = False

            elif ir == PRN:  # PRN   71
               
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == LDI: # LDI    130
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == MUL:  # MUL
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            elif ir == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3

            elif ir == JMP:
                jump_to = self.reg[operand_a]
                self.pc = jump_to

            elif ir == JEQ:
                if self.fl[2] == 1:
                    jump_to = self.reg[operand_a]
                    self.pc = jump_to
                else:
                    self.pc += 2
            
            elif ir == JNE:
                if self.fl[2] == 0:
                    jump_to = self.reg[operand_a]
                    self.pc = jump_to
                else:
                    self.pc += 2
                












                

   





        
