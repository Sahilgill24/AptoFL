import os
from flask import Flask, request, jsonify,render_template,redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'trialdata/'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')

# this would be the endpoint to send data for prediction
@app.route('/model_trainer', methods=['POST'])
def model_trainer():
    if (request.method == 'POST'):
        f= request.files['file']
        if(allowed_file(f.filename)):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/')
        else:
            return "File not allowed"
        





if __name__ == '__main__':
    app.run(port=5000,debug=True)