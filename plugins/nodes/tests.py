from horizon.test import helpers as test


class NodesTests(test.TestCase):
    # Unit tests for nodes.
    def test_me(self):
        self.assertTrue(1 + 1 == 2)
