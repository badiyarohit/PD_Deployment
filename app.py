from flask import Flask, render_template, request
import pd as p
app = Flask(__name__)

@app.route("/",methods = ["GET","POST"])
def pd():
	if request.method == "POST":
		doc1 = request.form["input_doc1"]
		doc2 = request.form["input_doc2"]
		similar_percentage = p.Plagiarism_Detector(doc1,doc2)
		# print("Percentage of similarity is : ",similar_percentage)
		sp = similar_percentage
	return render_template("index.html",perc_same = sp)

"""	
@app.route("/sub",methods = ['POST'])
def submit():
	if request.method == "POST":
		name = request.form["username"]
	return render_template("sub.html",n=name)
"""

if __name__ == "__main__":
	app.run(debug=True)
