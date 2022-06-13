# BUG IN PYTHON 3 NAME MANGLING MECHANISM

Bug report.

## SUMMARY

An incorrect message is generated when a protected instance field is accessed from an instance of another class.
It does not matter whether the object was created inside the object as a local variable of the method (`a = A(),
unittest`), assigned to an instance field (`self.a = A()`), or the object from which the method is called inherited
a class with a private field ( `class B(A)`).

## SYSTEM REQUIREMENTS

I used macOS Monterey, Version 12.4, Chip Apple M1, 8 GB of memory.
Python 3.9.2rc1

## How to run tests

You should have 2 tests with OK result.
```
python -m unittest discover -s tests  -p 'tests_*.py'
```

## Test example
All this research started with this code:
```

class A:
    __var = 2
```
## Correct message
```
a = A()
print(a.__var)  # AttributeError: 'A' object has no attribute '__var'
```
## Wrong behavior

### When using unittest
Read the comments in the tests:
```

class TestMangledNamesUsage(unittest.TestCase):

    # BUG (Wrong message generated)
    def test_wrong_mangled_name_in_exception_on_attempt_of_direct_access_to_private_var(self):
        # when trying to directly access a private field of an object, an exception is thrown containing
        # an incorrect mangled name of an attribute. Must be '_A__var'
        with self.assertRaises(AttributeError,
                               msg="'A' object has no attribute '_TestMangledNamesUsage__var'") as context:
            a = A().__var
        self.assertTrue("'A' object has no attribute '_TestMangledNamesUsage__var'" in str(context.exception),
                        msg="Wrong message.")

    def test_wrong_mangled_name_not_work(self):
        # the correct exception message is created here. there is no error accessing the private field.
        # this test is needed to show that THE ERROR is ONLY IN the EXCEPTION MESSAGE!
        with self.assertRaises(AttributeError,
                               msg="'A' object has no attribute '_TestMangledNamesUsage__var'") as context:
            a = A()._TestMangledNamesUsage__var
        self.assertTrue("'A' object has no attribute '_TestMangledNamesUsage__var'" in str(context.exception),
                        msg="Wrong message.")
```

### Without unittest

To show that it is not a bug of unittest module, I included this code:

```

class B:
    a = A()

    def test_1(self):
        a = self.a.__var  # AttributeError: 'A' object has no attribute '_B__var'
        return a


class C(A):

    def test_1(self):
        a = self.__var  # AttributeError: 'C' object has no attribute '_C__var'
        return a
```