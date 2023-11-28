from types import NoneType
from pandas import DataFrame, Series
from lightweight_charts import Chart


# TODO: I need to re-think if I can overlay multiple histograms pet subchart. Assuming no for now

# TODO: I would like to use histograms for rendering equity curves and indicator histograms
#  but tradingview lightweight chart does not support y-axis labels for histograms so I can't use this method
#  Overlaying a transparent line-overlay with a histogram with same value does not return desired result (charts are offset)
#  https://github.com/louisnw01/lightweight-charts-python/issues/124

def add_histogram(chart: Chart, data, label: str | None = None, color='#2596be', price_line: bool = False,
                  price_label: bool = False):

    if data.empty:
        return

    if isinstance(data, Series):
        data = data.to_frame()

    if len(data.columns) == 1:
        if isinstance(label, NoneType):
            rename_label = data.columns[0]
        else:
            rename_label = label
        data.columns = [rename_label]
        data['color'] = color

    elif len(data.columns) == 2 and 'color' in data.columns:
        rename_label = label
        label = set(data.columns) - set(['color'])
        label = list(label)[0]

        if not rename_label:
            rename_label = label

        data = data.rename(columns={label: rename_label})

    else:
        raise Exception('Histogram only accepts one value; and optional column color')

    # The expected behavior was that the y-axis would be taken from the line overaly and the histogram superimposed on that
    #    however, histogram gets offset, and not normalized around 0 y-axis between both charts
    # add_overlay(chart, data=data.drop('color', axis=1, errors='ignore'), color='rgba(0,0,0,0)')
    hist_chart = chart.create_histogram(name=rename_label, price_label=price_label, price_line=price_line)
    hist_chart.set(data)

    return hist_chart
