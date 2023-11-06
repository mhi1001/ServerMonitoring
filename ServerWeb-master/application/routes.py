import sys
import jsonpickle
from .ilo_server_class import Server_Ilo
from dataclasses import dataclass
from application import app, db
from flask import render_template, redirect, request, json, Response, flash, url_for, session
from application.models import User
from application.forms import LoginForm, RegisterForm
from datetime import timedelta

@dataclass
class Server:
        serialNo: str
        ipAddress: str
        powerPresent: str
        powerMin: str
        powerAverage: str
        powerMax: str
        upTime: str
        productName: str
        powerStatus: str
# Currently reads a json file.
# Future, it will receive a range of IP addresses and then try to get info via Ilo when on a live system.
def get_all_servers(mode, ips=[]):
    
    svr_list = []

    if mode == "ilo":
        
        for ip in ips:

            Server_Ilo(ip, "admin", "admin")
            power = Server_Ilo.get_power_reading()
            svr = Server(Server_Ilo.get_serial_no(),
            ip, 
            power[1],#present 
            power[2],#min 
            power[0],#avg 
            power[3],#max 
            Server_Ilo.get_uptime(), 
            Server_Ilo.get_prod_name(), 
            Server_Ilo.get_host_power_status())

            svr_list.append(svr)

    elif mode == "test":

        with open("application\static_servers.json") as fh:
            data = fh.read()

        server_dict = json.loads(data)

        for server in server_dict.values():   
            svr = Server(
                server["serialNo"],
                server["ipAddress"], 
                server["powerPresent"], 
                server["powerMin"], 
                server["powerAverage"], 
                server["powerMax"], 
                server["upTime"], 
                server["productName"], 
                server["powerStatus"]
                )

            svr_list.append(svr)
    
    return svr_list

# Populate server list
server_list = get_all_servers("test")

#create route to run the app
@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    #return "<h1>Welcome!</h1>"
    return render_template("index.html", index = True)    

@app.route("/servers", methods = ['GET', 'POST'])
def servers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == "POST":
        if request.form["action-button"] == "start":
            id = request.form["serialNo"]

            for server in server_list:
                if server.serialNo == id:
                    print(f"found server: {server.productName} s:n: {server.serialNo}")
                    print("STARTING IT")
                    index = server_list.index(server)
                    server_list[index].powerStatus = "ON"
                    break
                    
            return render_template("servers.html", serverData=server_list, servers = True)             
            
        elif request.form["action-button"] == "stop":
            id = request.form["serialNo"]
            
            for server in server_list:
                if server.serialNo == id:
                    print(f"found server: {server.productName} s:n: {server.serialNo}")
                    print("POWERING OFF")
                    index = server_list.index(server)
                    server_list[index].powerStatus = "OFF"
                    break
            server_list[0].powerStatus = "OFF"           
            return render_template("servers.html", serverData=server_list, servers = True) 

    return render_template("servers.html", serverData=server_list, servers = True)    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.objects(email = email).first()
        if user and user.get_password(password):
            session['logged_in'] = True
            #session expire after 5 minutes of inactivity
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=5)

            flash(f"{user.first_name}, you have successfully logged in!", "success")
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.","danger")
    return render_template("login.html", title = "Login", form = form, login = True)    

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You have registered successfully!", "success")
        
        return redirect(url_for('index'))

    return render_template("register.html", title = "Register", form = form, register = True)   

# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if(idx == None):
#         jdata = serverData
#     else:
#         jdata = serverData[int(idx)]
    
#     return Response(json.dumps(jdata), mimetype="application/json") 

@app.route("/user")
def user():
    users = User.objects.all()
    return render_template("user.html", users = users)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))