# nmutils.printer module


import io
import sys


def make_printer(out=None):
    return Printer(out=out)


def make_str_printer():
    out = io.StringIO()
    printer = Printer(out=out)
    return out, printer


class Printer:
    def __init__(self, out=None):
        if out is None:
            out = sys.stdout
        self._out = out

        self._indent_stack = ["", ]
        self._is_new_line = True

    @property
    def current_indent(self):
        return self._indent_stack[-1]

    def indent(self, value="  "):
        self._indent_stack.append(self.current_indent + str(value))

    def write(self, value):
        lines = str(value).splitlines(keepends=True)
        is_new_line = self._is_new_line
        w = self._out.write
        i = self.current_indent
        for line in lines:
            if is_new_line:
                w(i)
            w(line)
            is_new_line = line.endswith("\n")
        self._is_new_line = is_new_line

    def writef(self, value, *args, **kwargs):
        formatted = str(value).format(*args, **kwargs)
        self.write(formatted)

    def writel(self, value=None):
        w = self.write
        if value is not None:
            w(value)
        w("\n")


class TableColumn:
    def __init__(self, alignment="l"):
        self.alignment = alignment
        self.width = 0

    def format_unaligned(self, value):
        return str(value)

    def format_aligned(self, value):
        if self.alignment == "r":
            return value.rjust(self.width)
        return value.ljust(self.width)


class Table:
    def __init__(self, separator=" "):
        self._current_row = None
        self._rows = []
        self._columns = []
        self.separator = separator

    def column(self, alignment="l"):
        col = TableColumn(alignment=alignment)
        self._columns.append(col)
        return self

    def get_column(self, index):
        cols = self._columns
        while index >= len(cols):
            self.column()
        return cols[index]

    def row(self, *values):
        self.end_row()
        self._rows.append([str(v) for v in values])
        return self

    def cell(self, value=None):
        row = self._current_row
        if row is None:
            row = []
            self._current_row = row
            self._rows.append(row)
        if value is None:
            value = ""
        row.append(value)
        return self

    def end_row(self):
        self._current_row = None
        return self

    def calculate_col_widths(self):
        col_count = max(len(r) for r in self._rows)
        widths = [0, ] * col_count
        cols = [self.get_column(i) for i in range(col_count)]

        for col in cols:
            col.width = 0

        for row in self._rows:
            for i, value in enumerate(row):
                value_str = cols[i].format_unaligned(value)
                width = max(widths[i], len(value_str))
                widths[i] = width

        for col, width in zip(cols, widths):
            col.width = width

        return widths

    def to_lines(self):
        result = []

        widths = self.calculate_col_widths()
        sep = self.separator
        cols = [self.get_column(i) for i in range(len(widths))]

        for row in self._rows:
            line = ""
            for i, value in enumerate(row):
                if i > 0:
                    line += sep
                line += cols[i].format_aligned(value)
            result.append(line)

        return result

