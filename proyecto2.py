import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import contextily as cx
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import Point
from pandasql import sqldf
import os


pysqldf = lambda q: sqldf(q, globals())


####################################################################################################################
######################################## PROYECTO 2 ################################################################
####################################################################################################################

############################ DEF Y DICTS ########################################################################

#### DEF:
def dic(P,dic):
     censo[P]=censo[P].map(dic)

#### DICTS:
dict_var= {
    'P07':'relacion_parentesco',
    'P08':'sexo',
    'P09':'edad',
    'P13':'educ_formal_actual',
    'P14':'curso_mas_alto',
    'P15':'nivel_curso_mas_alto',
    'P15A':'completo_nivel_alto',
    'P16':'pueblo_indig',
    'P18':'rama_act_economica',
    'ESCOLARIDAD':'escolaridad'
    
}

dic_P07= {
1:'Jefe/a de hogar',
2:'Esposo/a o cónyuge',
3:'Conviviente por unión civil',
4:'Conviviente de hecho o pareja',
5:'Hijo/a',
6:'Hijo/a del cónyuge, conviviente o pareja',
7:'Hermano/a',
8:'Padre/madre',
9:'Cuñado/a',
10:'Suegro/a',
11:'Yerno/nuera',
12:'Nieto/a',
13:'Abuelo/a'
}
    
dic_P08= {
    1:'Mujer',
    2:'Hombre'
}

dic_P13 = {
    1:'Sí',
    98:'No aplica',
    99:'Missing',
    2:'No asiste actualmente',
    3:'Nunca asistió'
}

dic_P14 = {
    0:'0',
    98:'No aplica',
    99:'Missing',
    1:'1°',
    2:'2°',
    3:'3°',
    4:'4°',
    5:'5°',
    6:'6°',
    7:'7°',
    8:'8°'
}

dic_P15 = {
    1:'Sala cuna o jardín infantil',
    98:'No aplica',
    99:'Missing',
    2:'Prekínder',
    3:'Kínder',
    4:'Especial o diferencial',
    5:'Educación básica',
    6:'Primaria o preparatorio (sistema antiguo)',
    7:'Científico-humanista',
    8:'Técnica profesional',
    9:'Humanidades (sistema antiguo)',
    10:'Técnica comercial, industrial/normalista (sistema antiguo)',
    11:'Técnico superior (1-3 años)',
    12:'Profesional (4 o más años)',
    13:'Magíster',
    14:'Doctorado'
}

dic_P15A = {
    1:'Si',
    2:'No',
    98:'No Aplica',
    99:'Missing'
}

dic_P16 = {
    1:'Si',
    2:'No',
    98:'No Aplica',
    99:'Missing'
}

dic_P18 = {
    'A':'Agricultura, ganadería, silvicultura y pesca',
    '98':'No aplica',
    '99':'Missing',
    'B':'Explotación de minas y canteras',
    'C':'Industrias manufactureras',
    'D':'Suministro de electricidad, gas, vapor y aire acondicionado',
    'E':'Suministro de agua; evacuación de aguas residuales, gestión de desechos y descontaminación',
    'F':'Construcción',
    'G':'Comercio al por mayor y al por menor; reparación de vehículos automotores y motocicletas',
    'H':'Transporte y almacenamiento',
    'I':'Actividades de alojamiento y de servicios de comidas',
    'J':'Información y comunicaciones',
    'K':'Actividades financieras y de seguros',
    'L':'Actividades inmobiliarias',
    'M':'Actividades profesionales, científicas y técnicas',
    'N':'Actividades de servicios administrativos y de apoyo',
    'O':'Administración pública y defensa; planes de seguridad social de afiliación obligatoria',
    'P':'Enseñanza',
    'Q':'Actividades de atención de la salud humana y de asistencia social',
    'R':'Actividades artísticas, de entretenimiento y recreativas',
    'S':'Otras actividades de servicios',
    'T':'Actividades de los hogares como empleadores; actividades no diferenciadas de los hogares como productores de bienes y servicios para uso propio',
    'U':'Actividades de organizaciones y órganos extraterritoriales',
    'Z':'Rama no declarada'
}

dic_P12={
    1:'En esta comuna',
    98:'No aplica',
    99:'Missing',
    2:'En otra comuna',
    3:'Perú',
    4:'Argentina',
    5:'Bolivia',
    6:'Ecuador',
    7:'Colombia',
    8:'Otro'
}


############################ BASES: ############################################################################
    
prop=pd.read_csv('prop.csv')
viviendas=pd.read_csv('viviendas.csv')
censo=pd.read_csv('censo17.csv')

dic('P12',dic_P12)
df=gpd.read_file("C:\\Users\\vverg\\Desktop\\portafolio_vale\\Untitled Folder\\Zones Chile.shp")
metro=gpd.read_file("C:\\Users\\vverg\\Desktop\\portafolio_vale\\Untitled Folder\\Metro.shp")


eecc=df[df['cod_comuna']=='13106']

estaciones=['ESTACION CENTRAL','ECUADOR','LAS REJAS','PAJARITOS','PILA DEL GANSO']
metro1=metro[metro['nombre'].isin(estaciones)]

eecc_censo=eecc.drop(['market','nom_comuna', 'cod_comuna', 'poblacion',
       'metros2'],axis=1)
eecc_censo=eecc_censo.rename(columns={'geocodigo':'ZONA'})
censo['ZONA']=censo['ZONA'].astype(str)

censo_map=pd.merge(censo,eecc_censo,on='ZONA')
censo_map['P15']=censo_map['P15'].map(dic_P15)
censo_map['P13']=censo_map['P13'].map(dic_P13)
censo_map['P15A']=censo_map['P15A'].map(dic_P15A)
censo_map['P18']=censo_map['P18'].map(dic_P18)


censo_map['Universitarios'] = censo_map['ESCOLARIDAD'].apply(lambda x: 1 if x > 12 else 0)

censo_map1=censo_map.copy()
censo_map1=censo_map1[censo_map1['P09']>=25]

porcentaje_universitarios = (
    censo_map1.groupby('ZONA')['Universitarios']
    .mean()
    .apply(lambda x: round(x * 100, 2)) 
    .reset_index())
porcentaje_universitarios['pctj_univ']=porcentaje_universitarios['Universitarios'].apply(lambda x: '1' if x >= 50.0 else '0')

ptje_univ_map=gpd.GeoDataFrame(pd.merge(eecc_censo,porcentaje_universitarios,on='ZONA'))

censo_com=censo_map[(censo_map['P12']=='En esta comuna') | (censo_map['P12']=='En otra comuna') ]
censo_com['nacidos']=censo_map['P12'].apply(lambda x: 1 if x=='En esta comuna' else 0)

ptje_nacidos = (
    censo_com.groupby('ZONA')['nacidos']
    .mean()
    .apply(lambda x: round(x * 100, 2)) 
    .reset_index())
ptje_nacidos['dummy']=ptje_nacidos['nacidos'].apply(lambda x: '1' if x >= 50.0 else '0')
ptje_nacidos=gpd.GeoDataFrame(pd.merge(eecc_censo,ptje_nacidos,on='ZONA'))

censo_map2=censo_map.copy()
censo_map2['P09']=censo_map2['P09'].astype(int)

def asignar_rango_etario(edad):
    if edad >= 0 and edad < 5:
        return '[0-4]'
    else:
        return f'[{(edad // 5) * 5}-{((edad // 5) * 5) + 4}]'

censo_map2['rango_etario'] = censo_map2['P09'].apply(lambda edad: asignar_rango_etario(edad))

moda_por_zona = censo_map2.groupby('ZONA')['rango_etario'].apply(lambda x: x.mode().iloc[0]).reset_index()
rang_etario=gpd.GeoDataFrame(pd.merge(eecc_censo,moda_por_zona,on='ZONA'))
filtered_censo_map = censo_map[censo_map['P15A'] == 'Si']

moda_curso_alto=filtered_censo_map.groupby('ZONA')['P15'].apply(lambda x: x.mode().iloc[0]).reset_index()
curso_alto=gpd.GeoDataFrame(pd.merge(eecc_censo,moda_curso_alto,on='ZONA'))

gdf = gpd.read_file('permisos.geojson')
gdf=gdf[gdf['COD_COMUNA']==13106]
gdf['AÑO']=gdf['AÑO'].astype(str)

hab=gdf[gdf['USO_DESTIN']=='HABITACIONAL']
hab['casa']=hab['GLOSA_DEST'].apply(lambda x: 1 if x=='Casa continua' or x=='Casa pareada' else 0)
hab['tipo']=hab['casa'].apply(lambda x: 'Casa' if x==1 else 'Edificio')

evo=hab.groupby('AÑO')['tipo'].value_counts().reset_index(name='Cantidad')

hab_2017=hab[hab['AÑO']=='2017']
prop['ufm2']=prop['uf']/prop['m2_const']
geometry = [Point(xy) for xy in zip(prop['longitud'], prop['latitud'])]

gdf = gpd.GeoDataFrame(prop, geometry=geometry, crs='EPSG:4326')
prop_c=gdf[gdf['d_casa']==1]
prop_e=gdf[gdf['d_casa']==0]
prop_e=prop_e[prop_e['ufm2']<115]

################### CODE #####################################################################################

def main():
    st.title("Estudio Demográfico Estación Central")

    st.markdown("""<div style="text-align: justify;">
    Estación Central es una comuna de Santiago de Chile ubicada en el sector sur poniente de la ciudad y tal como 
    delata su nombre, en ella se encuentra la primera estación de ferrocarriles construida en 1857, que permitió 
    conectar la capital con diferentes puntos del país e impulsó la transformación del barrio en ferroviario y 
    urbano. Actualmente, existen varios centros comerciales, universidades, oficinas, museos y otros puntos de 
    interés ubicados en La Alameda, una de las calles más importantes de la ciudad y, además, cuenta con gran 
    variedad de locomoción colectiva. Esto, hace que la comuna sea atractiva para personas que necesiten vivir 
    cerca de un metro, supermercado, oficinas o universidades, por lo tanto, es de esperarse que cantidad de 
    habitantes en Estación Central se incremente al pasar los años, pues según los datos del INE (Instituto Nacional 
    de Estadística) en el 2017 la población total fue de 147.041 y para fines del 2023 se proyectan 219.897 
    habitantes. Esto, puede influir en el mercado inmobiliario del sector ya que será necesario satisfacer la 
    demanda de hogares con propiedades para los nuevos habitantes y, como cualquier negocio, entender las necesidades 
    de los clientes permite entregar el mejor producto al mejor precio. En este contexto, saber cómo son los habitantes 
    del lugar puede ayudar a las inmobiliarias a tener una idea de cómo serán los nuevos habitantes para comprender 
    el tipo de viviendas que pueden ofrecer y así, sacar un mejor provecho de su presupuesto y obtener mayores utilidades, 
    por ejemplo, si los propietarios llegasen a ser adultos mayores, las viviendas deberían adecuarse a ellos y ser 
    de bajos pisos, con accesos preferenciales (barandas, rampas, etc.), menor proporción de escaleras, entre otros. 
    El objetivo de este reporte es buscar los patrones de quienes viven en Estación Central, así como también 
    analizar el tipo de viviendas (casa o depto) que se ofrecen y su precio para comprender las tendencias del 
    sector. Para eso, se usó la información del Censo de Población y Vivienda del 2017, estudiando, por ejemplo, 
    la edad promedio de los habitantes, su escolaridad, entre otros, además, se utilizaron los datos de permisos 
    de edificación del Servicio de Impuestos Internos (SII) y una base de datos con algunas propiedades en venta 
    del 2022 obtenida a partir de un webscrapping de Portal Inmobiliario para estudiar el mercado inmobiliario.
    </div>""", unsafe_allow_html=True)  

    st.write('---')             

    st.header("Análisis Demográfico")

    st.markdown("""<div style="text-align: justify;">
    Estación Central, es una comuna ubicada cerca del centro de la capital y en el último censo del 2017 se 
    registraron 147.041 habitantes: 73.583 hombres y 73.458 mujeres. Al estudiar sus edades, se obtuvo que a grandes rasgos suelen vivir personas 
    jóvenes en la comuna, con una mayor concentración entre los 20 y 50 años, pero en promedio, 
    tienen entre 34 y 36 años, siendo las mujeres más jóvenes generalmente. 
                    </div>""", unsafe_allow_html=True)

    with st.container():

            censo['Sexo'] = censo['P08'].map({1: 'Mujer', 2: 'Hombre'})
            fig=px.box(censo,'P09',color='Sexo').update_xaxes(title_text='Edad')
            st.plotly_chart(fig)


            st.markdown("""<div style="text-align: justify;">
    Aun así, para comprender mejor las edades, se crearon grupos de rangos etarios con el objetivo de buscar los 
    que más se repiten (moda) por zona censal y se obtuvo que lidera el rango entre 25 y 29 años. Es probable que 
    ellos sean estudiantes o recién egresados, pues la mayoría viven en las zonas más cerca de La Alameda ya que 
    pueden aprovechar los beneficios de la avenida, pero esto será hablado más adelante. Por otro lado, los 
    habitantes entre 50 y 54 años se alejan de este centro ubicándose al sur de la comuna y finalmente el rango 
    60-64 años se encuentran en la avenida principal cerca de Maipú, pero solo en 2 zonas censales lidera este 
    rango de edades.
    </div>""", unsafe_allow_html=True)

            fig, ax = plt.subplots(figsize=(9, 9))
            rang_etario.plot(ax=ax,column='rango_etario',legend=True,alpha=0.5,cmap='RdYlBu')
            eecc.plot(ax=ax,edgecolor='black', facecolor='none',alpha=0.4)
            ax.set_title('Moda Segmento de Edad por Zona Censal')
            cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
            st.pyplot(fig)



            st.markdown("""<div style="text-align: justify;">
   Luego, al notar que en su gran mayoría viven jóvenes, se decidió analizar la migración al lugar calculando el 
    porcentaje de los que nacieron en la comuna versus los que no. Como se puede apreciar en el gráfico, gran parte 
    los habitantes nacieron en una comuna diferente a Estación Central (puede ser Santiago u otra ciudad) lo cual 
    es positivo ya que los nuevos residentes pueden traer nuevas experiencias y culturas al barrio, asi como también 
    nuevos conocimientos para compartir con la comunidad. Además, existe un beneficio económico ya que, al variar 
    la población, la demanda de productos y servicios se incrementa, lo cual estimula la economía local y permite 
    crear nuevas oportunidades laborales.
    </div>""", unsafe_allow_html=True)


    with st.container():
        fig=px.histogram((censo[(censo['P12'] == 'En esta comuna') | (censo['P12'] == 'En otra comuna')]).astype(str),
                'P12',
                title='Porcentaje de Nacimientos en Comuna',
                histnorm='percent').update_yaxes(title_text='Porcentaje (%)').update_xaxes(title_text='Comuna de Nacimiento')
        st.plotly_chart(fig)

        st.markdown("""<div style="text-align: justify;">
    Luego, para estudiar los porcentajes de nacidos en la comuna por zona censal, se crearon 2 grupos para facilitar 
    el análisis: Zonas con más del 50% de habitantes nacidos en la comuna versus zonas con menos del 50% nacido en 
    la comuna. Como se intuyó anteriormente, en las manzanas donde habitan jóvenes corresponden a las que tienen 
    menor cantidad de oriundos de Estación Central.
    </div>""", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(9, 9))

        var_dic={'0':'<50% Nacidos','1':'+50% Nacidos'}
        ptje_nacidos['dummy']=ptje_nacidos['dummy'].map(var_dic)

        ptje_nacidos.plot(ax=ax,column='dummy',legend=True,alpha=0.5,cmap='tab20c')
        eecc.plot(ax=ax,edgecolor='black', facecolor='none',alpha=0.4)
        plt.title('Porcentaje de Nacidos en la Comuna por Zona Censal')
        cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
        st.pyplot(fig)

        with st.container():
            st.markdown("""<div style="text-align: justify;">
    Al comprender que lideran rangos jóvenes en la comuna, se decidió analizar los universitarios del lugar, tomando 
    como supuesto que quienes tienen más de 12 años de escolaridad se encuentran desarrollando (o ya terminaron) su 
    carrera profesional/técnica. En el mapa, se puede apreciar que los mayores porcentajes (azules más oscuros) se 
    encuentran en la zona cercana a La Alameda coincidiendo espacialmente con los rangos etarios más jóvenes y nacidos 
    en otra comuna, por lo tanto, es de esperarse que cerca a esta calle vivan personas que están estudiando o 
    egresaron. Por otra parte, los que tienen menor porcentaje de educación se alejan de esta avenida principal, 
    agrupándose en la zona sur de la comuna. Esto, deja en evidencia que los habitantes con similitudes educacionales 
    tienden a agruparse lo cual puede ser beneficioso para ellos ya que el vivir cerca puede facilitar las juntas 
    de estudio, juntas recreacionales, entre otros.
    </div>""", unsafe_allow_html=True)


            fig, ax = plt.subplots(figsize=(9, 9))
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="3%", pad=0.2)
            ptje_univ_map.plot(ax=ax,column='Universitarios',legend=True,cax=cax,alpha=0.5,cmap='Blues')
            eecc.plot(ax=ax,edgecolor='black', facecolor='none',alpha=0.4)
            ax.set_title('Porcentaje de Universitarios por Zona Censal')
            cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
            st.pyplot(fig)

        

        with st.container():  
            st.markdown("""<div style="text-align: justify;">
    Teniendo en cuenta lo anterior ¿cuántos de estos universitarios son jefes/as de hogar? Ocurre que cerca de las 
    estaciones de metro (representadas con rojo) se encuentran porcentajes más altos de jefes/as de hogar universitarios 
    y en el resto de la comuna se nota una menor proporción. Nuevamente, los mayores porcentajes coinciden con los 
    segmentos jóvenes, lo que permite intuir que en el sector viven estudiantes que son de otras ciudades que eligen 
    vivir en el centro de la ciudad para tener mejor conectividad y acceso a comercio, casas de estudio, entre otros.
    </div>""", unsafe_allow_html=True)


            dic('P07',dic_P07)
            
            q="""
            SELECT P07, 
            ZONA,
            COUNT(P07) AS cant_jef
            FROM censo
            WHERE P07 IN ('Jefe/a de hogar') 
            AND ESCOLARIDAD > 12
            GROUP BY P07,ZONA
            ORDER BY cant_jef DESC
            """
            tabla2=sqldf(q,globals())
            tabla2['P07']=tabla2['P07'].astype(str)
            tabla2['Porcentaje']=round(100*tabla2['cant_jef']/tabla2.cant_jef.sum(),2)
            tabla2=gpd.GeoDataFrame(pd.merge(eecc_censo,tabla2,on='ZONA'))

            fig,ax=plt.subplots(figsize=(9,9))
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.2)
            tabla2.plot(ax=ax,column='Porcentaje',legend=True,cax=cax,cmap='Blues',alpha=0.7)
            metro1.plot(ax=ax,color='red',marker='o',label='Metro')
            eecc.plot(ax=ax, edgecolor='black',facecolor='none',alpha=0.4)
            ax.set_title('Porcentaje de Jefe/as de Hogar por Zona Censal Con más de 12 años de Estudios')
            cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
            st.pyplot(fig)

        st.markdown("""<div style="text-align: justify;">
        Como conclusión en este análisis demográfico, se puede decir que las personas que viven en Estación Central 
        suelen ser jóvenes y en su gran mayoría han nacido fuera de la comuna. Por eso, se analizó el nivel de estudios 
        de los habitantes ya que al saber que muchos son originarios de otras comunas, probablemente estén viviendo en 
        este sector para aprovechar las conectividades y puntos de interés en el sector y como resultado, se obtuvo que 
        la mayoría que vive cerca a La Alameda suelen tener más de 12 años de estudio y también, se encuentra el mayor 
        porcentaje de jefes/as de hogar universitarios lo cual permite pensar que son estudiantes que vienen de otras 
        ciudades del país ya que en Santiago hay gran variedad de universidades y también están las mejores del país 
        (u de chile, u católica).
        </div>""", unsafe_allow_html=True)

        st.write('---')

        st.header("Análisis Urbano")

        st.markdown("""<div style="text-align: justify;">
        En el aspecto urbano, Estación Central ha sido reconocida controversialmente por sus “mega construcciones”, 
        pues existen edificios hasta con 30 pisos de altura, pero ¿por qué sucede en este lugar? Tal como se mencionó 
        en párrafos anteriores, los residentes de la comuna suelen ser jóvenes/adultos y, al analizar patrones por zona 
        censal, los de menor edad se agrupan con mayor cercanía a La Alameda, mientras que los adultos suelen alejarse 
        de esta, un fenómeno parecido ocurre al estudiar las ubicaciones de quienes tienen más de 12 años de educación 
        versus los que no. Todo esto lleva 
        a pensar que los habitantes se agrupan de acuerdo con sus necesidades y estilo de vida y por eso los estudiantes jóvenes aprovechan la 
        buena conectividad de la comuna para cumplir con sus deberes estudiantiles. A esto también se le suma el hecho 
        de que en la avenida se encuentran diversos comercios y, además, el terminal de buses, pues recordando puntos 
        anteriores, gran parte de la comuna nació en otra, por ende, es probable que estos estudiantes sean de otras 
        regiones y tener cercanía con el terminal es un gran punto a favor.
        </div>""", unsafe_allow_html=True)

        fig = px.bar(evo,'AÑO','Cantidad',color='tipo',barmode='group',title='Evolución Permisos de Edificación')
        st.plotly_chart(fig)

        st.markdown("""<div style="text-align: justify;">
    Para estudiar el mercado inmobiliario de la zona, se estudiaron los permisos de edificación otorgados a 
    inmobiliarias en la comuna desde el año 2010 hasta 2018 así como también las ofertas de venta de propiedades en la zona durante. 
    En primer lugar, se destaca un alto numero de permisos para construir edificios en el primer año mencionado, 
    disminuyendo drásticamente al año siguiente. Luego, se nota un alza para ambos casos desde el 2013 hasta 2016 para  
    posteriormente disminuir la cantidad de permisos dados. En este mercado, destaca principalmente la construcción de 
    edificios por sobre casas. Ahora, si se observan los datos plasmados en la comuna, se aprecia que en los sectores 
    cercanos a las líneas del metro se encuentra una mayor concentración de edificios, mientras que las casas están 
    más alejadas, especialmente en la zona sur de la comuna. Una principal razón para esto es que mientras más se 
    aleja una propiedad de las oportunidades de conectividad y comercio que ofrece la comuna (ejemplo: metro, comercio, 
    terminal), más barato es el precio del metro cuadrado, pues estudios espaciales han demostrado que el tener mayor 
    cercanía al centro puede influir en el precio de una propiedad ya que se está más cerca de las casas de estudios, 
    oficinas de trabajo, supermercado, entre otros, por tanto, no se pierde tanto tiempo de viaje para realizar 
    actividades cotidianas. Esto, provoca que las personas en términos generales deseen vivir en estos lugares, 
    por ende, la oferta debe ajustarse a la demanda y se esperan precios más caros por metro cuadrado. Por el contrario, 
    quienes habitan lejos del centro pueden acceder a pisos más grandes por un precio menor, pero renunciando a 
    la oportunidad de acceder más rápidos a los servicios de la comuna.
        </div>""", unsafe_allow_html=True)


        fig,ax=plt.subplots(figsize=(9,9))

        hab.plot(ax=ax,column="tipo",legend=True,cmap='tab20',alpha=0.8)
        metro1.plot(ax=ax,color='red',marker='o',label='Metro')
        eecc.plot(ax=ax,edgecolor='black',facecolor='none',alpha=0.4)

        plt.title('Permisos de Edificación [2010-2018]')

        cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
        st.pyplot(fig)

        st.markdown("""<div style="text-align: justify;">
        Por otro lado, se estudió la oferta de propiedades en venta del año 2022 en la comuna, la cual se obtuvo a 
        partir de un webscrapping de Portal Inmobiliario. Para esto, se analizaron los valores en UF/m2 por tipo de 
        vivienda para realizar una comparación más homogénea. En primer lugar, al estudiar el mercado de las casas, 
        estas se encuentran dispersas a lo largo de la comuna y los índices UF/m2 son más bajos a medida que se 
        alejan de La Alameda, es decir, mientras más distante de la arteria principal se encuentre la casa en venta, 
        más barato cuesta el metro cuadrado y uno de los factores que provoca esto es que la vivienda se aleja de 
        los principales puntos de la comuna entonces quienes deseen ir por ejemplo a un gran supermercado, deberán 
        “viajar” a otro punto de la comuna. 
        </div>""", unsafe_allow_html=True)


        fig,ax=plt.subplots(figsize=(9,9))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.2)

        prop_c.plot(ax=ax,column="ufm2",legend=True,alpha=0.8,cax=cax)

        eecc.plot(ax=ax,edgecolor='black',facecolor='none',alpha=0.4)

        ax.set_title('Precio UF/m2 - Casas')

        cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
        st.pyplot(fig)

        st.markdown("""<div style="text-align: justify;">
        Pero con los departamentos ocurre otro fenómeno, pues la gran mayoría está concentrada en las zonas cercanas 
        a las estaciones de metro y presentan altos índices de UF/m2, mientras que los más distantes al metro, que 
        son muy pocos, presentan valores más bajos. Esto, se puede explicar (en parte) gracias a las características 
        de los lugareños, pues recordando todo lo expuesto en este informe, gran parte de la población de Estación 
        Central son jóvenes estudiantes oriundos de otras comunas, y para ellos vivir cerca de La Alameda, estaciones 
        de metros (línea 1), facultades de diferentes universidades, comercio, entre otros, puede tener una correlación 
        positiva con sus necesidades como estudiantes ¿por qué? Porque Santiago es una ciudad de grandes distancias, y, 
        por ejemplo, vivir en Peñalolén y estudiar en Estación Central implica varios minutos de viaje y esto puede ser 
        común para quienes llevan años en la capital, pero generalmente no suele ocurrir en otras ciudades, por tanto, 
        vivir cerca del metro o de la universidad u otro permite ahorrar gran tiempo de viaje a la persona. A causa de 
        lo anterior, es probable que la demanda de viviendas cercanas al metro en Estación Central sea alta 
        y las casas no permiten satisfacer completamente la demanda ya que la cantidad total de personas que pueden 
        habitar en ellas es menor que las de un edificio entero, por tanto, ofrecer departamentos pareciera ser una 
        solución para satisfacer gran parte de la demanda. Es importante dejar en claro que esta es una de las muchas 
        razones que pueden influir en la oferta y demanda de propiedades.
        </div>""", unsafe_allow_html=True)


        fig,ax=plt.subplots(figsize=(9,9))
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.2)

        prop_e.plot(ax=ax,column="ufm2",legend=True,alpha=0.8,cax=cax)

        #metro1.plot(ax=ax,color='red',marker='o',label='Metro')
        eecc.plot(ax=ax,edgecolor='black',facecolor='none',alpha=0.4)

        ax.set_title('Precio UF/m2 - Edificios')

        cx.add_basemap(ax, crs=eecc.crs.to_string(),source=cx.providers.CartoDB.Voyager)
        st.pyplot(fig)
    
    st.markdown("""<div style="text-align: justify;">
    Como conclusión de este punto, es notable que los departamentos suelen ser más comunes en Estación Central ya 
    que al tener habitantes jóvenes universitarios en su mayoría, da a pensar que ellos se encuentran en el sector 
    “de paso”, ósea, hay una probabilidad de que cuando terminen sus estudios vuelvan a sus hogares en otras ciudades. 
    Pero también, existe la probabilidad de que ellos mismos comiencen una nueva etapa de su vida en la capital luego 
    de terminar sus estudios y seguir prefiriendo el sector por su conectividad y demás comodidades y, las propiedades 
    que satisfacen esto, son las que se encuentran en La Alameda y su alrededor. Aun así, en el sector se nota la 
    alta oferta de propiedades a diferencia de otros lugares de la comuna, por lo tanto, construir nuevas viviendas 
    habitacionales cerca de la avenida principal no pareciera ser atractivo y sería interesante para las inmobiliarias 
    buscar otro tipo de construcciones que pueden aportar a los jóvenes universitarios, por ejemplo, centros de 
    estudio, locales con intenciones recreativas, librerías, entre otros. Por otro lado, es importante aclarar que 
    lo expuesto en este reporte no es algo definitivo y faltan otros factores que influyen en esto, como la densidad de 
    habitantes, estudio de metros cuadrados de las propiedades, estudio de comercio, entre otros que permiten tomar 
    las mejores decisiones.
    </div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()