#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB
"""

from pymongo import MongoClient


def log_stats():
    """
    Function to calculate and display Nginx log stats from MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods stats
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"    method {method}: {count}")

    # Number of status check
    status_check = collection.count_documents(
        {
            "method": "GET",
            "path": "/status"}
        )
    print(f"{status_check} status check")

if __name__ == "__main__":
    log_stats()
