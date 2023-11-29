import pytest
import unittest

def noop():
    pass

class SideEffects:
    def fn(self):
        """
        Empty function without any behaviour

        Return:
            Nothing
        """
        pass

    def always(self, *args, **kwargs):
        if len(args) > 0:
            return args[0]
        return kwargs

class BaseTestSuite(unittest.TestCase):
    """
    A base test suite providing assertion methods for dictionary or object properties.
    """

    side_effects = SideEffects()

    @pytest.fixture(autouse = True)
    def setup_test(self):
        before = getattr(self, "before", noop)
        before()
        yield
        after = getattr(self, "after", noop)
        after()

    def assertEqualDictProp(self, source, expected: dict|object, prop: str, *, source_name: str = 'source'):
        """
        Asserts that a specified property of a source dictionary or object is equal to the expected value.
        
        Parameters:
            source: The source dictionary or object.
            expected: The expected dictionary or object containing the property value.
            prop: The name of the property to be compared.
            source_name: (Optional) The name of the source, used in error messages.
        """
        
        self.assertIsInstance(source, dict | object)

        source_value = source.get(prop) if isinstance(source, dict) else getattr(source, prop)
        expected_value = expected.get(prop) if isinstance(expected, dict) else getattr(expected, prop)
        self.assertEqual(source_value, expected_value, f"{source_name}[{prop}] should be ({expected_value}), but ({source_value}) was received")

    def assertDictPropEqualTo(self, source, prop: str,*,expected_value, source_name: str = 'source'):
        """
        Asserts that a specified property of a source dictionary or object is equal to a specific expected value.
        
        Parameters:
            source: The source dictionary or object.
            prop: The name of the property to be compared.
            expected_value: The expected value for the property.
            source_name: (Optional) The name of the source, used in error messages.
        """
        
        expected = {}
        expected[prop] = expected_value
        return self. assertEqualDictProp(source, expected, prop, source_name = source_name)

    def assertMissing(self, source, prop: str,*, source_name: str = 'source'):
        """
        Asserts that a specified property is missing in the source dictionary or object.
        
        Parameters:
            source: The source dictionary or object.
            prop: The name of the property to check for missing.
            source_name: (Optional) The name of the source, used in error messages.
        """
        
        source_value = source.get(prop) if isinstance(source, dict) else getattr(source, prop)
        self.assertFalse(prop in source,f"{source_name}[{prop}] should be missing, but ({source_value}) was received")

    def assertHaving(self, source, prop: str,*, source_name: str = 'source'):
        """
        Asserts that a specified property is present in the source dictionary or object.
        
        Parameters:
            source: The source dictionary or object.
            prop: The name of the property to check for presence.
            source_name: (Optional) The name of the source, used in error messages.
        """
        
        source_value = source.get(prop) if isinstance(source, dict) else getattr(source, prop)
        self.assertTrue(prop in source,f"{source_name}[{prop}] should be set, but ({source_value}) was received")