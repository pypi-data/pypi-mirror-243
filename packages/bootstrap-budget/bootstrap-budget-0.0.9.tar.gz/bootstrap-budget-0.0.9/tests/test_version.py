import bootstrap_budget
import importlib.metadata
import unittest


class TestBootstrapVersion(unittest.TestCase):
    def test_version(self) -> None:
        """
        A test of the __version__ object to see if it behaves as expected when set or called.

        :return: None
        """
        print(f'bootstrap-budget version: {bootstrap_budget.__version__}')

        self.assertEqual(bootstrap_budget.__version__, importlib.metadata.version("bootstrap_budget"))


if __name__ == '__main__':
    unittest.main()
