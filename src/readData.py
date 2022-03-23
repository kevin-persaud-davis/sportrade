import os
import csv

import requests

import pandas as pd

class Event():

    validBooks = ["draftkings"]

    def __init__(self, id, sportKey, endTime, homeTeam, awayTeam):
        self.id = id
        self.sportKey = sportKey
        self.endTime = endTime
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.h2h = []
        self.spreads = []
        self.totals = []
        self.allPrices = ()

    def setAllPrices(self):
        if self.totals and self.spreads and self.h2h:
            self.allPrices += (
                            self.id, self.homeTeam, self.awayTeam, self.endTime, self.totals[0][0],
                            self.priceConversion(self.totals[0][2]), self.totals[0][3],
                            self.priceConversion(self.spreads[0][2]), self.spreads[0][3], self.spreads[1][3],
                            self.priceConversion(self.h2h[0][2]), self.priceConversion(self.h2h[1][2])
                            )
        else:
            print("Empty event prices.")
        # totals
        # total = (self.totals[0][2], self.totals[0][3])
        # # spreads
        # spread = (self.spreads[0][2], self.spreads[0][3], self.spreads[1][3])
        # # h2h (i.e. moneyline)
        # ml = (self.spreads[0][3], self.spreads[1][3])
    
    def getAllPrices(self):
        if self.allPrices:
            return self.allPrices
        else:
            print("Set Prices.")

    def priceConversion(self, price, priceType="decimal"):
        if priceType == "decimal":
            priceProb = round((1/price) * 100, 1)
            return priceProb
    
    def getPrices(self, eventType, ts, lines):
        if eventType == "h2h":
            for line in lines:
                # print(ts, ":", line)
                fullEvent = (ts, line["name"], line["price"])
                if fullEvent not in self.h2h:
                    self.h2h.append(fullEvent)
        elif eventType == "spreads":
            for line in lines:
                fullEvent = (ts, line["name"], line["price"], line["point"])
                if fullEvent not in self.spreads:
                    # self.spreads[ts] = {line["name"] : (line["price"], line["point"])}
                    self.spreads.append(fullEvent)
                else:
                    print(f"No price update for {fullEvent}.")
        elif eventType == "totals":
            for line in lines:
                fullEvent = (ts, line["name"], line["price"], line["point"])
                if fullEvent not in self.totals:
                    # self.spreads[ts] = {line["name"] : (line["price"], line["point"])}
                    self.totals.append(fullEvent)
                else:
                    print(f"No price update for {fullEvent}.")
            
        

def writeEventPrices(prices, fname):
    # header = [
    #         "eid", 
    #         "homeTeam", 
    #         "awayTeam", 
    #         "endDate", 
    #         "timestamp", 
    #         "totalPrice", 
    #         "total", 
    #         "spreadprice", 
    #         "spreadHT", 
    #         "spreadAT", 
    #         "mlHT",
    #         "mlAT"
    #     ]
    
    mainDirPath = os.path.dirname(os.path.dirname(__file__))
    
    fpath = os.path.join(mainDirPath, fname)
    with open(fpath, "a", encoding="UTF8", newline="") as f:
        writer = csv.writer(f, delimiter=",")

        for price in prices:
            writer.writerow(price)




def getOdds(apiKey, sports, regions, markets, oddsFormat, dateFormat):
    """Get bookmaker odds for events"""

    url = f"https://api.the-odds-api.com/v4/sports/{sports}/odds"
    with requests.Session() as s:
        r = s.get(url, 
            params={
            "api_key": apiKey,
            "regions": regions,
            "markets": markets,
            "oddsFormat": oddsFormat,
            "dateFormat": dateFormat,
            })

        if r.status_code == 200:
            odds = r.json()
            print(f"Number of events: {len(odds)}")

            allEvents = []
            # id = event id
            # sport_key = type of event
            # commence_time = end time of event
            # home_team = home team
            # away_team = away team
            for event in odds:
                eventId = event["id"]
                sportKey = event["sport_key"]
                endTime = event["commence_time"]
                homeTeam = event["home_team"]
                awayTeam = event["away_team"]

                sportEvent = Event(eventId, sportKey, endTime, homeTeam, awayTeam)
                
                bookmakers = event["bookmakers"]
                # validBooks = ["draftkings"]
                # books = []

                for book in bookmakers:
                    if book["key"] in sportEvent.validBooks:
                        name = book["key"]
                        lastUpdate = book["last_update"]

                        eMarkets = book["markets"]

                        for i, market in enumerate(eMarkets):
                            # print(i, market)
                            eventType = market["key"]
                            outcomes = market["outcomes"]
                            sportEvent.getPrices(eventType, lastUpdate, outcomes)
                            
                allEvents.append(sportEvent)



                # print("\nEvent Result: \n")
                # print(sportEvent.h2h)
                # print(sportEvent.spreads)
                # print(sportEvent.totals)

            # bookmakers = list of key-value pairs of bookmakers
            # Retrieve only draftkings

                # key = "draftkings"
                # last_update = last price update
                # markets = list of key value pairs

                    # key = markets (i.e. h2h, spread, total)
                    # outcome = list of key value pairs

                        # name = team
                        # price = odds price
            

            # check usage quota
            print(f"Remaining requests {r.headers['x-requests-remaining']}")
            return allEvents
        else:
            print(f"Failed to get odds: status_code {r.status_code}, response body {r.text}")

def getKey(fpath):
    # top level directory path
    mainDirPath = os.path.dirname(os.path.dirname(__file__))
    # file path containing key
    keyFile = os.path.join(mainDirPath, fpath)
    with open(keyFile, "r") as f:
        line = f.readline()
        k = line.split(":")[-1]
    return k


def main():

    API_KEY = getKey("private\\api.text")
    
    SPORT = 'basketball_ncaab' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

    REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited

    MARKETS = 'h2h,spreads,totals' # h2h | spreads | totals. Multiple can be specified if comma delimited

    ODDS_FORMAT = 'decimal' # decimal | american

    DATE_FORMAT = 'unix' # iso | unix
    
    eventOdds = getOdds(API_KEY, SPORT, REGIONS, MARKETS, ODDS_FORMAT, DATE_FORMAT)

    eventPrices = []
    for event in eventOdds:
        event.setAllPrices()
        price = event.getAllPrices()
        eventPrices.append(price)
    
    print(eventPrices)

    fname = "data\\eventPrices.csv"
    writeEventPrices(eventPrices, fname)
   
    # for event in eventOdds:
    #     print("\nEVENT:")
    #     event.setAllPrices()
    #     price = event.getAllPrices()
    #     print(price)
        # print(f"eid: {event.id}")
        # print(f"homeTeam: {event.homeTeam}")
        # print(f"awayTeam: {event.awayTeam}")
        # print(f"endTime: {event.endTime}")
        
        # print(f"{event.h2h}")
        # print(event.spreads)
        # print(event.totals[0][0])

    # sports_response = requests.get(
    # f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds', 
    # params={
    #     "api_key": API_KEY,
    #     "regions": REGIONS,
    #     "markets": MARKETS,
    #     "oddsFormat": ODDS_FORMAT,
    #     "dateFormat": DATE_FORMAT,
    #     }
    # )

    # if sports_response.status_code != 200:
    #     print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    # else:
    #     print('List of in season sports:\n')
    #     for sportKey in sports_response.json():
    #         print(sportKey)



if __name__ == "__main__":
    main()
    