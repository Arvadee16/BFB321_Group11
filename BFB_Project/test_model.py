
# MY Diners EOQ Unit Tests
# BFB 321 - Group 11

import unittest
from supply_chain import calculate_eoq, total_annual_cost


class TestEOQ(unittest.TestCase):

    def test_rice_eoq(self):
        result = calculate_eoq(2400, 100, 20)
        self.assertAlmostEqual(result, 154.91933, places=4)

    def test_chicken_eoq(self):
        result = calculate_eoq(6000, 150, 30)
        self.assertAlmostEqual(result, 244.94897, places=4)

    def test_rice_annual_cost(self):
        eoq = calculate_eoq(2400, 100, 20)
        cost = total_annual_cost(2400, 100, 20, eoq)
        self.assertAlmostEqual(cost, 3098.38668, places=4)

    def test_orders_per_year(self):
        eoq = calculate_eoq(2400, 100, 20)
        orders = 2400 / eoq
        self.assertAlmostEqual(orders, 15.49193, places=4)


if __name__ == "__main__":
    unittest.main()
