import unittest
import yaml
from main.core.transport import transport_emissions
from main.core.food import food_emissions
from main.core.energy import energy_emissions
from main.data.emission_factors import FOOD_FACTORS, ENERGY_FACTORS
# This code is a unit test for the emission calculator module.

class TestCalculator(unittest.TestCase):
    
    def test_transport_emissions(self):
        result = transport_emissions(100, 50, 200)
        expected = (100 * 0.192) + (50 * 0.105) + (200 * 0.255)
        self.assertAlmostEqual(result, expected, places=2)


    def test_food_emissions(self):
        result = food_emissions('high_meat')
        expected = 30 * FOOD_FACTORS['high_meat']
        self.assertAlmostEqual(result, expected, places=2)

        result = food_emissions('vegetarian')
        expected = 30 * FOOD_FACTORS['vegetarian']
        self.assertAlmostEqual(result, expected, places=2)

        result = food_emissions('vegan')
        expected = 30 * FOOD_FACTORS['vegan']
        self.assertAlmostEqual(result, expected, places=2)

        result = food_emissions('unkown_diet')
        expected = 30 * FOOD_FACTORS['average']  # Default to 'average' if diet type is unknown
        self.assertAlmostEqual(result, expected, places=2)
    
    
    def test_energy_emissions(self):
        result = energy_emissions(100, 0, 0, 0)
        expected = 100 * ENERGY_FACTORS['electricity']
        self.assertAlmostEqual(result, expected, places=2)

        result = energy_emissions(0, 200, 0, 0)
        expected = 200 * ENERGY_FACTORS['oil']
        self.assertAlmostEqual(result, expected, places=2)

        result = energy_emissions(0, 0, 0, 75)
        expected = 75 * ENERGY_FACTORS['wood']
        self.assertAlmostEqual(result, expected, places=2)

        result = energy_emissions(0, 0, 200, 0)
        expected = 200 * ENERGY_FACTORS['gas']
        self.assertAlmostEqual(result, expected, places=2)

        result = energy_emissions(10, 20, 30, 40)
        expected = (
            10 * ENERGY_FACTORS['electricity'] +
            20 * ENERGY_FACTORS['oil'] +
            30 * ENERGY_FACTORS['gas'] +
            40 * ENERGY_FACTORS['wood']
        )
        self.assertAlmostEqual(result, expected, places=2)



if __name__ == '__main__':
    unittest.main()
# This code is a unit test for the emission calculator module.