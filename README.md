# Overview

A little while ago, I produced a [real-time tram stop timetable (for Manchester's Metrolink)](http://github.com/jrmedd/metdisplay) using Open Data from TfGM. After my dad spotted this on a screen behind a bar in MediaCityUK, he asked if I could produce something similar for his local bus stop in Nottingham.

While [Nottingham City Transport only have a limited Open Data](https://www.nctx.co.uk/open-data) portal, they *do* have a real-time bus timetables on their site. In order to wrap this in something that could be displayed on a screen in my parents' hallway, I've made use of @maxhumber's [gazpacho](https://github.com/maxhumber/gazpacho) to scrape data from NCT, and provide an endpoint [for a dashboard I'm working on](https://github.com/jrmedd/nct-buses-display).

## Usage

For development and testing, clone this repo, install dependencies using `python3 -m pip install -r requirements.txt`, and start the dev server using `python3 web_app.py`. One the server is running, get [your desired stop ID from NCTX](https://www.nctx.co.uk/open-data/network/current) and you can request the next 5 bus times using http://localhost:5000/times/[stopID]
