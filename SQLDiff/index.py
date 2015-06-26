__author__ = 'aardr'

from flask import Flask, render_template, request, redirect, session, url_for
import SQLDiff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SOMETHINK'


@app.route("/<region_from>/<region_to>/<search_pattern>")
def start(region_from, region_to, search_pattern=""):
    sql_diff = SQLDiff()
    regions = [dict(name=i["name"], region=i["region"]) for i in sql_diff.regions]
    if region_from is None:
        return render_template("index.html", regions=regions)
    else:
        sql_diff = compare_general(region_from, region_to, search_pattern)
        return render_template("index.html",
                               regions=regions,
                               from_region=sql_diff.fromObject['region'],
                               to_region=sql_diff.toObject['region'],
                               from_only=sql_diff.mismatches_from,
                               len_from=len(sql_diff.mismatches_from),
                               to_only=sql_diff.mismatches_to,
                               len_to=len(sql_diff.mismatches_to),
                               common=sql_diff.common)


@app.route("/", methods=["GET"])
def search():
    session['region_from'] = request.args.get('regionFrom', '')
    session['region_to'] = request.args.get('regionTo', '')
    session['search_for'] = request.args.get('search_pattern', '')
    return url_for("start",
                   region_from=session['region_from'],
                   region_to=session['region_to'],
                   search_pattern=session['search_for'])


def compare_general(region_from, region_to, search_pattern):
    sql_diff = SQLDiff()
    sql_diff.set_search(search_pattern)
    sql_diff.set_from(region_from)
    sql_diff.set_to(region_to)
    sql_diff.get_mismatches()
    sql_diff.get_common()

    return sql_diff


if __name__ == "__main__":
    app.run(debug=True)

