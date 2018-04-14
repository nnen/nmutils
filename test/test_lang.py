
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


class TestProxy(unittest.TestCase):
    def setUp(self):
        class TestClass:
            def __init__(slf, name):
                slf.name = name
                slf.attr1 = None
                slf.attr2 = None

            def __str__(self):
                return self.name

        self.test_class = TestClass
        self.test_obj = self.test_class("TestName")
        self.proxy = lang.Proxy(self.test_obj)

    def tearDown(self):
        del self.test_class

    def test_str(self):
        self.assertEqual(str(self.test_obj), str(self.proxy))

    def test_getitem(self):
        p = lang.Proxy([1, 2, 3])
        self.assertEqual(1, p[0])
        self.assertEqual(2, p[1])
        self.assertEqual(3, p[2])

    def test_getitem(self):
        l = [None, None, None, ]
        p = lang.Proxy(l)
        p[0] = 1
        p[1] = 2
        p[2] = 3
        self.assertEqual(1, l[0])
        self.assertEqual(2, l[1])
        self.assertEqual(3, l[2])

    def test_setattr(self):
        self.proxy.attr1 = 123
        self.assertEqual(123, self.test_obj.attr1)
        self.proxy.attr1 = 234
        self.assertEqual(234, self.test_obj.attr1)

    def test_getattr(self):
        self.assertEqual(None, self.proxy.attr1)
        self.test_obj.attr1 = 123
        self.assertEqual(123, self.proxy.attr1)

