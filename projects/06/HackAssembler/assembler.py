asm = """// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/06/add/Add.asm

// Computes R0 = 2 + 3  (R0 refers to RAM[0])

@2
D=A
@3
D=D+A
@0
M=D
(xxx)
DM=D+A
D;JNE
"""

import re

class Parser:
    sym = r"([a-zA-Z_\.\$:][a-zA-Z0-9_\.\$:]+|[0-9]+)"
    a_instruction = re.compile(r"^@{0}$".format(sym))
    c_instruction = re.compile(r"^([ADM]+=[ADM](\+[ADM])?|[D0];J([GL][TE]|EQ|NE|MP]))$")
    l_instruction = re.compile(r"^\({0}\)$".format(sym))

    def __init__(self, file):
        self.file = self._preprocess_file(file)
        self.index = 0

    def _preprocess_file(self, file):
        file = [ s.strip() for s in file.split("\n") ]
        file = filter(lambda l: len(l) > 0, file)
        file = filter(lambda l: l[:2] != '//', file)
        return list(file)

    @property
    def has_more_lines(self):
        "Are there more lines in the input?"
        return self.index < len(self.file) - 1

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

        line = self.file[self.index]
        a = self.a_instruction.fullmatch(line)
        c = self.c_instruction.fullmatch(line)
        l = self.l_instruction.fullmatch(line)

        if a:
            return 'A_INSTRUCTION'
        elif c:
            return 'C_INSTRUCTION'
        elif l:
            return 'L_INSTRUCTION'
        else:
            return 'UNKNOWN: %s'.format(line)

    @property
    def symbol(self):
        """
        If the current instruction is (xxx), returns the symbol xxx.
        If the current instruction is @xxx, returns the symbol or decimal xxx
        (as a string).
        Should be called only if instruction_type is A_INSTRUCTION or L_INSTRUCTION.
        """
        return re.search(re.compile(self.sym), self.file[self.index]).group(1)

    @property
    def dest(self):
        """
        Returns the symbolic dest part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        pattern = r"^(A|D|M|AD|AM|DM|ADM)="
        # return re.search(re.compile(r"^([A?D?M?]{1,3})="), self.file[self.index]).group(1)
        return re.search(re.compile(pattern), self.file[self.index]).group(1)

    @property
    def comp(self):
        """
        Returns the symbolic comp part of the current C-instruction (28 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        pattern = r"^{0}=(0|[-!]?[ADM]|[ADM][+-]1|D[+-][AM]|[AM]-D|D[&\|][AM])$".format(self.dest)
        # pattern = r"^{0}=(0|1|-1|D|A|M|!D|!A|!M|-D|-A|-M|D+1|A+1|M+1|D-1|A-1|M-1|D+A|D+M|D-A|D-M|A-D|M-D|D&A|D&M|D\|A|D\|M)$".format(self.dest)
        return re.search(re.compile(pattern), self.file[self.index]).group(1)

    @property
    def jump(self):
        """
        Returns the symbolic jump part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION.
        """
        pattern = f"^[0ADM];(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)$"
        return re.search(re.compile(pattern), self.file[self.index]).group(1)


class Code:

    def dest(self, code):
        "Returns the binary code of the dest mnemonic."
        codes = {
            'M'  : '001',
            'D'  : '010',
            'DM' : '011',
            'A'  : '100',
            'AM' : '101',
            'AD' : '110',
            'ADM': '111'
        }
        return codes[code]

    def comp(self, code):
        "Returns the binary code of the comp mnemonic."
        codes = {
            '0'  : '0101010',
            '1'  : '0111111',
            '-1' : '0111010',
            'D'  : '0001100',
            'A'  : '0110000',
            'M'  : '1110000',
            '!D' : '0001101',
            '!A' : '0110001',
            '!M' : '1110001',
            '-D' : '0001111',
            '-A' : '0110011',
            '-M' : '1110011',
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
            'JGT' : '001',
            'JEQ' : '010',
            'JGE' : '011',
            'JLT' : '100',
            'JNE' : '101',
            'JLE' : '110',
            'JMP' : '111'
        }
        return codes[code]


def tests():
    
    def check_equal(L1, L2):
        return len(L1) == len(L2) and sorted(L1) == sorted(L2)

    p = Parser(asm)
    c = Code()
    assert check_equal(p.file, ['@2', 'D=A', '@3', 'D=D+A', '@0', 'M=D', '(xxx)',
                                'DM=D+A', 'D;JNE'])
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '2'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "D"
    assert c.dest(p.dest) == '010'
    assert p.comp == "A"
    assert c.comp(p.comp) == '0110000'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '3'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "D"
    assert c.dest(p.dest) == '010'
    assert p.comp == "D+A"
    assert c.comp(p.comp) == '0000010'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '0'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "M"
    assert c.dest(p.dest) == '001'
    assert p.comp == "D"
    assert c.comp(p.comp) == '0001100'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'L_INSTRUCTION'
    assert p.symbol == 'xxx'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "DM"
    assert c.dest(p.dest) == '011'
    assert p.comp == "D+A"
    assert c.comp(p.comp) == '0000010'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.jump == "JNE"
    assert c.jump(p.jump) == '101'
    assert not p.has_more_lines
    print("Tests pass")

tests()