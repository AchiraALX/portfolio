#!/usr/bin/env python3
""" Static functions for main.py
"""
from queries import main
from datetime import datetime, timedelta


def get_task_status(date_str, date_format="%Y-%m-%dT%H:%M:%S"):
    """Perform date comparison and return task status

    Arguments:
        date_str {str} -- Date string in the format: YYYY-MM-DDTHH:MM:SS
        date_format {str} -- Date format
    """
    try:
        # Convert date string to datetime object
        task_date = datetime.strptime(date_str, date_format)

        # Get current datetime object
        current_datetime = datetime.now()

        # Calculate boundaries for past, in progress, and future tasks
        past_boundary = current_datetime - timedelta(days=1)
        future_boundary = current_datetime + timedelta(days=1)

        # Compare datetime objects and determine task status
        if current_datetime >= task_date and \
                current_datetime >= past_boundary:
            return "Past Due"
        elif current_datetime <= task_date and \
                current_datetime <= future_boundary:
            return "In Progress"
        elif current_datetime < task_date:
            return "Future Task"
        else:
            return "Unknown Status"
    except ValueError:
        return """
            Invalid date format. Please provide
            dates in the format: YYYY-MM-DDTHH:MM:SS"""
