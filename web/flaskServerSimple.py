from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/roastLibrary')
def roastLibrary():
	return render_template('roastLibrary.html')
    
@app.route('/recordRoast')
def recordRoast():
	return render_template('recordRoast.html')
    
@app.route('/recordDrink')
def recordDink():
	return render_template('recordDrink.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
