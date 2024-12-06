from flask import Flask, render_template, request, redirect
from extractors.berlin import extract_jobs as extract_jobs_berlin
from extractors.wwr import extract_jobs as extract_jobs_wwr
from extractors.w3c import extract_jobs as extract_jobs_w3c

# keyword = input("What job do you want? ")
# results = []
# results.extend(extract_jobs_berlin(keyword))
# results.extend(extract_jobs_wwr(keyword))
# results.extend(extract_jobs_w3c(keyword))
# print(f"{len(results)}{results}")

app = Flask(__name__)
db = {}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        jobs = extract_jobs_berlin(keyword)
        jobs += extract_jobs_wwr(keyword)
        jobs += extract_jobs_w3c(keyword)
        db[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run("0,0,0,0", debug=True)