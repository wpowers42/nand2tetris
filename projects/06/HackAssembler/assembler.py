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
"""

import re

class Parser:
    _symbol = r"([a-zA-Z_\.\$:][a-zA-Z0-9_\.\$:]+|[0-9]+)"
    a_instruction = re.compile(r"^@{0}$".format(_symbol))
    c_instruction = re.compile(r"^[ADM]=[ADM](\+[ADM])?$")
    l_instruction = re.compile(r"^\({0}\)$".format(_symbol))

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
        return re.search(re.compile(self._symbol), self.file[self.index]).group(1)

    @property
    def dest(self):
        """
        Returns the symbolic dest part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        pass

    @property
    def comp(self):
        """
        Returns the symbolic comp part o fth ecurrent C-instruction (28 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        pass

    @property
    def jump(self):
        """
        Returns the symbolic jump part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION.
        """
        pass

# dest_codes = {
#             'M'  : '001',
#             'D'  : '010',
#             'DM' : '011',
#             'A'  : '100',
#             'AM' : '101',
#             'AD' : '110',
#             'ADM': '111'
#         }


def tests():
    
    def check_equal(L1, L2):
        return len(L1) == len(L2) and sorted(L1) == sorted(L2)

    p = Parser(asm)
    assert check_equal(p.file, ['@2', 'D=A', '@3', 'D=D+A', '@0', 'M=D', '(xxx)'])
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.has_more_lines
    assert p.symbol == '2'
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '3'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '0'
    assert p.has_more_lines
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    p.advance
    assert p.instruction_type == 'L_INSTRUCTION'
    assert p.symbol == 'xxx'
    assert not p.has_more_lines
    print("Tests pass")

tests()