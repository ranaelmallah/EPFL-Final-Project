from flask import Flask,render_template,url_for
app =Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/login")
def login():
   return render_template("login.html")

@app.route("/dashboard")
def dashboard():
   return render_template("dashboard.html")

@app.route("/profile")
def profile():
   return render_template("profile.html")

@app.route("/signup")
def signup():
   return render_template("signup.html")

@app.route("/about")
def about():
   return render_template("about.html")
@app.route("/forgetpassword")
def forgetpassword():
    return render_template("forgetpassword.html")  

@app.route("/reset")
def resetpassword():
    return render_template("resetpass.html") 

if __name__=="__main__":
    app.run(debug=True)
