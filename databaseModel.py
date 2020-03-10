# Created by GuoXin

from index_page import db


class Users(db.Model):
    __tablename__ = "Users"

    UserName = db.Column(db.String(20), primary_key=True)
    RealyName = db.Column(db.String(20))
    UserTele = db.Column(db.String(11))
    PassWord = db.Column(db.String(25))
    RoleNum = db.Column(db.INT)


class Staffs(db.Model):
    __tablename__ = "Staffs"
    UserName = db.Column(db.INT, primary_key=True)
    StaffName = db.Column(db.String(20))
    StaffIdCard = db.Column(db.String(18))
    StaffTele = db.Column(db.String(11))
    PassWord = db.Column(db.String(20))


class UserOrders(db.Model):
    __tablename__ = "UserOrders"

    UserName = db.Column(db.String(20),db.ForeignKey("Users.UserName"))
    OrderNum = db.Column(db.String(30),db.ForeignKey("Orders.OrderNum"),primary_key=True)


class HistoryOrders(db.Model):
    __tablename__ = "HistoryOrders"
    id = db.Column(db.INT,primary_key=True,autoincrement=True)
    OrderNum = db.Column(db.String(20),db.ForeignKey("Orders.OrderNum"))
    StaffNum = db.Column(db.String(20),db.ForeignKey("Staffs.UserName"))



class Roles(db.Model):
    __tablename__ = "Roles"
    RoleNum = db.Column(db.INT, primary_key=True)
    RoleName = db.Column(db.String(20))
    RoleRight = db.Column(db.String(50))


class Orders(db.Model):
    __tablename__ = "Orders"
    OrderNum = db.Column(db.String(30), primary_key=True)
    SendName = db.Column(db.String(20))
    SendAddr = db.Column(db.String(50))
    RecvName = db.Column(db.String(20))
    RecvAddr = db.Column(db.String(50))
    RecvTele = db.Column(db.String(11))
    StagNum = db.Column(db.INT)
    Price = db.Column(db.DECIMAL)
    Comment = db.Column(db.String(200))
    CityNum = db.Column(db.INT)

class OrderStaffs(db.Model):
    __tablename__ = "OrderStaffs"
    OrderNum = db.Column(db.String(30),db.ForeignKey("Orders.OrderNum"), primary_key=True)
    StaffNum = db.Column(db.INT, db.ForeignKey("Staffs.UserName"))



class OrderStag(db.Model):
    __tablename__ = "OrderStag"
    StagNum = db.Column(db.INT, primary_key=True)
    StagName = db.Column(db.String(15))


class CityArea(db.Model):
    __tablename__ = "CityArea"
    AreaNum = db.Column(db.INT, primary_key=True)
    CityNum = db.Column(db.INT)


class Cities(db.Model):
    __tablename__ = "Cities"
    CityNum = db.Column(db.INT, primary_key=True)
    CityName = db.Column(db.String(20))


class Areas(db.Model):
    __tablename__ = "Areas"
    AreaNum = db.Column(db.INT, primary_key=True)
    AreaName = db.Column(db.String(20))


class Admins(db.Model):
    __tablename__ = "Admins"
    UserName = db.Column(db.String(10),primary_key=True)
    PassWord = db.Column(db.String(20))