from flask import Flask, render_template, request, redirect, url_for
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
    
@app.route('/drinkLibrary')
def drinkLibrary():
    page = request.args.get('page', 1, type=int)
    drink_filter = request.args.get('drink')
    roast_filter = request.args.get('roast')
    sort_by = request.args.get('sort_by', 'date_desc') # Default sort
    
    try:
        conn = mysql.connector.connect(
        host="localhost",
        user="grafanaReader",
        password="spw",
        database="coach")
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM drink_table"
        where_clauses = []
        params = []
        
        if drink_filter and drink_filter != "all":
            where_clauses.append("drink = %s")
            params.append(drink_filter)
        if roast_filter and roast_filter != "all":
            where_clauses.append("roast = %s")
            params.append(roast_filter)
        
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)

        if sort_by == 'coffee_water_asc':
            sql += " ORDER BY coffee_water ASC"
        elif sort_by == 'coffee_water_desc':
            sql += " ORDER BY coffee_water DESC"
        elif sort_by == 'rating_asc':
            sql += " ORDER BY rating ASC"
        elif sort_by == 'rating_desc':
            sql += " ORDER BY rating DESC"
        else: # Default to date_desc
            sql += " ORDER BY date DESC"

        sql += f" LIMIT {ROWS_PER_PAGE} OFFSET {(page - 1) * ROWS_PER_PAGE}"
        
        cursor.execute(sql, tuple(params))
        results = cursor.fetchall()
        
        sql_count = "SELECT COUNT(*) FROM drink_table"
        if where_clauses:
            sql_count += " WHERE " + " AND ".join(where_clauses)
            cursor.execute(sql_count, tuple(params))
        else:
            cursor.execute(sql_count)
        
        total_rows = cursor.fetchone()['COUNT(*)']
        total_pages = (total_rows + ROWS_PER_PAGE - 1) // ROWS_PER_PAGE
        
        return render_template('drinkLibrary.html', data=results, drink_filter=drink_filter, roast_filter=roast_filter, page=page, total_pages=total_pages, sort_by=sort_by)

    except mysql.connector.Error as err:
        return f"Error: {err}"
    
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
@app.route('/recordRoast', methods=['GET'])
def recordRoast():
	return render_template('recordRoast.html')
    
@app.route('/submitRoast', methods=['POST'])
def submitRoast():
    if request.method == 'POST':
        date = request.form['date']
        country = request.form['country']
        farm = request.form['farm']
        roaster = request.form['roaster']
        roast = request.form['roast']
        duration = request.form['duration']
        mass_in = request.form['mass_in']
        mass_out = request.form['mass_out']
        loss = request.form['loss']
        profile = request.form['profile']
        
        formatted_duration = f"00:{duration}"

        try:
            conn = mysql.connector.connect(
            host="localhost",
            user="grafanaReader",
            password="spw",
            database="coach")
            
            cursor = conn.cursor()
            sql = "INSERT INTO roast_table (date, country, farm, roaster, roast, duration, mass_in, mass_out, loss, profile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (date, country, farm, roaster, roast, formatted_duration, mass_in, mass_out, loss, profile)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('home'))
            
        except mysql.connector.Error as err:
            return f"Error recording roast: {err}"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    return "Invalid request"

@app.route('/recordDrink')
def recordDrink():
	return render_template('recordDrink.html')

@app.route('/submitDrink', methods=['POST'])
def submitDrink():
    if request.method == 'POST':
        date = request.form['date']
        drink = request.form['drink']
        grind = request.form['grind']
        duration = request.form['duration']
        mass_in = request.form['mass_in']
        mass_out = request.form['mass_out']
        coffee_water = request.form['coffee_water']
        milk = request.form['milk']
        milk_coffee = request.form['milk_coffee']
        rating = request.form['rating']
        roast = request.form['roast']
        comments = request.form['comments']
        
        formatted_duration = f"00:{duration}"

        try:
            conn = mysql.connector.connect(
            host="localhost",
            user="grafanaReader",
            password="spw",
            database="coach")
            
            cursor = conn.cursor()
            sql = "INSERT INTO drink_table (date, drink, grind, duration, mass_in, mass_out, coffee_water, milk, milk_coffee, rating, roast, comments) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (date, drink, grind, duration, mass_in, mass_out, coffee_water, milk, milk_coffee, rating, roast, comments)
            cursor.execute(sql, values)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('home'))
            
        except mysql.connector.Error as err:
            return f"Error recording roast: {err}"
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()
    return "Invalid request"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
