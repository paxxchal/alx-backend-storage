#!/usr/bin/env python3
"""
Module that contains a function to list all documents in a MongoDB collection
"""


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection

    Args:
    mongo_collection: pymongo collection object

    Returns:
    List of all documents in the collection, or an empty list if no documents
    """
    return list(mongo_collection.find())
