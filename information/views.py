from django.shortcuts import render
import pandas as pd


def index(request):
    confirmed_global = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    total_count = confirmed_global[confirmed_global.columns[-1]].sum()
    bar_plot_data = confirmed_global[['Country/Region', confirmed_global.columns[-1]]].groupby('Country/Region').sum()
    bar_plot_data = bar_plot_data.reset_index()
    bar_plot_data.columns = ['Country/Region', 'Value']
    bar_plot_data = bar_plot_data.sort_values(by='Value', ascending=False)
    country_names = bar_plot_data['Country/Region'].tolist()
    bar_plot_values = bar_plot_data['Value'].tolist()

    unique_country_names = pd.unique(confirmed_global['Country/Region'])
    data_for_map = get_map_data(bar_plot_data, unique_country_names)

    context = {'total_count': total_count, 'country_names': country_names, 'bar_plot_values': bar_plot_values,
               'data_for_map': data_for_map}
    return render(request, 'index.html', context)


def get_map_data(bar_plot_data, unique_country_names):
    map_data_format = pd.read_json(
        'https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
    data_for_map = []
    for i in unique_country_names:
        try:
            temp_df = map_data_format[map_data_format['name'] == i]
            temp = {'code3': list(temp_df['code3'].values)[0], 'name': i,
                    'value': bar_plot_data[bar_plot_data['Country/Region'] == i]['Value'].sum(),
                    'code': list(temp_df['code'].values)[0]}
            data_for_map.append(temp)
        except:
            pass
    data_for_map.append({'code3': 'USA', 'name': 'United States',
                         'value': bar_plot_data[bar_plot_data['Country/Region'] == 'US']['Value'].sum(),
                         'code': 'US'})
    data_for_map.append({'code3': 'RUS', 'name': 'Russian Federation',
                         'value': bar_plot_data[bar_plot_data['Country/Region'] == 'Russia']['Value'].sum(),
                         'code': 'RU'})
    return data_for_map


def select_country(request):
    # data for the bar chart
    confirmed_global = pd.read_csv(
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    total_count = confirmed_global[confirmed_global.columns[-1]].sum()
    bar_plot_data = confirmed_global[['Country/Region', confirmed_global.columns[-1]]].groupby('Country/Region').sum()
    bar_plot_data = bar_plot_data.reset_index()
    bar_plot_data.columns = ['Country/Region', 'Value']
    bar_plot_data = bar_plot_data.sort_values(by='Value', ascending=False)
    country_names = bar_plot_data['Country/Region'].tolist()
    bar_plot_values = bar_plot_data['Value'].tolist()

    # data for the specific country
    specific_country = request.POST.get('country')
    if specific_country == 'UK':
        specific_country = 'United Kingdom'
    country_data = pd.DataFrame(confirmed_global[confirmed_global['Country/Region'] == specific_country][
                                    confirmed_global.columns[4:-1]].sum()).reset_index()
    country_data.columns = ['date', 'value']
    country_data['lagVal'] = country_data['value'].shift(1).fillna(0)
    country_data['incrementVal'] = country_data['value'] - country_data['lagVal']
    country_data['rollingMean'] = country_data['incrementVal'].rolling(window=4).mean()
    country_data = country_data.fillna(0)
    data_for_line = [
        {'label': 'Daily Cumulated Cases', 'data': country_data['value'].values.tolist(),
         'borderColor': 'rgb(127,0,255)', 'backgroundColor': 'rgb(127,0,255)', 'fill': 'false'},
        {'label': '4-day Rolling Mean of Increasing Cases', 'data': country_data['rollingMean'].values.tolist(),
         'borderColor': 'rgb(51,255,255)', 'backgroundColor': 'rgb(51,255,255)', 'fill': 'false'}]
    axis_values = country_data['date'].tolist()

    context = {'total_count': total_count, 'country_names': country_names,
               'bar_plot_values': bar_plot_values, 'specific_country': specific_country,
               'data_for_line': data_for_line, 'axis_values': axis_values}
    return render(request, 'index2.html', context)
