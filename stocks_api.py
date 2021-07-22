"""
Warren Outlaw
Final Project
CS-340-Q5079

This module implements a RESTful API using a Python web service framework
for a MongoDB collection of stock market summary data.
"""

import ast
import crud
import json
from bson import json_util
from bson.son import SON
from bottle import route, run, request, abort, HTTPResponse

cm = crud.CollectionMethods()


@route('/stocks/api/v1.0/createStock/<ticker>', method=['POST'])
def create_stock(ticker):
    """Create a new stock document for the given ticker symbol"""

    dupe_check = cm.read({"Ticker": ticker})
    if len(dupe_check) > 4:
        return "Ticker already exists in the database.\n"
    
    try:
        output = cm.create({"Ticker": ticker})
    except Exception as e:
        abort(404, str(e))
    else:
        if output:
            result = HTTPResponse(status=201, body="New document created!")
            return "{0}: {1}\n".format(result.status, result.body)
  

@route('/stocks/api/v1.0/getStock/<ticker>', method='GET')
def get_stock(ticker):
    """Retrieve stock document for the given ticker symbol"""

    try:
        output = cm.read({"Ticker": ticker})
        if len(output) < 4:
            result = HTTPResponse(status=404, body="Ticker symbol not found in the database.")
            return "{0}: {1}\n".format(result.status, result.body)
    except Exception as e:
        abort(404, str(e))
    else:
        return output


@route('/stocks/api/v1.0/updateStock/<ticker>', method=['PUT'])
def update_stock(ticker, key=None, value=None):
    """Update stock document for the given ticker symbol"""

    if key is None or value is None:
        try:
            body = request.json
        except:
            return "Please specify a key and value to update.\n"
        else:
            output = cm.update({"Ticker": ticker}, {"$set": body})
    else:
        output = cm.update({"Ticker": ticker}, {"$set": {key: value}})
    
    if "null" not in output:
        return output
    else:
        result = HTTPResponse(status=404, body="Ticker symbol not found in the database.")
        return "{0}: {1}\n".format(result.status, result.body)
  

@route('/stocks/api/v1.0/deleteStock/<ticker>', method=['DELETE'])
def delete_stock(ticker):
    """Remove stock document for the given ticker symbol"""
    
    output = cm.delete({"Ticker": ticker})
    
    if "null" not in output:
        return output
    else:
        result = HTTPResponse(status=404, body="Ticker symbol not found in the database.")
        return "{0}: {1}\n".format(result.status, result.body)


@route('/stocks/api/v1.0/portfolio/<sector>', method='GET')
def portfolio(sector):
    """Match stocks by the selected sector and return the total oustanding
    shares grouped by industry.
    """
    
    pipeline = [
                {"$match": {"Sector": sector}},
                {"$group": {"_id": "$Industry", "outstanding_shares": {"$sum": "$Shares Outstanding"}}},
                {"$project": {"_id": 1, "outstanding_shares": 1}}
               ]

    try:
        output = cm.aggregate(pipeline)
    except Exception as e:
        abort(404, str(e))
    else:
        return output


@route('/stocks/api/v1.0/stockReport', method='POST')
def stock_report():
    """Select and present specific stock summary information by a
    user-derived list of ticker symbols.
    """
    
    raw = request.body.read()
    data = ast.literal_eval(raw)
    usable = [n.strip() for n in data]
    output = []
    
    for ticker in usable:
        output.append(cm.read({"Ticker": ticker}, {"_id": 0, "Ticker": 1, "Performance (YTD)": 1, "Volume": 1}))
    
    return output


@route('/stocks/api/v1.0/industryReport/<industry>', method='GET')
def industry_report(industry):
    """Report a portfolio of five top stocks by a user-derived industry
    selection.
    """
    
    pipeline = [
                {"$match": {"Industry": industry}},
                {"$group": {"_id": "$Ticker", "performance (YTD)": {"$first": "$Performance (YTD)"}}},
                {"$project": {"_id": 1, "performance (YTD)": 1}},
                {"$sort": SON([("performance (YTD)", -1)])},
                {"$limit": 5}
               ]

    try:
        output = cm.aggregate(pipeline)
    except Exception as e:
        abort(404, str(e))
    else:
        return output


if __name__ == '__main__':
    run(host='localhost', port=8080, reloader=True)
    # run(host='localhost', port=8080)
