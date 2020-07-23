"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 7 + [255]
        self.pc = 0
        self.isrunning = True
        

    def load(self, p):
        """Load a program into memory."""

        address = 0
        # program = [
        #     0b10000010,
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,
        #     0b00000000,
        #     0b00000001,
        #     ]
        # for instruction in program:
        #         self.ram[address] = instruction
        #         address += 1
        with open(p) as program:
            for line in program:
                instruction = line.split("#")[0].strip()
                if instruction != '':
                    try:
                        self.ram[address] = int(instruction, 2)
                        address += 1
                    except IndexError:
                        print("Memory overflow!")
                        return        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
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
        while self.isrunning:
            # read the ram at that address and find if it's a command or a value
            instruction = self.ram_read(self.pc)
            if instruction == 0b10000010: # LDI
                reg_address = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                self.reg[reg_address] = reg_value
            elif instruction == 0b10100000: # ADD
                regA = self.ram_read(self.pc + 1)
                regB = self.ram_read(self.pc + 2)
                op = 'ADD'
                self.alu(op, regA, regB)
            elif instruction == 0b10100010: # MULT
                # store values in regA and regB
                regA = self.ram_read(self.pc + 1)
                regB = self.ram_read(self.pc + 2)
                op = 'MULT'
                # store product in regA
                self.alu(op, regA, regB)
            elif instruction == 0b01000101: # PUSH
                self.reg[7] -= 1
                mdr = self.reg[self.ram_read(self.pc + 1)]
                self.ram_write(self.reg[7], mdr)
            elif instruction == 0b01000110: # POP 
                regA = self.ram_read(self.pc + 1)
                mdr = self.ram_read(self.reg[7])
                self.reg[regA] = mdr
                self.reg[7] += 1
            elif instruction == 0b01000111: # PRN
                print(self.reg[self.ram_read(self.pc + 1)])
            elif instruction == 0b00000001: # HLT
                self.isrunning = False
            elif instruction == 0b01010000: # CALL
                jump_value = self.reg[self.ram_read(self.pc + 1)]
                return_value = self.pc + 2
                self.reg[7] -= 1
                self.ram_write(self.reg[7], return_value) 
                self.pc = jump_value
                continue
            elif instruction == 0b00010001: # RET
                return_value = self.ram_read(self.reg[7])
                self.reg[7] += 1
                self.pc = return_value
                continue
            else:
                self.pc += 1 + (instruction >> 6)
            self.pc += 1 + (instruction >> 6)
            if self.pc > 255:
                self.isrunning = False
        
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr