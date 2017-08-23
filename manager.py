from coinut import Coinut
import csv
import math
import time

env = {}
with open(".env", "r") as e:
    for row in e:
        r = row.strip().split("=")
        env[r[0]] = r[1]

USERNAME = env["USERNAME"]
API_KEY = env["API_KEY"]
D_TYPE = env["D_TYPE"]
ASSET = env["ASSET"]
PUT_CALL = env["PUT_CALL"]
PATH = env["PATH"]
FILE_NAME = env["FILE_NAME"]

class Manager:
    def __init__(self):
        self.coinut = Coinut(USERNAME, API_KEY)
        self.d_type = D_TYPE
        self.asset = ASSET
        self.put_call = PUT_CALL
        self.path = PATH
        self.file_name = FILE_NAME

    def getUpperBound(self, current_price):
        return math.ceil(float(current_price) * 10) / 10

    def getLowerBound(self, current_price):
        return math.floor(float(current_price) * 10) / 10

    def getNearestExpiry(self):
        return self.coinut.expiry_time(D_TYPE, ASSET)[0]

    def getCurrentPrice(self):
        return float(self.coinut.tick(ASSET)["tick"])

    def recordExpiryPrice(self, nearest_expiry):
        current_price = self.GetCurrentPrice()
        price_history = [nearest_expiry, current_price]
        with open(self.path + self.file_name, "ab") as f:
            writer = csv.writer(f)
            writer.writerow(price_history)

    def sleepToExpiry(self):
        nearest_expiry = self.GetNearestExpiry()
        tte = int(nearest_expiry - time.time())
        while tte:
            mins, secs = divmod(tte, 60)
            print('\rSleeping for {:02d}:{:02d}'.format(mins, secs)),
            time.sleep(1)
            tte -= 1
        print("")
