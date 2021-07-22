"""
Warren Outlaw
Final Project
CS-340-Q5079

This module contains additional functions required by the rubric
"""

import crud

cm = crud.CollectionMethods()


def sma(low, high):
    """Find documents for which the "50-Day Simple Moving Average" is
    between a low and high value and return the number of documents
    found.
    """
    
    pipeline = [
                {"$match": {"50-Day Simple Moving Average": {"$gte": low, "$lte": high}}},
                {"$group": {"_id": "Ticker", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "count": 1}}
               ]
    
    try:
        results = cm.aggregate(pipeline)
    except Exception as e:
        return "Error: " + str(e) + "\n"
    else:
        return results
        

def industry_list(industry):
    """Returns a list of ticker symbols based on an industry selected
    by the user.
    """
    
    try:
        results = cm.read({"Industry": industry}, {"_id": 0, "Ticker": 1})
    except Exception as e:
        return "Error: " + str(e) + "\n"
    else:
        return results
    