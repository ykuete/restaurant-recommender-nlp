import pandas as pd
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
#parser.add_argument('--city', default='Philadelphia')        
args = parser.parse_args()

print(f"Loading businesses...")

# Load and filter business data
<<<<<<< HEAD:src/generate_data.py
business_df = pd.read_json('../data/yelp_academic_dataset_business.json', lines=True)
=======
business_df = pd.read_json('../data/yelp_dataset/yelp_academic_dataset_business.json', lines=True)
>>>>>>> 041f4daab33d672975d2c828ceda0dbdec20fc47:src/01_data_pipeline.py

# Filter for Restaurants
restaurant = business_df[business_df['categories'].str.contains('Restaurant', na=False)]

#restaurant = restaurant[restaurant['city'] == args.city]        # Parse with argument for city

restaurant = restaurant[['business_id', 'name', 'city', 'state','stars', 'review_count', 'is_open', 'attributes', 'categories']]


rest_ids = set(restaurant['business_id'])

chunk_size = 100000
review_chunks = []
<<<<<<< HEAD:src/generate_data.py
for chunk in pd.read_json('../data/yelp_academic_dataset_review.json', lines=True, chunksize=chunk_size):
=======
for chunk in pd.read_json('../data/yelp_dataset/yelp_academic_dataset_review.json', lines=True, chunksize=chunk_size):
>>>>>>> 041f4daab33d672975d2c828ceda0dbdec20fc47:src/01_data_pipeline.py
    # Keep only reviews for the restaurants in our target city
    filtered_chunk = chunk[chunk['business_id'].isin(rest_ids)]
    review_chunks.append(filtered_chunk)

review = pd.concat(review_chunks, ignore_index=True)
print(f"{len(review)} reviews concatenated for restaurants.")

#output_rest = f'restaurant_{args.city.replace(" ", "")}.parquet'
#output_rev = f'review_{args.city.replace(" ", "")}.parquet'
restaurant_name =f'restaurant_global.parquet'
review_name =f'review_global.parquet'

restaurant.to_parquet(restaurant_name, index=False)
review.to_parquet(review_name, index=False)

print("Done! Data is ready to be used")