from flask import Flask,render_template,request,redirect,flash
import pymysql as ps
import datetime

#DATABASE CCONNECCTION
con=ps.connect(host="localhost",user="root",password="h13143m17",database="hotel",cursorclass=ps.cursors.DictCursor)
cursor=con.cursor()

app=Flask(__name__)#DEFINING

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

#EMPLOYEE MANAGEMENT

#EMPLOYEE MANAGEMENT INTRO PAGE HERE THE EMPLOYEE'S DETAILS ARE PRESENT
@app.route('/empinfo',methods=['POST','GET'])
def empinfo():
    cursor.execute("select * from employee")
    datas=cursor.fetchall()
    return render_template("employee.html",infos=datas)

# ADD EMPLOYEE TO THE DATABASE
@app.route('/add_emp',methods=['POST','GET'])
def add_emp():
    if request.method== 'POST':
        try:
            n=request.form["name"]
            i=int(request.form["id"])
            d=request.form["doj"]
            j=request.form["job"]
            a=request.form["addr"]
            s=int(request.form["sal"])
            b=request.form["bank"]
            acc=int(request.form["accno"])
            m=int(request.form["mobile"])
            t=request.form["shift"]
            cursor.execute(f"insert into employee values({i},'{n}','{a}',{s},'{d}','{j}','{t}',{m},{acc},'{b}')")
            con.commit()
            flash("Record Added Successfully.")
        except:
            flash("Record Does Not Added.")
        return redirect("/empinfo")
    return render_template("add_emp.html")

# EDIT THE EMPLOYEE DETAILS
@app.route("/edit_emp/<int:id>",methods=['POST','GET'])
def edit_emp(id):
    if request.method== 'POST':
        try:
            n=request.form["name"]
            i=int(request.form["id"])
            d=request.form["doj"]
            j=request.form["job"]
            a=request.form["addr"]
            s=int(request.form["sal"])
            b=request.form["bank"]
            acc=int(request.form["accno"])
            m=int(request.form["mobile"])
            t=request.form["shift"]
            cursor.execute(f"update employee set eid={i},ename='{n}',eadd='{a}',esalary={s},edoj='{d}',ejob='{j}',ebank='{b}',eaccno={acc},emobile={m},eshift='{t}' where eid={id}")
            con.commit()
            flash("Record Updated Successfully")
        except:
            flash("Record Does Not Updated.")
        return redirect("/empinfo")
    cursor.execute(f"select * from employee where eid={id}")
    res=cursor.fetchone()
    return render_template("edit_emp.html",infos=res)

# DELETEING THE EMPLOYEE DETAILS
@app.route("/delete_emp/<int:id>",methods=['POST','GET'])
def delete_emp(id):
    try:
        cursor.execute(f"delete from employee where eid={id}")
        con.commit()
    except:
        print("delete error")
    return redirect("/empinfo")

# SEARCH THE EMPLOYEE 
@app.route("/search_emp",methods=['POST','GET'])
def search_emp():
    if request.method=='POST':
        try:
            find=int(request.form.get("find"))
            print(find)
            cursor.execute(f"select * from employee where eid={find}")
            s_res=cursor.fetchone()
            return render_template("employee.html",infos=[s_res])
        except:
            flash("Record Not Found or Invalid ID.")
            return redirect("/empinfo")
        
#CUSTOMER MANAGEMENT 

#CUSTOMER MANAGEMENT INTRO PAGE HERE THE EMPLOYEE'S DETAILS ARE PRESENT
@app.route('/custinfo',methods=['POST','GET'])
def custinfo():
    cursor.execute("select * from customer where cbill is null")
    datas=cursor.fetchall()

    return render_template("customer.html",infos=datas)

#CUSTOMER CHECKIN FORM 
@app.route('/add_cust',methods=['POST','GET'])
def add_cust():
    if request.method== 'POST':
        try:
            n=request.form["name"]
            r=int(request.form['id'])
            a=request.form['addr']
            m=int(request.form['mobile'])
            ci=request.form['checkin']
            mem=int(request.form['member'])
            vid=request.form['vid']
            vidtype=request.form['idtype']
            cursor.execute(f"insert into customer (cid,cname,cadd,cmember,ccheckin,cmobile,vid,vidtype) values({r},'{n}','{a}',{mem},'{ci}',{m},'{vid}','{vidtype}')")
            con.commit()
            flash("Record Added Successfully")
        except:
            flash("Something Wrong Record Dose not Added.")
        return redirect('/custinfo')
    return render_template("add_cust.html")

#SEARCHING OF CUSTOMER
@app.route("/search_cust",methods=['POST','GET'])
def search_cust():
    if request.method=='POST':
        try:
            find=request.form.get("find")
            cursor.execute(f"select * from customer where vid='{find}'")
            s_res=cursor.fetchone()
            if s_res==None:
                flash("Record Not Found or invalid ID")
                return redirect("/custinfo")
            else:
                return render_template("customer.html",infos=[s_res])
        except:
            pass

#CUSTOMER CHECKOUT AND BILL HERE CHANGES ARE BEEN DONE BY HERE ACCORDING TO AMOUNT
@app.route('/checkout_cust/<string:vno>',methods=['POST','GET'])
def checkout_cust(vno):
    oneday=500
    now=datetime.datetime.now()
    try:
        cursor.execute(f"select ccheckin,cbill from customer where vid='{vno}'")
        cdate=cursor.fetchone()#checken date
        if cdate['cbill']==None:
            today=now.strftime("20%y-%m-%d")
            checkindate=datetime.date(int(cdate["ccheckin"][:4]),int(cdate["ccheckin"][5:7]),int(cdate["ccheckin"][8:]))
            checkoutdate=datetime.date(int(today[:4]),int(today[5:7]),int(today[8:]))
            dayscount=checkoutdate-checkindate
            no_of_days=dayscount.days
            bill=oneday*no_of_days
            cursor.execute(f"update customer set ccheckout='{today}',cbill={bill} where vid='{vno}'")
            con.commit()
        return redirect("/custinfo")
    except:
        pass
    return redirect("/custinfo")
if __name__=="__main__":
    app.secret_key="admin480"
    app.run(debug=True)