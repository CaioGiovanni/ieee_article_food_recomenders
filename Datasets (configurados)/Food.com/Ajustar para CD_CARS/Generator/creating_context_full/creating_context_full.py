import random
import string
from datetime import datetime

group_contextual, product_contextual, rating_contextual, timestamp_weekend_contextual = [], [], [], []

# types = ['book', 'food']
types = ['food']

for type in types:
    group_id, users_group_id = [], []

    with open(f'../{type}/data/MovieLens-Rand/groupMember.dat') as f:
        lines = f.read().splitlines()

    for i, line in enumerate(lines):
        if type == 'book' or i != (len(lines) - 1):
            line_splited = line.split(" ")
            group_id.append(line_splited[0])
            users_group_id.append(line_splited[1])

    group_id_GROUP_RATING, product_id_GROUP_RATING, ratings_GROUP_RATING = [], [], []

    files = [f'../{type}/data/MovieLens-Rand/groupRatingTrain.dat', f'../{type}/data/MovieLens-Rand/groupRatingTest.dat', f'../{type}/data/MovieLens-Rand/groupRatingVal.dat']

    for file in files:
        with open(file) as f:
            lines = f.read().splitlines()

            for line in lines:
                line_splited = line.split(" ")
                group_id_GROUP_RATING.append(line_splited[0])
                product_id_GROUP_RATING.append(line_splited[1])
                ratings_GROUP_RATING.append(line_splited[2])

    users_id, product_id, timestamp_weekend = [], [], []

    with open(f'../{type}/data/MovieLens-1M/ratings.dat') as f:
        lines = f.read().splitlines()

    for line in lines:
        line_splited = line.split("::")
        users_id.append(line_splited[0])
        product_id.append(line_splited[1])
        timestamp_weekend.append(line_splited[4])
    
    sum = 0
    #if type == 'food':
    #        sum = 1000
    for i, group in enumerate(group_id):
        indices = [j for j, x in enumerate(group_id_GROUP_RATING) if x == group]
        for indice in indices:
            group_contextual.append(int(group) + sum)
            users_group = users_group_id[i].split(",")
            product_contextual.append(product_id_GROUP_RATING[indice])
            rating_contextual.append(5 if int(ratings_GROUP_RATING[indice]) == 1 else 1)
            timestamp_temp = []
            for user in users_group:
                for j, product in enumerate(product_id):
                    if product == product_id_GROUP_RATING[indice] and users_id[j] == user:
                        timestamp_temp.append(timestamp_weekend[j])
            if timestamp_temp == []:
                timestamp_weekend_contextual.append(1)
                group_contextual.append(int(group) + sum)
                users_group = users_group_id[i].split(",")
                product_contextual.append(product_id_GROUP_RATING[indice])
                rating_contextual.append(5 if int(ratings_GROUP_RATING[indice]) == 1 else 1)
                timestamp_weekend_contextual.append(0)
            elif all(int(x) == 1 for x in timestamp_temp):
                timestamp_weekend_contextual.append(1)
            elif all(int(x) == 0 for x in timestamp_temp):
                timestamp_weekend_contextual.append(0)
            else:
                timestamp_weekend_contextual.append(1)
                group_contextual.append(int(group) + sum)
                users_group = users_group_id[i].split(",")
                product_contextual.append(product_id_GROUP_RATING[indice])
                rating_contextual.append(5 if int(ratings_GROUP_RATING[indice]) == 1 else 1)
                timestamp_weekend_contextual.append(0)

# Pegando book do full ratings
with open('../../Full ratings/full-ratings-information.dat') as f:
    lines = f.readlines()

product_id_full = []

for line in lines:
    line_splited = line.split(";")
    if line_splited[4] == "Book\n":
        product_id_full.append(int(line_splited[0]) + 100000000)

with open('../../Full ratings/contextual-ratings-full-new-thesis.dat') as f:
    lines = f.readlines()

group_full_new, product_full_new, rating_full_new, timestamp_full_new = [], [], [], []
        
for line in lines:
    line_splited = line.split("	")
    if (int(line_splited[1]) + 100000000) in product_id_full and line_splited[3].split('|')[5] == '1' and int(line_splited[0]) in group_contextual:
        group_full_new.append(int(line_splited[0]))
        product_full_new.append(int(line_splited[1]) + 100000000)
        rating_full_new.append(line_splited[2])
        timestamp_full_new.append(line_splited[3].split('|')[0])

group_contextual += group_full_new
product_contextual += product_full_new
rating_contextual += rating_full_new
timestamp_weekend_contextual += timestamp_full_new

with open('contextual-ratings-full-new-thesis.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(group_contextual):
        # Comment this condition to not filter
        if group_contextual[i] in group_full_new:
            f.write('{}	{}	{}	{}|-1|-1|-1|-1|1|-1|-1\n'.format(group_contextual[i], product_contextual[i], rating_contextual[i], timestamp_weekend_contextual[i]))


with open('../../full-ratings-information_CONVERTED.dat', encoding="utf8") as f:
        lines = f.read().splitlines()

types = []
product_id, number_id, name, cat, cat_2 = [], [], [], [], []

count = 100
for line in lines:
        line_splited = line.split(";")
        product_id.append(line_splited[0])
        number_id.append(line_splited[1])
        name.append(line_splited[2])
        cat_2.append(line_splited[4])
        cat_set = line_splited[3].upper().replace('.', '_').replace(':', '_').replace('-', '_').replace(' ', '_').replace('60_MINUTES_OR_LESS', 'MINUTES_OR_LESS_60').replace('30_MINUTES_OR_LESS', 'MINUTES_OR_LESS_30').replace('15_MINUTES_OR_LESS', 'MINUTES_OR_LESS_15').replace('4_HOURS_OR_LESS', 'HOURS_OR_LESS_4').replace('5_INGREDIENTS_OR_LESS', 'INGREDIENTS_OR_LESS_5').replace('3_STEPS_OR_LESS', 'STEPS_OR_LESS_3').replace('1_DAY_OR_MORE', 'DAY_OR_MORE_1')
        if cat_set == "":
            cat_set = 'NONE'
        if cat_2[-1] != 'Book':
            for type in cat_set.split('|'):
                if type not in types:
                    types.append(type)
        cat.append(cat_set)

with open('full-ratings-information_CONVERTED_CORRECT.dat', 'w', encoding='UTF8') as f:
    for i, x in enumerate(product_id):
        f.write('{};{};{};{};{}\n'.format(product_id[i], number_id[i], name[i], cat[i], cat_2[i].upper().replace('-', '_').replace(' ', '_')))

with open('types.dat', 'w', encoding='UTF8') as f:
    for i, type in enumerate(types):
        if i == 0:
            f.write(f'{type}({i + 100},ItemDomain.FOOD)')
        else:
            f.write(f', {type}({i + 100},ItemDomain.FOOD)')