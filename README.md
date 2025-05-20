# Web Scraper Project

This project contains two web scraping tasks: easy-task and hard-task.

## Easy Task (easy-task/)

The easy-task scrapes data from [https://www.amgr.org/frm_directorySearch.cfm](https://www.amgr.org/frm_directorySearch.cfm).

### Functionality:
- Fetches lookup maps for state, member, and breed IDs.
- Queries the directory based on user input (hard-coded in the example).
- Parses and displays the search results.

### Files:
- main.py: The main script for the easy task.
- README.md: This file.

## Hard Task (hard-task/)

The hard-task scrapes data from [https://shorthorn.digitalbeef.com](https://shorthorn.digitalbeef.com). It uses natural language processing to interpret user queries.

### Functionality:
- Takes a natural language query as input.
- Uses an LLM (Large Language Model) via an API to convert the natural language query into search parameters.
- Performs a search on the website using the generated parameters.
- Parses and displays the search results.

### Files:
- hard.py: The main script for the hard task.
- NL_processing.py: Handles natural language processing and API calls to the LLM.
- prompt.txt: Contains the prompt used for the LLM.
- index.html:  (Generated file) Stores the HTML response from the search.
- data.json: (Generated file) Stores the JSON response from the LLM API.


## Dependencies

The project relies on the following Python libraries:

- requests: For making HTTP requests.
- beautifulsoup4: For parsing HTML content.
- urllib3: Used by requests, warnings are disabled for insecure requests in hard-task.


To install the dependencies, run:
pip install -r requirements.txt