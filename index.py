#-----------------------------------------------------------------------------
# Filename:    index.py
# Purpose:     Web app for the Ghibli Fans website
#              Requires a login to access the forum pages
#              Or setting up a new user account
#
#              1. Create the Flask application
#              2. Make database connection
#              3. Run SQL statements
#              4. Provide validations
#              5. Provide web page content
#
# Author:      Hans Telford
# Date:        07-Oct-2024 to 21-Oct-2024
# Version:     1.0
# Notes:       Intended as a basic web site with database connection example
#              using Flask/Python
#              TO DO: Add register and comment functionalities (24-Oct-2024)
#
# References:  Code used here is based on article by: David Adams (May, 2024)
#              "Login system with Python Flask and MySQL"
#              Link: https://codeshack.io/login-system-python-flask-mysql/
#              Other helpful URLs:
#              https://hackersandslackers.com/flask-routes/
#              https://code.tutsplus.com/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972t
#              https://code.tutsplus.com/creating-a-web-app-from-scratch-using-python-flask-and-mysql-part-2--cms-22999t
#              https://tecadmin.net/custom-host-and-port-settings-in-flask/
#              https://pythonprogramming.net/flask-get-post-requests-handling-tutorial/
#-----------------------------------------------------------------------------
# IMPORT STATEMENTS
#-----------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
#from pathlib import Path

#def getSSLPath():
    #return Path.joinpath(Path(__file__).resolve().parents[0], 'cert\DigiCertGlobalRootCA.crt.pem')

#-----------------------------------------------------------------------------
# GLOBAL VARIABLES (for all methods)
#-----------------------------------------------------------------------------
# create the Flask web app
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ghibli'
app.config['MYSQL_OPTIONS'] = {'ssl_ca':'D:/XAMPP/apache/conf/ca.pem'}
# app.config['MYSQL_CUSTOM_OPTIONS'] = {"ssl": {"ca": getSSLPath()}}
# secret key (can be any string value)
app.secret_key = 'database'

mysql = MySQL(app)
#-----------------------------------------------------------------------------
# METHODS
#-----------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    # display message if an error occurs
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        
        # Check if account exists using MySQL
        # Create a cursor object to make the MySQL connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Run the SQL script to confirm the logged in member from the database
        # NOTE: The %s placeholder in the query string will help prevent SQL injection,
        # as their bound values will be escaped before insertion.
        cursor.execute('SELECT memberID, member_name, email, usrid, usrpwd FROM member WHERE usrid = %s AND usrpwd = %s', (username, password,))
        # Fetch one record and return result
        resultset = cursor.fetchone()
        # Check if resultset contains no record
        # This confirms that the user id and password entered does not exist
        # in the database
        if resultset == None:
            msg = 'ERROR: Incorrect username and/or password!'
        else:
            # At this point, we have a confirmed member login
            # Create session variables, so we can access this data in other routes
            session['loggedin'] = True
            session['newreg'] = False
            session['id'] = resultset['memberID'] 
            session['usrid'] = resultset['usrid']
            session['fullname'] = resultset['member_name']
            session['new_comment'] = False
            # close the cursor object
            cursor.close()
            # Redirect to home page
            #return render_template('movies.html')
            return redirect(url_for('movies'))
        cursor.close()
    else:
        # reset msg to blank
        msg = ''
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/movies')
def movies():
    # Check if the user is logged in
    if 'loggedin' in session:
        try:
            # SQL query to fetch movie data from database
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT movieID, title, releaseYear, director, length, rating FROM ghibli.movie")
            data = cursor.fetchall()
            cursor.close()
            return render_template('movies.html', data=data)
        except Exception as e:
            print(f"ERROR: Database/SQL issue - {type(e)} {e}")
            #return redirect(url_for('login'), errMsg)
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
@app.route('/editMovie/<movieNbr>', methods=[])
def editMovie(movieNbr):
    if 'loggedin' in session:
        eYear = request.form['year']
        eDirector = request.form['director']
        eLength = request.form['length']
        eRating = request.form['rating']
        movieID = movieNbr
        
        query = "UPDATE movie SET releaseYear = %s, director = %s, length = %s, rating = %s WHERE movieID = %s;"
        values = (eYear, eDirector, eLength, eRating, movieID)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('movies'))
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    try:
        # Check if the user is logged in
        if 'loggedin' in session:
            # Remove session data, this will log the user out
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('usrid', None)
            session.pop('newreg', None)
            session.pop('fullname', None)

            # Redirect to login page
            return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    except:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not 'newreg' in session:
        # Output message if something goes wrong...
        msg=''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'fullname' in request.form and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            membername = request.form['fullname']
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            
             # Check if account already exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #cursor.execute('SELECT * FROM member WHERE username = %s', (username,))
            cursor.execute('SELECT memberID, member_name, email, usrid, usrpwd FROM member WHERE usrid = %s OR email = %s', (username, email))
            resultset = cursor.fetchone()
            # If account exists show error and validation checks
            if resultset:
                msg = 'ERROR: Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'ERROR: Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'ERROR: Username must contain only letters and numbers!'
            elif not username or not password or not email:
                msg = 'ERROR: Please fill out the form!'
            else:
                # Hash the password
                #hash = password + app.secret_key
                #hash = hashlib.sha1(hash.encode())
                #password = hash.hexdigest()
                # Account doesn't exist, and the form data is valid, so insert the new account into the accounts table
                cursor.execute('INSERT INTO member (member_name, email, usrid, usrpwd) VALUES (%s, %s, %s, %s);', (membername, email, username, password))
                mysql.connection.commit()
                session['newreg'] = True
                msg = 'SUCCESS: You have successfully registered! Enter your details to log in'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Go back to login.html page
        return render_template('register.html', msg=msg)
    # end if
    else:
        msg = 'Your account has already been registered. Please log in.'
        return render_template('login.html', msg=msg)
        
# end method

@app.route('/discussion/<movieNbr>')
def discussion(movieNbr):
    # Check if the user is logged in
    if 'loggedin' in session:
        msg = ''
        if request.method == 'GET':
            movieID = movieNbr
            session['movie_id'] = movieNbr
            # SQL query to fetch discussion for a particular movie
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT usrid, comments, commentDate, discussionID FROM discussion INNER JOIN member ON discussion.memberID = member.memberID WHERE discussion.movieID = %s', (movieID,))
            #cursor.execute('SELECT member.usrid, discussion.comments, movie.movieID, movie.title FROM discussion INNER JOIN member ON discussion.memberID = member.memberID INNER JOIN movie ON discussion.movieID = movie.movieID WHERE movie.movieID = %s', (movieID,))
            data = cursor.fetchall()
            cursor.close()
            return render_template('discussion.html', data=data, movieNbr=movieID)
        else:
            print("Invalid HTTP request")
    else:
        return render_template('login.html')
@app.route("/")
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # username=session['username']
        return redirect(url_for('movies'))
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))

@app.route('/comment', methods=['POST'])
def comment():
    #check if user is logged in
    if 'loggedin' in session:
        # display message if an error occurs
        msg = ''
        # Check if method == POST and there is a comment entry
        if request.method == 'POST' and 'entry' in request.form:
            
            # Check if inputs exist, else print error
            if not 'entry' in request.form:
                msg+="No message in comment entry.\n"
                # msg+="No movieID in session.\n"
            if not 'id' in session:
                msg+="No memberID in session.\n"
            if len(msg) == 0:

                # Create variables for easy access
                entry = request.form['entry']
                movieID = session['movie_id']
                movieID = str(movieID)
                memberID = session['id']
                memberID = str(memberID)
                cursor = mysql.connection.cursor()
                comment_date = datetime.now()
                comment_date = comment_date.strftime("%d-%b-%Y")

                #sql query and values
                query = "INSERT INTO ghibli.discussion (commentDate, comments, memberID, movieID) VALUES (%s, %s, %s, %s);"
                values = (comment_date, entry,memberID,movieID)
                print(session['usrid'])
                # executing query
                cursor.execute(query, values)
                mysql.connection.commit()
                # close sql cursor
                cursor.close()
                # Returns updated page with new comment
                return redirect(url_for('discussion', movieNbr=movieID))
            else:
                # All errors are returned to website
                return (msg)
        else:
            # No comment entered
            msg = 'No comment has been entered!'
        return (msg)
    else:
     # User returns to log-in
     return redirect(url_for('login'))

#-----------------------------------------------------------------------------
@app.route('/updateComment/<discussionID>', methods=['POST'])
def updateComment(discussionID):
    if 'loggedin' in session:
        if request.method == 'POST' and 'newComment' in request.form:
            #create variables
            entry = request.form['newComment']
            movieID = session['movie_id']
            discussionID = discussionID
            comment_date = datetime.now()
            comment_date = comment_date.strftime("%d-%b-%Y")

            query = "UPDATE discussion SET comments = %s, commentDate = %s WHERE discussionID = %s;"
            values = (entry, comment_date, discussionID)

            cursor = mysql.connection.cursor()
            cursor.execute(query, values)
            mysql.connection.commit()

            cursor.close()

            return redirect(url_for('discussion', movieNbr=movieID))
        else:
            return("Invalid request")
    else:
        return redirect(url_for('login'))
#-----------------------------------------------------------------------------
@app.route('/deleteComment/<discussionID>', methods=['POST', 'GET'])
def deleteComment(discussionID):
    if 'loggedin' in session:
        if request.method == 'POST':
            #create variables
            movieID = session['movie_id']
            discussionID = discussionID
            comment_date = datetime.now()
            comment_date = comment_date.strftime("%d-%b-%Y")

            query = "DELETE FROM discussion WHERE discussionID = %s;"
            values = (discussionID,)
            print(discussionID)

            cursor = mysql.connection.cursor()
            cursor.execute(query, values)
            mysql.connection.commit()

            cursor.close()

            return redirect(url_for('discussion', movieNbr=movieID))
        else:
            return("Invalid request")
    else:
        return redirect(url_for('login'))

#-----------------------------------------------------------------------------
def main():
    app.run(debug=True)

# end main() method
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------------