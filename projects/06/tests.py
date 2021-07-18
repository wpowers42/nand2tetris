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


class CodeTestCase(unittest.TestCase):

    def setUp(self):
        self.code = assembler.Code()

    def test_dest(self):
        self.assertEqual(self.code.dest('D'), '010')
        self.assertEqual(self.code.dest('M'), '001')
        self.assertEqual(self.code.dest('DM'), '011')
        self.assertEqual(self.code.dest('null'), '000')

    def test_comp(self):
        self.assertEqual(self.code.comp('A'), '0110000')
        self.assertEqual(self.code.comp('D+A'), '0000010')
        self.assertEqual(self.code.comp('D'), '0001100')

    def test_jump(self):
        self.assertEqual(self.code.jump('JNE'), '101')


class SymbolTestCase(unittest.TestCase):
    def setUp(self):
        self.symbol = assembler.Symbol()

    def test_contains(self):
        self.assertTrue(self.symbol.contains('R3'))
        self.assertTrue(self.symbol.contains('SCREEN'))
        self.assertTrue(self.symbol.contains('KBD'))

    def test_get_address(self):
        self.assertEqual(self.symbol.get_address('KBD'), 24576)
        self.assertEqual(self.symbol.get_address('R0'), 0)
        self.assertEqual(self.symbol.get_address('SP'), 0)

    def test_add_entry(self):
        self.symbol.add_entry('ENTRY', 56)
        self.assertTrue(self.symbol.contains('ENTRY'))
        self.assertEqual(self.symbol.get_address('ENTRY'), 56)
        self.symbol.add_entry('LOOP')
        self.assertTrue(self.symbol.contains('LOOP'))
        self.assertEqual(self.symbol.get_address('LOOP'), 16)

if __name__ == "__main__":
    unittest.main(exit=False)