# This file is created to check the bug with different Python versions by GitHub Actions.

# Error in the exception message generated when trying to access the private field of the instance.
import unittest


class A:
    __var = 2


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