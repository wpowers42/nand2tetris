import assembler
import unittest

class ParserTestCase(unittest.TestCase):

    file = """// This file is part of www.nand2tetris.org
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
        """

    def setUp(self):
        self.p = assembler.Parser(file=self.file)

    def test_processed_file(self):
        self.assertListEqual( self.p.file, ['@2', 'D=A;null', '@3', 'D=D+A;null',
            '@0','M=D;null', '(xxx)', 'DM=D+A;null', 'null=D;JNE', 'D=M;null',
            'D=D-M;null', 'null=D;JGT', '@256', 'MD=M+1;null'])

    def test_advance(self):
        for _ in range(len(self.p.file)): self.p.advance
        self.assertFalse(self.p.has_more_lines)

    def test_instruction_type(self):
        instructions = ['A_INSTRUCTION', 'C_INSTRUCTION', 'A_INSTRUCTION', 'C_INSTRUCTION',
            'A_INSTRUCTION', 'C_INSTRUCTION', 'L_INSTRUCTION', 'C_INSTRUCTION', 'C_INSTRUCTION',
            'C_INSTRUCTION', 'C_INSTRUCTION', 'C_INSTRUCTION', 'A_INSTRUCTION', 'C_INSTRUCTION']
        pinstructions = []
        while self.p.has_more_lines:
            pinstructions.append(self.p.instruction_type)
            self.p.advance

        self.assertListEqual(pinstructions, instructions)
    
    def test_symbol(self):
        symbols = ['2', '3', '0', 'xxx', '256']
        psymbols = []
        while self.p.has_more_lines:
            if self.p.instruction_type != "C_INSTRUCTION":
                psymbols.append(self.p.symbol)
            self.p.advance

        self.assertListEqual(symbols, psymbols)

    def test_dest(self):
        dests = ['D', 'D', 'M', 'DM', 'null', 'D', 'D', 'null', 'DM']
        pdests = []
        while self.p.has_more_lines:
            if self.p.instruction_type == "C_INSTRUCTION":
                pdests.append(self.p.dest)
            self.p.advance

        self.assertListEqual(dests, pdests)

    def test_comp(self):
        compare = ['A', 'D+A', 'D', 'D+A', 'D', 'M', 'D-M', 'D', 'M+1']
        results = []
        while self.p.has_more_lines:
            if self.p.instruction_type == "C_INSTRUCTION":
                results.append(self.p.comp)
            self.p.advance

        self.assertListEqual(results, compare)

    def test_jump(self):
        compare = ['null', 'null', 'null', 'null', 'JNE', 'null', 'null', 'JGT', 'null']
        results = []
        while self.p.has_more_lines:
            if self.p.instruction_type == "C_INSTRUCTION":
                results.append(self.p.jump)
            self.p.advance

        self.assertListEqual(results, compare)
    
    def test_improperly_formatted_symbol(self):
        p = assembler.Parser(file="@2ABC")
        with self.assertRaises(ValueError) as context:
            p.symbol

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