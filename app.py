from flask import Flask,render_template,request,session,logging,url_for,redirect,flash,g 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from werkzeug.exceptions import HTTPException,NotFound,abort
import dataQueries
#import scrapper


    
app = Flask(__name__)
app.secret_key = "super secret key"

#index
@app.route("/",methods=["GET","POST"])
def home():
    
    if request.method=="POST":
        if 'app_login' in request.form:
            return redirect(url_for("user_login"))
        if 'rec_login' in request.form:
            return redirect(url_for("recruiter_login"))
        if 'app_reg' in request.form:
            return redirect(url_for("user_register"))
        if 'rec_reg' in request.form:
            return redirect(url_for("recruiter_register"))
    #scrapper.scrap_jobs()
    #run above code once to scrap job data in jobs table
            
    return render_template("index.html")


#registration 
@app.route("/user_register",methods=["GET","POST"])
def user_register():
    if request.method == "POST":
        name=request.form.get("name")
        dob=request.form.get("dob")
        email=request.form.get("email")
        password=request.form.get("password")
        contact=request.form.get("contact")
        gender=request.form.get("gender")
        category=request.form.get("category")
        address=request.form.get("address")
        tenth=request.form.get("tenth")
        twelve=request.form.get("twelve")
        re=request.form.get("re-password")
        address=address.replace(', ',',')
        if password==re:
            dataQueries.make_user(name,contact,email,address,tenth,twelve,gender,dob,password,category)
            flash("Registration Successful")
            return redirect(url_for(('user_login')))
        else:
            flash("password doesn't match")
            #return render_template("user_register.html")
                 
    return render_template("user_registration.html")


@app.route("/recruiter_register",methods=["GET","POST"])
def recruiter_register():
    if request.method == "POST":
        if 'submit' in request.form:
            company_name=request.form.get("name")
            email=request.form.get("email")
            password=request.form.get("password")
            contact=request.form.get("contact")
            address=request.form.get("address")
            re=request.form.get("re-password")
            
            if password==re:
                dataQueries.make_recruiter(company_name,contact,email,address,password)
                flash("Registration Successful")
                return redirect(url_for('recruiter_login'))
            else:
                flash("password doesn't match")
                #return render_template("user_register.html")
                 
    return render_template("recruiter_registration.html")


#login
@app.route("/user_login",methods=["GET","POST"])
def user_login():
    if request.method=="POST":
         name=request.form.get("name")
         passwd=request.form.get("password")
         if name==None:
            flash("Please enter a username")
         else:
            passwddata=dataQueries.user_check(name)
            if passwddata==None:
                flash("wrong username")
            else:
                if passwd==passwddata[1]:
                    userdata=dataQueries.user_info(name)
                    return redirect(url_for("user_profile",Name=userdata))
                else:
                    flash("invalid username or password")
                    #return render_template("test.html", ah=g)
    return render_template("user_login.html")   




@app.route("/recruiter_login",methods=["GET","POST"])
def recruiter_login():
    if request.method=="POST":
        if 'submit' in request.form:
            name=request.form.get("name")
            passwd=request.form.get("password")
            if name==None:
                flash("please enter a username")
            else:
                rc=dataQueries.spoc_check(name)
                if rc==None:
                    flash("invalid username or password")
                else:
                    if passwd==rc[1]:
                        session['user']=name
                        recruiterdata=dataQueries.spoc_info(name)
                        flash("successfully logged in")
                        return redirect(url_for('recruiter_profile',rd=recruiterdata))
                        
        
        
    return render_template("recruiter_login.html")   



#profile
@app.route("/user_profile/<Name>",methods=["GET","POST"])
def user_profile(Name):
    #Name=Name.replace("(","").replace(")","").replace(" '","").replace("'","").split(',')
    Name=Name.split(", ")
   
    d=dataQueries.fetch_scrap()
    job_applied=dataQueries.user_job(Name[0])
    
    if job_applied==None:
        job_applied==["no applications","filled"]
    for i in range(len(Name)):
        if i==0:
            Name[i]=Name[i][1:]
        elif i==1 or i==3 or i==4 or i==7 or i==8 or i==9:
            Name[i]=Name[i][1:-1]
        if i==(len(Name)-1):
            Name[i]=Name[i][:-1]
    udet=Name[0]
    if request.method== 'POST':
        if 'logout' in request.form: 
            return redirect(url_for('user_login'))

        if 'more_jobs' in request.form:
            return redirect(url_for('more_jobs',udet=udet))
        
        if 'recommender' in request.form:
            state=request.form.get('state')
            sector=request.form.get('sector')
            d=dataQueries.fetch_recommend(state, sector)
            
        
    try:return render_template("user_page.html",name=Name,scrap=d,job_applied=job_applied)
    except:return render_template("user_page.html",name=Name,scrap=d)


@app.route("/recruiter_profile/<rd>",methods=["GET","POST"])
def recruiter_profile(rd):
    if g.user :
        #Name=rd.replace("(","").replace(")","").replace(" '","").replace("'","").split(',')
        rd=rd.split(", ")
        for i in range(len(rd)):
            if i==0:
                rd[i]=rd[i][1:]
            elif i==1 or i==3 or i==4 or i==7 or i==8 or i==9:
                rd[i]=rd[i][1:-1]
            if i==(len(rd)-1):
                rd[i]=rd[i][:-1]
        Name=rd
        if request.method== 'POST':
            if 'logout' in request.form:
                session.pop('user',None)
                return redirect(url_for('recruiter_login'))
            if 'addjob'in request.form:
                return redirect(url_for('add_job',rd=rd))
            if 'check' in request.form:
                jn=request.form.get('check')
                
                return redirect(url_for('job_details_recruiter',job_details=jn))
            
        job_added=dataQueries.fetch_job_name(Name[1])
        
        
        return render_template("recruiter_page.html",rdata=Name,jdata=job_added)
    else:
        return redirect(url_for("recruiter_login"))

@app.route("/add_job/<rd>",methods=["GET","POST"])
def add_job(rd):
    if request.method=='POST':
        if "add" in request.form:
            company_name=request.form.get("company name")
            vacant_post=request.form.get("vacant post")
            Skill_required=request.form.get("skill required")
            job_description=request.form.get("job description")
            expected_salary=request.form.get("expected salary")
            state=request.form.get("state")
            address=request.form.get("address")
            dataQueries.add_job(vacant_post, Skill_required, job_description, expected_salary, state, address, company_name)
            return redirect(url_for("recruiter_profile",rd=rd))
        
            
    return render_template("add_job.html")

@app.route("/job_details_recruiter/<job_details>",methods=['GET','POST'])
def job_details_recruiter(job_details):
    det=dataQueries.fetch_job(job_details)
    if request.method=='POST':
        if 'update' in request.form:
            job_name=request.form.get('job_name')
            job_description=request.form.get('job_description')
            skill_required=request.form.get('skills_required')
            expected_salary=request.form.get('expected_salary')
            state=request.form.get('state')
            address=request.form.get('address')
            dataQueries.update_job(job_name, skill_required, job_description, expected_salary, state, address, det[0][6])
            
            rd=dataQueries.spoc_info(det[0][6])
            return redirect(url_for("recruiter_profile",rd=rd))
        if 'applications' in request.form:
            return redirect(url_for('job_applications',rd=det))
        if 'close' in request.form:
            pass
    return render_template("jobs.html", det=det)
        
@app.before_request
def before_request():
    g.user=None
    if 'user' in session:
        g.user=session['user']
    
''' test route is to check the format of data passed to a route'''   

@app.route("/more_jobs/<udet>",methods=['GET','POST'])
def  more_jobs(udet):
    if request.method=='POST':
        if 'logout' in request.form:
            return redirect(url_for('user_login'))
        if 'kapil' in request.form:
            det=request.form.get('kapil')
            det=dataQueries.fetch_job_id(int(det))
            #return redirect(url_for('test',det = det))
            return redirect(url_for('fjob_details',det=det,udet=udet))
    govt=dataQueries.fetch_scrap()
    private=dataQueries.free_jobs()
    return render_template('more_jobs.html',scrap=govt,pscrap=private)

@app.route("/fjob_details/<det>/<udet>",methods=['GET','POST'])
def fjob_details(det,udet):
    if request.method=='POST':
        if 'apply' in request.form:
            t=dataQueries.job_apply(int(udet),int(det))
            return redirect(url_for("test",t=t,det=type(det)))
            
            
            
    return render_template('apply_job.html',det=det)
    

@app.route("/job_applications/<rd>")
def job_applications(rd):
    applicants=dataQueries.recruiter_job(rd[0])
    
    return render_template('applications.html',applicants=applicants)

@app.route("/test/<state>/<sector>",methods=["GET","POST"])
def test(state,sector):
    return render_template("test.html",state=state,sector=sector)

if __name__ == "__main__":
    app.run(debug=True)
