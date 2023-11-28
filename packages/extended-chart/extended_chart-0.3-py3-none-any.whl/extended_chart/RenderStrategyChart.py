import time

import pandas as pd
from pathlib import Path
from extended_chart import ExtendedChart
from extended_chart.style import black_background, white_background
from extended_chart.utils.rename_columns import rename_iqfeed_cols
from extended_chart import add_overlay, add_marker, add_histogram, add_trade_marker
from extended_chart.add_table import add_stats_table, add_pnl_table
from extended_chart.add_background_color import add_background_color
from extended_chart.add_horizontal_line import add_horizontal_line
import warnings
import re

warnings.simplefilter('ignore')

# TODO: I need to address the symbol lookup being a parameter
#  The reason it is there is that it allows the chart to render RTH vs ETH hours
#  As a result I need to be able to figure out what the RTH hours are for the symbol defined in the pnl_data

# TODO: I need to be able to pass in indicator color for overlays, maybe rewrite the color logic to use key_color
#  Or I introduce the color column to the class paramaters

# TODO: Marketdata and features data need to be modified together, there is an issue


subchart_minimum_height = 0.15
maximum_main_chart_height = 0.7

from collections import defaultdict


class RenderStrategyChart:

    def __init__(self, strategy_dir, show_volume=False, toolbar_freq=('1Min', '5Min', '15Min', '30Min', '1H', '4H'),
                 main_overlays=[], symbol_lookup={}, **kwargs):
        '''
        Helper function that renders the strategy metadata folder in a view

        :param strategy_dir: Path to the strategy/vector or strategy/event folder where metadata exists
        :param show_volume: Show/hide volume on main chart
        :param toolbar_freq: Define the resample frequency to render
        :param main_chart_overlay: list of feature column that is defined in the features_data
        :param symbol_lookup: (deprecate) lookup table that defines a symbols rth_start and rth_end time

        chart_### will create a suplot
        chart_###_spans will create a vertical span background overlay
        chart_###_supports will create a horizontal support line
        chart_###_trendlines will create trendline, but only supported on main chart for now
        '''
        self.strategy_dir = strategy_dir
        self.show_volume = show_volume
        self.symbol_lookup = symbol_lookup

        if isinstance(strategy_dir, str):
            self.strategy_dir = Path(self.strategy_dir)

        # TODO: I need to make this dynamic I think because right now it limits to Minute Bars
        #  User should be able to define optionns to change
        self.freq = toolbar_freq[0]
        self.toolbar_freq = toolbar_freq

        # Features
        self.rth = 'ETH'
        self.show_markers = 'show_trades'
        self.marker_lines = []
        self.marker_arrows = []

        # TODO: I might want to change this from main_ to chart_one
        self.main_overlays = main_overlays
        self.main_supports = kwargs.pop('main_supports', pd.DataFrame(columns=['price']))
        self.main_trendlines = kwargs.pop('main_trendlines',
                                          pd.DataFrame(columns=['start_time', 'end_time', 'start_price', 'end_price']))

        self.chart_width = 0.7
        self.chart_height = 0.7

        # TODO: This might be fore mail chart overlay, need to revist
        self.overlay_lines_and_hist = []

        self.consolidated_subplot_and_overlays = defaultdict(list)
        self.subplot_object_lookup = dict()
        self.market_data_matching_index = []

        self.subchart_overlays = dict()
        self.span_overlays = dict()
        self.support_overlays = dict()

        for k, data in kwargs.items():
            if re.match(r'chart_(.*?)_span[s]?', k):
                self.span_overlays[k] = data
            elif re.match(r'chart_(.*?)support[s]?', k):
                self.support_overlays[k] = data
            elif re.match(r'chart_(.*?)$', k):
                self.subchart_overlays[k] = data

        self._load_init_render()

    def _load_init_render(self):
        self.market_data = pd.read_pickle(self.strategy_dir / 'market_data.p')
        self.market_data = self.market_data.rename(columns=rename_iqfeed_cols)['open high low close volume'.split()]

        if not self.show_volume:
            self.market_data = self.market_data.drop('volume', axis=1, errors='ignore')

        self.pnl_data = pd.read_pickle(self.strategy_dir / 'pnl_data.p')
        self.stats_data = pd.read_pickle(self.strategy_dir / 'stats_data.p')
        self.features_data = pd.read_pickle(self.strategy_dir / 'features_data.p').set_index('datetime')
        self.symbol = self.pnl_data.symbol.min()

        # TODO: I need to remove this once done
        self.pnl_data = self.pnl_data.head(13)

        # TODO: Test the case where there is too many charts and this goes negative
        # TODO: This needs to be 0.7 in total, but as subcharts get added, main chart should not be penilized
        self.inner_height = maximum_main_chart_height - len(self.subchart_overlays) * subchart_minimum_height

        self.chart = ExtendedChart(inner_width=self.chart_width, inner_height=self.inner_height, width=1200, height=800,
                                   debug=True)
        self.chart = black_background(self.chart)

        self.chart.topbar.menu('switcher_freq', options=self.toolbar_freq, align='left',
                               func=lambda chart: self._change_timeframe(chart, 'switcher_freq'))

        self.chart.topbar.menu('switcher_rth', options=('ETH', 'RTH'), align='left',
                               func=lambda chart: self._change_rth(chart=chart, switcher_name='switcher_rth'))
        self.chart.topbar.menu('menu_trade_markers', options=('Trade Lines', 'Trade Markers', 'No Markers'), align='left',
                               func=lambda chart: self._show_trade_markers(chart=chart, switcher_name='menu_trade_markers'))

        self.chart.topbar.button('button_fullscreen', '🗖 Fullscreen', align='right',
                                 func=lambda chart: self._change_fullscreen(chart, 'button_fullscreen'))

        self.stats_table = add_stats_table(self.chart, data=self.stats_data, width=0.3, height=0.7)

        self._refresh_plots_and_indicators()

        self.pnl_table = add_pnl_table(self.chart, data=self.pnl_data, width=1, height=0.3)

    def show(self, block: bool = True):
        self.chart.show(block=block)

    def _delete_trade_line_and_markers(self):
        for trend_line in self.marker_lines:
            trend_line.delete()

        for marker in self.marker_arrows:
            self.chart.remove_marker(marker_id=marker)

    def _delete_overlay_lines(self):
        while self.overlay_lines_and_hist:
            overlay = self.overlay_lines_and_hist.pop()
            if not overlay:
                continue

            overlay.delete()
            print(f'.    {len(self.overlay_lines_and_hist) + 1} delete - {overlay}')

    def _refresh_plots_and_indicators(self):
        self._delete_trade_line_and_markers()
        self._delete_overlay_lines()

        self.chart.set(self._set_market_data())
        self.overlay_lines_and_hist = add_overlay(self.chart, self._set_features_data(columns=self.main_overlays))

        for chart_name, indicators in self.subchart_overlays.items():
            print(f'Rendering: {chart_name=}   with {indicators=}')

            if not self.subplot_object_lookup.get(chart_name):
                print(f'Creating New Chart for {chart_name=}')
                _new_subchart = self.chart.add_subplot(height=subchart_minimum_height, width=self.chart_width, sync=True)
                self.subplot_object_lookup[chart_name] = black_background(_new_subchart)

            i_hist = set([x for x in indicators if ('_hist' in x.lower() or 'hist_' in x.lower())])
            i_lines = set(indicators).difference(i_hist)

            i_lines = add_overlay(self.subplot_object_lookup[chart_name], data=self._set_features_data(columns=list(i_lines)))
            self.overlay_lines_and_hist.extend(i_lines)

            _hist = add_histogram(self.subplot_object_lookup[chart_name], data=self._set_features_data(columns=list(i_hist)))
            self.overlay_lines_and_hist.append(_hist)

        self.marker_lines, self.marker_arrows = add_trade_marker(self.chart, data=self.pnl_data,
                                                                 marking_style=self.show_markers)
        self._add_spans()
        self._add_support_lines()
        self._add_trendlines()

    def _add_trendlines(self):
        default_color = 'rgba(201,29,35,1.0)'
        default_style = 'solid'

        df = self.main_trendlines
        assert set(['start_time', 'end_time', 'start_price', 'end_price']).issubset(
            df.columns), 'To draw trendlines [start_time, end_time, start_price, end_price] columns are required '

        df = df.sort_values('start_time', ascending=True)
        if 'color' not in df.columns:
            df['color'] = default_color
        if 'style' not in df.columns:
            df['style'] = default_style

        for x in df.itertuples():
            self.chart.trend_line(start_time=x.start_time, end_time=x.end_time, start_value=x.start_price,
                                  end_value=x.end_price, color=x.color, style=x.style)

    def _add_spans(self):
        # TODO: This feature can not be implemented on subplot at the moment
        #   https://github.com/louisnw01/lightweight-charts-python/issues/164
        for k, spans_df in self.span_overlays.items():
            # Assumes there will be at least one line overlay on a subplot, otherwise there is no need to create subplot
            try:
                chart_lookup = re.findall('(chart_.*?)_span', k)[0]
                _line = self.consolidated_subplot_and_overlays[chart_lookup][0][0]
                add_background_color(_line, data=spans_df, alpha=0.2)
            except:
                ...

    def _add_support_lines(self):

        add_horizontal_line(self.chart, data=self.main_supports)

        for k, lines_df in self.support_overlays.items():
            # Assumes there will be at least one line overlay on a subplot, otherwise there is no need to create subplot
            try:
                chart_lookup = re.findall('(chart_.*?)_support', k)[0]
                _chart = self.subplot_object_lookup[chart_lookup]
                _line = self.consolidated_subplot_and_overlays[chart_lookup][0][0]
                add_horizontal_line(_line, lines_df)
            except:
                ...

    def _set_market_data(self):

        df = self.market_data.copy()
        agg_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}

        if not self.show_volume:
            agg_dict.pop('volume')

        df = df.groupby(pd.Grouper(freq=self.freq)).agg(agg_dict)
        df = df.dropna()
        self.market_data_matching_index = df.index

        if self.rth == 'RTH':
            symbol_detail = self.symbol_lookup.get(self.symbol)
            if symbol_detail:
                rth_start = symbol_detail.rth_start
                rth_end = symbol_detail.rth_end

                if rth_start and rth_end:
                    df = df.between_time(start_time=rth_start, end_time=rth_end, inclusive='both')

        return df

    def _set_features_data(self, columns):

        df = self.features_data.copy()
        df = df[columns]
        df = df.groupby(pd.Grouper(freq=self.freq)).last()
        df = df[df.index.isin(self.market_data_matching_index)]

        if self.rth == 'RTH':
            symbol_detail = self.symbol_lookup.get(self.symbol)
            if symbol_detail:
                rth_start = symbol_detail.rth_start
                rth_end = symbol_detail.rth_end

                if rth_start and rth_end:
                    df = df.between_time(start_time=rth_start, end_time=rth_end, inclusive='both')
        return df

    def _change_rth(self, chart, switcher_name):
        if self.chart.topbar[switcher_name].value == 'ETH':
            self.rth = 'ETH'

        elif self.chart.topbar[switcher_name].value == 'RTH':
            self.rth = 'RTH'

        self._refresh_plots_and_indicators()

    def _change_fullscreen(self, chart: ExtendedChart, button_name):
        if chart.topbar[button_name].value == '🗖 Fullscreen':
            chart.resize(height=maximum_main_chart_height, width=1)
            chart.topbar[button_name].set('🗕 Minimize')

            self.stats_table.resize(width=0, height=0)
            self.pnl_table.resize(width=0, height=0)

            normalized_subchart_size = (1 - maximum_main_chart_height) / len(self.subplot_object_lookup)

            for _, subchart in self.subplot_object_lookup.items():
                subchart.resize(height=normalized_subchart_size, width=1)

        elif chart.topbar[button_name].value == '🗕 Minimize':
            chart.resize(height=0.7 - len(self.subplot_object_lookup) * subchart_minimum_height, width=0.7)
            chart.topbar[button_name].set('🗖 Fullscreen')

            self.stats_table.resize(width=0.3, height=0.7)
            self.pnl_table.resize(width=1, height=0.3)

            for _, subchart in self.subplot_object_lookup.items():
                subchart.resize(height=subchart_minimum_height, width=0.7)

    def _change_timeframe(self, chart, switcher_name):
        self.freq = chart.topbar[switcher_name].value
        self._refresh_plots_and_indicators()

    def _show_trade_markers(self, chart, switcher_name):
        for trend_line in self.marker_lines:
            trend_line.delete()

        for marker in self.marker_arrows:
            self.chart.remove_marker(marker_id=marker)

        if chart.topbar[switcher_name].value == 'Trade Lines':
            self.show_markers = 'show_trades'
        elif chart.topbar[switcher_name].value == 'Trade Markers':
            self.show_markers = 'show_markers'
        elif chart.topbar[switcher_name].value == 'No Markers':
            self.show_markers = None

        self.marker_lines, self.marker_arrows = add_trade_marker(self.chart, self.pnl_data, marking_style=self.show_markers)
