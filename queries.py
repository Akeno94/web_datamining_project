import pandas as pd

# a description of every query
descript = [
    'List the instances of the museum',
    'List the instances of the train_station',
    'List the instances of the bike_station',
    'List the name of all train station. For each one, display its city',
    'List the name of stations in {city}',
    'List the name of bike station that have 30 or more bikes available',
    '''list of every museum name and city, the url to their website if they have one, and the train_station in the same city if exists.''',
    'List of bike and train stations in {city}',
    'Construction of codeDep',
    'Is there a museum in the city of {city}',
    'List of the 5 paths that make the least distance between {city} and {city2} (difference latitude & longitude)',
    'Description of the museum in the city of {city}'
]


def city_list(gr):  # a query to get every city in the graph
    query_city = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>
    
    SELECT distinct ?city
    WHERE {
      ?obj ns:city ?city .
    }'''
    lst = []
    query_result = gr.query(query_city)  # execute the query
    for row in query_result:
        lst.append(row.city)  # adding cities to the list
    return lst


def make_query_1(gr, *params):
    desc = descript[0]  # getting the description of the query
    query_1 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?museum
WHERE {
  ?museum rdf:type ns:Museum .
}'''
    query_result = gr.query(query_1)  # execute the query
    df = pd.DataFrame(columns=['museum'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'museum': row.museum},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


def make_query_2(gr, *params):
    desc = descript[1]  # getting the description of the query
    query_2 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?train
WHERE {
  ?train rdf:type ns:Train_station .
}'''
    query_result = gr.query(query_2)  # execute the query
    df = pd.DataFrame(columns=['train'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'train': row.train},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


def make_query_3(gr, *params):
    desc = descript[2]  # getting the description of the query
    query_3 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?bike
WHERE {
  ?bike rdf:type ns:Bike_station .
}'''
    query_result = gr.query(query_3)  # execute the query
    df = pd.DataFrame(columns=['bike'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'bike': row.bike},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


def make_query_4(gr, *params):
    desc = descript[3]  # getting the description of the query
    query_4 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>
    
    SELECT ?name ?city
    WHERE {
      ?train rdf:type ns:Train_station .
      ?train ns:name ?name .
      ?train ns:city ?city .
    }'''
    query_result = gr.query(query_4)  # execute the query
    df = pd.DataFrame(columns=['name', 'city'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'name': row.name, 'city': row.city},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


def make_query_5(gr, *params):
    city = params[0]  # getting the city to use it in the query
    desc = descript[4].format(city=city)  # getting the description of the query
    query_5 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>
    
    SELECT ?object ?station ?name
    WHERE {
      ?object rdfs:subClassOf ns:Station .
      ?station rdf:type ?object .
      ?station ns:name ?name .
      ?station ns:city \'''' + city + '''\' .
    }'''
    query_result = gr.query(query_5)  # execute the query
    df = pd.DataFrame(columns=['class', 'station', 'name'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'class': row.object, 'station': row.station, 'name': row.name},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


def make_query_6(gr, *params):
    desc = descript[5]  # getting the description of the query
    query_6 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?name ?city ?nb
WHERE {
  ?bike rdf:type ns:Bike_station .
  ?bike ns:name ?name .
  ?bike ns:city ?city .
  ?bike ns:available_bike ?nb .
  FILTER (?nb >= 30) .
}'''
    query_result = gr.query(query_6)  # execute the query
    df = pd.DataFrame(columns=['name', 'city', 'nb'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'name': row.name, 'city': row.city, 'nb': row.nb},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# A query that contains at least 2 Optional Graph Patterns
def make_query_7(gr, *params):
    desc = descript[6]  # getting the description of the query
    query_7 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?name ?city ?url ?name_train
WHERE {
  ?museum rdf:type ns:Museum .
  ?museum ns:name ?name .
  ?museum ns:city ?city .
  OPTIONAL {?museum ns:url ?url }
  OPTIONAL {
    ?train ns:city ?city .
    ?train rdf:type ns:Train_station . 
	?train ns:name ?name_train
  }
}'''
    query_result = gr.query(query_7)  # execute the query
    df = pd.DataFrame(columns=['name', 'city', 'url', 'name_train'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'name': row.name, 'city': row.city, 'url': row.url, 'name_train': row.name_train},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# A query that contains at least 2 alternatives and conjunctions
def make_query_8(gr, *params):
    city = params[0]  # getting the city to use it in the query
    desc = descript[7].format(city=city)  # getting the description of the query
    query_8 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?name_train ?name_bike
WHERE {
  {
    ?train rdf:type ns:Train_station .
    ?train ns:city \'''' + city + '''\' .
    ?train ns:name ?name_train .
  }
  union
  {
    ?bike rdf:type ns:Bike_station .
    ?bike ns:city \'''' + city + '''\' .
    ?bike ns:name ?name_bike .
  }
}'''
    query_result = gr.query(query_8)  # execute the query
    df = pd.DataFrame(columns=['name_train', 'name_bike'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'name_train': row.name_train, 'name_bike': row.name_bike},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# A query that contains a CONSTRUCT query form
def make_query_9(gr, *params):
    desc = descript[8]  # getting the description of the query
    query_9 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

CONSTRUCT {?obj ns:codeDep ?postal_code}
WHERE {
  ?obj ns:postal_code ?postal_code .
}'''
    query_result = gr.query(query_9)  # execute the query
    df = pd.DataFrame(columns=['subject', 'predicate', 'object'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'subject': row[0], 'predicate': row[1], 'object': row[2]},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# A query that contains an ASK query form
def make_query_10(gr, *params):
    city = params[0]  # getting the city to use it in the query
    desc = descript[9].format(city=city)  # getting the description of the query
    query_10 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

ASK {
  ?museum rdf:type ns:Museum .
  ?museum ns:city \'''' + city + '''\' .
}'''
    query_result = gr.query(query_10)  # execute the query
    df = pd.DataFrame(columns=['bool'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'bool': row},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# Trip query
def make_query_11(gr, *params):
    city = params[0]  # getting the city to use it in the query
    city2 = params[1]  # getting the second city to use it in the query
    desc = descript[10].format(city=city, city2=city2)  # getting the description of the query
    query_bonus = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

SELECT ?object ?name_origin ?name_destination
WHERE {
  	?object rdfs:subClassOf ns:Station .
  
    ?origin rdf:type ?object .
    ?origin ns:city \'''' + city + '''\' .
    ?origin ns:name ?name_origin .
    ?origin ns:latitude ?lat_origin .
    ?origin ns:longitude ?long_origin .

    ?destination rdf:type ?object .
    ?destination ns:city \'''' + city2 + '''\' .
    ?destination ns:name ?name_destination .
    ?destination ns:latitude ?lat_destination .
    ?destination ns:longitude ?long_destination .
} ORDER BY ABS((?lat_origin-?lat_destination) + (?long_origin-?long_destination))
LIMIT 5'''
    query_result = gr.query(query_bonus)  # execute the query
    df = pd.DataFrame(columns=['class', 'name_origin', 'name_destination'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'class': row.object, 'name_origin': row.name_origin, 'name_destination': row.name_destination},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc


# A query that contains a DESCRIBE query for
def make_query_12(gr, *params):
    city = params[0]  # getting the city to use it in the query
    desc = descript[11].format(city=city)  # getting the description of the query
    query_11 = '''PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns: <http://www.semanticweb.org/kevin/ontologies/2022/2/untitled-ontology-49#>

DESCRIBE ?museum
WHERE {
  ?museum rdf:type ns:Museum .
  ?museum ns:city \'''' + city + '''\' .
}'''
    query_result = gr.query(query_11)  # execute the query
    df = pd.DataFrame(columns=['subject', 'predicate', 'object'])  # creating the dataframe to stock result
    for row in query_result:
        df = df.append({'subject': row.subject, 'predicate': row.predicate, 'object': row.object},
                       ignore_index=True)  # adding rows to the dataframe
    return df, desc
