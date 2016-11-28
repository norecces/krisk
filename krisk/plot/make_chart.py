from copy import deepcopy
from krisk.chart.api import Chart


def round_list(arr):
    try:
        return arr.values.round(3).tolist()  # Numeric Array
    except TypeError:
        try:
            return arr.tolist()  #String Array
        except AttributeError:
            return (arr.apply(lambda x: x.values.round(3)  #Dataframe
                              if x.dtype.name.startswith('float') else x)
                    .values.tolist())


def insert_series_data(data, x, chart_type, chart, cat=None):
    elem_series = {'name': '', 'type': chart_type, 'data': []}
    series = deepcopy(elem_series)
    series['data'] = round_list(data)
    series['type'] = chart_type

    if cat:
        series['name'] = cat
        chart.option['legend']['data'].append(str(cat))
    else:
        series['name'] = x

    chart.option['series'].append(series)

    return series


def make_chart(df, **kwargs):

    from krisk.plot.make_bar_line import (set_bar_line_chart,
                                          set_barline,
                                          set_waterfall)
    from krisk.plot.make_scatter_geo import set_scatter_chart

    chart = Chart(**kwargs)

    if kwargs['type'] not in ['waterfall']:
        chart.kwargs['data_columns'] = df.columns
        chart.set_xlabel(kwargs['x'])

    if kwargs.get('y', None):
        chart.set_ylabel(kwargs['y'])

    if kwargs['type'] == 'line':
        chart.set_tooltip_style(trigger='axis', axis_pointer='shadow')
    if kwargs['type'] in ['bar', 'line', 'hist']:
        set_bar_line_chart(chart, df, **kwargs)
    elif kwargs['type'] == 'bar_line':
        set_barline(chart, df, **kwargs)
    elif kwargs['type'] == 'waterfall':
        set_waterfall(chart, df,   **kwargs)
    elif kwargs['type'] == 'scatter':
        set_scatter_chart(chart, df, **kwargs)

    return chart