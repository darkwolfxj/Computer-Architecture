def handle_LDI(self):
    reg_address = self.ram_read(self.pc + 1)
    reg_value = self.ram_read(self.pc + 2)
    self.reg[reg_address] = reg_value
def handle_ADD(self):
    regA = self.ram_read(self.pc + 1)
    regB = self.ram_read(self.pc + 2)
    op = 'ADD'
    self.alu(op, regA, regB)
def handle_MULT(self):
    # store values in regA and regB
    regA = self.ram_read(self.pc + 1)
    regB = self.ram_read(self.pc + 2)
    op = 'MULT'
    # store product in regA
    self.alu(op, regA, regB)
def handle_PUSH(self):
    self.reg[7] -= 1
    mdr = self.reg[self.ram_read(self.pc + 1)]
    self.ram_write(self.reg[7], mdr)
def handle_POP(self):
    regA = self.ram_read(self.pc + 1)
    mdr = self.ram_read(self.reg[7])
    self.reg[regA] = mdr
    self.reg[7] += 1
def handle_PRN(self):
    print(self.reg[self.ram_read(self.pc + 1)])
def handle_HLT(self):
    self.isrunning = False
def handle_CMP(self):
    op = "CMP"
    reg_a = self.ram_read(self.pc + 1)
    reg_b = self.ram_read(self.pc + 2)
    self.alu(op, reg_a, reg_b)
def handle_JEQ(self):
    if self.e_flag == 1:
        jump_value = self.reg[self.ram_read(self.pc + 1)]
        self.pc = jump_value
        self.e_flag = 0
        return "jump"
def handle_JNE(self):
    if self.e_flag == 0:
        jump_value = self.reg[self.ram_read(self.pc + 1)]
        self.pc = jump_value
        self.e_flag = 0
        return "jump"
def handle_CALL(self):
    jump_value = self.reg[self.ram_read(self.pc + 1)]
    return_value = self.pc + 2
    self.reg[7] -= 1
    self.ram_write(self.reg[7], return_value) 
    self.pc = jump_value
def handle_RET(self):
    return_value = self.ram_read(self.reg[7])
    self.reg[7] += 1
    self.pc = return_value