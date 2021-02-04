# Image-Morphing

import numpy as np
import plotDecBoundaries as pD


def sample_mean(data):
    x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0
    l1, l2, l3 = 0, 0, 0
    for i in data:
        if i[-1] == 1:
            x1 += i[0]
            y1 += i[1]
            l1 += 1
        elif i[-1] == 2:
            x2 += i[0]
            y2 += i[1]
            l2 += 1
        else:
            x3 += i[0]
            y3 += i[1]
            l3 += 1
    if l3 == 0:
        return np.array([[x1/l1, y1/l1], [x2/l2, y2/l2]])
    else:
        return np.array([[x1/l1, y1/l1], [x2/l2, y2/l2], [x3/l3, y3/l3]])


def error_rate(data, mean, wine):
    err = 0

    def distance(p1, p2):
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    if wine:
        for line in data:
            d1 = distance(line[:2], mean[0])
            d2 = distance(line[:2], mean[1])
            d3 = distance(line[:2], mean[2])
            m = min(d1, d2, d3)
            if (m == d1 and (int(line[-1]) != 1)) or (m == d2 and (int(line[-1]) != 2)) \
                    or (m == d3 and (int(line[-1]) != 3)):
                err += 1
    else:
        for line in data:
            d1 = distance(line[:2], mean[0])
            d2 = distance(line[:2], mean[1])
            if (d1 < d2 and (int(line[-1]) == 2)) or (d2 < d1 and (int(line[-1]) == 1)):
                err += 1
    return err/len(data)


if __name__ == "__main__":

    # ---------------------------Question a ------------------------- #
    train1_data = np.loadtxt('synthetic1_train.csv', delimiter=',')
    train2_data = np.loadtxt('synthetic2_train.csv', delimiter=',')
    test1_data = np.loadtxt('synthetic1_test.csv', delimiter=',')
    test2_data = np.loadtxt('synthetic2_test.csv', delimiter=',')

    mean1 = sample_mean(train1_data)
    err1_train = error_rate(train1_data, mean1, 0)
    err1_test = error_rate(test1_data, mean1, 0)
    pD.plotDecBoundaries(train1_data, train1_data[:, 2], mean1)
    print(err1_train, err1_test)

    mean2 = sample_mean(train2_data)
    err2_train = error_rate(train2_data, mean2, 0)
    err2_test = error_rate(test2_data, mean2, 0)
    pD.plotDecBoundaries(train2_data, train2_data[:, 2], mean2)
    print(err2_train, err2_test)

    # ---------------------------Question c ------------------------- #
    wine_train = np.loadtxt('wine_train.csv', delimiter=',')
    wine_test = np.loadtxt('wine_test.csv', delimiter=',')
    mean_wine = sample_mean(wine_train)
    err_wine_train = error_rate(wine_train, mean_wine, 1)
    err_wine_test = error_rate(wine_test, mean_wine, 1)
    print(mean_wine, err_wine_test, err_wine_train)
    pD.plotDecBoundaries(wine_train[:, (0, 1)], wine_train[:, 13], mean_wine)

    # ---------------------------Question d ------------------------- #
    lst = []
    for i in range(13):
        for j in range(i+1, 13):
            temp_mean = sample_mean(wine_train[:, (i, j, 13)])
            temp_error_train = error_rate(wine_train[:, (i, j, 13)], temp_mean, 1)
            temp_error_test = error_rate(wine_test[:, (i, j, 13)], temp_mean, 1)
            lst.append([i, j, temp_error_train, temp_error_test])
    lst.sort(key=lambda x: x[2])
    print(lst[0], lst[-1])
    lst.sort(key=lambda x: x[3])
    print(lst[0], lst[-1])
