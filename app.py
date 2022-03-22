from flask import Flask, render_template, request
from rdflib import Graph
from main import create_and_populate_graph
from queries import city_list, descript, make_query_1, make_query_2, make_query_3, make_query_4, make_query_5, \
    make_query_6, make_query_7, make_query_8, make_query_9, make_query_10, make_query_11, make_query_12
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "A dimension is an integer."


@app.route('/', methods=['GET', 'POST'])
def home_app():
    g = create_and_populate_graph()

    cities = city_list(g)  # creating a list of every city in our graph
    queries = descript.copy()  # stocking a copy of our list to modify it

    # We don't use the query 12 (pos 11) because it's a DESCRIPTION query, and DESCRIPTION is not implemented in rdflib.
    queries.pop(11)

    return render_template('/home.html', cities=cities, queries=queries)


@app.route("/query/", methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        # getting our parameters from the home page
        result = request.form
        query_selected = result['query-select']
        city = result['city-select']
        city2 = result['city-select-2']
        i = descript.index(query_selected) + 1  # setting the number of the chosen query

        g = Graph()
        g.parse('serialized.ttl')  # creating a graph with data to launch the chosen query
        df, desc = globals()[f'make_query_{i}'](g, city, city2)  # launching the query
        columns = df.columns.tolist()  # getting the columns of our result
        results = df.values.tolist()  # getting the rows of our result

        return render_template('query.html', columns=columns, results=results, desc=desc)


if __name__ == '__main__':
    app.run()
