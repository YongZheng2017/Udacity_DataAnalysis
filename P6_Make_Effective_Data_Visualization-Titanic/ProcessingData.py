#导入要用到的包
import numpy as np
import pandas as pd

#导入数据
filename = 'titanic_dataset.csv'
titanic_df = pd.read_csv(filename)
bins = np.arange(0,90,20)
titanic_df['age_group'] = pd.cut(titanic_df['age'], bins)
print titanic_df.head()
titanic_df.to_csv('titanic_dataset_updated2.csv')

