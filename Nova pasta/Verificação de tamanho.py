import os
import statistics

with open(f'FULL-overlapping-database.dat') as f:
    lines = f.read().splitlines()

groups = []
products = []
ratings = []

ratings_count_pergroup = {}
ratings_count_pergroup_food = {}
ratings_count_pergroup_music = {}
ratings_count_pergroup_movie = {}

group_total = []

group_food = []
group_music = []
group_movie = []

products_food = []
products_music = []
products_movie = []

for line in lines:
    line_splited = line.split('	')
    group = line_splited[0]
    product = line_splited[1]
    ratings.append(int(line_splited[2]))
    if group not in groups:
        ratings_count_pergroup[group] = 1
    else:
        ratings_count_pergroup[group] += 1
    groups.append(group)
    products.append(product)

    if product[0] == '2':
        if group not in group_food:
            group_food.append(group)
            ratings_count_pergroup_food[group] = 1
        else:
            ratings_count_pergroup_food[group] += 1
        if product not in products_food:
            products_food.append(product)

    elif product[0] == '3':
        if group not in group_music:
            group_music.append(group)
            ratings_count_pergroup_music[group] = 1
        else:
            ratings_count_pergroup_music[group] += 1
        if product not in products_music:
            products_music.append(product)
    else:
        if group not in group_movie:
            group_movie.append(group)
            ratings_count_pergroup_movie[group] = 1
        else:
            ratings_count_pergroup_movie[group] += 1
        if product not in products_movie:
            products_movie.append(product)

print(statistics.mean(list(ratings_count_pergroup.values())))
# print(statistics.mean(ratings))
# print(len(products))
