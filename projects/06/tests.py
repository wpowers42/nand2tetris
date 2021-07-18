import assembler
import unittest

def parser_tests():

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
        D=M              // D = first number
        D=D-M
        D;JGT
        @256
        MD=M+1
        @2ABC
        """
    
    def check_equal(L1, L2):
        return len(L1) == len(L2) and sorted(L1) == sorted(L2)

    p = assembler.Parser(file=asm)
    assert check_equal(p.file, ['@2', 'D=A;null', '@3', 'D=D+A;null', '@0', 'M=D;null', '(xxx)',
                                'DM=D+A;null', 'null=D;JNE', 'D=M;null', 'D=D-M;null', 'null=D;JGT',
                                '@256', 'MD=M+1;null', "@2ABC"])
    assert p.has_more_lines
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '2'
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "D"
    assert p.comp == "A"
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '3'
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "D"
    assert p.comp == "D+A"
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'A_INSTRUCTION'
    assert p.symbol == '0'
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "M"
    assert p.comp == "D"
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'L_INSTRUCTION'
    assert p.symbol == 'xxx'
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.dest == "DM"
    assert p.comp == "D+A"
    p.advance
    assert p.has_more_lines
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.jump == "JNE"
    p.advance
    p.advance
    p.advance
    assert p.instruction_type == 'C_INSTRUCTION'
    assert p.jump == "JGT"
    p.advance
    assert p.symbol == "256"
    p.advance
    assert p.dest == "DM"
    p.advance

    
    p.advance
    assert not p.has_more_lines
    
    print("parser tests pass")

class ParserTestCase(unittest.TestCase):
    infile = """
        @2ABC
        """
    p = assembler.Parser(file=infile)

    def test_improperly_formatted_symbol(self):
        with self.assertRaises(ValueError) as context:
            self.p.symbol

        self.assertEqual("improperly formatted symbol: 2ABC", context.exception.args[0])



def code_tests():

    c = assembler.Code()
    
    assert c.dest('D') == '010'
    assert c.comp('A') == '0110000'
    assert c.dest('D') == '010'
    assert c.comp('D+A') == '0000010'
    assert c.dest('M') == '001'
    assert c.comp('D') == '0001100'
    assert c.dest('DM') == '011'
    assert c.comp('D+A') == '0000010'
    assert c.jump('JNE') == '101'
    assert c.dest('null') == '000'
    
    print("code tests pass")


def symbol_tests():
    s = assembler.Symbol()
    assert s.contains('SCREEN')
    assert s.get_address('KBD') == 24576
    s.add_entry('ENTRY', 56)
    assert s.contains('ENTRY')
    assert s.get_address('ENTRY') == 56
    s.add_entry('LOOP')
    assert s.contains('LOOP')
    assert s.get_address('LOOP') == 16
    assert s.get_address('R0') == 0
    assert s.get_address('SP') == 0

    print('symbol tests pass')

def run_tests():
    code_tests()
    parser_tests()
    symbol_tests()

if __name__ == "__main__":
    run_tests()
    unittest.main(exit=False)