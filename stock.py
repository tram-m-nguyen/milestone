"""Function for handling stock info."""

import requests
import json
from api import API_KEY
import pandas as pd 
from bokeh.io import show 
from bokeh.plotting import figure



def getStock(stockName):
	"""Returns stock daily data for the entire month."""

	url = "https://www.alphavantage.co/query?"
	
	payload = {"function": "TIME_SERIES_DAILY_ADJUSTED", 'symbol': stockName, \
                'apikey': API_KEY}
	
	response = requests.get(url, params=payload)

	daily = response.json()['Time Series (Daily)']
	
	return daily


def plotStock(stock):
	"""Returns a plot.
	
	stock: json object looks like this:  
	{'2021-01-05': {'1. open': '125.01', 
					'2. high': '126.68', 
					'3. low': '124.61', 
					'4. close': '126.14', 
					'5. adjusted close': '126.14', 
					'6. volume': '5944120', 
					'7. dividend amount': '0.0000', 
					'8. split coefficient': '1.0'}}
    """

	df = pd.DataFrame(stock)

	df2 = df.T

	# index the date and turn into datetime ns
	df2.index = pd.to_datetime(df2.index)

	# rename columns
	old_cols_name = df2.columns.tolist()
	new_cols_name = ["open", "high", "low", "close", "adjusted_close", "volume",\
		"dividend_amount", "split_coefficient"]  
	
	df2 = df2.rename(columns=dict(zip(old_cols_name, new_cols_name)))

	month = df2.loc['2020-12-31':'2020-01-01']

	plt = figure(x_axis_type='datetime', title='Stock', plot_height=400, \
				plot_width = 800)
	
	plt.xgrid.grid_line_color=None
	plt.ygrid.grid_line_alpha=0.5
	plt.xaxis.axis_label = "Date"
	plt.yaxis.axis_label = 'Price'

	plt.line(month.index, month.adjusted_close)

	#can leave this here to show plot
	# show(plt)

	return plt





	