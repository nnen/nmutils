

from nmutils import printer

import unittest


class TestTable(unittest.TestCase):
    def test_to_lines(self):
        tbl = printer.Table()
        tbl.column("l").column("r").column("r")
        tbl.row("a", "b", "c")
        tbl.row(1, 2, 3)
        tbl.row(10, 20, 300)

        expected_lines = [
            "a   b   c",
            "1   2   3",
            "10 20 300",
        ]

        self.assertEqual(expected_lines, tbl.to_lines())

