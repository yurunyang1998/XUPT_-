
from flask import *
from werkzeug.security import check_password_hash, generate_password_hash
import databaseModel
from functools import wraps
import time

bp = Blueprint('AdminPage', __name__, url_prefix='/AdminPage')


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



@bp.route("/ViewOrders",methods=["POST","GET"])
@login_required
def ViewOrders():
    AllOrders = databaseModel.Orders.query.all()
    jsondata = {}
    for c, i in enumerate(AllOrders):
        try:
            OrderNum = i.OrderNum
            SendName = i.SendName
            SendAddr = i.SendAddr
            RecvName = i.RecvName
            RecvAddr = i.RecvAddr
            RecvTele = i.RecvTele
            StagNum = i.StagNum
            Price = i.Price
            Comment = i.Comment
            CityNum = i.CityNum

            StagName = databaseModel.OrderStag.query.filter_by(StagNum = StagNum).first().StagName
            CityName = databaseModel.Cities.query.filter_by(CityNum = CityNum).first().CityName

            order = {"OrderNum":OrderNum,"SendName":SendName,"SendAddr":SendAddr,
                     "RecvName":RecvName,"RecvAddr":RecvAddr,"RecvTele":RecvTele,
                     "StagName":StagName,"CityName":CityName,"Price":str(Price),"Comment":Comment}

            jsondata[c]=order
        except Exception as e:
            current_app.logger.debug(e)

    return jsondata



@bp.route("/ViewStaffs",methods=["GET"])
@login_required
def ViewStaffs():
    AllStaffs = databaseModel.Staffs.query.all()
    jsondata = {}
    for i, c in enumerate(AllStaffs):
        try:
            StaffNum = c.UserName
            StaffName = c.StaffName
            StaffTele = c.StaffTele
            if( StaffNum == "0"):   #编号为0的员工为暂无
                continue
            staff = {"StaffNum":StaffNum,"StaffName":StaffName,
                     "StaffTele":StaffTele}
            jsondata[i] = staff
        except Exception as e:
            current_app.logger.debug(e)

    return jsondata




@bp.route("/DeleteStaff",methods=["POST"])
@login_required
def DeleteStaff():
    try:
        StaffNum = request.get_json("StaffNum")["StaffNum"]

        staffdel = databaseModel.Staffs.query.filter_by(UserName=StaffNum).first()
        databaseModel.db.session.delete(staffdel)
        databaseModel.db.session.commit()

    except Exception as e:
        current_app.logger.debug(e)
        return "0"

    return {"code":"1"}


@bp.route("/AddStaff",methods=["POST"])
@login_required
def AddStaff():
    try:
        StaffNum = request.form["StaffNum"]
        StaffName = request.form["StaffName"]
        StaffTele = request.form["StaffTele"]
        StaffIdCard = request.form["StaffIdCard"]
        PassWord = request.form["PassWord"]

        newstaff = databaseModel.Staffs(UserName = StaffNum,
                                        StaffTele = StaffTele,
                                        StaffIdCard = StaffIdCard,
                                        PassWord = PassWord,
                                        StaffName = StaffName
                                        )

        databaseModel.db.session.add(newstaff)
        databaseModel.db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        return  "0"
    return {"code":"200"}


@bp.route("/ViewCities", methods=["GET"])
@login_required
def ViewCitied():
    AllAreas = databaseModel.CityArea.query.all()
    jsondata = {}
    for i,c in enumerate(AllAreas):
        AreaNum_ = c.AreaNum
        CityNum_ = c.CityNum
        AreaName_ = databaseModel.Areas.query.filter_by(AreaNum = AreaNum_).first().AreaName
        CityName_ = databaseModel.Cities.query.filter_by(CityNum=CityNum_).first().CityName

        data = {"AreaName":AreaName_,"CityName":CityName_,"CityNum":CityNum_}
        jsondata[i] = data

    return jsondata

@bp.route("/ViewUsers", methods=["POST","GET"])
@login_required
def ViewUsers():
    AllCustomers = databaseModel.Users.query.all()
    jsondata = {}
    try:
        for i,c in enumerate(AllCustomers):
            username = c.UserName
            realyname = c.RealyName
            usertele = c.UserTele
            data = {"UserNum":username,
                    "UserName":realyname,
                    "UserTele":usertele}

            jsondata[i] = data

    except Exception as e:
        current_app.logger.debug(e)
        return {"code":"0"}

    return  jsondata


