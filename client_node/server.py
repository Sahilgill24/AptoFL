from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/model_trainer', methods=['POST'])
def model_trainer():
    pass

  

if __name__ == '__main__':
    app.run(port=5000,debug=True)