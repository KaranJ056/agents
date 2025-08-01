#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from financial_researcher_me.crew import FinancialResearcherMe
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the financial researcher crew.
    """
    
    inputs = {
        'company': 'Crest Infosystems Pvt. Ltd.'
    }
    
    try:
        result = FinancialResearcherMe().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")