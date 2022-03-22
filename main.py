import pandas as pd
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, XSD
from data import museum_link, museum_columns, train_station_link, train_station_columns, bike_station_link, \
    bike_station_columns, ontology
from queries import make_query_1, make_query_2, make_query_3, make_query_4, make_query_5, make_query_6, make_query_7, \
    make_query_8, make_query_9, make_query_10, make_query_11, make_query_12
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def prepare_df(df, col_dict):
    cols = list(col_dict.keys())
    new_df = df[cols]  # we're only taking the necessary columns for our dataframe
    new_df = new_df.rename(columns=col_dict)  # and rename with our wanted names (in the data.py file)
    new_df = new_df.dropna(subset=['id'])  # dropping the rows without id
    new_df = new_df.reset_index().drop('index', axis=1)  # reset indexes of rows after removing rows
    if 'coordinates' in new_df.columns:  # if our dataset contains coordinates column instead of latitude and longitude
        new_df[['latitude', 'longitude']] = new_df.coordinates.str.split(",", expand=True)  # creating columns
        new_df['latitude'] = new_df['latitude'].astype(float)
        new_df['longitude'] = new_df['longitude'].astype(float)
        new_df.drop('coordinates', inplace=True, axis=1)  # dropping the previous coordinates column
    new_df['id'] = new_df['id'].astype(str)

    if 'postal_code' in new_df.columns:  # using the str format for postal_code because of postal_code starting by 0
        new_df['postal_code'] = new_df['postal_code'].fillna(0)
        new_df['postal_code'] = new_df['postal_code'].astype(int).astype(str)
        new_df['postal_code'] = new_df['postal_code'].apply(lambda x: '0' * (5 - len(x)) + x if len(x) < 5 else x)
    return new_df


def populate_museum(gr, df, namespace):
    for i in range(len(df)):  # for each row of our dataset
        name = 'Museum_' + df.loc[i, 'id']  # creating an object name
        population = URIRef(namespace + name)  # creating our object id for our graph
        # adding every information in our graph
        gr.add((population, RDF.type, namespace.Museum))
        gr.add((population, namespace.id, Literal(df.loc[i, 'id'])))
        gr.add((population, namespace.region, Literal(df.loc[i, 'region'])))
        gr.add((population, namespace.city, Literal(df.loc[i, 'city'])))
        gr.add((population, namespace.name, Literal(df.loc[i, 'name'])))
        gr.add((population, namespace.address, Literal(df.loc[i, 'address'])))
        gr.add((population, namespace.postal_code, Literal(df.loc[i, 'postal_code'])))
        gr.add((population, namespace.url, Literal(df.loc[i, 'url'])))
        gr.add((population, namespace.latitude, Literal(df.loc[i, 'latitude'])))
        gr.add((population, namespace.longitude, Literal(df.loc[i, 'longitude'])))


def populate_train_station(gr, df, namespace):
    for i in range(len(df)):  # for each row of our dataset
        name = 'Train_station_' + df.loc[i, 'id']  # creating an object name
        population = URIRef(namespace + name)  # creating our object id for our graph
        # adding every information in our graph
        gr.add((population, RDF.type, namespace.Train_station))
        gr.add((population, namespace.id, Literal(df.loc[i, 'id'])))
        gr.add((population, namespace.name, Literal(df.loc[i, 'name'])))
        gr.add((population, namespace.postal_code, Literal(df.loc[i, 'postal_code'])))
        gr.add((population, namespace.city, Literal(df.loc[i, 'city'])))
        gr.add((population, namespace.department, Literal(df.loc[i, 'department'])))
        gr.add((population, namespace.longitude, Literal(df.loc[i, 'longitude'])))
        gr.add((population, namespace.latitude, Literal(df.loc[i, 'latitude'])))
        gr.add((population, namespace.region, Literal(df.loc[i, 'region'])))


def populate_bike_station(gr, df, namespace):
    for i in range(len(df)):  # for each row of our dataset
        name = 'Bike_station_' + df.loc[i, 'id']  # creating an object name
        population = URIRef(namespace + name)  # creating our object id for our graph
        # adding every information in our graph
        gr.add((population, RDF.type, namespace.Bike_station))
        gr.add((population, namespace.id, Literal(df.loc[i, 'id'])))
        gr.add((population, namespace.name, Literal(df.loc[i, 'name'])))
        gr.add((population, namespace.station_capacity, Literal(df.loc[i, 'station_capacity'], datatype=XSD.integer)))
        gr.add((population, namespace.free_block, Literal(df.loc[i, 'free_block'], datatype=XSD.integer)))
        gr.add((population, namespace.available_bike, Literal(df.loc[i, 'available_bike'], datatype=XSD.integer)))
        gr.add((population, namespace.mechanical_bike, Literal(df.loc[i, 'mechanical_bike'], datatype=XSD.integer)))
        gr.add((population, namespace.electric_bike, Literal(df.loc[i, 'electric_bike'], datatype=XSD.integer)))
        gr.add((population, namespace.return_bike, Literal(df.loc[i, 'return_bike'])))
        gr.add((population, namespace.city, Literal(df.loc[i, 'city'])))
        gr.add((population, namespace.latitude, Literal(df.loc[i, 'latitude'])))
        gr.add((population, namespace.longitude, Literal(df.loc[i, 'longitude'])))


def serialize_graph(gr, file_name):
    gr.serialize(destination=file_name)  # serialize our graph into a file


def create_and_populate_graph():
    print('importing dataset')
    # read our online files
    train_station = pd.read_csv(train_station_link, sep=';')
    bike_station = pd.read_csv(bike_station_link, sep=";")
    museum = pd.read_excel(museum_link, engine='openpyxl')

    # prepare our dataframe before inserting data into our graph
    train_station = prepare_df(train_station, train_station_columns)
    bike_station = prepare_df(bike_station, bike_station_columns)
    museum = prepare_df(museum, museum_columns)

    ns = Namespace(ontology)  # set our namespace
    gr = Graph()  # create our graph
    gr.parse('project.owl')  # loading our protege ontology

    print('populating the graph')
    # populate our graph with data from our previously created dataframe
    populate_train_station(gr, train_station, ns)
    populate_bike_station(gr, bike_station, ns)
    populate_museum(gr, museum, ns)

    print('serializing the graph')
    # save our graph into a turtle file
    serialize_graph(gr, 'serialized.ttl')

    return gr


if __name__ == '__main__':
    g = create_and_populate_graph()

    # set variable for queries
    city = 'Paris'
    city2 = 'Meudon'
    print('making queries')
    print(make_query_1(g))
    # print(make_query_2(g))
    # print(make_query_3(g))
    # print(make_query_4(g))
    # print(make_query_5(g, city))
    # print(make_query_6(g))
    # print(make_query_7(g))
    # print(make_query_8(g, city))
    # print(make_query_9(g))
    # print(make_query_10(g, city))
    # print(make_query_11(g, city, city2))
    # print(make_query_12(g, city))  # DESCRIBE not implemented
