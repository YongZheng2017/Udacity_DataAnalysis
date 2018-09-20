#!/usr/bin/python
# -*- coding:utf-8 -*- 

import sys
import pickle
sys.path.append("../tools/")
from time import time

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list_all = ['poi','salary', 'bonus', 'to_messages', 'deferral_payments',
                 'total_payments','exercised_stock_options','restricted_stock',
                 'shared_receipt_with_poi','restricted_stock_deferred','total_stock_value',
                 'expenses','loan_advances','from_messages',
                 'other','from_this_person_to_poi','director_fees',
                 'deferred_income','long_term_incentive','from_poi_to_this_person',
                 'salary_ratio'] 
            
# features_list = ['poi', 'salary', 'bonus', 'deferred_income', 'total_stock_value', 'exercised_stock_options']
 # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### Task 2: Remove outliers
### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.

### 探索数据集
#查看数据集大小
print '数据集大小：',len(data_dict)
#查看特征数量
print '特征数量：',len(data_dict.items()[0][1])-1
#查看嫌疑犯的数量
count = 0
for item in data_dict.items():
    if item[1]['poi'] == True:
        count +=1
print '嫌疑犯数量：',count
#查看salary值为NaN的数量
count = 0
for item in data_dict.items():
    if item[1]['salary'] == 'NaN':
        count +=1
print 'alary值为NaN的数量：',count
#查看email_address值为NaN的数量
count = 0
for item in data_dict.items():
    if item[1]['email_address'] == 'NaN':
        count +=1
print 'email_address值为NaN的数量：',count
#大于出salayr和bonus的异常值
for x in data_dict.items():
    if x[1]['salary'] > 10000000 and x[1]['bonus'] > 2000000 and x[1]['salary'] != 'NaN' and x[1]['bonus'] != 'NaN':
        print x[0], x[1]['salary'], x[1]['bonus']
#删除异常值
data_dict.pop('TOTAL')
data_dict.pop('THE TRAVEL AGENCY IN THE PARK')

my_dataset = data_dict

#创建新的特征
def salary_ratio(salary, total_payments):
    if salary == 'NaN' or total_payments == 'NaN':
        salary_ratio = 0
    else:
        salary_ratio = float(salary)/total_payments
    return salary_ratio

for key in my_dataset:
    my_dataset[key]['salary_ratio'] = salary_ratio(my_dataset[key]['salary'],  my_dataset[key]['total_payments'])

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list_all, sort_keys = True)
labels, features = targetFeatureSplit(data)

# 特征选择
from sklearn.feature_selection import SelectKBest, f_classif
selector = SelectKBest(f_classif, k=5)
selector.fit(features, labels).scores_
index =  selector.get_support(indices=True)
features_list_best = features_list_all[1:]
print '最佳特征组合：',
features_list = ['poi',]
for i in index:
      print features_list_best[i],
      features_list.append(features_list_best[i])
     
print
print features_list

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.

# 选择朴素贝叶斯算法建立机器学习模型
from sklearn.naive_bayes import GaussianNB
GaussianNB_clf = GaussianNB()

# 选择支持向量机算法建立机器学习模型
from sklearn.svm import SVC
SVC_clf = SVC(kernel = 'rbf')


### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

# 朴素贝叶斯算法
t0 = time()
GaussianNB_clf.fit(features_train, labels_train)
print "GaussianNB_clf training time:", round(time()-t0, 3), "s"
t1 = time()
GaussianNB_pred = GaussianNB_clf.predict(features_test)
print "GaussianNB_clf predict time:", round(time()-t1, 3), "s"

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
GaussianNB_recall = recall_score(labels_test, GaussianNB_pred, average='micro')
GaussianNB_precision = precision_score(labels_test, GaussianNB_pred, average='micro')
print "The naive_bayes's recall is: %s " % GaussianNB_recall
print "The naive_bayes's precision is : %s" % GaussianNB_precision


# 支持向量机算法

# 特征缩放
from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()
features_train = min_max_scaler.fit_transform(features_train)
labels_train = min_max_scaler.fit_transform(labels_train)

# 参数调整
from sklearn.model_selection import GridSearchCV
parameters = {'C':[0.00001,0.0001,0.001,0.01,.1,1,10,100,1000]}
SVC_clf = GridSearchCV(SVC_clf, parameters ) 

t0 = time()
SVC_clf.fit(features_train, labels_train)
print "SVC_clf training time:", round(time()-t0, 3), "s"
t1 = time()
SVC_pred = SVC_clf.predict(features_test)
print "SVC_clf predict time:", round(time()-t1, 3), "s"

SVC_recall = recall_score(labels_test, SVC_pred, average='micro')
SVC_precision = precision_score(labels_test, SVC_pred, average='micro')
print "The SVC's recall is: %s " % SVC_recall
print "The SVC's precision is : %s" % SVC_precision

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(GaussianNB_clf, my_dataset, features_list)