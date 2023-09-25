import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


####################################################################################################################
######################################## PROYECTO 1 ################################################################
####################################################################################################################

#### APP: 

### TITULO ###
def main():

    st.title("Predicción de Precio de Propiedades")

    ### INTRODUCCION: ###

    st.write("""
    El aprendizaje automático es un campo que ha llegado a revolucionar diferentes industrias en los negocios ya que 
    se pueden realizar predicciones o clasificaciones a partir de datos históricos que ayudan a la toma de decisiones. 
    Un rubro en dónde se ha visto gran uso de inteligencia artificial es en Marketing, pues empresas de comercio 
    *(como retail por ejemplo)* suelen guardar la información de compra de los clientes para después crear estrategias 
    personalizadas a ellos y fomentar su fidelización a la empresa, un clásico ejemplo son los descuentos que se 
    imprimen con la boleta en los supermercados luego de ingresar el Rut de comprador frecuente, generalmente estos 
    tienen relación con el historial de compras.  """)


    st.markdown("""

    La siguiente aplicación tienen como objetivo predecir el valor en UF de las propiedades en Santiago de Chile. 
    El modelo fue entrenado con 20.000 datos del año 2022 y se tomaron las 3 variables con mayor correlación al precio: 
    Superficie útil, número de dormitorios y número de baños. Con este, se puede tener una idea del mercado inmobiliario 
    en la capital, pues permite conocer los precios aproximados ofrecidos en el mercado. También, sirve para quienes desean 
    comprar una propiedad en el corto plazo y tener un valor aproximado a pagar por las características de la vivienda. 
    Es importante destacar que este es un modelo en versión simplificada, existen otras variables que también pueden 
    influir en el modelo como la distancia al metro, ubicación, comercios cerca, entre otros.
    """)


    st.subheader("Aplicación: ")

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



    data1_casa=data[data['tipo']=='Casa']
    data1_dpto=data[data['tipo']=='Departamento']

    data1_v2_casa=data1_casa.drop(['superficie_total','estacionamientos','tipo'],axis=1)
    data1_v2_dpto=data1_dpto.drop(['superficie_total','estacionamientos','tipo'],axis=1)


    X=data1_v2_casa.drop(['precio'],axis=1)
    y=data1_v2_casa['precio']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)

    lr_casa=LinearRegression()
    lr_casa.fit(X_train,y_train)


    X=data1_v2_dpto.drop(['precio'],axis=1)
    y=data1_v2_dpto['precio']
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=42)


    lr_dpto=LinearRegression()
    lr_dpto.fit(X_train,y_train)


    ### BOTON TIPO PROP ###

    tipo_propiedad = st.selectbox("Tipo de propiedad", ["Casa", "Departamento"])

    ### BOTON DORMITORIOS ###
    dormitorios = st.number_input("Número de Dormitorios", min_value=1, max_value=10)

    ### BOTON SUP UTIL ###
    superficie_util = st.number_input("Superficie Útil (m²)", min_value=1.0, value=60.0 ,max_value=1000.0)

    ### BAÑOS ###
    num_banos = st.number_input("Número de Baños", min_value=1, max_value=10)

    ### BOTON PREDICCION ###
    if st.button("Predecir Precio"):
        if tipo_propiedad == "Casa":
            # Cargar el modelo de casa
            model = lr_casa
        else:
            # Cargar el modelo de departamento
            model = lr_dpto

        precio_predicho = model.predict([[superficie_util,dormitorios, num_banos]])[0]

        st.write(f"El precio predicho es: {precio_predicho:.2f} UF")

if __name__ == "__main__":
    main()
