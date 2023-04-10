import os

with open(f'FULL-overlapping-database_CONVERTED.dat') as f:
    lines = f.read().splitlines()

remove_half_movie = True
new_lines = []

for _ in range(6):
    users_food = []
    users_music = []
    users_movie = []

    user_product = dict()
    product_user = dict()

    products_food = []
    products_music = []
    products_movie = []

    for line in lines:
        user = line.split('	')[0]
        product = line.split('	')[1]

        if product not in product_user:
            product_user[product] = [user]
        else:
            product_user[product].append(user)

        if user not in user_product:
            user_product[user] = [product]
        else:
            user_product[user].append(product)

        if product[0] == '2' and user not in users_food:
            users_food.append(user)
        if product[0] == '3' and user not in users_music:
            users_music.append(user)
        if product[0] == '1' and user not in users_movie:
            users_movie.append(user)
        if product[0] == '2' and product not in products_food:
            products_food.append(product)
        if product[0] == '3' and product not in products_music:
            products_music.append(product)
        if product[0] == '1' and product not in products_movie:
            products_movie.append(product)

    music_count = len(users_music) - min(len(products_movie), len(products_music))
    food_count = len(users_food) - len(products_food)
    movie_count = len(users_movie) - min(len(products_movie), len(products_music))
    new_lines = []

    ## Removendo filmes para igualar ################

    if remove_half_movie:
        remove_movie_users = []
        remove_movie_products = []
        remove_half_movie = False
        # jump = 3800
        jump = 0
        movie_count = len(products_movie) - min(len(products_movie), len(products_music))
        for line in lines:
            user = line.split('	')[0]
            product = line.split('	')[1]
            if product[0] == '1' and movie_count > 0 and jump < 0 and product not in remove_movie_products:
                remove_movie_products.append(product)
                movie_count -= 1
            else:
                jump -= 1

            if product not in remove_movie_products:
                new_lines.append(line)
        lines = new_lines
    else:
        # Removendo usuários ###########################
        print('\nPré-remoção usuários')
        print(len(users_movie))
        print(len(products_movie))
        print(music_count)
        print(food_count)
        print(movie_count)

        remove_user_list = []
        product_with_removed_user = []

        for line in lines:
            user = line.split('	')[0]
            product = line.split('	')[1]
            remove_user_bool = True
            if user == '121080':
                print('Entrou')
            if user in remove_user_list:
                remove_user_bool = True
            elif (product[0] == '3' and music_count > 0) or (product[0] == '2' and food_count > 0) or (product[0] == '1'
                                                                                                       and movie_count > 0):
                # x = user_product[user]
                # if len(user_product[user]) > 1:  # Lista de produtos
                for product_filtered in user_product[user]:
                    if (len(product_user[product_filtered]) - product_with_removed_user.count(product_filtered)) < 2:  # Lista de usuários
                        remove_user_bool = False
                # else:
                #     remove_user_bool = False
            else:
                remove_user_bool = False

            if remove_user_bool and user not in remove_user_list:
                remove_food_bool = False
                remove_music_bool = False
                remove_movie_bool = False

                remove_user_list.append(user)
                for product_removed in user_product[user]:
                    product_with_removed_user.append(product_removed)

                    if product_removed in products_food:
                        remove_food_bool = True
                    if product_removed in products_music:
                        remove_music_bool = True
                    if product_removed in products_movie:
                        remove_movie_bool = True

                if remove_food_bool:
                    food_count -= 1
                if remove_music_bool:
                    music_count -= 1
                if remove_movie_bool:
                    movie_count -= 1

            if not remove_user_bool:
                new_lines.append(line)

        lines = new_lines

        print('\nRemovidos usuários')
        print(music_count)
        print(food_count)
        print(movie_count)

# Removendo produtos #######################
# new_lines = []
# remove_product_list = []
# user_with_removed_product = []
#
# for line in lines:
#     user = line.split('	')[0]
#     product = line.split('	')[1]
#     remove_product_bool = True
#     if product in remove_product_list:
#         remove_product_bool = True
#     elif (product[0] == '3' and music_count < 0) or (product[0] == '2' and food_count < 0) or (product[0] == '1' and
#                                                                                                movie_count < 0):
#         for user_filtered in list(set(product_user[product])):
#             filtered_list = []
#             if product[0] == '2':
#                 for x in list(set(user_product[user_filtered])):
#                     if x[0] == '2':
#                         filtered_list.append(x)
#             if product[0] == '3':
#                 for x in list(set(user_product[user_filtered])):
#                     if x[0] == '3' or x[0] == '2':
#                         filtered_list.append(x)
#             if product[0] == '1':
#                 for x in list(set(user_product[user_filtered])):
#                     if x[0] == '1' or x[0] == '2':
#                         filtered_list.append(x)
#             if (len(filtered_list) - user_with_removed_product.count(user_filtered)) < 2:  # Lista de produtos
#                 remove_product_bool = False
#     else:
#         remove_product_bool = False
#
#     if remove_product_bool and product not in remove_product_list:
#         remove_product_list.append(product)
#         for user_removed in list(set(product_user[product])):
#             user_with_removed_product.append(user_removed)
#
#         if product[0] == '2':
#             food_count += 1
#         if product[0] == '3':
#             music_count += 1
#         if product[0] == '1':
#             movie_count += 1
#
#     if not remove_product_bool:
#         new_lines.append(line)
#
# print('\nRemovidos produtos')
# print(len(users_movie))
# print(len(products_movie))
# print(music_count)
# print(food_count)
# print(movie_count)


## RESET ################
lines = new_lines

users_food = []
users_music = []
users_movie = []

user_product = dict()
product_user = dict()

products_food = []
products_music = []
products_movie = []

for line in lines:
    user = line.split('	')[0]
    product = line.split('	')[1]

    if product not in product_user:
        product_user[product] = [user]
    else:
        product_user[product].append(user)

    if user not in user_product:
        user_product[user] = [product]
    else:
        user_product[user].append(product)

    if product[0] == '2' and user not in users_food:
        users_food.append(user)
    if product[0] == '3' and user not in users_music:
        users_music.append(user)
    if product[0] == '1' and user not in users_movie:
        users_movie.append(user)
    if product[0] == '2' and product not in products_food:
        products_food.append(product)
    if product[0] == '3' and product not in products_music:
        products_music.append(product)
    if product[0] == '1' and product not in products_movie:
        products_movie.append(product)

music_count = len(users_music) - len(products_music)
food_count = len(users_food) - len(products_food)
movie_count = len(users_movie) - len(products_movie)

print('\nPós reset')
print(len(users_movie))
print(len(products_movie))
print(len(users_music))
print(len(products_music))
print(len(users_food))
print(len(products_food))

# Removendo produtos e usuários ###############################
# new_lines = []
# remove_product_user_list = []
# music_count = len(users_music)
# movie_count = len(users_movie)
# to_be_removed_movie_or_music = '0'
# if max(movie_count, music_count) == movie_count:
#     to_be_removed_movie_or_music = '1'
#     to_not_remove_movie_or_music = '3'
# else:
#     to_be_removed_movie_or_music = '3'
#     to_not_remove_movie_or_music = '1'
# result = max(movie_count, music_count) - min(movie_count, music_count)
#
# for line in lines:
#     user = line.split('	')[0]
#     product = line.split('	')[1]
#     remove_bool = True
#     # if len(list(set(product_user[product]))) == 1 and len(list(set(user_product[user]))) == 1 and result > 0 and product not in remove_product_user_list and product[0] == to_be_removed_movie_or_music:
#     if len(list(set(product_user[product]))) == 1 and result > 0 and product not in remove_product_user_list and product[0] == to_be_removed_movie_or_music:
#         for product_filtered in user_product[user]:
#             if product_filtered[0] == to_not_remove_movie_or_music:
#                 remove_bool = False
#     else:
#         remove_bool = False
#
#     if remove_bool:
#         remove_product_user_list.append(product)
#         result -= 1
#
#     if not remove_bool:
#         new_lines.append(line)
#
# print('\nRemovidos produtos e usuários')
# print(result)
#
# ##### RESET #######
# lines = new_lines
#
# users_food = []
# users_music = []
# users_movie = []
#
# user_product = dict()
# product_user = dict()
#
# products_food = []
# products_music = []
# products_movie = []
#
# for line in lines:
#     user = line.split('	')[0]
#     product = line.split('	')[1]
#
#     if product not in product_user:
#         product_user[product] = [user]
#     else:
#         product_user[product].append(user)
#
#     if user not in user_product:
#         user_product[user] = [product]
#     else:
#         user_product[user].append(product)
#
#     if product[0] == '2' and user not in users_food:
#         users_food.append(user)
#     if product[0] == '3' and user not in users_music:
#         users_music.append(user)
#     if product[0] == '1' and user not in users_movie:
#         users_movie.append(user)
#     if product[0] == '2' and product not in products_food:
#         products_food.append(product)
#     if product[0] == '3' and product not in products_music:
#         products_music.append(product)
#     if product[0] == '1' and product not in products_movie:
#         products_movie.append(product)
#
# music_count = len(users_music) - len(products_music)
# food_count = len(users_food) - len(products_food)
# movie_count = len(users_movie) - len(products_movie)
#
# print('\nPós reset')
# print(len(users_movie))
# print(len(products_movie))
# print(len(users_music))
# print(len(products_music))
# print(len(users_food))
# print(len(products_food))

# Escrever as novas linhas
with open('FULL-overlapping-database_CONVERTED_FILTERED.dat', 'w', encoding='UTF8') as f:
    for x in new_lines:
        f.write(f'{x}\n')
