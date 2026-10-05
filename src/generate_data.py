import pandas as pd
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('--city', default='Philadelphia')        
args = parser.parse_args()

print(f"Loading businesses for {args.city}...")

# Load and filter business data
business_df = pd.read_json('yelp_academic_dataset_business.json', lines=True)

# Filter for Restaurants
restaurant = business_df[business_df['categories'].str.contains('Restaurant', na=False)]

restaurant = restaurant[restaurant['city'] == args.city]        # Parse with argument for city

restaurant = restaurant[['business_id', 'name', 'city', 'state','stars', 'review_count', 'is_open', 'attributes', 'categories']]


rest_ids = set(restaurant['business_id'])

chunk_size = 100000
review_chunks = []
for chunk in pd.read_json('yelp_academic_dataset_review.json', lines=True, chunksize=chunk_size):
    # Keep only reviews for the restaurants in our target city
    filtered_chunk = chunk[chunk['business_id'].isin(rest_ids)]
    review_chunks.append(filtered_chunk)

review = pd.concat(review_chunks, ignore_index=True)
print(f"{len(review)} reviews concatenated for {args.city} restaurants.")

output_rest = f'restaurant_{args.city.replace(" ", "")}.parquet'
output_rev = f'review_{args.city.replace(" ", "")}.parquet'

restaurant.to_parquet(output_rest, index=False)
review.to_parquet(output_rev, index=False)

print("Done! Data is ready to be used")