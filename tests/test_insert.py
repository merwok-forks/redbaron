#!/usr/bin/python
# -*- coding:Utf-8 -*-

""" Tests the code insertion features """

import pytest
# pylint: disable=redefined-outer-name
from redbaron import RedBaron


def assert_with_indent(left, right):
    # Replace is not strictly necessary but shows indents
    assert left.dumps().replace(' ', '.') == right.replace(' ', '.')


@pytest.fixture
def red_A_B():
    return RedBaron("""\
class A:
    pass

class B:
    pass
""")


@pytest.fixture
def red_nested():
    return RedBaron("""\
class A:
    class B:
        pass
""")


def test_insert_with_class_0(red_A_B):
    red_A_B.insert(0, "a = 1")

    assert_with_indent(red_A_B, """\
a = 1
class A:
    pass

class B:
    pass
""")


def test_insert_with_class_1(red_A_B):
    red_A_B.insert(1, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

a = 1
class B:
    pass
""")


def test_insert_with_class_2(red_A_B):
    red_A_B.insert(2, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
a = 1
""")


def test_insert_with_class_3(red_A_B):
    red_A_B.insert(3, "a = 1")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
a = 1
""")


def test_insert_class_with_class_0(red_A_B):
    red_A_B.insert(0, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class C:
    pass
class A:
    pass

class B:
    pass
""")


def test_insert_class_with_class_1(red_A_B):
    red_A_B.insert(1, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class C:
    pass
class B:
    pass
""")


def test_insert_class_with_class_2(red_A_B):
    red_A_B.insert(2, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
class C:
    pass
""")


def test_insert_class_with_class_3(red_A_B):
    red_A_B.insert(3, "class C:\n    pass")

    assert_with_indent(red_A_B, """\
class A:
    pass

class B:
    pass
class C:
    pass
""")


def test_insert_with_nested_class_0(red_nested):
    red_nested.insert(0, "a = 1")

    assert_with_indent(red_nested, """\
a = 1
class A:
    class B:
        pass
""")


def test_insert_with_nested_class_1(red_nested):
    red_nested.insert(1, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
a = 1
""")


def test_insert_inside_nested_class_0(red_nested):
    red_nested[0].insert(0, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    a = 1
    class B:
        pass
""")


def test_insert_inside_nested_class_1(red_nested):
    red_nested[0].insert(1, "a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    a = 1
""")


def test_insert_class_inside_nested_class_0(red_nested):
    red_nested[0].insert(0, "class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class C:
        pass
    class B:
        pass
""")


def test_insert_class_inside_nested_class_1(red_nested):
    red_nested[0].insert(1, "class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    class C:
        pass
""")


def test_append_inside_nested_class(red_nested):
    red_nested[0].append("a = 1")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    a = 1
""")


def test_append_class_inside_nested_class(red_nested):
    red_nested[0].append("class C:\n    pass")

    assert_with_indent(red_nested, """\
class A:
    class B:
        pass
    class C:
        pass
""")


def test_append_method_in_nested_with_methods():
    red = RedBaron("""\
class A:
    def a(self):
        pass

    def b(self):
        pass

""")

    red[0].append("def c(self):\n    pass")

    assert_with_indent(red, """\
class A:
    def a(self):
        pass

    def b(self):
        pass

    def c(self):
        pass
""")


def test_append_class_in_nested_with_methods():
    red = RedBaron("""\
class A:
    def a(self):
        pass

    def b(self):
        pass

""")

    red[0].append("class C:\n    pass")

    assert_with_indent(red, """\
class A:
    def a(self):
        pass

    def b(self):
        pass

    class C:
        pass
""")
