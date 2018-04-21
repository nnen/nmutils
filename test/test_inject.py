import unittest
import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


from nmutils import inject


class TestBase(unittest.TestCase):
    def tearDown(self):
        inject.MANAGER.reset()


class TestDependency(TestBase):
    def test_simple(self):
        printer = inject.dependency("nmutils.printer.Printer").value
        self.assertIsNotNone(printer)

    def test_provider(self):
        print("TEST OUTPUT")

        from nmutils import printer

        @inject.provider("nmutils.printer.Printer")
        class CustomPrinterClass(printer.Printer):
            pass

        printer = inject.dependency("nmutils.printer.Printer").value
        self.assertIsNotNone(printer)
        self.assertIsInstance(printer, CustomPrinterClass)

    def test_proxy(self):
        printer = inject.proxy("nmutils.printer.Printer")
        self.assertIsNotNone(printer.write)
        self.assertIsNone(getattr(printer, "attributeThatDoesntExist", None))

