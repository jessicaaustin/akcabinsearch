
Setup
===

Install Anaconda: https://www.continuum.io/downloads

Setup environment:
```
conda create -n akcabinsearch python=3.5
source activate akcabinsearch
conda install --file requirements.txt
```


Facilities
===

Federally owned cabins: Recreation.gov
* API: http://usda.github.io/RIDB/
* Usage: http://www.recreation.gov/marketing.do?goto=/shareRecreationData.html 
 * tl;dr: can use the API and data for your website with no restrictions

State owned cabins: http://dnr.alaska.gov/parks/cabins
* No API, need to scrape pages
* Usage: http://dnr.alaska.gov/shared/notices/copyright.htm
 * tl;dr: need to request permission to use

Operated by a third party (e.g., Shoup Bay State Marine Park: http://dnr.alaska.gov/parks/cabins/pws)
* Would need to scrape each site individually


Roadmap
===

MVP
---

1. State-owned cabins only
1. Scrape data from their website periodically and store in local db
1. Web interface to search facilities
1. Display facilities on a map


Later
---

1. Include federally owned facilities
1. Include 3rd-party facilities
1. Allow users to sign up for notifications
1. "Cabin share" -- users can transfer a reservation to someone else (reservation number, name, door code?)

