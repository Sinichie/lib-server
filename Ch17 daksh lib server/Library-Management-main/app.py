from flask import Flask, render_template, request , jsonify 
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dak082610#'
app.config['MYSQL_DB'] = 'library'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def logIn():
    if request.method == 'GET':
        return render_template('main.html')

    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')

        if not userName or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        query = "SELECT PASSWORD FROM ADMIN WHERE USERNAME = %s"
        
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (userName,))
            result = cur.fetchone()

            if result:
                # Compare the provided password with the stored hashed password
                if check_password_hash(result[0], password):
                    return render_template("admin.html")
                else:
                    return jsonify({"error": "Invalid credentials"}), 401
            else:
                return jsonify({"error": "User not found"}), 404
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        finally:
            cur.close()

@app.route('/userFunc', methods=['GET'])
def userFunc():
    return render_template('users.html')

@app.route('/register', methods=['POST'])
def register():
    
        userName = request.form.get('userName')
        password = request.form.get('password')

        if not userName or not password:
            return jsonify({"error": "Username and password are required"}), 400

        hashed_password = generate_password_hash(password)
        
        query = "INSERT INTO ADMIN (USERNAME, PASSWORD) VALUES (%s, %s)"
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, (userName, hashed_password))
            mysql.connection.commit()  
            return jsonify({"message": "User registered successfully!"}), 201
        except MySQLdb.Error as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cur.close()

@app.route('/add_book', methods=['POST'])
def addBook():
    cur = mysql.connection.cursor()
    
    book_name = (request.form['book_name']).upper()
    book_author = (request.form['book_author']).upper()
    book_quantity = request.form['book_quantity']
    
    if (book_name is None) | ( book_quantity is None) | (book_author is None):
        return "Incorrect info", 400

    query = "INSERT INTO BOOKS (NAME, AUTHOR , QUANTITY) VALUES (%s, %s,%s)"
    values = (book_name, book_author, book_quantity,)

    try:
        cur.execute(query, values)
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': f"Book {book_name}, Author {book_author} with quantity {book_quantity} added successfully."})

    except MySQLdb.Error as e:
        if e.args[0] == 1062:
            return jsonify({'error': f"A book with the name {book_name} already exists. Please choose a different name or update the book."})
        else:
            return jsonify({'error': str(e)})

@app.route('/remove_book', methods=['POST'])
def remove_book():

        remove_choice = request.form.get('remove_choice')
        query = ""
        values = ()

        if remove_choice == '1':
            book_id = request.form.get('book_id')
            query = "DELETE FROM BOOKS WHERE ID = %s LIMIT 1"
            values = (book_id,)

        elif remove_choice == '2':
            book_name = request.form.get('book_name')
            query = "DELETE FROM BOOKS WHERE NAME = %s LIMIT 1"
            values = (book_name,)
        
        else:
            return jsonify({"error": "Invalid choice. Please enter 1 or 2."}), 400
        
        try:
            cur = mysql.connection.cursor()
            cur.execute(query, values)
            mysql.connection.commit()
            if cur.rowcount > 0:
                return jsonify({"message": f"Book {'with ID ' + book_id if remove_choice == '1' else 'named ' + book_name} removed successfully."}), 200
            else:
                return jsonify({"message": "No book found with the given details."}), 404

        except MySQLdb.Error as e:
            return jsonify({"error": str(e)}), 500
        
        finally:
            cur.close()

@app.route('/search_book', methods=['POST'])
def searchBook():
    search_choice = request.form.get('search_choice')

    if not search_choice:
        return jsonify({"error": "Please select 1 or 2"}), 400

    query = ""
    values = ()

    try:
        cur = mysql.connection.cursor()

        if search_choice == '1':
            book_id = request.form.get('book_id')
            if not book_id:
                return jsonify({"error": "Book ID is required"}), 400
            query = "SELECT * FROM BOOKS WHERE ID = %s"
            values = (book_id,)

        elif search_choice == '2':
            book_name = request.form.get('book_name')
            if not book_name:
                return jsonify({"error": "Book name is required"}), 400
            query = "SELECT * FROM BOOKS WHERE NAME = %s"
            values = (book_name,)

        else:
            return jsonify({"error": "Invalid choice. Please enter 1 or 2"}), 400

        cur.execute(query, values)
        result = cur.fetchone()

        if result:
            books = {"ID": result[0], "Name": result[1], "Quantity": result[3], "Author": result[2]}
            return jsonify({"message": "Book(s) found", "books": books}), 200
        else:
            return jsonify({"error": "No book found with the given details"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        
@app.route('/update_book', methods=['POST'])
def update_book():
    
        search_choice = request.form.get('update_choice')
        
        if not search_choice:
            return jsonify({"error": "Please select 1 or 2"}), 400
        query = ""
        values = ()

        try:
            cur = mysql.connection.cursor()

            if search_choice == '1':
                book_id = request.form.get('book_id')
                new_name = request.form.get('new_name')
                new_quantity = request.form['new_quantity']
                query = "UPDATE Books SET name = %s, quantity = %s WHERE id = %s"
                values = (new_name, new_quantity, book_id,)

            elif search_choice == '2':
                old_name = request.form.get('old_name')
                new_name = request.form.get('new_name2')
                new_quantity = request.form['new_quantity2']
                query = "UPDATE Books SET name = %s, quantity = %s WHERE name = %s"
                values = (new_name, new_quantity, old_name,)

            else:
                return jsonify({"error": "Invalid choice. Please choose 1 or 2."}), 400
            
            cur.execute(query, values)
            mysql.connection.commit()

            if cur.rowcount > 0:
                return jsonify({"message": "Book updated successfully!"}), 200
            else:
                return jsonify({"message": "No book found with the given details."}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            cur.close()

@app.route('/showBooks', methods=['GET'])
def showBooks():
    conn = mysql.connection
    my_cursor = conn.cursor()
    
    try:
        query = "SELECT * FROM BOOKS"
        my_cursor.execute(query)
        books = my_cursor.fetchall()

        book_data = [list(book) for book in books]
        return jsonify({'books': book_data}) 

    except MySQLdb.Error as err:
        return jsonify({'error': f"Error occurred: {err}"}), 500  

    finally:
        my_cursor.close()

@app.route('/issueBook', methods=['POST'])
def issueBook():
    conn = mysql.connection
    my_cursor = conn.cursor()
    
    if request.method == 'POST':
        rollNo = (request.form['rollNo']).upper()
        issue_choice = request.form['issue_choice']

        query = ""
        values = ()

        try:

            if issue_choice == '1':
                book_id = request.form['book_id']

                # Check if the book is already issued to the student
                query_check_existing = "SELECT * FROM BOOKS_ISSUED WHERE ID = %s AND ROLL_NUM = %s"
                my_cursor.execute(query_check_existing, (book_id, rollNo))
                existing_issue = my_cursor.fetchone()

                if existing_issue:
                    return jsonify({"message":f"Book with ID {book_id} is already issued to student with Roll No {rollNo}."})
                
                # Check if the book exists and has available quantity
                query_check = "SELECT QUANTITY FROM BOOKS WHERE ID = %s"
                my_cursor.execute(query_check, (book_id,))
                book_result = my_cursor.fetchone()

                if book_result and book_result[0] > 0:
                    query = "INSERT INTO BOOKS_ISSUED(ID, ROLL_NUM) VALUES (%s, %s)"
                    values = (book_id, rollNo,)

                    update_quantity_query = "UPDATE BOOKS SET QUANTITY = QUANTITY - 1 WHERE ID = %s"
                    my_cursor.execute(update_quantity_query, (book_id,))
                else:
                    return jsonify({"error":f"No book found with the ID {book_id} or insufficient quantity."})
            
            elif issue_choice == '2':
                book_name = request.form['book_name']

                # Get the book ID and quantity by book name
                query1 = "SELECT ID, QUANTITY FROM BOOKS WHERE NAME = %s"
                my_cursor.execute(query1, (book_name,))
                book_result = my_cursor.fetchone()

                if book_result and book_result[1] > 0:
                    book_id = book_result[0]

                    # Check if the book is already issued to the student
                    query_check_existing = "SELECT * FROM BOOKS_ISSUED WHERE ID = %s AND ROLL_NUM = %s"
                    my_cursor.execute(query_check_existing, (book_id, rollNo))
                    existing_issue = my_cursor.fetchone()

                    if existing_issue:
                        return jsonify({"message":f"Book '{book_name}' is already issued to student with Roll No {rollNo}."})

                    query = "INSERT INTO BOOKS_ISSUED(ID, ROLL_NUM) VALUES (%s, %s)"
                    values = (book_id, rollNo)

                    update_quantity_query = "UPDATE BOOKS SET QUANTITY = QUANTITY - 1 WHERE ID = %s"
                    my_cursor.execute(update_quantity_query, (book_id,))
                else:
                    return jsonify({"error":f"No book found with the name '{book_name}' or insufficient quantity."})
            else:
                return jsonify({"error":"Invalid choice. Please enter 1 or 2."})

            my_cursor.execute(query, values)
            conn.commit()

            return jsonify({"message":f"Book with ID {book_id} issued successfully to student with Roll No {rollNo}"})

        except MySQLdb.Error as err:
            conn.rollback()
            if err.args[0] == 1452:
                return jsonify({"error": "Wrong roll number."})
            return jsonify({"error":f"Error occurred: {err}"})

@app.route('/returnBook', methods=['POST'])
def returnBook():
    conn = mysql.connection
    my_cursor = conn.cursor()
    fine_message = "No fine Applicable"

    if request.method == 'POST':
        rollNo = request.form['rollNo2'].upper()
        issue_choice = request.form['return_choice']
        book_id = None

        try:
            if issue_choice == '1':
                book_id = request.form['book_id2']

                query_check = "SELECT bi.ISSUE_DATE FROM BOOKS_ISSUED AS bi WHERE bi.ID = %s AND bi.ROLL_NUM = %s"
                my_cursor.execute(query_check, (book_id, rollNo))
                issue_date_result = my_cursor.fetchone()

                if issue_date_result:
                    issue_date = issue_date_result[0]
                    current_date = datetime.now().date()
                    days_difference = (current_date - issue_date).days

                    if days_difference > 30:
                        fine_amount = 10 
                        fine_message = f"Book is overdue. Please pay a fine of {fine_amount}."

                    query = "DELETE FROM BOOKS_ISSUED WHERE ID = %s AND ROLL_NUM = %s LIMIT 1"
                    my_cursor.execute(query, (book_id, rollNo))
                        
                    update_quantity_query = "UPDATE BOOKS SET QUANTITY = QUANTITY + 1 WHERE ID = %s"
                    my_cursor.execute(update_quantity_query, (book_id,))
                else:
                    return jsonify({"error": "No book found with the given ID or wrong Roll Number."})

            elif issue_choice == '2':
                book_name = request.form['book_name2']

                query1 = "SELECT b.ID, bi.ISSUE_DATE FROM BOOKS AS b JOIN BOOKS_ISSUED AS bi ON b.ID = bi.ID WHERE b.NAME = %s AND bi.ROLL_NUM = %s"
                my_cursor.execute(query1, (book_name, rollNo))
                book_result = my_cursor.fetchone()

                if book_result:
                    book_id = book_result[0]
                    issue_date = book_result[1]
                    current_date = datetime.now().date()
                    days_difference = (current_date - issue_date).days

                    if days_difference > 30:
                        fine_amount = 10 
                        fine_message = f"Book is overdue. Please pay a fine of {fine_amount}."

                    query = "DELETE FROM BOOKS_ISSUED WHERE ID = %s AND ROLL_NUM = %s LIMIT 1"
                    my_cursor.execute(query, (book_id, rollNo))

                    update_quantity_query = "UPDATE BOOKS SET QUANTITY = QUANTITY + 1 WHERE ID = %s"
                    my_cursor.execute(update_quantity_query, (book_id,))
                else:
                    return jsonify({"error": f"No issued book found with the name '{book_name}' for Roll Number {rollNo}."})

            else:
                return jsonify({"error": "Invalid choice. Please enter 1 or 2."})

            conn.commit() 
            
            return jsonify({"message":f"Book with ID {book_id} returned successfully by student with Roll No {rollNo}"+" -> "+ fine_message})

        except MySQLdb.Error as err:
            conn.rollback()
            if err.args[0] == 1452:
                return jsonify({"error": "Wrong roll number."})
            return jsonify({"error": f"Error occurred: {err}"})

        finally:
            my_cursor.close()

@app.route('/issuedBooks', methods=['GET'])
def allIssuedBook():
    if request.method == 'GET':
        conn = mysql.connection
        my_cursor = conn.cursor()
    
        try:
            query = "SELECT b.NAME AS book_name, b.ID AS book_id, bi.ROLL_NUM AS roll_num, bi.ISSUE_DATE AS issue_date,s.NAME AS student_name FROM BOOKS AS b JOIN BOOKS_ISSUED AS bi ON bi.ID = b.ID JOIN STUDENTS AS s ON bi.ROLL_NUM = s.ROLL_NUM order by issue_date"

            my_cursor.execute(query)
            issued_books = my_cursor.fetchall()

            issued_book_data = [list(book) for book in issued_books]
            return jsonify({'issued_books': issued_book_data}) 

        except MySQLdb.Error as err:
            return jsonify({"error": f"Error occurred: {err}"}), 500 

        finally:
            my_cursor.close()

@app.route('/displayStudents', methods=['GET'])
def displayStudents():
    conn = mysql.connection
    my_cursor = conn.cursor()
    
    try:
        query = "SELECT ROLL_NUM, NAME FROM STUDENTS"
        my_cursor.execute(query)
        students = my_cursor.fetchall()

        student_data = [list(student) for student in students]
        return jsonify({'students': student_data}) 
        
    except MySQLdb.Error as err:
        return jsonify({"error": f"Error occurred: {err}"}), 500 

    finally:
        my_cursor.close()

@app.route('/addStudent', methods=['POST'])
def add_student():
    if request.method == 'POST':
        conn = mysql.connection
        my_cursor = conn.cursor()
        
        roll_num = (request.form.get("roll_num")).upper()
        name = (request.form.get("name")).upper()

        try:
            query = "INSERT INTO STUDENTS (ROLL_NUM, NAME) VALUES (%s, %s)"
            my_cursor.execute(query, (roll_num, name,))
            conn.commit() 
            return jsonify({"message": "Student added successfully!"}), 200
        
        except MySQLdb.Error as err:
            return jsonify({"error": f"Error occurred: {err}"}), 500 

        finally:
            my_cursor.close()


@app.route('/deleteStudent', methods=[ 'POST'])
def delete_student():
    if request.method == 'POST':
        conn = mysql.connection
        my_cursor = conn.cursor()
        
        roll_num = request.form.get("roll_num2")

        try:
            query = "DELETE FROM STUDENTS WHERE ROLL_NUM = %s LIMIT 1"
            my_cursor.execute(query, (roll_num,))
            conn.commit() 

            if my_cursor.rowcount == 0:
                return jsonify({"message": "No student found with the given roll number."}), 404
            
            return jsonify({"message": f"Student with roll number {roll_num} deleted successfully."}), 200
        
        except MySQLdb.Error as err:
            return jsonify({"error": f"Error occurred: {err}"}), 500 

        finally:
            my_cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
