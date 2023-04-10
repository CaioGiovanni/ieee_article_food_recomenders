'''
Created on Nov 10, 2017
Deal something

@author: Lianhai Miao
'''
from time import sleep
import torch
from torch.autograd import Variable
import numpy as np
import math
import heapq
import csv

class Helper(object):
    """
        utils class: it can provide any function that we need
    """
    def __init__(self):
        self.timber = True

    def gen_group_member_dict(self, path):
        g_m_d = {}
        with open(path, 'r') as f:
            line = f.readline().strip()
            while line != None and line != "":
                a = line.split(' ')
                g = int(a[0])
                g_m_d[g] = []
                for m in a[1].split(','):
                    g_m_d[g].append(int(m))
                line = f.readline().strip()
        return g_m_d

    def evaluate_model(self, model, testRatings, testNegatives, K, type_m, epoch):
        """
        Evaluate the performance (Hit_Ratio, NDCG) of top-K recommendation
        Return: score of each test rating.
        """
        precisions, hits, ndcgs, real_score, prediction_score = [], [], [], [], []

        for idx in range(len(testRatings)):
            real_score.append(testRatings[idx][2])
            precision, hr, ndcg, prediction = self.eval_one_rating(model, testRatings, testNegatives, K, type_m, idx)
            prediction_score.append(prediction)
            precisions.append(precision)
            hits.append(hr)
            ndcgs.append(ndcg)
        with open(f'results_exported_{epoch}.csv', 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(precisions)
            wr.writerow(hits)
            wr.writerow(ndcgs)
            wr.writerow(prediction_score)
            wr.writerow(real_score)
        precision, hr, ndcg = np.array(precisions).mean(), np.array(hits).mean(), np.array(ndcgs).mean()
        mae_score = self.mae(real_score, prediction_score)
        rmse_score = self.rmse(real_score, prediction_score)
        f1_score = 2*precision*hr/(precision+hr)
        return precision, hr, ndcg, f1_score, mae_score, rmse_score

    def eval_one_rating(self, model, testRatings, testNegatives, K, type_m, idx):
        rating = testRatings[idx]
        items = testNegatives[idx]
        u = rating[0]
        gtItem = rating[1]
        items.append(gtItem)
        map_item_score = {}
        users = np.full(len(items), u)

        users_var = torch.from_numpy(users)
        users_var = users_var.long()
        items_var = torch.LongTensor(items)
        if type_m == 'group':
            predictions = model(users_var, None, items_var)
        elif type_m == 'user':
            predictions = model(None, users_var, items_var)
        for i in range(len(items)):
            item = items[i]
            map_item_score[item] = predictions.data.numpy()[i]
        items.pop()

        # Evaluate top rank list
        ranklist = heapq.nlargest(K, map_item_score, key=map_item_score.get)
        hr = self.getHitRatio(ranklist, gtItem)
        precision = self.getPrecisionRatio(ranklist, gtItem)
        ndcg = self.getNDCG(ranklist, gtItem)
        prediction_score = map_item_score[gtItem]
        return precision, hr, ndcg, prediction_score

    def getHitRatio(self, ranklist, gtItem):
        for i, item in enumerate(ranklist):
            if item == gtItem:
                return float(1/(i+1))
        return 0

    def getPrecisionRatio(self, ranklist, gtItem):
        for item in ranklist:
            if item == gtItem:
                return 1
        return 0

    def getNDCG(self, ranklist, gtItem):
        for i in range(len(ranklist)):
            item = ranklist[i]
            if item == gtItem:
                return math.log(2) / math.log(i+2)
        return 0

    def mae(self, real, predictions):
        return np.absolute(np.subtract(real, predictions)).mean()

    def rmse(self, real, predictions):
        return math.sqrt(np.square(np.subtract(real, predictions)).mean())
