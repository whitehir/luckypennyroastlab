from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/roastProbePage')
def roast_probe_page():
	return render_template('roastProbePage.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
