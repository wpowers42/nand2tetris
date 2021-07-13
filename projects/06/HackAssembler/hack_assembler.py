import sys
import argparse

class Parser:
    index = 0

    def __init__(self, infile=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin)
        if infile:
            args = parser.parse_args([infile])
        else:
            args = parser.parse_args()
        args.infile.seek(0,0)
        self.file = [ s.strip() for s in args.infile.readlines() ]

    @property
    def has_more_lines(self):
        "Are there more lines in the input?"
        return self.index < len(self.file) - 1

    @property
    def current_instruction(self):
        return self.file[self.index]

    @property
    def advance(self):
        """
        Skips over white space and comments, if necessary.
        Reads the next instruction from the input, and makes it the current instruction.
        This routine should be called only if has_more_lines is true.
        Initially there is no current instruction.
        """
        if self.has_more_lines:
            self.index += 1
            if (self.current_instruction[:2] == '//' or not len(self.current_instruction)):
                self.advance 

    @property
    def instruction_type(self):
        """
        Returns the type of the current instruction:
        A_INSTRUCTION for @xxx, where xxx is either a decimal number or a symbol
        C_INSTRUCTION for dest=comp;jump
        L_INSTRUCTION for (xxx), where xxx is a symbol.
        """
        # if not self.has_more_lines: return
        ins = self.current_instruction
        if ins[0] == '@':
            return 'A_INSTRUCTION'
        elif ins[0] in ('D', 'M', 'A', '0'):
            return 'C_INSTRUCTION'
        elif ins[0] == '(':
            return 'L_INSTRUCTION'
        else:
            raise ValueError(ins)

    @property
    def symbol(self):
        """
        If the current instruction is (xxx), returns the symbol xxx.
        If the current instruction is @xxx, returns the symbol or decimal xxx
        (as a string).
        Should be called only if instruction_type is A_INSTRUCTION or L_INSTRUCTION.
        """
        ins = self.current_instruction
        if self.instruction_type == 'A_INSTRUCTION':
            return ins[1:]
        elif self.instruction_type == 'L_INSTRUCTION':
            return ins[1:-1]
        else:
            raise ValueError('Not A_INSTRUCTION or L_INSTRUCTION')


    @property
    def dest(self):
        """
        Returns the symbolic dest part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        ins = self.current_instruction
        if self.instruction_type == 'C_INSTRUCTION':
            split = '=' if '=' in ins else ';'
            return ins.split(split)[0]
        else:
            raise ValueError('Not C_INSTRUCTION')

    @property
    def comp(self):
        """
        Returns the symbolic comp part o fth ecurrent C-instruction (28 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION
        """
        ins = self.current_instruction
        if self.instruction_type == 'C_INSTRUCTION':
            split = '=' if '=' in ins else ';'
            return ins.split(split)[1]
        else:
            raise ValueError('Not C_INSTRUCTION')

    @property
    def jump(self):
        """
        Returns the symbolic jump part of the current C-instruction (8 possibilities).
        Should be called only if instruction_type is C_INSTRUCTION.
        """


def test():
    parser = Parser(infile='../add/Add.asm')
    parser.advance
    assert parser.instruction_type == 'A_INSTRUCTION'
    assert parser.symbol == '2'
    parser.advance
    assert parser.instruction_type == 'C_INSTRUCTION'
    assert parser.dest == 'D'
    assert parser.comp == 'A'
    parser.advance
    assert parser.instruction_type == 'A_INSTRUCTION'
    assert parser.symbol == '3'
    parser.advance
    assert parser.instruction_type == 'C_INSTRUCTION'
    assert parser.dest == 'D'
    assert parser.comp == 'D+A'
    parser.advance
    assert parser.instruction_type == 'A_INSTRUCTION'
    assert parser.symbol == '0'
    parser.advance
    assert parser.instruction_type == 'C_INSTRUCTION'
    assert parser.dest == 'M'
    assert parser.comp == 'D'
    parser.advance
    assert parser.instruction_type == 'C_INSTRUCTION'

    code = Code()
    assert code.dest('DM') == '011'
    # assert code.comp('A+1') == '0110111'
    # assert code.jump('JNE') == '101'




class Code:
    def dest(self, d):
        if not d: return '000'
        dest_codes = {
            'M'  : '001',
            'D'  : '010',
            'DM' : '011',
            'A'  : '100',
            'AM' : '101',
            'AD' : '110',
            'ADM': '111'
        }
        return dest_codes[d]
        

    def comp(self, c):
        pass

    def jump(self, j):
        pass


test()