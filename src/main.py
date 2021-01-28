
# Make sure you install the following packages
# pip install requests beautifulsoup4

# Built-in packages
import logging
from os import stat
import pprint # For printing dicts in a readable format
import concurrent.futures # For threading each weather station

# Extra packages
import requests # For downloading the page
from bs4 import BeautifulSoup # For parsing the page

logging.basicConfig(level = logging.DEBUG)

def findLocation(soup = BeautifulSoup):
    """
    This function will parse the location field.
    If the elevation is negative, it is cleaned to display 0.
    This function assumes N and W for Long and Lat
    """
    mData = {}

    header = soup.find(class_ = "dashboard__header")
    content = header.find(class_ = "sub-heading")

    # The location data is in a string as follows,
    # Elev  -107507 ft, 49.38 °N, 122.88 °W
    items = content.span.get_text().split(",")

    # Parse the elevation field, which is seperated by spaces
    elevationField = list(filter(None, items[0].split(" ")))
    mData["elevation"] = float(elevationField[1]) if float(elevationField[1]) >= 0 else 0.0
    mData["units"] = elevationField[2]

    # Parse the Latitude (assume always N)
    mData["latitude"] = float(items[1].split(" ")[1])

    # Parse the Longitude (assume always W and multiply by -1)
    mData["longitude"] = float(items[2].split(" ")[1]) * -1

    return {"location" : mData}


def findUptime(soup = BeautifulSoup):
    mData = {}
    return {"updated" : mData}


def findWind(soup = BeautifulSoup):
    """
    This function locates the wind details and returns the direction, speed,
    gust, and units. If the units are in MPH, it converts to knots.
    """
    mData = {}

    direction = soup.find(class_="wind-dial__container")
    mData["direction"] = direction.span.string

    wind = soup.find(class_="weather__data weather__wind-gust")

    mData["speed"] = wind.find(class_="wu-value wu-value-to").string
    gustAndUnits = wind.find(class_="test-false wu-unit wu-unit-speed ng-star-inserted")
    mData["gust"] = gustAndUnits.span.string
    mData["units"] = gustAndUnits.find(class_="ng-star-inserted").string

    logging.debug(mData)

    # Website provides MPH, convert and update to knots
    if mData["units"].lower() == "mph":
        mData["speed"] = str(round(float(mData["speed"]) * 0.868974, 2))
        mData["gust"] = str(round(float(mData["gust"]) * 0.868974, 2))
        mData["units"] = "knots"

    return {"wind" : mData}


def findTemp(soup = BeautifulSoup):
    mData = {}
    return {"temperature" : mData}


def parsePage(name = "", url = ""):
    """
    This function drives the logic for downloading and parsing the Weather
    Underground page. Designed to be used in a multithreaded manner.
    """
    mStationData = {}
    mStationData[name] = {}

    # Make sure we allow the GET call to timeout
    page = requests.get(url = url, timeout = 5)
    logging.debug(page.status_code)
    if page.status_code != 200:
        return mStationData
    data = BeautifulSoup(page.content, features="html.parser")

    mStationData[name].update(findWind(data))
    mStationData[name].update(findTemp(data))
    mStationData[name].update(findLocation(data))
    return mStationData


def parseWeatherUnderground():
    mStations = {"Best Point" : "https://www.wunderground.com/dashboard/pws/INORTH193",
                "Little Cates Park" : "https://www.wunderground.com/dashboard/pws/INORTH428",
                "Stone Haven" : "https://www.wunderground.com/dashboard/pws/INORTH269",
                "Deep Cove" : "https://www.wunderground.com/dashboard/pws/IBRITISH267"
                }

    mStationData = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
        # Start the load operations and mark each future with its URL
        futures = []
        for name, url in mStations.items():
            futures.append(executor.submit(parsePage, name = name, url = url))
        for future in concurrent.futures.as_completed(futures):
            mStationData.update(future.result())

    return mStationData

def downloadWeatherUnderground(station = requests.Response):
    # Save the file (so we don't hit the website when debugging)
    with open('index.html', 'wb') as f:
       f.write(station.content)

    # with open('pretty_index.html', 'w') as f:
    #     f.write(soup.prettify())


def debugWithFile():
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path     = os.path.dirname(os.path.abspath(filename))
    station = ""
    with open(path + '\\..\\test_data\\index.html', 'r') as f:
        station = f.read()
    soup = BeautifulSoup(station, features="html.parser")
    pprint.pprint(findLocation(soup))

def printWind(data = dict):
    for station in data:
        print(station)
        pprint.pprint(stationData[station]["wind"])

#debugWithFile()

stationData = parseWeatherUnderground()

printWind(stationData)
