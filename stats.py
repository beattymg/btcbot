from manager import Manager
import csv
import math
import sys
import time

class Stats(Manager):
    def __init__(self):
        Manager.__init__(self)
        self.data = self.ReadData()

    def readData(self):
        with open(self.path + self.file_name, "rb") as f:
            reader = csv.reader(f)
            return list(reader)

    def calculatePoP(self, value):
        n = 0
        d = 0
        value_cent = int((float(value) * 100) % 10)
        for i in range(len(self.data) - 1):
            ex1 = int(self.data[i][0])
            ex2 = int(self.data[i + 1][0])
            data_cent = int((float(self.data[i][1]) * 100) % 10)
            if ex2 - ex1 == 300 and data_cent == value_cent:
                p1, p2 = self.GetPriceTuple(self.data[i][0])
                if p2 < self.GetUpperBound(p1):
                    n += 1
                d += 1
        return (float(n) / d, d)

    def getPriceTuple(self, expiry_time):
        expiry_index = self.GetItemIndex(expiry_time)
        p1 = float(self.data[expiry_index][1])
        p2 = float(self.data[expiry_index + 1][1])
        return (p1, p2)

    def getItemIndex(self, item):
        for i in range(len(self.data)):
            if item in self.data[i]:
                return i

if __name__ == "__main__":
    s = Stats()

    # Record statistics.
    if "-s" in sys.argv:
        while True:
            nearest_expiry = s.GetNearestExpiry()
            s.SleepToExpiry()
            s.RecordExpiryPrice(nearest_expiry)
            time.sleep(5)

    elif "-p" in sys.argv:
        count = 0
        for i in range(10):
            pop, n = s.CalculatePoP(i / 100.0)
            count += n
            print("\t{0} -> {1:.2f}% \t[n={2}]").format(i, pop * 100, n)
        print("\tTOTAL\t\t[n={0}]").format(count)
