import json

file = open("yelp_academic_dataset_review.json")
reviews = [json.loads(line) for line in file]