import matplotlib.pyplot as plt
import numpy as np
from itertools import groupby

import db

'''
Если четное кол-во, то задаем позицию с отступом d = width/2
Если нечетное кол-во, то элементу по середине задаем позицию x
'''

db.upload_data(db.database)
# def all_users_graph():
# dates = [f'{log.time_log_out:%m/%d}' for log in db.logs]

# g_list = []
# dates = [data for data, _ in groupby([f'{log.time_log_out:%m/%d}' for log in db.logs])]
#
# for user in db.users:
#     g = []
#     g_list.append(g)
#
# for date in dates:
#     for log in db.logs:


# cat_par = [data for data, _ in groupby(dates)]

# for user in db.users:

cat_par = [f'P{i}' for i in range(5)]
g1 = [10, 21, 34, 12, 27]
g2 = [17, 15, 25, 21, 26]
g3 = [1, 1, 5, 1, 2]
g4 = [1, 1, 5, 1, 2]
g5 = [1, 1, 5, 1, 2]
g6 = [1, 1, 5, 1, 2]
g7 = [1, 1, 5, 1, 2]
g8 = [1, 1, 5, 1, 2]

width = 0.1
d = width / 2
x = np.arange(len(cat_par))
fig, ax = plt.subplots()
# rects1 = ax.bar(x - width + d, g1, width, label='g1')
# rects2 = ax.bar(x - width * 2 + d, g2, width, label='g2')
# rects3 = ax.bar(x - width * 3 + d, g3, width, label='g3')
# rects4 = ax.bar(x - width * 4 + d, g4, width, label='g4')
# rects5 = ax.bar(x + width - d, g5, width, label='g5')
# rects6 = ax.bar(x + width * 2 - d, g6, width, label='g6')
# rects7 = ax.bar(x + width * 3 - d, g7, width, label='g7')
# rects8 = ax.bar(x + width * 4 - d, g8, width, label='g8')

rects1 = ax.bar(x - width, g1, width, label='g1')
rects2 = ax.bar(x - width * 2, g2, width, label='g2')
rects3 = ax.bar(x, g3, width, label='g3')
rects4 = ax.bar(x + width, g4, width, label='g4')
rects5 = ax.bar(x + width * 2, g5, width, label='g5')

# rects6 = ax.bar(x + width * 2, g6, width, label='g6')
# rects7 = ax.bar(x + width * 3, g7, width, label='g7')
# rects8 = ax.bar(x + width * 4, g8, width, label='g8')

ax.set_title('Пример групповой диаграммы')
ax.set_xticks(x)
ax.set_xticklabels(cat_par)
ax.legend()

plt.show()
