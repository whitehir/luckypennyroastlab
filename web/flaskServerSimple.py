from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():

    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="grafanaReader",
        password="spw",
        database="coach")

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM garage ORDER BY timestamp DESC LIMIT 10")
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('index.html', data=results)

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
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
