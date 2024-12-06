from extractors.berlin import extract_jobs as extract_jobs_berlin
from extractors.w3c import extract_jobs as extract_jobs_w3c
from extractors.wwr import extract_jobs as extract_jobs_wwr
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword is None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        w3c = extract_jobs_w3c(keyword)
        wwr = extract_jobs_wwr(keyword)
        berlin = extract_jobs_berlin(keyword)
        jobs = w3c + wwr +berlin
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True)