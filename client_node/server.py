import os
import json
from flask import Flask, request, jsonify,render_template,redirect
from werkzeug.utils import secure_filename
from flask_cors import CORS
import subprocess


UPLOAD_FOLDER = 'modeltraining/'
ALLOWED_EXTENSIONS_DATASET = {'csv'}
ALLOWED_EXTENSIONS_MODEL={'pkl','py'}



app = Flask(__name__)
CORS(app)
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
        if not request.data:
            return "No data received", 400

        # Get the file content from the request body
        file_content = request.data.decode('utf-8')
        file_content = json.loads(file_content)['data']
        
        print(file_content)

        # Save the content to a file
        filename = 'model.py'  # You can also allow the client to specify the filename if needed
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            with open(file_path, 'w') as file:
                file.write(file_content)
            return "Model uploaded successfully", 200
        except IOError:
            return "Error writing file", 500
        

@app.route('/stake')
def stake():
    try:
        # Path to the bash script
        script_path = os.path.join(app.config['UPLOAD_FOLDER'], 'run.sh')
        
        # Run the bash script
        result = subprocess.run(['/bin/bash', script_path], capture_output=True, text=True, check=True)
        print(result.stdout)
        
        # Return the output of the script
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'error': result.stderr
        }), 200
    except subprocess.CalledProcessError as e:
        # If the script fails, return the error
        return jsonify({
            'status': 'error',
            'message': 'Failed to run the model',
            'error': e.stderr
        }), 500
    except Exception as e:
        # For any other exceptions
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred',
            'error': str(e)
        }), 500
    



if __name__ == '__main__':
    app.run(port=5000,debug=True)