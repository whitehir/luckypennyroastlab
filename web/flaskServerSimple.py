from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

ROWS_PER_PAGE = 15

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    country_filter = request.args.get('country')
    roast_filter = request.args.get('roast')
    
    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="grafanaReader",
        password="spw",
        database="coach")
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM roast_table"
        where_clauses = []
        params = []
        
        if country_filter and country_filter != "all":
            where_clauses.append("country = %s")
            params.append(country_filter)
        if roast_filter and roast_filter != "all":
            where_clauses.append("roast = %s")
            params.append(roast_filter)
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
        
        sql += " ORDER BY date DESC"
        sql += f" LIMIT {ROWS_PER_PAGE} OFFSET {(page - 1) * ROWS_PER_PAGE}"
        
        cursor.execute(sql, tuple(params))
        results = cursor.fetchall()
        
        sql_count = "SELECT COUNT(*) FROM roast_table"
        if where_clauses:
            sql_count += " WHERE " + " AND ".join(where_clauses)
            cursor.execute(sql_count, tuple(params))
        else:
            cursor.execute(sql_count)
        
        total_rows = cursor.fetchone()['COUNT(*)']
        total_pages = (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
        
        return render_template('index.html', data=results, country_filter=country_filter, roast_filter=roast_filter, page=page, total_pages=total_pages)

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
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
