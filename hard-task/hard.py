import re
import requests
import urllib3
from bs4 import BeautifulSoup
from NL_processing import get_args_from_users_prompt

# Disable InsecureRequestWarning for self-signed SSL certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base URL for all AJAX search endpoints
URL_BASE = "https://shorthorn.digitalbeef.com/modules/DigitalBeef-Landing/ajax"


def get_data_from_table(table: BeautifulSoup) -> tuple[str, list[str], list[list[str]]]:
    """
    Parse an HTML <table> and extract the match count, headers, and row data.
    Returns:
      - matches_count: text of the second row (number of results)
      - headers: list of header names from the third row
      - data: list of rows, each row is a list of cell texts
    If the table contains "No results", returns ("No results", [], []).
    """
    # Check for no-results case
    if "No results" in table.text:
        return "No results", [], []

    # Find all data rows prefixed with id="tr_"
    rows = table.find_all("tr", id=re.compile(r"^tr_"))
    data = [
        [cell.get_text(strip=True) for cell in row.find_all("td")]
        for row in rows
    ]

    # The first three <tr>s: header label row (_), count row, and header names row
    _, count_row, header_row = table.find_all("tr")[:3]
    matches_count = count_row.get_text(strip=True)
    headers = [cell.get_text(strip=True) for cell in header_row.find_all("td")]

    return matches_count, headers, data


def search(search_by: str, params: dict) -> tuple[str, list[str], list[list[str]]]:
    """
    Perform the AJAX GET request for the given search type and parameters.
    Saves the raw HTML to index.html for debugging, then parses the response table.
    """
    endpoint = f"{URL_BASE}/search_results_{search_by}.php"
    response = requests.get(endpoint, params=params, verify=False)

    # Save raw HTML for inspection if needed
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Parse and return the structured table data
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    return get_data_from_table(table)


if __name__ == "__main__":
    # Prompt the user for a natural language query
    user_query = input("Enter your search request: ")

    # Extract search_by and params via your NL processor
    search_by, params = get_args_from_users_prompt(user_query)

    # Execute the search and unpack the results
    matches_count, headers, rows = search(search_by, params)

    # Display results
    print("Matches:", matches_count)
    print("Columns:", headers)
    for row in rows:
        print(row)
