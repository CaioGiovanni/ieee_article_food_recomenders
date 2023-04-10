""" import random

with open('ratings.dat') as f:
    lines = f.readlines()

user_id, product_id, rating = [], [], []

for line in lines:
    line_splited = line.split("::")
    user_id.append(line_splited[0])
    product_id.append(line_splited[1])
    rating.append(line_splited[2])

with open('contextual-ratings10overlapTargetBOOK.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(rating):
        f.write('{}	{}	{}	-1|-1|-1|-1|-1|-1|-1|-1\n'.format(user_id[i], product_id[i], rating[i])) """

import random
import string

with open('Full ratings/full-ratings-information.dat') as f:
    lines = f.readlines()

product_id, amazon_id, name_list, classification_list, book_type = [], [], [], [], []

for line in lines:
    line_splited = line.split(";")
    product_id.append(int(line_splited[0]) + 100000000)
    amazon_id.append(line_splited[1])
    name_list.append(line_splited[2])
    classification_list.append(line_splited[3])
    book_type.append(line_splited[4])

with open('movies.dat') as f:
    lines = f.readlines()

product_id_food, name_list_food, classification_list_food = [], [], []

for line in lines:
    line_splited = line.split("::")
    product_id_food.append(int(line_splited[0]) + 200000000)
    name_list_food.append(line_splited[1])
    classification_list_food.append(line_splited[2])

with open('full-ratings-information_CONVERTED.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(product_id):
        if str(book_type[i])[:-1] == 'Book':
            f.write('{};{};{};{};{}'.format(product_id[i], amazon_id[i], name_list[i], classification_list[i], book_type[i]))
    for i, _ in enumerate(product_id_food):
        m = max(amazon_id)

        random_choosed = amazon_id[0]
        while random_choosed in amazon_id:
            random_choosed = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
        amazon_id.append(random_choosed)
        f.write('{};{};{};{};Food\n'.format(product_id_food[i], random_choosed, name_list_food[i], str(classification_list_food[i])[:-1]))