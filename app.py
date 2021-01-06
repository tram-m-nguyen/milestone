from flask import Flask, render_template, request, redirect, flash
from stock import getStock, plotStock
from bokeh.embed import components 

app = Flask(__name__)
app.config['SECRET_KEY'] = '98876'


@app.route('/')
def index():
	"""Renders form"""

	return render_template('form.html')


@app.route('/convert')
def process_form():
	"""Converts currency and shows historical info about the currency."""

	stockName = request.args['stock'].upper()
	errs = []
	
	if stockName == "":
		errs.append("Please enter a stock name.")

	result = getStock(stockName)
	
	if 'Error Message' in result:
		errs.append(f"Not a valid stock name: {stockName}")

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
