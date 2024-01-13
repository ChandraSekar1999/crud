from flask import Flask, render_template, url_for, redirect, request, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql server page
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Paramakudi@1999"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

#Loading HOME page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "SELECT * FROM users"
    con.execute(sql)
    res = con.fetchall()
    return render_template("home.html", users=res)

#NEW User
@app.route("/addusers", methods=['GET', 'POST'])
def addusers():
    if request.method == 'POST':
        
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
       
        con = mysql.connection.cursor()
        sql = "insert into users (NAME, CITY, AGE) value (%s, %s, %s)"

        con.execute(sql, [name, city, age])
        mysql.connection.commit()
      
        con.close()
        #USER DETAIL ADDED *****FLASH****** MESSAGE
        flash('User Details Added')
        return redirect(url_for("home"))

    return render_template("addusers.html")



# UPDATE USERS
@app.route("/editusers/<string:id>", methods=['GET', 'POST'])
def editusers(id):
    con = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        sql = "update users set NAME=%s,AGE=%s,CITY=%s where ID=%s"
        con.execute(sql, [name, age, city, id])
        mysql.connection.commit()
        con.close()
        #USER DETAIL UPDATED *****FLASH****** MESSAGE
        flash('User Details Updated')
        return redirect(url_for("home"))

    con = mysql.connection.cursor()
    sql = "select * from users where ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    con.close()
    return render_template("editusers.html", users=res)


#DELETE USERS
@app.route("/deleteuser/<string:id>", methods=['GET', 'POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    #sql = "delete from users where ID=%s"
    #con.execute(sql,id)
    sql = "DELETE FROM users WHERE ID = %s"
    con.execute(sql, (id,))
    mysql.connection.commit()
    con.close()
    #USER DETAIL DELETE *****FLASH****** MESSAGE
    flash('User Details Deleted')
    return redirect(url_for("home"))
    
    
if __name__ == '__main__':
    app.secret_key="abc123"
    #app.run(debug=True)
    app.run(debug=False,host='0.0.0.0')
    
