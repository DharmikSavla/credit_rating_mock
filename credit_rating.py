from concurrent.futures import ProcessPoolExecutor
import multiprocessing

# Predefined configs to avoid static implementation
ALLOWED_LOAN_TYPE = ["fixed", "adjustable"]
ALLOWED_PROPERTY_TYPE = ["single_family", "condo"]
HIGH_RATING = "AAA"
MEDIUM_RATING = "BBB"
LOW_RATING = "C"

# In schema both int and float has been mentioned for loan_amount and other values because the sample json given in assignment pdf is int for e.g. "250000" but the constraint to implement is mentioned float
mortgage_schema = {
    "credit_score": int,
    "loan_amount": (int, float),
    "property_value": (int, float),
    "annual_income": (int, float),
    "debt_amount": (int, float),
    "loan_type": str,
    "property_type": str,
}


class Mortgage:
    """
    Contains business logic of the credit rating algorithm and validates constraints
    """

    def __init__(self, data: dict):
        self.credit_score = data.get("credit_score")
        self.loan_amount = data.get("loan_amount")
        self.property_value = data.get("property_value")
        self.annual_income = data.get("annual_income")
        self.debt_amount = data.get("debt_amount")
        self.loan_type = data.get("loan_type")
        self.property_type = data.get("property_type")

        self._validate_values(schema=mortgage_schema, mortgage_data=data)

    def _validate_values(self, schema: dict, mortgage_data: dict) -> None:
        """Validates constraints and data types"""

        # Checks for missing required fields
        missing_attr = [key for key in schema if key not in mortgage_data]
        if missing_attr:
            raise Exception(f"Missing required attributes: {', '.join(missing_attr)}")

        for key, expected_type in schema.items():
            value = getattr(self, key, None)

            if value is not None and not isinstance(value, expected_type):
                expected_types_str = " & ".join(t.__name__ for t in expected_type)
                raise Exception(
                    f"Invalid type for {key}: Expected {expected_types_str}, got {type(value).__name__}"
                )

            if key == "credit_score" and value not in range(300, 851):
                raise ValueError(f"Credit score must be between 300 and 850")

            if key == "loan_type" and value not in ALLOWED_LOAN_TYPE:
                raise Exception(
                    f"""Loan type must be from these options: {", ".join(ALLOWED_LOAN_TYPE)} """
                )

            if key == "property_type" and value not in ALLOWED_PROPERTY_TYPE:
                raise Exception(
                    f"""Property type must be from these options: {", ".join(ALLOWED_PROPERTY_TYPE)} """
                )

    @staticmethod
    def extract_ratio(point_A: int, point_B: int) -> int:
        """Calculate ratio"""
        if point_A > point_B:
            raise Exception("Ratio cannot exceed more then 100%")

        return (point_A / point_B) * 100

    def compute_risk_score(self) -> int:
        """Computes and returns risk score per mortgage"""

        risk_score = 0

        # Calculates Loan-to-Value (LTV) ratio: Loan amount to the property value
        ltv = self.extract_ratio(point_A=self.loan_amount, point_B=self.property_value)
        risk_score += 2 if ltv > 90 else 1 if ltv > 80 else 0

        # Calculates Debt-to-Income (DTI) Ratio: Borrower’s existing debt to their annual income
        dti = self.extract_ratio(point_A=self.debt_amount, point_B=self.annual_income)
        risk_score += 2 if dti > 50 else 1 if dti > 40 else 0

        # Add/Subsctract points depending on the credit score
        if self.credit_score >= 700:
            risk_score -= 1
        elif self.credit_score < 650:
            risk_score += 1

        # Loan & Property type affecting the risk score
        risk_score += -1 if self.loan_type == "fixed" else 1
        risk_score += 1 if self.property_type == "condo" else 0

        return risk_score


# --------------------------------------------------------------------------------
""" 
Naive approach when I surely know that the data set is not that large because multiprocessing can be overkill for smaller data sets 
"""
# def compute_credit_rating_factors(mortgages: list[dict]):
#     total_risk = []
#     credit_scores = []
#     for mortgage_data in mortgages:
#         mortgage = Mortgage(mortgage_data)
#         total_risk.append(mortgage.compute_risk_score())
#         credit_scores.append(mortgage_data.get("credit_score", 0))

#     return total_risk, credit_scores
# --------------------------------------------------------------------------------


def process_mortgage_batch(mortgage_batch):
    """Process a batch of mortgages to reduce inter-process communication"""
    batch_risks = []
    batch_scores = []
    for data in mortgage_batch:
        mortgage = Mortgage(data)
        batch_risks.append(mortgage.compute_risk_score())
        batch_scores.append(data.get("credit_score", 0))

    return batch_risks, batch_scores


def compute_credit_rating_factors(mortgages: list[dict]):
    """Parallel processing with batching"""
    total_risk = []
    credit_scores = []
    batch_size = int(len(mortgages) / 10) if len(mortgages) > 1000 else 100

    # Depending on the size, splitting them into diff. batches...
    batches = [
        mortgages[i : i + batch_size] for i in range(0, len(mortgages), batch_size)
    ]

    # Using 75% of the available CPUs so the system doesnt crashes
    workers = max(1, int(multiprocessing.cpu_count() * 0.75))

    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Processing batches parallelly so it doesnt wait for other tasks
        futures = []
        for batch in batches:
            futures.append(executor.submit(process_mortgage_batch, batch))

        for future in futures:
            batch_risks, batch_scores = future.result()
            total_risk.extend(batch_risks)
            credit_scores.extend(batch_scores)

    return total_risk, credit_scores


def extract_post_average_risk_score(data: list, total_risk: int) -> float:
    """Calculate average of credit scores of all mortgages and return total risk"""
    total_risk = sum(total_risk)
    average_cr_score = sum(data) / len(data)
    if average_cr_score >= 700:
        total_risk -= 1
    elif average_cr_score < 650:
        total_risk += 1

    return total_risk


def compute_credit_rating(total_risk: int) -> str:
    """Assign credit rating as per final risk score"""
    credit_rating = ""
    if total_risk <= 2:
        credit_rating = HIGH_RATING
    elif total_risk in range(3, 6):
        credit_rating = MEDIUM_RATING
    elif total_risk > 5:
        credit_rating = LOW_RATING

    return credit_rating


def calculate_credit_rating(data: dict[list[dict]]):
    """
    Calculates credit rating and return the same depending on various mortgage factors
    """
    try:
        mortgages = data.get("mortgages")

        if not mortgages:
            raise Exception("No mortgages were provided for computation")

        total_risk, credit_scores = compute_credit_rating_factors(mortgages=mortgages)

        total_risk = extract_post_average_risk_score(
            data=credit_scores, total_risk=total_risk
        )

        credit_rating = compute_credit_rating(total_risk=total_risk)

        return credit_rating

    except Exception as e:
        # Raising exception to return it in test cases, generally I would return it in reponse assuming it's an API call with status code as 502, 500 or 406
        raise Exception(e)
