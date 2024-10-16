import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

####P5 기준 분류
# 데이터 전처리
data = pd.read_csv("데이터 전처리/data_042.csv", encoding='cp949')
# P5에 따라 분류. P5_True는 주식투자를 하는 사람, P5_False는 주식투자를 하지 않는 사람.
P5_True = pd.DataFrame(data[data['P5'] == 1]).reset_index()
P5_True.drop(columns='index', inplace=True)
P5_False = pd.DataFrame(data[data['P5'] == 0]).reset_index()
P5_False.drop(columns='index', inplace=True)

temp = []
for i in range(0, 425531, 20):
    temp.append(P5_False.iloc[i, :])

P5_False_divide_by20 = pd.DataFrame(temp)
P5_False_divide_by20.reset_index(inplace=True)
P5_False_divide_by20.drop(columns='index', inplace=True)

temp.clear()
for i in range(0, 47698, 2):
    temp.append(P5_True.iloc[i, :])

P5_True_divide_by2 = pd.DataFrame(temp)
P5_True_divide_by2.reset_index(inplace=True)
P5_True_divide_by2.drop(columns='index', inplace=True)

# p-value가 0.05보다 작은 B___를 찾기 위함. p-value가 0.05보다 작은 B는 Pass_p_value에 저장.
Pass_p_value = []
for i in range(1, 168):
    levene = stats.levene(P5_False_divide_by20['B' + str(i)][P5_False_divide_by20['B' + str(i)] != 0],
                          P5_True_divide_by2['B' + str(i)][P5_True_divide_by2['B' + str(i)] != 0])
    if levene[1] >= 0.05:
        boolean = True
    else:
        boolean = False
    #print(boolean)
    p_value = stats.ttest_ind(P5_False_divide_by20['B' + str(i)][P5_False_divide_by20['B' + str(i)] != 0],
                              P5_True_divide_by2['B' + str(i)][P5_True_divide_by2['B' + str(i)] != 0], equal_var=boolean)
    if p_value[1] < 0.05:
        # print('B' + str(i) + "   " + str(p_value[1]))
        print('B' + str(i) + "   " + "%.10f" % p_value[1])
        # print(p_value[0])
        Pass_p_value.append(i)
len(Pass_p_value)

# Pass_p_value에 근거해 그린 boxplot
for i in Pass_p_value:
    sns.boxplot(x="P5", y="B" + str(i), data=data[data['B' + str(i)] != 0])
    plt.savefig('데이터 전처리/boxplot/B' + str(i) + ".png")
sns.boxplot(x="P5", y="C1", data=data[data['C1'] != 0])
plt.show()
