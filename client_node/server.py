from flask import Flask, request, jsonify,render_template,redirect


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# this would be the endpoint to send data for prediction
@app.route('/model_trainer', methods=['POST'])
def model_trainer():
    if (request.method == 'POST'):
        f= request.files['file']
        f.save(f'trialdata/{f.filename}')
        return redirect('/')
        


@app.route('/predict', methods=['POST'])
def training():
    return render_template('predict.html')


if __name__ == '__main__':
    app.run(port=5000,debug=True)