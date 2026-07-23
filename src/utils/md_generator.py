import requests
from markdownify import markdownify as md

def html_to_markdown(html_content):
    """
    Convert HTML content to Markdown format.

    Args:
        html_content (str): The HTML content to be converted.

    Returns:
        str: The converted Markdown content.
    """
    return md(html_content)

def fetch_html_content(url):
    """
    Fetch HTML content from a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content.
    """
    response = requests.get(url)
    return response.text

def fetch_and_convert_to_markdown(url):
    """
    Fetch HTML content from a URL and convert it to Markdown format.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The converted Markdown content.
    """
    html_content = fetch_html_content(url)
    markdown_content = html_to_markdown(html_content)
    return markdown_content