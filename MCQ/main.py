from flask import Flask,render_template,request,redirect,flash
import pymysql as ps
import random
import time
from datetime import datetime

try:
    con=ps.connect(host="localhost",user="root",password="h13143m17",database="MCQTEST",cursorclass=ps.cursors.DictCursor)
    cursor=con.cursor()
except:
    print("Error")

warning ="rgb(255, 80, 80)"
alert="rgb(255, 162, 48)"
success="rgb(111, 255, 85)"
user_id = 0
user_name = "guest"

app=Flask(__name__)

@app.route('/')
@app.route('/login')
def index():    
    return render_template("loginPage.html")

@app.route('/logout')
def logout():
    global user_id,user_name
    user_name = "guest"
    user_id = 0
    return redirect('login')
@app.route('/login_verify',methods=['POST','GET'])
def login_verify():
    global user_id,user_name
    if request.method == 'POST':
        EMAIL = request.form['EMAIL']
        PASSWORD = request.form['PASSWORD']
        try:
            cursor.execute(f"select * from USERS where USER_MAIL = '{EMAIL}'")
            DATA = cursor.fetchone()
            if DATA['USER_PASSWORD'] == PASSWORD:
                user_id = DATA['ID']
                user_name = DATA['USER_NAME']
                flash("Successfully Entered.",success)
            else:
                flash("Incorrect Password.",warning)
                return redirect('/login')
        except:
            flash("No Data Found Please Signup.",alert)
            return redirect('/login')
    return redirect('/home_page')

@app.route('/signup_verify',methods=['POST','GET'])
def signup_verify():
    global user_id,user_name
    if request.method == 'POST':
        USERNAME = request.form['USERNAME']
        EMAIL = request.form['EMAIL']
        PASSWORD = request.form['PASSWORD']
        try:
            cursor.execute(f"select * from USERS where USER_MAIL = '{EMAIL}'")
            DATA = cursor.fetchone()
            if DATA != None:
                flash("You have an account please Login.",alert)
            else:
                try:
                    cursor.execute(f"INSERT INTO USERS (USER_NAME,USER_PASSWORD,USER_MAIL) VALUES('{USERNAME}','{PASSWORD}','{EMAIL}');")
                    con.commit()
                    cursor.execute(f"SELECT ID,USER_NAME FROM USERS WHERE USER_MAIL = '{EMAIL}'")
                    USER_DATA = cursor.fetchone()
                    user_id = USER_DATA['ID']
                    user_name = USER_DATA['USER_NAME']
                    flash("Successfully Entered.",success)
                except:
                    flash("Server Down Please Try Again!",warning)
                    return redirect('/login')
        except:
            flash("Server Error.",alert)
            return redirect('/login')
    return redirect('/home_page')


@app.route('/home_page')
def home_page():
    try:
        cursor.execute(f"SELECT * FROM USERS WHERE ID = {user_id}")
        DATA = cursor.fetchone()
        cursor.execute(f"SELECT * FROM TESTS WHERE USER_ID = {user_id}")
        TEST_DATA = cursor.fetchall()
        cursor.execute(f"SELECT TEST_ID FROM LEADERBOARD WHERE USER_ID = {user_id}")
        ATTENDED_TESTS = cursor.fetchall()
        return render_template("homePage.html",info = DATA,test_infos = TEST_DATA, attended_tests = ATTENDED_TESTS)
    except Exception as e:
        # print(e)
        flash("Server Error, Try Again",alert)
        return redirect('/login')

@app.route('/delete_test/<string:code>')
def delete_test(code):
    try:
        cursor.execute(f"DELETE FROM TESTS WHERE ID='{code}'")
        con.commit()
        flash("Test Deleted Successfully.",success)
    except:
        flash("Delete test error. try again",warning)
    return redirect('/home_page')

@app.route('/delete_question/<int:test_id>/<string:code>')
def delete_question(test_id,code):
    try:
        cursor.execute(f"DELETE FROM QUESTIONS WHERE ID = {test_id}")
        con.commit()
    except:
        flash("Deletion error Try again.",warning)
    return redirect(f"/test_edit/{code}")

@app.route('/test_edit/<string:code>',methods=['POST','GET'])
@app.route('/test_edit')
def test_edit(code=None):
    CODE = ""
    TEST_DATA = {}
    if code == None:
        try:
            cursor.execute(f"SELECT COUNT(ID) AS TOTAL FROM TESTS WHERE USER_ID = {user_id}")
            tot = cursor.fetchone()
            if (tot['TOTAL']) < 2:
                for i in range(6):
                    CODE += chr(random.randint(65,90))
                try:
                    cursor.execute(f"INSERT INTO TESTS (ID,USER_ID) VALUES('{CODE}',{user_id});")
                    con.commit()
                    flash("Write Your Questions.",success)
                except:
                    flash("Server Error.",warning)
                    return redirect('/home_page')
            else:
                flash("You can create only 2 tests.",warning)
                return redirect('/home_page')
        except:
            pass
    else:
        CODE = code
        try:
            cursor.execute(f"SELECT * FROM TESTS WHERE ID = '{CODE}'")
            TEST_DATA = cursor.fetchone()
        except:
            flash("Server Erroe.",alert)
            return redirect('/home_page')
    QUESTION_DATA = []
    try:
        if CODE:
            cursor.execute(f"SELECT * FROM QUESTIONS WHERE TEST_ID = '{CODE}'")
        else:
            cursor.execute(f"SELECT * FROM QUESTIONS WHERE ID = 1")
        QUESTION_DATA = cursor.fetchall()
    except:
        pass
    if request.method == 'POST':
        TITLE = request.form['title']
        START_TIME = request.form['starttime']
        END_TIME = request.form['endtime']
        DESCRIPTION = request.form['description']
        QUESTION = request.form.getlist('question[]')
        OPTION1 = request.form.getlist('option1[]')
        OPTION2 = request.form.getlist('option2[]')
        OPTION3 = request.form.getlist('option3[]')
        OPTION4 = request.form.getlist('option4[]')
        CORRECT = request.form.getlist('correct[]')
        SCORE = request.form.getlist('score[]')
        NEGATIVE_SCORE = request.form.getlist('negative_score[]')
        for neg in NEGATIVE_SCORE:
            if neg == '':
                NEGATIVE_SCORE[NEGATIVE_SCORE.index(neg)] = 0
        QUESTION_ID = request.form.getlist('questionid')
        # print(QUESTION_ID,"\n",CODE,"\n",TITLE,"\n",DESCRIPTION,"\n",START_TIME,"\n",END_TIME,"\n",QUESTION,"\n",OPTION1,"\n",OPTION2,"\n",OPTION3,"\n",OPTION4,"\n",SCORE,"\n",NEGATIVE_SCORE)
        try:
            cursor.execute(f"UPDATE TESTS SET TEST_TITLE='{TITLE}', TEST_DESCRIPTION='{DESCRIPTION}', START_TIME='{START_TIME}', END_TIME='{END_TIME}' WHERE ID = '{code}'")
            con.commit()
            #   TESTEDIT LA ERUNTHU QUESTIONS VARUM ATHA NE QUESTIONS DB LA INSERT PANNANUM DA AVLOTHA OK
            for i in range(len(QUESTION)):
                if(QUESTION_ID[i] == ''):
                    QUESTION_ID[i]=0
                try:
                    cursor.execute(f"INSERT INTO QUESTIONS (ID,TEST_ID,QUESTION,OPTION1,OPTION2,OPTION3,OPTION4,CORRECT,SCORE,NEG_SCORE) VALUES({int(QUESTION_ID[i])},'{CODE}','{QUESTION[i]}','{OPTION1[i]}','{OPTION2[i]}','{OPTION3[i]}','{OPTION4[i]}','{CORRECT[i]}',{int(SCORE[i])},{int(NEGATIVE_SCORE[i])}) ON DUPLICATE KEY UPDATE TEST_ID = '{CODE}',QUESTION = '{QUESTION[i]}',OPTION1 = '{OPTION1[i]}',OPTION2 = '{OPTION2[i]}',OPTION3 = '{OPTION3[i]}',OPTION4 = '{OPTION4[i]}',CORRECT = '{CORRECT[i]}',SCORE = {int(SCORE[i])},NEG_SCORE = {int(NEGATIVE_SCORE[i])}")
                    con.commit()
                except Exception as e:
                    print(e)
            return redirect(f"/test_edit/{CODE}")
        except:
            pass
    return render_template("testEdit.html",test_code = CODE,infos=QUESTION_DATA,test_detail = TEST_DATA, name=user_name)
# ________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

total_questions = 0
begin = 0
stop =0
@app.route('/test_atten',methods=['POST','GET'])
@app.route('/test_atten/<string:code>/<int:mode>')
def test_atten(code=None,mode=0):
    global total_questions,begin
    if request.method == 'POST':
        TESTCODE =request.form['TESTCODE']
        today = datetime.now()
        try:
            cursor.execute(f"SELECT * FROM TESTS WHERE ID = '{TESTCODE}'")
            TESTDATAS = cursor.fetchone()
            cursor.execute(f"SELECT USER_ID FROM LEADERBOARD WHERE TEST_ID = '{TESTCODE}' AND USER_ID = {user_id}")
            permission = cursor.fetchall()
            if(len(permission))!=0:
                flash("You already attended this test,check leaderboard.",alert)
                return redirect('/home_page')
            if len(TESTDATAS)==0:
                flash("No test Found!",warning)
                return redirect('/home_page')
            else:
                start_time = datetime.strptime(TESTDATAS['START_TIME'],"%Y-%m-%dT%H:%M")
                end_time = datetime.strptime(TESTDATAS['END_TIME'],"%Y-%m-%dT%H:%M")
                if start_time > today:
                    flash('Test not yet Started.',warning)
                    return redirect('/home_page')
                elif end_time < today:
                    flash('Test has Ended.',warning)
                    return redirect('/home_page')
                else:
                    cursor.execute(f"SELECT * FROM QUESTIONS WHERE TEST_ID = '{TESTCODE}'")
                    QUESTIONDATA = cursor.fetchall()
                    total_questions = len(QUESTIONDATA)
                    begin = time.time()
                    return render_template("testattend.html",username = user_name, testdata = TESTDATAS, questions = QUESTIONDATA, view=mode)
        except Exception as e:
            flash("Test Not found!",warning)
            return redirect('/home_page')
    if mode:
        try:
            cursor.execute(f"SELECT * FROM TESTS WHERE ID = '{code}'")
            TESTDATAS = cursor.fetchone()
            if len(TESTDATAS)!= None:
                try:
                    cursor.execute(f"SELECT * FROM QUESTIONS WHERE TEST_ID = '{code}'")
                    QUESTIONDATA = cursor.fetchall()
                    return render_template("testattend.html",username = user_name, testdata = TESTDATAS, questions = QUESTIONDATA, view=mode)
                except:
                    flash("Error in fetching!",warning)
                    return redirect(f"/leader_board/{code}")        
        except Exception as e:
            flash("Tes not found!",warning)
            return redirect(f"/leader_board/{code}")
        

@app.route('/submit_test/<string:code>',methods=['POST','GET'])
def submit_test(code):
    global stop
    if request.method == 'POST':
        stop =time.time()
        QUESTIONID = request.form.getlist('questionid')
        OPTIONS = []
        for i in range(total_questions):
            try:
                OPTION = request.form[f"question{i+1}"]
            except:
                OPTION = ''
            OPTIONS.append(OPTION)
        try:
            cursor.execute(f"SELECT ID,SCORE,CORRECT,NEG_SCORE FROM QUESTIONS WHERE TEST_ID = '{code}'")
            ANSWER_CHECK = cursor.fetchall()
            SCORED = 0
            MAX_SCORE =0
            for i in QUESTIONID:
                for j in ANSWER_CHECK:
                    if int(i) == j['ID']:
                        MAX_SCORE += j['SCORE']
                        if OPTIONS[QUESTIONID.index(i)] == j['CORRECT']:
                            SCORED += j['SCORE']
                        elif  OPTIONS[QUESTIONID.index(i)] == '':
                            pass
                        else:
                            SCORED += j['NEG_SCORE']
            time_taken = stop - begin
            mins,secs = divmod(time_taken,60)
            try:
                cursor.execute(f"INSERT INTO LEADERBOARD (TEST_ID,USER_ID,RANKED,SCORED,MAXSCORE,TIMEFINISH) VALUES ('{code}',{user_id},{1},{SCORED},{MAX_SCORE},'{int(mins):02d}:{int(secs):02d}')" )
                con.commit()
            except:
                pass
            flash("Test completed Check leaderboard.",success)
        except:
            flash("Error in server.",warning)
    return redirect('/home_page')

@app.route('/leader_board/<string:code>',methods=['POST','GET'])
def leader_board(code):
    try:
        cursor.execute(f"SELECT USERS.USER_NAME, LEADERBOARD.* FROM USERS INNER JOIN LEADERBOARD ON USERS.ID = LEADERBOARD.USER_ID WHERE TEST_ID = '{code}' order by SCORED DESC;")
        BOARD = cursor.fetchall()
    except:
        flash("Server Error.",warning)
    return render_template("leaderboard.html",board = BOARD, TEST_CODE = code, USER = user_name)
if __name__=="__main__":
    app.secret_key="admin480"
    app.run(debug=True)