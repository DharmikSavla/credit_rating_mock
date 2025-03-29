# Credit Rating Agency - Residential Mortgage Securities (RMBS)

## Project Overview

Implementing the credit rating calculation algorithm for residential mortgage-backed
securities (RMBS) using Python as the programming language that computes the credit rating based
on the composition of the underlying mortgages, the financial status of the borrowers, 
and various risk factors.

## Features

- Processes mortgage data in JSON format.
- Calculates individual risk scores for each mortgage.
- Computes aggregate credit ratings (AAA, BBB, or C).
- Supports **Multiprocessing** for large datasets.
- Batch processing implementation.
- Extensive Exception handling for multiple test cases.
- Tested with 100K+ mortgages to confirm linear scaling.

## Thought Process and Design Choices

### 1. **Real-World Relevance**
   - This solution directly supports my work at **United Community Bank**, where I maintain Criticized Asset Reports for non-performing loans. The rating calculation logic mirrors our actual risk assessment workflows for commercial lending portfolios.

### 2. **Error Handling and Validations**
   - **Pre-Processing Checks**: Every mortgage undergoes validation before calculations begin, verifying data types, value ranges, and business rules.
   - **Contextual Feedback**: Instead of generic errors, the system explains exactly what went wrong maintaining a clear communication.

### 3. **Multiprocessing Implementation**
   - **Automatic Batching**: Dynamically groups mortgages into optimal chunks doing parallel batch processing.
   - **Resource-Aware**: Uses 75% of available CPU cores by default, preventing system overload.

### 4. **Future Improvements**
   - Libraries like numpy or pandas can be used if the data becomes more complex. For now the current standard library implementation provides adequate performance while maintaining zero external dependencies.

## Setup and Installation

### 1. Set up a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
```

### 2. Install dependencies
```sh
pip install -r requirements.txt
```

### Testing
```sh
python -m unittest test_credit_rating.py
```
