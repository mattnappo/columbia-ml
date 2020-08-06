# Main imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# sklearn imports
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

# Web server imports
import flask, sys
from flask import Flask, render_template, session, request
from wtforms import Form, StringField, validators

# --- ML CODE --- #

# Load the data and select the data that we actually want and clean it up
df = pd.read_csv('./Columbia_CLI.csv', index_col=0)
minified_cols = [
  'CLI',
  'annual_inc', 'dti', 'delinq_2yrs', 'inq_last_6mths',
  'total_acc', 'open_acc', 'int_rate', 'total_pymnt',
]
necessary_cols = [
  'int_rate', 'CLI',
  'annual_inc', 'dti', 'delinq_2yrs', 'inq_last_6mths',
  'open_acc', 'revol_util', 'total_acc', 'total_pymnt',
  'total_rec_int', 'last_pymnt_amnt',
  'installment',
]

clean_terms = []
for term in df['term']:
  clean_terms.append(int(term.replace(' months', '')))

model_df = df.loc[:, minified_cols]
model_df.insert(3, 'term', clean_terms)

# Prepare the dataset
all_features = model_df.drop('total_pymnt', axis=1)
targeted_feature = model_df['total_pymnt']

# Find the mode interest rate in the dataset
# mode_int_rate = all_features.groupby('int_rate')['int_rate'].max()
# Just hard code it for now because that doesn't work above

mode_int_rate = 11.71

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
  all_features,
  targeted_feature,
  test_size=0.30,
  random_state=39,
) 

# Build the model
linreg = LinearRegression()
linreg.fit(X_train, y_train)

# Test it
y_pred = linreg.predict(X_test)

print(f'accuracy: {round(metrics.r2_score(y_test, y_pred), 2)}')

# -- WEB SERVER CODE -- #

class BasicForm(Form):
  cli = StringField('', [validators.DataRequired()])
  term = StringField('', [validators.DataRequired()])
  annual_inc = StringField('', [validators.DataRequired()])
  dti = StringField('', [validators.DataRequired()])
  delinq = StringField('', [validators.DataRequired()])
  inq = StringField('', [validators.DataRequired()])
  total_acc = StringField('', [validators.DataRequired()])
  open_acc = StringField('', [validators.DataRequired()])

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def predict():
  session['predicted'] = False
  form = BasicForm(request.form)

  if request.method == 'POST' and form.validate():
    # Extract the data from the form
    user_input_data = [
      float(form.cli.data),
      float(form.annual_inc.data),
      float(form.dti.data),
      float(form.term.data),
      float(form.delinq.data),
      float(form.inq.data),
      float(form.total_acc.data),
      float(form.open_acc.data),
      float(mode_int_rate),
    ]

    # Use the model to predict given the data extracted from the website
    prediction = linreg.predict([user_input_data])

    # r_over_n = (mode_int_rate / 100) / 12
    # nt = 12 * (form.term / 12)
    # required = form.cli * (1 + (r_over_n)) ** nt
    required = float(form.cli.data) * (1.0 + (mode_int_rate / 100.0))
    percent = round((prediction / required)[0], 2) * 100.0
    session['predicted'] = True

    if percent > 100:
      percent = 100
      prediction = [required]

    return render_template(
      'index.html',

      required=str(round(required, 2)),
      prediction=str(round(prediction[0], 2)),
      percent=percent,
      int_rate=mode_int_rate,
     
      form=form,
    )

  return render_template('index.html', form=form)

# Actually run the web server
if __name__ == '__main__':
  app.secret_key = 'hahahahahaha gini haha'
  app.run(host='0.0.0.0', debug=True, port=8088)
