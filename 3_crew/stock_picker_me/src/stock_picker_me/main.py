#!/usr/bin/env python
import warnings
from stock_picker_me.crew import StockPickerMe

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology'
    }
    
    try:
        result = StockPickerMe().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")