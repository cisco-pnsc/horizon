from horizon.test import helpers as test


class BrokersTests(test.TestCase):
    # Unit tests for brokers.
    def test_me(self):
        self.assertTrue(1 + 1 == 2)
