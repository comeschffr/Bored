from flask import Flask, render_template, url_for, request, make_response
from flask_wtf import FlaskForm
from wtforms.fields.html5 import IntegerRangeField, DecimalRangeField
from wtforms import SubmitField
import requests
import json
import os


# Improvements:
# Make the response object earlier and then bind the arguments (form and result)


app = Flask(__name__)
app.secret_key = os.urandom(24)
API_URL = 'http://www.boredapi.com/api/activity/'


def get_color(result):
	access = result.get('accessibility')
	access = float(access) if access else 0
	if access < 1/3:
		result['color'] = 'success'
	elif access < 2/3:
		result['color'] = 'warning'
	else:
		result['color'] = 'danger'
	return result


@app.route('/', methods=['GET', 'POST'])
def main():
	args = {}
	form = QueryForm()
	last_key = 0
	
	if form.validate_on_submit():
		args = {'participants': form.participants.data}
		last_key = request.cookies.get('last_key', 0)
	elif request.method == 'GET':
		form.participants.data = 1

	counter = 0
	while counter < 10: # Doesn't block in case solely one activity
		result = json.loads(requests.get(API_URL, params=args).content)
		if result.get('key') != last_key:
			last_key = result.get('key')
			break
		counter += 1


	if not result.get('error'):
		result = get_color(result)
		category = result.get("type") if result.get("type") else 'default'
		result['image_file'] = url_for('static', filename=f'thumbnails/{result.get("type")}.jpg')

	resp = make_response(render_template('main.html',
										result=result, 
										form=form))
	resp.set_cookie('last_key', result.get('key'))
	return resp


class QueryForm(FlaskForm):
	participants = IntegerRangeField('How many are you?') # should be between 1 and 5
	submit = SubmitField('Draw')


if __name__ == '__main__':
	app.run(debug=True)