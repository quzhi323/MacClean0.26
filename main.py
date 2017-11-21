import json
import os

from flask import Flask
from flask import render_template, app

from data_processing import post_data_info

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['basefiledir'] = os.path.join(basedir, 'experiment')
app.config['example_1']= os.path.join(basedir, 'example_1')

@app.route('/',methods=['GET','POST'])
def init():

    example_data_info=post_data_info(app,"example_1", "data.csv")

    print(example_data_info[3])

    result={
        'EXAMPLE_ATTRIBUTS':example_data_info[3]
    }
    result = json.dumps(result)

    return render_template("input.html",result=result)

if __name__ == '__main__':
    app.run(debug=True)
