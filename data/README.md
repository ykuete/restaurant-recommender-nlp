# Data

Raw review datasets are not committed to this repo (see `.gitignore`).

## Licence

This project uses the [Yelp Open Dataset](https://www.yelp.com/dataset) for educational purposes. Yelp's terms prohibit redistributing the dataset, so no data file is committed, and anything derived from it that still contains review text (parquet files, review snippets) stays private.

## Setup

1. Download the Yelp Open Dataset.
2. Put the two files you need in this folder:
   - `yelp_academic_dataset_business.json`
   - `yelp_academic_dataset_review.json`
3. Run the data pipeline in `recommender/pipeline.py`. It keeps restaurants only and writes two parquet files (about 687k restaurant reviews).

## Other sources considered

- [Google Local Reviews (UCSD)](https://cseweb.ucsd.edu/~jmcauley/datasets.html#google_local)
- Scraped data, only if the site's terms allow it and the instructor agrees
