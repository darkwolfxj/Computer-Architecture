"""CPU functionality."""
from handlers import handle_LDI, handle_ADD, handle_MULT, handle_PUSH, handle_POP, handle_PRN, handle_HLT, handle_CMP,handle_JEQ,handle_JNE,handle_CALL,handle_RET
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 7 + [255]
        self.pc = 0
        self.isrunning = True
        self.e_flag = 0
        self.l_flag = 0
        self.g_flag = 0
        self.ops = {
            0b10000010: 
                "LDI",
            0b10100000:
                "ADD",
            0b10100010:
                "MULT",
            0b01000101:
                "PUSH",
            0b01000110:
                "POP",
            0b01000111:
                "PRN",
            0b00000001:
                "HLT",
            0b10100111:
                "CMP",
            0b01010101:
                "JEQ",
            0b01010110:
                "JNE",
            0b01010000:
                "CALL",
            0b00010001:
                "RET"
        }
    def load(self, p="ls8/examples/sctest.ls8"):
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
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.g_flag = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.l_flag = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.e_flag = 1
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
    def execute(self, op):
        commands = {
            "LDI": 
                handle_LDI,
            "ADD":
                handle_ADD,
            "MULT":
                handle_MULT,
            "PUSH":
                handle_PUSH,
            "POP":
                handle_POP,
            "PRN":
                handle_PRN,
            "HLT":
                handle_HLT,
            "CMP":
                handle_CMP,
            "JEQ":
                handle_JEQ,
            "JNE":
                handle_JNE,
            "CALL":
                handle_CALL,
            "RET":
                handle_RET         
        }
        op = self.ops[op] if op in self.ops else op
        if op in commands:
            return commands[op](self)
        else:
            self.pc += 1 + (op >> 6)
    
    def run(self):
        """Run the CPU."""
        while self.isrunning:
            # read the ram at that address and find if it's a command or a value
            instruction = self.ram_read(self.pc)
            if instruction not in [0b01010101,0b01010110,0b010100000,0b00010001]:
                self.execute(instruction)
                self.pc += 1 + (instruction >> 6)
            else:
                if self.execute(instruction) == "jump":
                    continue
                else:
                    self.pc += 1 + (instruction >> 6)
            if self.pc > 255:
                self.isrunning = False
        
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
# for debugging     
cpu = CPU()
cpu.load()
cpu.run()