import os
from flask import Flask, request, jsonify,render_template,redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'trialdata/'
ALLOWED_EXTENSIONS_DATASET = {'csv'}
ALLOWED_EXTENSIONS_MODEL={'pkl','py'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file_dataset(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_DATASET


def allowed_file_model(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_MODEL

@app.route('/')
def index():
    return render_template('index.html')

# this would be the endpoint to send data for prediction
@app.route('/model_trainer', methods=['POST'])
def model_trainer():
    if (request.method == 'POST'):
        f= request.files['file']
        if(allowed_file_dataset(f.filename)):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
        else:
            return "File not allowed"
        
@app.route('/model_upload', methods=['POST'])
def model_upload():
    if (request.method == 'POST'):
        f= request.files['file']
        if(allowed_file_model(f.filename)):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
        else:
            return "File not allowed"



if __name__ == '__main__':
    app.run(port=5000,debug=True)