from flask import Flask, request, Response
import json
import pandas as pd
app = Flask(__name__)

# TODO: use a database :)
global data
with open('data/cabins.json', 'r') as f:
    data = json.load(f)
global cabins
cabins = pd.read_pickle('data/cabin_db.pickle')

def JsonResponse(j):
   return Response(j, mimetype='application/json') 

@app.route("/")
def areas():
    return JsonResponse(json.dumps(data))

@app.route("/cabin/<int:code>")
def cabin(code):
    cabin = cabins[cabins.index == code]
    if len(cabin) == 0:
        return JsonResponse("No cabin found with code={}".format(code))
    return JsonResponse(cabin.to_json())

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

