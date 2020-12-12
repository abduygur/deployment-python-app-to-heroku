from worldbankapp import app
import json
import plotly
from flask import render_template, request
from scripts.data_process import return_figures


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():

    country_codes = [['Turkey', 'TUR'], ['United States', 'USA'],
                         ['Greece', 'GRC'], ['Italia', 'ITA'],['China','CHN']]

    if (request.method == 'POST') and request.form:
        figures = return_figures(request.form)
        countries_selected = []

        for country in request.form.lists():
            countries_selected.append(country[1][0])


    else:
        figures = return_figures()
        countries_selected = []
        for country in country_codes:
            countries_selected.append(country[1])

    ids = ["figure {}".format(i) for i, _ in enumerate(figures)]

    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', ids=ids,
                           figuresJSON=figuresJSON,
                           all_countries=country_codes,
                           countries_selected=countries_selected)

