
from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
# from index_page import  login_required
import databaseModel
from functools import wraps
import time

bp = Blueprint('UserPage', __name__, url_prefix='/UserPage')


def CreateOrederNum():
    return  time.strftime("%Y%m%d%H%M%S", time.localtime())

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



@bp.route("/TakeOrder", methods=["POST"])
@login_required
def TakeOrder():
    SendName = request.form['SendName']           #从request 表单中获取数据
    SendAddr = request.form["SendAddr"]
    RecvAddr = request.form['RecvAddr']
    RecvName = request.form['RecvName']
    RecvTele = request.form['RecvTele']
    Price    = request.form["Price"]
    Comment  = request.form["Comment"]
    CityName = request.form["CityName"]

    if( SendName and SendAddr and RecvAddr and RecvName and RecvTele and Price ):     #如果这几个数据不为空

        try:
            OrderNum = CreateOrederNum()
            CityNum  = databaseModel.Cities.query.filter_by(CityName=CityName).first().CityNum #根据城市名称查询出城市id
            StagNum = 1

            OrderOne = databaseModel.Orders(OrderNum=OrderNum,        #创建订单数据对象
                                            SendName=SendName,
                                            SendAddr=SendAddr,
                                            RecvName=RecvName,
                                            RecvAddr=RecvAddr,
                                            RecvTele=RecvTele,
                                            StagNum=StagNum,
                                            Price=Price,
                                            Comment=Comment,
                                            CityNum = CityNum)

            databaseModel.db.session.add(OrderOne)        #写入数据库
            databaseModel.db.session.commit()                 #必须先提交一次，因为有外键

            userorder_ = databaseModel.UserOrders(UserName=g.UserName, OrderNum=OrderNum)
            databaseModel.db.session.add(userorder_)
            OrderStaff_ = databaseModel.OrderStaffs(OrderNum= OrderNum,StaffNum ="0")
            databaseModel.db.session.add(OrderStaff_)
            databaseModel.db.session.commit()
            return {"code":"1"}
        except Exception as e:
            current_app.logger.debug(e)

    return {"code":0}

@bp.route("/MyOrders",methods=["POST","GET"])
@login_required
def MyOrders():
    try:
        orders = databaseModel.UserOrders.query.filter_by(UserName=g.UserName).all()
        jsondata ={}
        for i,c in enumerate(orders):
            OrderNum_ = c.OrderNum
            order = databaseModel.Orders.query.filter_by(OrderNum = OrderNum_).first()
            citynum_ = order.CityNum
            cityname_ = databaseModel.Cities.query.filter_by(CityNum=citynum_).first().CityName
            if(order.StagNum == 1):
                finish_ = "已寄出"
            else:
                finish_ = "已签收"
            staffnum_ = databaseModel.OrderStaffs.query.filter_by(OrderNum=OrderNum_).first().StaffNum
            staff = databaseModel.Staffs.query.filter_by(UserName= staffnum_).first()
            staffname_ = staff.StaffName
            stafftell_ = staff.StaffTele

            data_ = {"OrderNum":OrderNum_,
                     "City":cityname_,
                     "finish":finish_,
                     "StaffName":staffname_,
                     "StaffTele":stafftell_}

            jsondata[i] = data_
    except Exception as e:
        current_app.logger.debug(e)

    return jsondata


@bp.route("/CountInfo",methods=["POST","GET"])
@login_required
def CountInfo():
    user_ = databaseModel.Users.query.filter_by(UserName=g.UserName).first()
    username_ = user_.UserName
    realyname_ = user_.RealyName
    usertele_ = user_.UserTele
    data = {"RealyName":realyname_,"UserName":username_,"UserTele":usertele_}
    return jsonify(data)



if __name__ == '__main__':
    CreateOrederNum()
