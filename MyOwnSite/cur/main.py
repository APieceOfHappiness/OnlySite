from flask import Flask, render_template, request, session, redirect, make_response
import sqlite3
import os
import pdfkit

app = Flask(__name__, static_folder='src_data', static_url_path='/')
app.config['SECRET_KEY'] = os.urandom(20).hex()


@app.route("/user/<string:login_>/resume", methods=['POST', 'GET'])
def resume(login_):
    if session.get('login') is not None and session['login'] == login_:
        db = sqlite3.connect('./cur/databases/users.db')
        cur = db.cursor()
        cur.execute('SELECT * FROM saved_forms WHERE login=?', [login_])
        saved_form = cur.fetchone()

        sex = saved_form[1] if saved_form[1] is not None else ""
        date = saved_form[2] if saved_form[2] is not None else ""
        profile = saved_form[3] if saved_form[3] is not None else ""
        truth = saved_form[4] if saved_form[4] is not None else False
        coffee = saved_form[5] if saved_form[5] is not None else False
        not_coffee = saved_form[6] if saved_form[6] is not None else False
        additional_info = saved_form[7] if saved_form[7] is not None else ""
        html = render_template('/resume.html', login=login_, sex=sex, date=date, profile=profile, truth=truth,
                               coffee=coffee, not_coffee=not_coffee, additional_info=additional_info)
        if request.method == "POST":
            print('smth')
            pdf = pdfkit.from_string(html, False)
            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = "inline; filename=MyResume"
            return response
        return html


@app.route("/user/<string:login_>", methods=["POST", "GET"])
def user(login_):
    if session.get('login') is not None and session['login'] == login_:
        db = sqlite3.connect('./cur/databases/users.db')
        cur = db.cursor()
        if request.method == "POST":
            sex = request.form.get('sex')
            date = request.form.get('date')
            profile = request.form.get('profile')
            additional_info = request.form.get('additional_info')
            truth = request.form.get('truth')
            coffee = {'coffee': request.form.get('coffee'), 'not_coffee': request.form.get('not_coffee')}
            cur.execute('DELETE FROM saved_forms WHERE login=?', [login_])
            cur.execute('INSERT INTO saved_forms VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                        [login_, sex, date, profile, truth, coffee['coffee'], coffee['not_coffee'], additional_info])
            db.commit()
        cur.execute('SELECT * FROM saved_forms WHERE login=?', [login_])
        saved_form = cur.fetchone()
        if saved_form:
            sex = saved_form[1] if saved_form[1] is not None else ""
            date = saved_form[2] if saved_form[2] is not None else ""
            profile = saved_form[3] if saved_form[3] is not None else ""
            truth = saved_form[4] if saved_form[4] is not None else False
            coffee = saved_form[5] if saved_form[5] is not None else False
            not_coffee = saved_form[6] if saved_form[6] is not None else False
            additional_info = saved_form[7] if saved_form[7] is not None else ""
            return render_template('/user.html', login=login_, sex=sex, date=date, profile=profile, truth=truth,
                                   coffee=coffee, not_coffee=not_coffee, additional_info=additional_info)
        db.commit()
        db.close()
        return render_template('/user.html', sex="")
    else:
        return "You do not have enough permissions"


@app.route("/login", methods=["POST", "GET"])
def login():
    message = ""
    login = ""
    password = ""
    if request.method == "POST":
        login = request.form.get('username')
        password = request.form.get('password')
        if len(login) > 0:
            db = sqlite3.connect("./cur/databases/users.db")
            cur = db.cursor()
            cur.execute("SELECT * FROM users WHERE login = ?", [login])
            saved_user = cur.fetchone()
            db.close()
            if saved_user is not None and saved_user[1] == password:
                message = 'CONGRATS'
                session['login'] = login
                return redirect('/user/' + login)
            else:
                message = 'Password or login are incorrect'
    session['login'] = None
    return render_template('/login.html', message=message)


@app.route("/")
def main_page():
    return render_template('/main_page.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    message = ""
    password_1 = ""
    password_2 = ""
    if request.method == "POST":
        username = request.form.get('username')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
    if len(password_1) > 0 and password_2 == password_1:
        message = "You have been registered"
        db = sqlite3.connect('./cur/databases/users.db')
        cur = db.cursor()
        cur.execute("INSERT INTO users VALUES(?, ?)", (username, password_1))
        db.commit()
        db.close()

    elif len(password_1) > 0 or len(password_2) > 0:
        message = "incorrect password"
    return render_template('/register.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
