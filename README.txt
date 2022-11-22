## Setup - before you run the script, I use python3, pip3, and a few packages. Run in the terminal if needed: 
python3 -m ensurepip --default-pip
pip3 install pyyaml
pip3 install requests

## To Run - enter the following in the terminal:
python3 website_monitor.py

## Config - This script reads the following from a config yaml file:
1. Period of time in seconds between http get requests
2. Log file name
3. List of urls to check. The list format starts with a dash then the url

## Structure
I considered breaking up the script, especially the get request as an OOP class, but in the interest of time I left it as a single script.

## App
1. Starts with an initial prompt, where user can input a custom period of time between a check of each url in the list, or hit ENTER to use the config default
2. Uses the requests library to make http requests which provides the elapsed time to receive the response
3. Writes the result of the http requests to a log file. The data written is the date & time, url, status, and time in seconds for the response
4. Use CTRL C to quit the app. Unfortunately I did not have time to add an elegant quit in v1, but with more time it's definitely possible

## Status
The value logged is the http response with its name. This is a rather limited representation of a website's status and not fully descriptive.
There are several scenarios that may present themselves:
1. Errors in the config list/nonexistant urls - added exception handling to abort the async loop running
2. 400 & 500 range HTTP response errors - These generally signify the most catastrophic events that should be highlighted as critically not OK. The site is unreachable, poor server performance, etc.
3. Other HTTP codes - Whether other scenarios should be treated as less than OK would be up to the requirements of the owners of the websites
4. Header response - Whether the header response is fully formed could affect the site in some way, but aside from testing whether it exists, further testing would require custom tests
5. Content response - A site can have a complete server response, but there can be plenty of site-specific issues with content, such as malformed HTML, JavaScript, cookie, and other site-specific content. Testing that there is content is the most simple, but doesn't tell much about the status of the site

There are many levels of depth to evaluate the status/health of a site. Aggregating the above into one status value can be useful at a glance, but may hide things, be error prone, and require a lot of logic. Breaking up a status report to many of its components may be more informative, but harder to parse 
