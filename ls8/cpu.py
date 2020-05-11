"""CPU functionality."""

import sys

# need to make my op codes for translation of the functions below
# if using binary to match decimal style being saved need to have
# the starting zeros removed when saving then to the ops code below

ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b1100101
DEC = 0b1100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b1101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101


LDI = 0b10000010  # load immediate - goes into a reg
PRN = 0b01000111  # prints a number from reg
HLT = 0b1  # stops program

print(f"0b1010: ", 0b1010)
print(f"binary for 10: {int('1010', 2)}")
print(f"decimal to what should be binary: {bin(10)}")


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # this emulator only has * registers
        self.ram = [0] * 256  # ram is the memory i believe so far
        self.pc = 0  # this is the Program Counter... points to the location in memory at what program to read...current action
        self.running = True  # sets this as a starter flag for the loop to run
        self.fl = 0
        self.ie = 0
        pass


# this gets me  a simplified binary number without the first zeros
# may need to get to the shift part


    def get_number(self, list):
        add_up = 0
        if list[0] == '1':
            add_up += 128
        if list[1] == '1':
            add_up += 64
        if list[2] == '1':
            add_up += 32
        if list[3] == '1':
            add_up += 16
        if list[4] == '1':
            add_up += 8
        if list[5] == '1':
            add_up += 4
        if list[6] == '1':
            add_up += 2
        if list[7] == '1':
            add_up += 1

        return bin(add_up)

    def load(self):
        # may be a good idea to set this up with a
        # default as sys.argv[1] which is the file after
        # "python ls8.py [sys.argv file name here]"
        """Load a program into memory."""
        address = 0
        print(sys.argv)
        if len(sys.argv) != 2:
            print("to enter a file to run")
            sys.exit(1)
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                if line == '':
                    continue
                comment_split = line.split('#')
                num = comment_split[0].strip()
                new_num = num
                if len(new_num) > 2:
                    # print(str(new_num))
                    num = new_num
                    num = int(num, 2)
                    print(bin(num))
                    # print(self.get_number(num))
                    # self.ram[address] = self.get_number(num)
                    self.ram[address] = num
                    address += 1

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]  # this emulates grabbing the info from the file

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[self.ram[reg_a]] += self.reg[self.ram[reg_b]]

        elif op == "SUB":
            # this may need adjustment..
            # don't think binary handles neg numbers...
            # we'll see i guess
            val1 = self.reg[self.ram[reg_a]]
            val2 = self.reg[self.ram[reg_b]]
            new_val = val1 - val2
            self.reg[self.ram[reg_a]] = new_val

        elif op == MUL:
            val1 = self.reg[self.ram[reg_a]]
            val2 = self.reg[self.ram[reg_b]]
            new_val = val1 * val2
            self.reg[self.ram[reg_a]] = new_val

        elif op == "DIV":
            self.reg[self.ram[reg_a]] /= self.reg[self.ram[reg_b]]

        else:
            raise Exception("Unsupported ALU operation")

    def ldi(self, regN, value):  # in run()
        self.reg[regN] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, pc):  # reads data from ram/memory at a specific location
        read_at = self.ram[pc]
        print(read_at)

    def ram_write(self, ramN, value):  # writes info to the ram/memory at a specific location
        self.ram[ramN] = value

    def halt(self):  # in run()
        self.running = False

    def PRN(self):  # in run()
        # self.ram_read(self.pc+1)
        the_P = self.ram[self.pc+1]
        # print(f"the_P: ", the_P)
        print_it = self.reg[the_P]
        print(print_it)
        self.pc += 2

    def run(self):
        """Run the CPU."""
        while self.running:
            command = self.ram[self.pc]

            if command == PRN:
                self.PRN()

            elif command == MUL:
                print(f"printing self.reg: \n", self.reg)
                print(f"ram/memory: \n{self.ram}")
                print(f"pc current location: {self.pc}")
                counter1 = self.pc+1
                counter2 = self.pc+2
                print(counter1, counter2)
                print(f"the pc is at: {self.pc}")
                self.alu(MUL, counter1, counter2)
                self.pc += 3

            elif command == LDI:
                self.pc += 1
                register_number = self.ram[self.pc]
                rg = register_number
                self.pc += 1
                self.reg[rg] = self.ram[self.pc]
                value_string = self.reg[rg]
                vs = value_string
                # print(f"just before assigning: rg: {rg}, vs: {vs}")
                self.ldi(rg, vs)

                self.pc += 1

            elif command == HLT:
                self.halt()

            else:
                print(f"we don't know that shit... need to add more funcitons")
                sys.exit(1)
