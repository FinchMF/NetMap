from flask import ( Flask, render_template, request, url_for )
from NetMap import ( LINE, plotly )
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading', methods=['POST'])
def loading():

    params: dict = {

        'q': request.json.q,
        'location': request.json.location
        # need date - use datetime and get day of
        # add number of days look back - choose 7
    } 

    records: int = 1 # try more variables / or create security around number of locations and words
    pipeline = LINE(params=params, records=records)
    pipeline.getData()
    pipeline.send2db()
    data = pipeline.callData()
    data = pipeline.dataFramed(data)
    net = pipeline.generateNetwork(data=data, title='Accounts <-> Hashtags')
    graphJSON = json.dumps([net], cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON