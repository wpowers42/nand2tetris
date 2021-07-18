import re
import sys
import os

class Parser:    

    def __init__(self, filename=None, file=None):
        if not file:
            self.file = self._open_file(filename)
        else:
            self.file = file
        self.file = self._preprocess_file(self.file)
        self.index = 0

    def _open_file(self, filename):
        with open(filename) as f:
            return ''.join(f.readlines())

    def _preprocess_file(self, file):
        file = file.split("\n")
        file = [ s.split("//")[0] for s in file]
        file = [ s.strip() for s in file ]
        file = filter(lambda l: len(l) > 0, file)
        file = filter(lambda l: l[:2] != '//', file)
        file = [ self._normalize(l) for l in file ]
        return list(file)

    def _normalize(self, line):
        # normalizes c-instructions by adding null dest & jump fields
        # if they're unspecified
        # credit: https://github.com/rose/nand2tetris/blob/master/assembler.py

        if line[0] == "@" or line[0] == "(":
            pass
        elif not "=" in line:
            line = "null=" + line
        elif not ";" in line:
            line = line + ";null"
        return line

    @property
    def has_more_lines(self):
        "Are there more lines in the input?"
        return self.index < len(self.file)

    @property
    def instruction(self):
        "What is the current instruction"
        return self.file[self.index]

    @property
    def advance(self):
        """
        Skips over white space and comments, if necessary.
        Reads the next instruction from the input, and makes it the current instruction.
        This routine should be called only if has_more_lines is true.
        Initially there is no current instruction.
        """
        self.index += 1

    @property
    def instruction_type(self):
        """
        Returns the type of the current instruction:
        A_INSTRUCTION for @xxx, where xxx is either a decimal number or a symbol
        C_INSTRUCTION for dest=comp;jump
        L_INSTRUCTION for (xxx), where xxx is a symbol.
        """
        if re.compile(r"^@.+$").match(self.file[self.index]):
            return 'A_INSTRUCTION'
        elif re.compile(r"^(.{1,3}|null)=.+;.+$").match(self.file[self.index]):
            return 'C_INSTRUCTION'
        elif re.compile(r"^\(.+\)$").match(self.file[self.index]):
            return 'L_INSTRUCTION'
        else:
            print('Unable to process line: {0}'.format(self.file[self.index]))

    @property
    def symbol(self):
        """
        If the current instruction is (xxx), returns the symbol xxx.
        If the current instruction is @xxx, returns the symbol or decimal xxx
        (as a string).
        Should be called only if instruction_type is A_INSTRUCTION or L_INSTRUCTION.
        """ 
        if self.instruction_type == "A_INSTRUCTION":
            symbol = self.file[self.index][1:]
        elif self.instruction_type == "L_INSTRUCTION":
            symbol = self.file[self.index][1:-1]
        else:
            raise ValueError("symbol called for invalid instruction")

        if re.compile(r"^(?!\d)[a-zA-Z0-9_\.\$:]+$").match(symbol) or symbol.isnumeric():
            return symbol
        else:
            raise ValueError("improperly formatted symbol: {0}".format(symbol))
    @property
    def dest(self):
        """
        Returns the symbolic dest part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        dest = self.file[self.index].split("=")[0]
        if dest != "null":
            dest = "".join(sorted(dest))
        return dest

    @property
    def comp(self):
        """
        Returns the symbolic comp part of the current C-instruction (28 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        return self.file[self.index].split("=")[1].split(";")[0]

    @property
    def jump(self):
        """
        Returns the symbolic jump part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION.
        """
        return self.file[self.index].split("=")[1].split(";")[1]

class Code:

    def dest(self, code):
        "Returns the binary code of the dest mnemonic."
        if not code:
            return '000'

        codes = {
            'null' : '000',
            'M'    : '001',
            'D'    : '010',
            'DM'   : '011',
            'A'    : '100',
            'AM'   : '101',
            'AD'   : '110',
            'ADM'  : '111'
        }
        return codes[code]

    def comp(self, code):
        "Returns the binary code of the comp mnemonic."
        codes = {
            '0'   : '0101010',
            '1'   : '0111111',
            '-1'  : '0111010',
            'D'   : '0001100',
            'A'   : '0110000',
            'M'   : '1110000',
            '!D'  : '0001101',
            '!A'  : '0110001',
            '!M'  : '1110001',
            '-D'  : '0001111',
            '-A'  : '0110011',
            '-M'  : '1110011',
            'D+1' : '0011111',
            'A+1' : '0110111',
            'M+1' : '1110111',
            'D-1' : '0001110',
            'A-1' : '0110010',
            'M-1' : '1110010',
            'D+A' : '0000010',
            'D+M' : '1000010',
            'D-A' : '0010011',
            'D-M' : '1010011',
            'A-D' : '0000111',
            'M-D' : '1000111',
            'D&A' : '0000000',
            'D&M' : '1000000',
            'D|A' : '0010101',
            'D|M' : '1010101'
        }

        return codes[code]

    def jump(self, code):
        "Returns the binary code of the jump mnemonic."
        if not code: return '000'
        codes = {
            'null': '000',
            'JGT' : '001',
            'JEQ' : '010',
            'JGE' : '011',
            'JLT' : '100',
            'JNE' : '101',
            'JLE' : '110',
            'JMP' : '111'
        }
        return codes[code]

class Symbol():

    def __init__(self):
        self.table = { }

        for i in range(16):
            self.add_entry(f'R{i}', i)

        self.add_entry('SP' , 0)
        self.add_entry('LCL', 1)
        self.add_entry('ARG', 2)
        self.add_entry('THIS', 3)
        self.add_entry('THAT', 4)
        self.add_entry('SCREEN', 16384)
        self.add_entry('KBD', 24576)
        self.next_address = 16

    def add_entry(self, entry, address=None):
        if address is None:
            address = self.next_address
            self.next_address += 1
        self.table[entry] = address

    def contains(self, symbol):
        return symbol in self.table

    def get_address(self, symbol):
        return self.table[symbol]

class Assembler():

    def __init__(self, filename=None):
        self.infile = filename if filename else sys.argv[1]
        self._create_outfile()
        
        self.code = Code()
        self.symbol = Symbol()

        self._first_pass()
        self._second_pass()

    def _first_pass(self):
        self.parser = Parser(filename=self.infile)
        index = 0
        while True:
            if not self.parser.has_more_lines:
                break
            if self.parser.instruction_type == 'L_INSTRUCTION':
                self.symbol.add_entry(self.parser.symbol, index)
            else:
                index += 1
            self.parser.advance

    def _second_pass(self):
        self.parser = Parser(filename=self.infile)
        while True:
            if not self.parser.has_more_lines:
                break
            if self.parser.instruction_type == 'A_INSTRUCTION':
                self._parse_a_instruction()
            elif self.parser.instruction_type == 'C_INSTRUCTION':
                self._parse_c_instruction()
            elif self.parser.instruction_type == 'L_INSTRUCTION':
                pass
            else:
                Exception(self.parser.instruction_type)
            self.parser.advance

    def _create_outfile(self):
        self.outfile = os.path.splitext(self.infile)[0] + '.hack'
        open(self.outfile, 'w')

    def _write_line(self, line):
        with open(self.outfile, 'a') as f:
            f.write(line + '\n')

    def _parse_a_instruction(self):
        symbol = self.parser.symbol
        if not symbol.isnumeric():
            if not self.symbol.contains(symbol):
                self.symbol.add_entry(symbol)

            symbol = self.symbol.get_address(symbol)

        line = "{0:b}".format(int(symbol)).zfill(16)
        # print(self.parser.symbol, symbol, line)

        self._write_line(line)

    def _parse_c_instruction(self):
        line = '111'
        line += self.code.comp(self.parser.comp)
        line += self.code.dest(self.parser.dest)
        line += self.code.jump(self.parser.jump)
        self._write_line(line)

if __name__ == "__main__":
    Assembler()