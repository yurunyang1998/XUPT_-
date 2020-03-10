
from flask import  *
import logging
# from flask_cors import *
import  databaseModel
import UserPage
import AdminPage
import StaffPage
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import ReadConfig






def CreateApp():
    app = Flask(__name__, static_url_path="")

    app.register_blueprint(UserPage.bp)
    app.register_blueprint(StaffPage.bp)
    app.register_blueprint(AdminPage.bp)

    config = ReadConfig.readconfig("./config.json")

    app.secret_key = config['key_secret']

    app.config['SQLALCHEMY_DATABASE_URI'] = config["databaseAddr"]
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

    return app


app= CreateApp()
db = SQLAlchemy(app)


@app.route('/index',methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/',methods=['GET'])
def index2():
    return redirect(url_for("index"))


@app.route('/Login', methods=['POST'])
def Login():

    username,pwd,role = request.form['username'],request.form['pwd'],request.form['role']
    if(role == 'user'):
        try:
                pwdInData = databaseModel.Users.query.filter_by(UserName=username).first()
                if(pwdInData == None):                        #用户不存在
                    # current_app.logger.info("Logerror")
                    return redirect(url_for("LoginError"))
                if(pwdInData.PassWord == pwd):                 #登录成功
                    current_app.logger.debug("Log success")
                    session['UserName'] = username

                    return  redirect(url_for("UserPage"))

                else:
                        return redirect(url_for("LoginError"))     #密码错误
        except Exception as e:    ## 数据库错误
            current_app.logger.debug(e)

    if(role == 'admin'):
        try:
                pwdInData = databaseModel.Admins.query.filter_by(UserName=username).first()
                if(pwdInData == None):                        #用户不存在
                    # current_app.logger.info("Logerror")
                    return redirect(url_for("LoginError"))
                if(pwdInData.PassWord == pwd):                 #登录成功
                    current_app.logger.debug("Log success")
                    session['UserName'] = username

                    return  redirect(url_for("AdminPage"))

                else:
                        return redirect(url_for("LoginError"))     #密码错误
        except Exception as e:    ## 数据库错误
            current_app.logger.debug(e)

    if(role == 'staff'):
        try:
                pwdInData = databaseModel.Staffs.query.filter_by(UserName=username).first()
                if(pwdInData == None):                        #用户不存在
                    # current_app.logger.info("Logerror")
                    return redirect(url_for("LoginError"))
                if(pwdInData.PassWord == pwd):                 #登录成功
                    current_app.logger.debug("Log success")
                    session['UserName'] = username

                    return  redirect(url_for("StaffPage"))

                else:
                        return redirect(url_for("LoginError"))     #密码错误
        except Exception as e:    ## 数据库错误
            current_app.logger.debug(e)

@app.route('/LogOut')
def LogOut():
    session.pop('UserName', None)
    # return redirect("/index")
    return "200"

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        UserName = session.get('UserName')
        if(UserName is not None):
            g.UserName = UserName
            return func(*args, **kwargs)
        else:
            return redirect(url_for("index"))
    return wrapper

@app.route('/UserPage',methods=["GET","POST"])
@login_required
def UserPage():
    return render_template("userpage.html")


@app.route('/StaffPage',methods=["GET","POST"])
@login_required
def StaffPage():
    return render_template("staffview.html")


@app.route("/AdminPage", methods=["GET","POST"])
@login_required
def AdminPage():
    return render_template("adminview.html")




@app.route("/LoginError")
def LoginError():

    return render_template("LoginError.html")


@app.errorhandler(500)
def error(e):
    return render_template('index.html'), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='80',debug=True)





