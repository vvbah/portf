import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import joblib


data = pd.read_csv('propiedades_Chile_venta.csv')



data.drop(data[data.precio>30000].index,inplace=True)
data.drop(data[data.precio<1000].index,inplace=True)
data.drop(data[data.dormitorios>10].index,inplace=True)
data.drop(data[data.estacionamientos>10].index,inplace=True)
data.drop(data[data.estacionamientos<0].index,inplace=True)
data.drop(data[data.superficie_total>2000].index,inplace=True)
data.drop(data[data.superficie_total<30].index,inplace=True)
data.drop(data[data.superficie_util>700].index,inplace=True)
data.drop(data[data.superficie_util<30].index,inplace=True)


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler,StandardScaler,Normalizer
from sklearn.metrics import mean_squared_error,r2_score
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())


data1=data.copy()

q="""
SELECT *
FROM data1
WHERE tipo in ('Casa')
"""
data1_casa=sqldf(q,globals())


q="""
SELECT *
FROM data1
WHERE tipo in ('Departamento')
"""
data1_dpto=sqldf(q,globals())


data1_v2=data1.drop(['superficie_total','estacionamientos','tipo'],axis=1)
data1_v2_casa=data1_casa.drop(['superficie_total','estacionamientos','tipo'],axis=1)
data1_v2_dpto=data1_dpto.drop(['superficie_total','estacionamientos','tipo'],axis=1)


scaler=MinMaxScaler()
data1_v2_casa_mm=scaler.fit_transform(data1_v2_casa)
data1_v2_casa_mm=pd.DataFrame(data1_v2_casa_mm,columns=['precio', 'superficie_util', 'dormitorios', 'banos'])

data1_v2_dpto_mm=scaler.fit_transform(data1_v2_dpto)
data1_v2_dpto_mm=pd.DataFrame(data1_v2_dpto_mm,columns=['precio', 'superficie_util', 'dormitorios', 'banos'])


X=data1_v2_casa_mm.drop(['precio'],axis=1)
y=data1_v2_casa_mm['precio']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

lr_casa=LinearRegression()
lr_casa.fit(X_train,y_train)

y_pred_lr_casa_v2=lr_casa.predict(X_test)

mean_squared_error(y_test,y_pred_lr_casa_v2)

joblib.dump(lr_casa,'reg_lineal_casa.joblib')


X=data1_v2_dpto_mm.drop(['precio'],axis=1)
y=data1_v2_dpto_mm['precio']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)


lr_dpto=LinearRegression()
lr_dpto.fit(X_train,y_train)

y_pred_lr_dpto_v2=lr_dpto.predict(X_test)

mean_squared_error(y_test,y_pred_lr_dpto_v2)


joblib.dump(lr_dpto,'reg_lineal_dpto.joblib')