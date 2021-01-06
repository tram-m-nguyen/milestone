from flask import Flask, render_template, request, redirect, flash
from stock import getStock, plotStock
from bokeh.embed import components 
import pandas as pd
from bokeh.plotting import figure

app = Flask(__name__)



@app.route('/')
def index():
	"""Renders form"""

	return render_template('form.html')


@app.route('/convert')
def process_form():
	"""Converts currency and shows historical info about the currency."""

	stockName = request.args['stock'].upper()
	#month = request.args['month']
	result = None

	errs = []
	
	if stockName is None:
		errs.append("Please enter stock name")

	if not errs:
		result = getStock(stockName)
		if result is None:
			errs.append("Unable to find stock info.")

	if errs:
		for err in errs:
			flash(err)
			return render_template("form.html", stockName=stockName)
	
	else:
		plot = plotStock(result)
		script, div = components(plot)

		return render_template('result.html', stockName=stockName,\
			script=script, div=div)



if __name__ == '__main__':
  		app.run(port=33507)
