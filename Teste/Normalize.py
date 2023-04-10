import numpy as np
import math


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


def mae(real, predictions):
    return np.absolute(np.subtract(real, predictions)).mean()


def rmse(real, predictions):
    return math.sqrt(np.square(np.subtract(real, predictions)).mean())


with open(
        f'PostF(CF-based=br.cin.tbookmarks.recommender.algorithms.RecommenderBuilderUserBasedTracer'
        f')_DayTypeContextualAttribute (4).txt') as f:
    lines = f.read().splitlines()

    start_line = None
    result_list, result_list_prediction = [], []
    for i, line in enumerate(lines):
        if '(TRACER : POS-FILTER) PREDICTIONS VALUES' in line and start_line is None:
            start_line = i

        if start_line is not None and i > start_line + 1:
            line_splited = line.split("	")
            result_list.append(float(line_splited[3]))
            result_list_prediction.append(float(line_splited[4]))

result_list.append(5)
result_list_prediction.append(4.9)

results_normalized = NormalizeData(np.array(result_list))
print(results_normalized)

result_list_prediction.append(1.0)
result_list_prediction.append(5.0)
preditictions_normalized = NormalizeData(np.array(result_list_prediction))
preditictions_normalized = preditictions_normalized[:-2]
print(preditictions_normalized)

print(mae(results_normalized, preditictions_normalized))
print(rmse(results_normalized, preditictions_normalized))

# with open('full-ratings-information_CONVERTED_CORRECT.dat', 'w', encoding='UTF8') as f:
#     for i, x in enumerate(product_id):
#         f.write('{};{};{};{};{}\n'.format(product_id[i], number_id[i], name[i], cat[i], cat_2[i].upper().replace('-', '_').replace(' ', '_')))
