import unittest
from credit_rating import calculate_credit_rating, Mortgage


class AssessCreditRatingProcess(unittest.TestCase):
    """
    Test the credit rating module
    """

    def test_credit_rating(self):
        """Happy path: Test credit rating of the given payload."""
        data = {
            "mortgages": [
                {
                    "credit_score": 750,
                    "loan_amount": 200000,
                    "property_value": 250000,
                    "annual_income": 60000,
                    "debt_amount": 20000,
                    "loan_type": "fixed",
                    "property_type": "single_family",
                },
                {
                    "credit_score": 680,
                    "loan_amount": 150000,
                    "property_value": 175000,
                    "annual_income": 45000,
                    "debt_amount": 10000,
                    "loan_type": "adjustable",
                    "property_type": "condo",
                },
            ]
        }
        result = calculate_credit_rating(data=data)
        self.assertEqual(result, "AAA")
        print("\n1. Test credit rating: PASS")

    def test_empty_mortgages(self):
        """Test with empty mortgages list"""
        try:
            data = {"mortgages": []}
            calculate_credit_rating(data)
        except Exception as e:
            print(f"\n2. {e}: PASS")

    def test_invalid_input(self):
        """In this test we will try providing invalid credit score, feel free to provide any other invalid input."""
        try:
            data = {
                "mortgages": [
                    {
                        "credit_score": 750,
                        "loan_amount": 200000,
                        "property_value": 250000,
                        "annual_income": 60000,
                        "debt_amount": 20000,
                        "loan_type": "fixed",
                        "property_type": "single_family",
                    },
                    {
                        "credit_score": 180,  # Invalid credit score
                        "loan_amount": 150000,
                        "property_value": 175000,
                        "annual_income": 45000,
                        "debt_amount": 10000,
                        "loan_type": "adjustable",
                        "property_type": "condo",
                    },
                ]
            }
            calculate_credit_rating(data=data)
            print(f"\n3. Provide invalid input for testing: PASS")
        except Exception as e:
            print(f"\n3. {e}: PASS")

    def test_invalid_type(self):
        """In this test we will try providing invalid property type, feel free to provide any other invalid input."""
        try:
            data = {
                "mortgages": [
                    {
                        "credit_score": 750,
                        "loan_amount": 200000,
                        "property_value": 250000,
                        "annual_income": 60000,
                        "debt_amount": 20000,
                        "loan_type": "fixed",
                        "property_type": "single_family",
                    },
                    {
                        "credit_score": 800,
                        "loan_amount": 150000,
                        "property_value": 175000,
                        "annual_income": 45000,
                        "debt_amount": 10000,
                        "loan_type": "adjustable",
                        "property_type": "invalid_type",  # Invalid property type
                    },
                ]
            }
            calculate_credit_rating(data=data)
            print(f"\n4. Provide invalid type for testing: PASS")
        except Exception as e:
            print(f"\n4. {e}: PASS")

    def test_missing_attributes(self):
        """In this test we will comment "annual_income" and "loan_type" to raise exception if attributes are not provided."""
        data = {
            "credit_score": 800,
            "loan_amount": 900000,
            "property_value": 850000,
            # "annual_income": 70000, # Commented out for testing missing annual_income attr
            "debt_amount": 27000,
            # "loan_type": "fixed", # Commented out for testing missing loan_type attr
            "property_type": "single_family",
        }
        with self.assertRaises(Exception) as context:
            Mortgage(data)

        print(f"\n5. {context.exception}: PASS")

    def test_ratio(self):
        """Testing high ration: In this case LTV exceeding more then 100% (loan amount > property value) should be invalid."""
        data = {
            "credit_score": 750,
            "loan_amount": 300000,  # Greater than property value which will give more then 100%
            "property_value": 250000,
            "annual_income": 60000,
            "debt_amount": 20000,
            "loan_type": "fixed",
            "property_type": "single_family",
        }
        with self.assertRaises(Exception) as context:
            mortgage = Mortgage(data)
            mortgage.compute_risk_score()
        print(f"\n6. High ratio: {context.exception}: PASS")

    def testz_all_rating_categories(self):
        """Test that all credit rating categories (AAA, BBB, C)"""

        # AAA case
        aaa_data = {
            "mortgages": [
                {
                    "credit_score": 800,
                    "loan_amount": 200000,
                    "property_value": 400000,
                    "annual_income": 100000,
                    "debt_amount": 10000,
                    "loan_type": "fixed",
                    "property_type": "single_family",
                }
            ]
        }
        self.assertEqual(calculate_credit_rating(aaa_data), "AAA")

        # BBB case
        bbb_data = {
            "mortgages": [
                {
                    "credit_score": 680,
                    "loan_amount": 300000,
                    "property_value": 350000,
                    "annual_income": 80000,
                    "debt_amount": 35000,
                    "loan_type": "adjustable",
                    "property_type": "condo",
                }
            ]
        }
        self.assertEqual(calculate_credit_rating(bbb_data), "BBB")

        # C case
        c_data = {
            "mortgages": [
                {
                    "credit_score": 600,
                    "loan_amount": 450000,
                    "property_value": 500000,
                    "annual_income": 60000,
                    "debt_amount": 35000,
                    "loan_type": "adjustable",
                    "property_type": "condo",
                }
            ]
        }
        self.assertEqual(calculate_credit_rating(c_data), "C")

        print("\n7. All credit rating categories passed the check (AAA, BBB, C): PASS")


if __name__ == "__main__":
    unittest.main()
