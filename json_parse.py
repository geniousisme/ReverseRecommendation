import json

file = open("yelp_academic_dataset_review.json")
reviews = [json.loads(line) for line in file]

negative_reviews = []
for review in reviews:
    if review[u'stars'] <= 3:
        negative_reviews.append(review)