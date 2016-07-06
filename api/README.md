
Setup
===


Install Anaconda: https://www.continuum.io/downloads

Setup environment:
```
conda create -n akcabinsearch python=3.5
source activate akcabinsearch
conda install --file requirements.txt
# install manually
pip install jsonpickle
```

Load cabin data:
```
cd data
source activate akcabinsearch
python scrape.py
# data should save in data/cabins.json
```

Start up flask app:
```
export FLASK_APP=api.py
export FLASK_DEBUG=1
flask run
```

