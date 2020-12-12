import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.colors
import requests

country_dict = dict([('Turkey', 'TUR'), ('United States', 'USA'),
   ('Greece', 'GRC'), ('Italia', 'ITA'), ('China', 'CHN')])


def return_figures(countries=country_dict):

    if not bool(countries):
        countries = country_dict

    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    indicators = ['AG.LND.AGRI.ZS']  # Children out of school female and GDP

    dfs = []
    urls = []

    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/' + country_filter + \
              '/indicators/' + indicator + '?date=1990:2019&per_page=1000&format=json'
        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()[1]  # 0 Have metadata

        except:
            print('Failed to load data')

        for value in data:
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        dfs.append(data)

    # Graph One
    graph_one = []

    df_one = pd.DataFrame(dfs[0])

    df_one = df_one[(df_one['date'] >= '1990') & (df_one['date'] <= '2016')]
    df_one.sort_values(['date','value'], ascending=False, inplace=True)

    countries = df_one.country.unique().tolist()

    for country in countries:
        x_val = df_one[df_one['country'] == country].date.tolist()
        y_val = df_one[df_one['country'] == country].value.tolist()

        graph_one.append(

            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_one = dict(title='Agricultural land (% of land area) <br> 1990 to 2016',
                      xaxis=dict(title='Year',
                                 autotick= True, tick0=1990,dtick1=2016),
                      yaxis=dict(title='% of land area'),
                      )

    graph_two = []

    df_one = df_one[df_one['date'] == '2016']

    graph_two.append(
        go.Bar(
            x=df_one.country.tolist(),
            y=df_one.value.tolist(),
        )
    )

    layout_two = dict(title='Agricultural land (% of land area) <br> 2016',
                      xaxis=dict(title='Country'),
                      yaxis=dict(title='% of land area'),
                      )

    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))

    return figures