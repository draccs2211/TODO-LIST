from flask import Flask,render_template,redirect,request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#app
app=Flask(__name__)
Scss(app)
#DATABASE CONGFIGURATION
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODILFICATION"]=False
db=SQLAlchemy(app)
#DATA CLASSS-ROW OF DATA
class Mytask(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(100),nullable=False)
    complete=db.Column(db.Integer)
    created=db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return f"TASK {self.id}"
with app.app_context():
    db.create_all()
    
    
    
    
#homepage    
@app.route("/",methods=["POST","GET"]) 
def index():
    



#add  task
    if request.method=='POST':
        current_task=request.form['content']
        new_task=Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR {e}")
            return f"ERROR {e}"
    #SEE ALL CURRENT TASK
    else:
        tasks=Mytask.query.order_by(Mytask.created).all()
        return render_template("index.html",tasks=tasks)
    
#DELETE AN ITEMS
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task=Mytask.query.get_or_404(id)
    try: 
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"error{e}"
#UPDATE ITEMS
@app.route("/edit/<int:id>",methods=['GET','POST'])
def edit(id:int):
    task=Mytask.query.get_or_404(id)
    if request.method=='POST':
        task.content=request.form['content']
        try: 
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"error{e}"

    else:
        return render_template("edit.html",task=task)
    





if __name__ == "__main__":
    
    app.run(debug=True)
    