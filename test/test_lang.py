
from nmutils import lang

import unittest


class TestObjRepr(unittest.TestCase):
    def setUp(self):
        class TestClass:
            def __repr__(self):
                return lang.obj_repr(self, 13, 14)

        self.test_obj = TestClass()

    def tearDown(self):
        self.test_obj = None

    def test_no_args(self):
        repr_str = lang.obj_repr(self.test_obj)
        self.assertEqual("TestClass()", repr_str)

    def test_position_args(self):
        repr_str = lang.obj_repr(self.test_obj, 1, 2, 3, "hello")
        self.assertEqual("TestClass(1, 2, 3, \'hello\')", repr_str)

    def test_keyword_args(self):
        repr_str = lang.obj_repr(self.test_obj, a=1, b=2, c="hello")
        self.assertEqual("TestClass(a=1, b=2, c='hello')", repr_str)

    def test_obj_repr_with_obj(self):
        class TestClass:
            def __repr__(self):
                return lang.obj_repr(self, 13, 14)

        test_obj = TestClass()

        repr_str = repr(test_obj)

        self.assertEqual("TestClass(13, 14)", repr_str)

