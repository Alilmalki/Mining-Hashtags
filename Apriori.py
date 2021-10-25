import itertools

def load_hashtags():
    with open('hashtag_baskets.csv') as f:
        return [
            set(line.strip().split(','))
            for line in f
        ]

def get_frequent_items(items_baskets, support):
    all_items = {}

    for basket in items_baskets:
        for hashtag in basket:
            all_items[hashtag] = (all_items[hashtag]+1 if hashtag in all_items.keys() else 1)
    frequent_items = {}
    for k, v in all_items.items():
        if v >= support:
            frequent_items[k] = v
    
    return frequent_items


frequent_items = get_frequent_items(hashtag_baskets, 10)
candidate_pairs = set(itertools.combinations(frequent_items, 2))


#Finding frequent pairs
temp_pairs = {}
for pair in candidate_pairs:
    for basket in hashtag_baskets:
        if set(pair).issubset(set(basket)):
            temp_pairs[pair] = (
                    temp_pairs[pair]+1 if pair in temp_pairs.keys() 
                    else 1
            )


frequent_pairs = {}
for k, v in temp_pairs.items():
    if v >= support:
        frequent_pairs[k] = v



#Generating association rules
association_rules = {}
confidence_threshold = 0.6

for pair in frequent_pairs.keys():
    rule1 = (pair[0], pair[1])
    rule2 = (pair[1], pair[0])

    confidence_rule1 = frequent_pairs[pair]/frequent_items[pair[0]]
    confidence_rule2 = frequent_pairs[pair]/frequent_items[pair[1]]

    association_rules[rule1] = confidence_rule1
    association_rules[rule2] = confidence_rule2
association_rules_filtered = {}

for k, v in association_rules.items():
    if v >= confidence_threshold:
        association_rules_filtered[k] = v
for k, v in association_rules_filtered.items():
    print(str(k[0]) + ' ==> ' + str(k[1]) + '. Confidence = ' + str(v))