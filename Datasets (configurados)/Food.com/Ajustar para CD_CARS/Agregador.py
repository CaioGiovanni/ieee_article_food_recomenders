import random
import string
from datetime import datetime

user_id, product_id, rating_list, timestamp_list = [], [], [], []

with open('Original/interactions_test.csv') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i != 0:
        line_splited = line.split(",")
        user_id.append(line_splited[4])
        timestamp_list.append(line_splited[2])
        product_id.append(int(line_splited[1]) + 200000000)
        rating_list.append(int(float(line_splited[3])))

with open('Original/interactions_train.csv') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i != 0:
        line_splited = line.split(",")
        user_id.append(line_splited[4])
        timestamp_list.append(line_splited[2])
        product_id.append(int(line_splited[1]) + 200000000)
        rating_list.append(int(float(line_splited[3])))

with open('Original/interactions_validation.csv') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if i != 0:
        line_splited = line.split(",")
        user_id.append(line_splited[4])
        timestamp_list.append(line_splited[2])
        product_id.append(int(line_splited[1]) + 200000000)
        rating_list.append(int(float(line_splited[3])))

with open('ratings_food.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(user_id):
        timestamp = timestamp_list[i].split('-')
        f.write('{}::{}::{}::{}::{}\n'.format(user_id[i], product_id[i], rating_list[i], timestamp[0] + timestamp[1] + timestamp[2], 
                                            1 if datetime(int(timestamp[0]), int(timestamp[1]), int(timestamp[2])).weekday() > 4 else 0))

with open('ratings_food.dat', 'r') as f:
    x = sorted(f)

with open('ratings_food.dat', 'w') as f:
    for line in x:
        f.write(line)

with open('movies.dat', 'r') as f:
    lines = f.readlines()

product_id = []
others = []
with open('movies_food.dat', 'w') as f:
    for line in lines:
        line_splited = line.split("::")
        f.write('{}::{}::{}'.format(int(line_splited[0]) + 200000000, line_splited[1], line_splited[2]))