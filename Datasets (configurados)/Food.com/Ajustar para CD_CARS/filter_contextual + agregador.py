import random
import string

with open('Full ratings/full-ratings-information.dat') as f:
    lines = f.readlines()

product_id, amazon_id, name_list, classification_list, book_type = [], [], [], [], []

for line in lines:
    line_splited = line.split(";")
    if line_splited[4] == "Book\n":
        product_id.append(int(line_splited[0]) + 100000000)
        amazon_id.append(line_splited[1])
        name_list.append(line_splited[2])
        classification_list.append(line_splited[3])
        book_type.append(line_splited[4])

with open('Full ratings/contextual-ratings-full-new-thesis.dat') as f:
    lines = f.readlines()

user_id_contextual, product_list_contextual, rating_list_contextual, contextual_list_contextual = [], [], [], []

for line in lines:
    line_splited = line.split("	")
    user_id_contextual.append(line_splited[0])
    product_list_contextual.append(int(line_splited[1]) + 100000000)
    rating_list_contextual.append(line_splited[2])
    contextual_list_contextual.append(line_splited[3])

with open('contextual-ratings-full-new-thesis_CONVERTED.dat', 'w', encoding='UTF8') as f:
    for i, _ in enumerate(product_list_contextual):
        if product_list_contextual[i] in product_id:
            f.write('{}	{}	{}	{}'.format(user_id_contextual[i], product_list_contextual[i], rating_list_contextual[i], contextual_list_contextual[i]))