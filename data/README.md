# Data

Raw review datasets are not committed to this repo (see `.gitignore`).

## Suggested sources

- [Yelp Open Dataset](https://www.yelp.com/dataset) — large, free, restaurant reviews with ratings and metadata
- [Google Local Reviews (UCSD)](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local) — an alternative if Yelp's terms don't fit the project
- Scraped data — only if scraping is permitted by the target site's terms of service; check with the instructor first

## User Agreement
Since this project uses Yelp dataset, the website specifically prohibited redistribution of dataset, therefore, there is no datafile in the data folder. Instead, we included a `generate_data.py` to read and parse through the JSON files ("Business" and "Reviews") then output to a parquet file of a limited portion of data value (687k reviews). Below is the detailed instruction to download and parse the data.

## Setup

Yelp Open Dataset
1. Download Yelp Open Dataset into this folder (`data`).
2. It's possible to only keep JSON business and JSON review
3. Run the `generate_data.py` script.
*Note: We might need to fix the path of the `generating_data.py` for it to work
