from flask import Flask, request, Response
import json
app = Flask(__name__)

# TODO: use a database :)
global data
with open('data/cabins.json', 'r') as f:
    data = json.load(f)

@app.route("/")
def areas():
    return Response(json.dumps(data), mimetype='application/json')

@app.route("/cabin/<int:code>")
def cabin(code):
    # TODO: return all cabin data, including metadata and availability
    return "Returning data for cabin {}".format(id)

# curl -X GET "http://localhost:5000/search?area_id=1"
@app.route("/search")
def search():
    # TODO: implement search
    area_id = request.args.get('area_id', '')
    date_start = request.args.get('date_start', '')
    date_end = request.args.get('date_end', '')
    return "Searching... area={}, dates={} to {}".format(area_id, date_start, date_end)

if __name__ == "__main__":
    app.run()

