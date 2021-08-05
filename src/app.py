from flask import ( Flask, render_template, request, url_for, send_from_directory )
from NetMap import ( LINE, plotly )
import json

app = Flask(__name__)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static/images'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loading', methods=['POST'])
def loading():

    params: dict = {

        'words': [str(request.json['q'])],
        'locations': [str(request.json['location'])],
        'start_date': '2021-08-02',
        'num_days': 7
    } 

    records: int = 1 # try more variables / or create security around number of locations and words
    pipeline = LINE(params=params, records=records)
    pipeline.getData()
    pipeline.send2db()
    data = pipeline.callData()
    data = pipeline.dataFramed(data)
    net = pipeline.generateNetwork(data=data, title='Accounts <-> Hashtags')
    graphJSON = json.dumps(net, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON    