import streamlit as st
import pandas as pd


def main():
    st.title('Modelo para Comparar Similitud entre Textos')

    st.write("""
    Hoy en día, los clientes suelen entregar su opinión luego de una compra e-commerce, también tienden a opinar en redes 
    sociales sobre algún producto o servicio, además, pueden enviar mails a la empresa respecto a un tema específico, 
    entre otros. Desde el punto de la empresa, toda esta información puede entregar *insights* importantes para apoyar la 
    toma de decisiones en las empresas y mejorar su producto/servicio. Por ejemplo, si una organización recibe 1000 
    correos diarios de clientes con su nivel de satisfacción es muy demoroso para un trabajador revisar cada uno de 
    y clasificarlos, pero si esta tarea se realiza con un computador de manera automática, se puede reducir el tiempo 
    y recursos humanos, agregando valor a la empresa porque cumplir el objetivo en poco tiempo *(incluso un par de minutos)* 
    permite tomar decisiones estratégicas rápidas en la firma respecto a los resultados.  


    """)

    st.write("""
    Todo lo anterior, es posible gracias al **Procesamiento del Lenguaje Natural** (NLP), un área de Machine Learning que 
    permite a las computadoras comprender el lenguaje humano para agilizar procesos específicos. Para esto, es necesario 
    transformar la data no estructurada, ya sean textos o mensajes de voz en alguna representación matemática para poder 
    ejecutar algún algoritmo. Esto se logra extrayendo cada palabra de los documentos en forma de *“tokens”* para luego 
    crear vectores representando los textos.  


    """)

    st.write("""
    Antes de comprender la transformación vectorial de los textos, es importante comprender lo que ocurre con las palabras 
    en sí. En primer lugar, se puede estudiar su morfología, es decir, la estructura interna que separa las palabras en 
    unidades más pequeñas (morfema) para comprenderlas desde su raíz. Luego estos términos se “lematizan”, ósea, se dejan 
    en su forma más pura y válida, por ejemplo, el lema de “tomaste” es “tomar”. Después, estas transforman en expresiones 
    regulares, es decir, en un conjunto de símbolos que se pueden concatenar, unir y/o repetir para que sean entendidas 
    por las computadoras como un “lenguaje regular”. Estos caracteres permiten generalizar las palabras 
    *(lenguaje expresiones regulares - referencia rápida: https://learn.microsoft.com/es-es/dotnet/standard/base-types/regular-expression-language-quick-reference).*  


    """)

    st.write(r"""
    Entendiendo como se preprocesan los términos de los documentos, es posible comprender su representación vectorial. 
    Como se mencionó, para que un modelo de Machine Learning pueda ser entrenado es necesario tener la data representada 
    en forma numérica, pero ¿cómo se pueden transformar textos en números? Primero, se debe considerar que cada 
    documento ($d_i$) tiene N palabras ($w_i$) y a partir de los términos únicos se crea el vocabulario ($V_i$) del texto:  
    """)  

    col1, col2, col3 = st.columns(3)

    with col2:
        st.write(r"""
        $d_i = (w_1, w_2, w_3, w_4, w_5)$  
        $d_i=(a,b,a,a,c)$  
        $V_i = (a,b,c)$
        """)

    st.write(r"""
    Ahora, para transformar un documento en forma vectorial, se toman todas sus palabras como se muestra en $d_i$ y 
    se eliminan las *stopwords*, ósea, todos los términos que no son relevante para la comprensión del texto general 
    (por ejemplo: el, la, un, nos, entre otros) y preprocesar la data hasta que queden en lemas. Luego, se les debe 
    dar un peso a los términos y para esto, se usa el método **TF x IDF**:  
    """)

    st.write(f"""
    + **TF (Term Frequency)**: Entrega la cantidad de veces que se encuentra un término en el documento. Suponiendo que 
    W representa el peso, i los términos y j los documentos, se tiene que:  
    """)

    col1, col2, col3 = st.columns(3)

    with col2:
        st.write(r"$TF(i,j)=W(i,j)$")

    st.write("""
    + **IDF (Inverse Document Frequency)**: Es un ponderador que mide que tan común es una palabra dentro del vocabulario. 
    Teniendo N como el número total de documentos y df(i) como el número de documentos en donde ocurre el i-ésimo 
    término:  
    """)

    col1, col2, col3 = st.columns(3)

    with col2:
        st.write(r"$IDF =log \frac{N}{df(i)}$")

    st.write("""
    Luego, ambos valores se multiplican para así darle un peso representativo a cada término presente en los documentos 
    respecto al vocabulario total. Esto, permite que los documentos sean representados a través de vectores puedan 
    compararse entre sí usando la similitud, en donde los documentos que tienen menor distancia en un espacio 
    multidimensional compuesto por las palabras del vocabulario son los más similares, ósea, los que tengan un valor 
    más cercano a 1 son más similares.  


    """)

    st.subheader("Aplicación TFxIDF")  

    st.write("""
    En Chile, los discursos de los presidentes suelen ser almacenados en https://prensa.presidencia.cl/discursos.aspx, 
    y durante el 2021 se pensaba que muchos de los discursos ya habían sido escuchados antes. Existen más 700 discursos 
    para ser analizados y buscar alguna similitud en ellos, pero realizar esta tarea a mano puede demorar mucho tiempo. 
    Dado esto, se usó Python para buscar la similitud entre pares de discursos, en donde se aplicó todo lo mencionado 
    antes. Como resultado, se obtiene la tabla que se muestra a continuación con el porcentaje de similitud entre ambos 
    discursos:
    """)

    df = pd.read_csv('textos.csv') #data con modelo entrenado anteriormente



    porcentaje_similitud = st.slider('Porcentaje de Similitud', min_value=0.0, max_value=100.0, value=70.0, step=1.0)

    
    resultados_filtrados = df[df['similarity'] >= porcentaje_similitud/100.0] 

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(resultados_filtrados [["pair", "similarity"]])
    
    with col2:
        st.write(f"Se encontraron {resultados_filtrados.shape[0]} pares de discursos con una similitud mayor a {porcentaje_similitud}%")

if __name__ == "__main__":
    main()