import requests
import os

CONFLUENCE_URL = os.getenv("CONFLUENCE_URL")
CONFLUENCE_API_KEY = os.getenv("CONFLUENCE_API_KEY")

SPACES_URI = f"{CONFLUENCE_URL}/rest/api/space"
CONTENT_URI = f"{CONFLUENCE_URL}/rest/api/content"

def getSpaces():
    """
    Fetch HTML content from a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content.
    """
    url = f"{CONFLUENCE_URL}/rest/api/space"
    response = requests.get(url, headers={"Authorization": f"Bearer {CONFLUENCE_API_KEY}"})
    return response.text

def getSpace(space_key):
    """
    Fetch HTML content from a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content.
    """
    url = f"{CONFLUENCE_URL}/rest/api/space/{space_key}"
    response = requests.get(url, headers={"Authorization": f"Bearer {CONFLUENCE_API_KEY}"})
    return response.text

def getContent(content_id):
    """
    Fetch HTML content from a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content.
    """
    url = f"{CONFLUENCE_URL}/rest/api/content/{content_id}"
    response = requests.get(url, headers={"Authorization": f"Bearer {CONFLUENCE_API_KEY}"})
    return response.text