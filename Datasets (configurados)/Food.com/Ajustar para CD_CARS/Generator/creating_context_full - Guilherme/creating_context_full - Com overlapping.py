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
with open('full-ratings-information_movie.dat') as f:
    lines = f.readlines()

product_id_full_movie, number_id_movie, name_movie, cat_movie, cat_2_movie = [], [], [], [], []

for line in lines:
    line_splited = line.split(";")
    if line_splited[4] == "MOVIE\n":
        product_id_full_movie.append(int(line_splited[0]) + 100000000)
        number_id_movie.append(line_splited[1])
        name_movie.append(line_splited[2])
        cat_movie.append(line_splited[3])
        cat_2_movie.append(line_splited[4][:-1])

with open('FULL-overlapping-database.dat') as f:
    lines = f.readlines()

group_full_new, product_full_new, rating_full_new, timestamp_full_new = [], [], [], []

for line in lines:
    line_splited = line.split("	")
    if (int(line_splited[1]) + 100000000) in product_id_full_movie and line_splited[3].split('|')[5] == '1':
        group_full_new.append(int(line_splited[0]))
        product_full_new.append(int(line_splited[1]) + 100000000)
        rating_full_new.append(line_splited[2])
        timestamp_full_new.append(line_splited[3].split('|')[0])

group_contextual += group_full_new
product_contextual += product_full_new
rating_contextual += rating_full_new
timestamp_weekend_contextual += timestamp_full_new

with open('full-ratings-information_music.dat') as f:
    lines = f.readlines()

product_id_full_music, number_id_music, name_music, cat_music, cat_2_music = [], [], [], [], []

for line in lines:
    line_splited = line.split(";")
    if line_splited[4] == "Music\n":
        product_id_full_music.append(int(line_splited[0]) + 300000000)
        number_id_music.append(line_splited[1])
        name_music.append(line_splited[2])
        cat_music.append(line_splited[3])
        cat_2_music.append(line_splited[4][:-1])

with open('FULL-overlapping-database.dat') as f:
    lines = f.readlines()

group_full_new, product_full_new, rating_full_new, timestamp_full_new = [], [], [], []

for line in lines:
    line_splited = line.split("	")
    if (int(line_splited[1]) + 300000000) in product_id_full_music and line_splited[3].split('|')[5] == '1':
        group_full_new.append(int(line_splited[0]))
        product_full_new.append(int(line_splited[1]) + 300000000)
        rating_full_new.append(line_splited[2])
        timestamp_full_new.append(line_splited[3].split('|')[0])

group_contextual += group_full_new
product_contextual += product_full_new
rating_contextual += rating_full_new
timestamp_weekend_contextual += timestamp_full_new

with open('FULL-overlapping-database_CONVERTED.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(group_contextual):
        # Comment this condition to not filter
        # if group_contextual[i] in group_full_new:
        f.write('{}	{}	{}	{}|-1|-1|-1|-1|1|-1|-1\n'.format(group_contextual[i], product_contextual[i], rating_contextual[i], timestamp_weekend_contextual[i]))


with open('../../full-ratings-information_CONVERTED.dat', encoding="utf8") as f:
        lines = f.read().splitlines()

types = []
product_id, number_id, name, cat, cat_2 = [], [], [], [], []

for line in lines:
    line_splited = line.split(";")
    if line_splited[4] != 'BOOK' and line_splited[4] != 'Book':
        product_id.append(line_splited[0])
        number_id.append(line_splited[1])
        name.append(line_splited[2])
        cat_2.append(line_splited[4])
        cat_set = line_splited[3].upper().replace('.', '_').replace(':', '_').replace('-', '_').replace(' ', '_').replace('60_MINUTES_OR_LESS', 'MINUTES_OR_LESS_60').replace('30_MINUTES_OR_LESS', 'MINUTES_OR_LESS_30').replace('15_MINUTES_OR_LESS', 'MINUTES_OR_LESS_15').replace('4_HOURS_OR_LESS', 'HOURS_OR_LESS_4').replace('5_INGREDIENTS_OR_LESS', 'INGREDIENTS_OR_LESS_5').replace('3_STEPS_OR_LESS', 'STEPS_OR_LESS_3').replace('1_DAY_OR_MORE', 'DAY_OR_MORE_1')
        if cat_set == "":
            cat_set = 'NONE'
        if cat_2[-1] != 'BOOK' and cat_2[-1] != 'Book':
            for type in cat_set.split('|'):
                if type not in types:
                    types.append(type)
        cat.append(cat_set)

product_id_full_movie += product_id
number_id_movie += number_id
name_movie += name
cat_movie += cat
cat_2_movie += cat_2

product_id_full_music += product_id
number_id_music += number_id
name_music += name
cat_music += cat
cat_2_music += cat_2

with open('output/full-ratings-information_movie.dat', 'w', encoding='UTF8') as f:
    for i, x in enumerate(product_id_full_movie):
        f.write('{};{};{};{};{}\n'.format(product_id_full_movie[i], number_id_movie[i], name_movie[i], cat_movie[i], cat_2_movie[i].upper().replace('-', '_').replace(' ', '_')))

with open('output/full-ratings-information_music.dat', 'w', encoding='UTF8') as f:
    for i, x in enumerate(product_id_full_music):
        f.write('{};{};{};{};{}\n'.format(product_id_full_music[i], number_id_music[i], name_music[i], cat_music[i], cat_2_music[i].upper().replace('-', '_').replace(' ', '_')))

with open('types.dat', 'w', encoding='UTF8') as f:
    for i, type in enumerate(types):
        if i == 0:
            f.write(f'{type}({i + 100},ItemDomain.FOOD)')
        else:
            f.write(f', {type}({i + 100},ItemDomain.FOOD)')