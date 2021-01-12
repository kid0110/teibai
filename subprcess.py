import keepa
import pandas as pd
import matplotlib
import requests
import datetime
import time
import schedule
import csv
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import sys
import argparse
import subprocess

cmd = 'C:\work\ShopDingDong_346\ShopDingDong.exe'
url = "sample"
quant = "quant"
choice = "choice"
test = "Test"
returncode = subprocess.call(cmd, shell = True)

print(returncode)