"""
Warren Outlaw
Final Project
CS-340-Q5079

This module implements MongoDB collection level methods.
"""

import dbconfig
import json
from bson import json_util
from pymongo import MongoClient
from pymongo import ReturnDocument
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.errors import PyMongoError

HOST = dbconfig.HOST
PORT = dbconfig.PORT
DB = dbconfig.DB
COLL = dbconfig.COLL
TIMEOUT = dbconfig.TIMEOUT


class CollectionMethods(object):

    def __init__(self):
        """Try to establish a connection to the MongoDB server.
        
        Will exit if the server does not respond within the assigned
        TIMEOUT value in milliseconds.
        """
      
        try:
            self.connection = MongoClient(HOST, PORT, serverSelectionTimeoutMS=TIMEOUT)
            self.connection.server_info()
        except ServerSelectionTimeoutError as e:
            print str(e)
            exit()
        else:
            self.db = self.connection[DB]
            self.collection = self.db[COLL]

    def create(self, document):
        """Insert a single document into the collection.

        Args:
          document (dict): Single document or array of documents to insert.

        Returns:
          bool: True for success, False otherwise.
        """

        try:
            self.collection.insert_one(document)
        except PyMongoError:
            return False
        else:
            return True

    def read(self, query, projection=None):
        """Query the collection for documents.

        Args:
          query (dict): Key/value lookup pair.

        Returns:
          str: Documents matching query criteria in JSON format.
        """

        try:
            results = self.collection.find(query, projection)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return json_util.dumps(results, indent=4, sort_keys=True) + "\n"

    def read_one(self, query=None):
        """Get a single document from the database.

        Args:
          query (dict, optional): Key/value lookup pair.

        Returns:
          str: Documents matching query criteria in JSON format.
        """

        if query is None:
            try:
                result = self.collection.find_one()
            except PyMongoError as e:
                return "Error: " + str(e) + "\n"
            else:
                return json_util.dumps(result, indent=4, sort_keys=True) + "\n"

        try:
            result = self.collection.find_one(query)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return json_util.dumps(result, indent=4, sort_keys=True) + "\n"

    def update(self, query, mod):
        """Modifies an existing document.

        Args:
          query (dict): Key/value pair of the document to update.
          mod (dict): Key/value pair of modifications to apply.

        Returns:
          str: Document after modifications have been applied in JSON format.
        """

        try:
            result = self.collection.find_one_and_update(query, mod, return_document=ReturnDocument.AFTER)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return json_util.dumps(result, indent=4, sort_keys=True) + "\n"

    def delete(self, document):
        """Removes a document from the collection.

        Args:
          document (dict): Key/value pair of the document to delete.

        Returns:
          str: Document that was deleted in JSON format.
        """

        try:
            result = self.collection.find_one_and_delete(document)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return json_util.dumps(result, indent=4, sort_keys=True) + "\n"
          
    def aggregate(self, pipeline):
        """Perform aggregation operations on a collection.

        Args:
          pipeline (list): A list of aggregation pipeline stages

        Returns:
          str: Documents matching query criteria in JSON format.
        """

        try:
            results = self.collection.aggregate(pipeline)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return json_util.dumps(results, indent=4, sort_keys=True) + "\n"
          
    def count(self, query):
      
        try:
            results = self.collection.count_documents(query)
        except PyMongoError as e:
            return "Error: " + str(e) + "\n"
        else:
            return results + "\n"
