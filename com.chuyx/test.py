
# @Date 2022/05/09
# @Author special 15


import csv
import pandas as pd


# E:\qiweiDown\WXWork\1688850806126338\Cache\File\2022-05\186459.csv
# with open ("E:\qiweiDown\WXWork\1688850806126338\Cache\File\2022-05\186459.csv", encoding="utf-8-fig") as f:
#     reader = csv.DictReader(f)

#     for row in reader:
#         print(row)

iris_train=pd.read_csv("E:\qiweiDown\WXWork\1688850806126338\Cache\File\2022-05\186459.csv")
print(iris_train)
