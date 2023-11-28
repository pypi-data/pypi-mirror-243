import logging, time, os
import pandas as pd
from lightweight_charts import Chart

pd.set_option('display.width', 1000, 'display.max_columns', 1000)


# TODO: I need to check if this works on chart or line
#  if this needs to be one a line, this actually complicates things for the chart render
#  I would need to create an arbitary line for the lines to render

def add_horizontal_line(line: Chart, data: pd.DataFrame() = None, price: float = None, color='rgba(252, 219, 3, 0.8)',
                        width=1, style='solid', label=''):
    if isinstance(data, pd.DataFrame):
        assert 'price' in data.columns, 'price= values needs to be provided in the dataframe to draw horizontal lines'
        if 'width' not in data.columns:
            data['width'] = width
        if 'color' not in data.columns:
            data['color'] = color
        if 'style' not in data.columns:
            data['style'] = 'solid'
        if 'label' not in data.columns:
            data['label'] = label

        data = data[['price', 'width', 'color', 'style', 'label']]

        for x in data.itertuples():
            line.horizontal_line(price=x.price, color=x.color, width=x.width, style=x.style, text=x.label)

    elif isinstance(price, (float, int)):
        line.horizontal_line(price=price, color=color, width=width, style=style, text=label)
