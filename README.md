# Weather Scraper

## Background
The wind in Indian Arm is hard to predict due to the surrounding terrain (although it can be done, see https://www.canada.ca/en/environment-climate-change/services/general-marine-weather-information/regional-guides/british-columbia.html).

Current models such as NAM and HRRR still struggle in the mountainous terrain around Indian Arm. Since prediction is hard, gathering data from actual weather stations for current conditions and comparing to available wind models can aid in determining accuracy of said models. 

## Problem
It turns out that obtaining current weather conditions from individual weather stations is difficult or not completely obvious. You either need API keys that cost thousands of dollars or need to access each station from a webpage. This python application aims to make this process easier from publicly available sites.

## Solution
Using BeautifulSoup, we're able to retrieve the contents of the webpage and parse out just the *useful* data and throw away all the junk! We can then compare current conditions from stations in Indian Arm with the wind models to determine accuracy.
