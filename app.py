###################### IMPORTS ######################
""" Crawler to return the page content of an URL """
from flask import Flask, request, jsonify
from selenium import webdriver
from platform import system # to get the name of the system
from hashlib import md5 # generate the md5 hash
import ipgetter # to get the external ip
import time # to measure the time spend on the phantomjs process
#####################################################

###################### VARIABLES ####################
# Define the app flask
APP = Flask("python-crawler")
# Set the IPs of the application
EXTERNAL_IP = ipgetter.myip()

# check the system name to set the enviroment variables
ENV = 'DEV' # default value
if system() == 'Windows':
    PATH_PHANTOM = "phantomjs.exe"
    ENV = open('C:/Windows/env.file', 'r').read().splitlines()[0]  # environment mode
else:
    PATH_PHANTOM = "./phantomjs"
    ENV = open('/etc/env.file', 'r').read().splitlines()[0]  # environment mode

if ENV == 'PROD':
    APP_DEBUG = False
    APP_RELOAD = False
    WD_LOGLV = "INFO"
else:
    APP_DEBUG = True
    APP_RELOAD = True
    WD_LOGLV = "DEBUG"

# Define phantom properties
PHANTOM_ARGS = [
    "--ignore-ssl-errors=yes",
    "--load-images=no",
    "--web-security=no",
    "--webdriver-loglevel=" + WD_LOGLV
    ]
######################################################

####################### ROUTES #######################
# Default route to return the content from the crawler
@APP.route("/")
def get_content_page():
    "Endpoint to return the content of the crawled page"
    start_time = time.time() # Set the start time of the process
    url = request.args.get("url") # Gets the query string argument
    if not (url is None):
        # Open the webdriver with phantomjs
        driver = webdriver.PhantomJS(executable_path=PATH_PHANTOM, service_args=PHANTOM_ARGS)
        driver.set_window_size(1280, 720)
        driver.get(url)
        page_source = driver.page_source
        driver.quit()
        return jsonify({"message": "OK", "pageSource": page_source,
                        "external_ip": EXTERNAL_IP,
                        "took_seconds": (time.time() - start_time)}), 200
    else:
        return jsonify({"message": "Missing url parameter.",
                        "external_ip": EXTERNAL_IP,
                        "took_seconds": (time.time() - start_time)}), 400
######################################################

####################### MAIN CODE #######################
print("Running app.py as " + ENV + " mode.")
APP.run(debug=APP_DEBUG, use_reloader=APP_RELOAD, host='0.0.0.0')

## ./app.py
