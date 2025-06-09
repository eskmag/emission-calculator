import unittest
from emission_calculator.calculator import calculate_transport_emissions, calculate_energy_emissions, calulcate_food_emissions

class TestCalculator(unittest.TestCase):
    
    def test_transport_emissions(self):
        result = calculate_transport_emissions(100, 50, 200)
        expected = (100 * 0.192) + (50 * 0.105) + (200 * 0.255)
        self.assertAlmostEqual(result, expected, places=2)


    def test_food_emissions(self):
        result = calulcate_food_emissions('high_meat')
        expected = 7.2 * 30
        self.assertAlmostEqual(result, expected, places=2)

        result = calulcate_food_emissions('vegetarian')
        expected = 3.8 * 30
        self.assertAlmostEqual(result, expected, places=2)

        result = calulcate_food_emissions('vegan')
        expected = 2.9 * 30
        self.assertAlmostEqual(result, expected, places=2)

        result = calulcate_food_emissions('unkown_diet')
        expected = 5.6 * 30
        self.assertAlmostEqual(result, expected, places=2)
    
    
    def test_energy_emissions(self):
        result = calculate_energy_emissions(100, 'electricity')
        expected = 100 * 0.02
        self.assertAlmostEqual(result, expected, places=2)

        result = calculate_energy_emissions(200, 'oil')
        expected = 200 * 0.267
        self.assertAlmostEqual(result, expected, places=2)

        result = calculate_energy_emissions(75, 'wood')
        expected = 75 * 0.018
        self.assertAlmostEqual(result, expected, places=2)

        result = calculate_energy_emissions(200, 'gas')
        expected = 200 * 0.25
        self.assertAlmostEqual(result, expected, places=2)

        result = calculate_energy_emissions(100, 'unknown_source') # fallback to electricity
        expected = 100 * 0.02
        self.assertAlmostEqual(result, expected, places=2)

if __name__ == '__main__':
    unittest.main()
# This code is a unit test for the emission calculator module.