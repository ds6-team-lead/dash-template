import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from joblib import load
pipeline = load('assets/pipeline.joblib')

import pandas as pd
bitcoin = pd.read_csv('bitcoin.csv')



bitcoin['string_date'] = bitcoin['Date'].copy()
bitcoin['Date'] = pd.to_datetime(bitcoin['Date'])
bitcoin['Year'] = bitcoin['Date'].dt.year
bitcoin['Month'] = bitcoin['Date'].dt.month
bitcoin['Day'] = bitcoin['Date'].dt.day

drop_columns = ['Date','Close**', 'Volume', 'Market Cap', 'High', 'Low']
new_bitcoin = bitcoin.drop(columns=drop_columns)

column1 = dbc.Col(
    [
        dcc.Markdown('## Predictions', className='mb-5'),
        dcc.Markdown('#### Textbox'),
        dcc.Input(
            id='textbox1',
            placeholder='Enter a value...',
            type='text',
            value=''
        ),

        dcc.Markdown('#### Year'),
        dcc.Slider(
            id='year',
            min=2018,
            max=2019,
            step=1,
            value=2018,
            marks={n: str(n) for n in range(2018,2019,1)},
            className='mb-5'
        ),
        dcc.Markdown('#### Month'),
        dcc.Slider(
            id='month',
            min=1,
            max=12,
            step=1,
            value=6,
            marks={n: str(n) for n in range(1,12,1)},
            className='mb-5'
        ),
        dcc.Markdown('#### Day'),
        dcc.Slider(
            id='day',
            min=1,
            max=31,
            step=1,
            value=8,
            marks={n: str(n) for n in range(1,31,1)},
            className='mb-5'
        ),
    ],
    md=4,
)
column2 = dbc.Col(
    [
        html.H2('Expected Price', className='mb-5'), 
        html.Div(id='prediction-content', className='lead')
    ]
)

layout = dbc.Row([column1, column2])


@app.callback(
    Output('prediction-content', 'children'),
    [Input('year', 'value'), Input('month', 'value'), Input('day','value')],
)
def predict(year, month, day):
    str_date = str(month) + '/' + str(day) + '/' + str(year)
    row = new_bitcoin.query('string_date==@str_date')
    if row.shape[0] == 0:
        return ''
    else:
        y_pred = pipeline.predict(row)[0]
    return f'{y_pred:.2f} dollars'
    #return row