
from flask import *

import databaseModel
from functools import wraps
import time

bp = Blueprint("StaffPage", __name__, url_prefix='/StaffPage')


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



@bp.route("/OrderToStore",methods=["POST"])
@login_required
def OrderToStore():

    try:
        OrderNum =  request.form["OrderNum"]
        method  = request.form["way"]
        order = databaseModel.Orders.query.filter_by(OrderNum = OrderNum).first()
        if(order != None):
            if(method == "inStore"):   #如果是入库操作
                neworder_ = databaseModel.HistoryOrders(OrderNum=OrderNum, StaffNum=g.UserName)     #像historyorder表里添加一行，表示该快递员经手过这个快递
                databaseModel.db.session.add(neworder_)

                orderstaff_ = databaseModel.OrderStaffs.query.filter_by(OrderNum=OrderNum).first()  #修改orderstaff 表的staffnum，表示当前快递已更换配送者
                orderstaff_.StaffNum = g.UserName
                databaseModel.db.session.commit()
            if(method == "sigh"):     #如果是签收操作
                order_ = databaseModel.Orders.query.filter_by(OrderNum=OrderNum).first()
                order_.StagNum = 2       #更改为已签收
                neworder_ = databaseModel.HistoryOrders(OrderNum=OrderNum, StaffNum=g.UserName)  # 像historyorder表里添加一行，表示该快递员经手过这个快递
                databaseModel.db.session.add(neworder_)
                orderstaff_ = databaseModel.OrderStaffs.query.filter_by(OrderNum=OrderNum).first()  # 修改orderstaff 表的staffnum，表示当前快递已更换配送者
                orderstaff_.StaffNum = "0"

                databaseModel.db.session.commit()
    except Exception as e:
        return {"code":"0"}

    return {"code":"200"}



@bp.route("/HistoryOrders",methods=["GET"])
@login_required
def HistoryOrders():

    historyorders = databaseModel.HistoryOrders.query.filter_by(StaffNum= g.UserName).all()
    jsondata = {}
    for i,c in enumerate(historyorders):
        ordernum_ = c.OrderNum
        order = databaseModel.Orders.query.filter_by(OrderNum=ordernum_).first()
        recvaddr_ = order.RecvAddr
        if(order.StagNum == 1):
            orderstag_ = '已寄出'
        if(order.StagNum == 2):
            orderstag_ = "已签收"
        data = {"OrderNum":ordernum_,"RecvAddr":recvaddr_,"OrderStag":orderstag_}
        jsondata[i] = data

    return jsondata


@bp.route("/StaffInfo",methods=["POST"])
@login_required
def StaffInfo():
    try:
        staffinfo  = databaseModel.Staffs.query.filter_by(UserName=g.UserName).first()
        jsondata = {}
        StaffName =staffinfo.StaffName
        StaffNum  = staffinfo.UserName
        StaffTele = staffinfo.StaffTele
        StaffIdCard = staffinfo.StaffIdCard

        print(StaffIdCard,StaffName)


        jsondata["code"] = "1"
        jsondata["StaffName"]= StaffName
        jsondata["StaffNum"] = StaffNum
        jsondata["StaffTele"] = StaffTele
        jsondata["StaffIdCard"] = StaffIdCard
    except Exception as e:
        current_app.logger.debug(e)
        return {"code":"0"}
    return jsondata

