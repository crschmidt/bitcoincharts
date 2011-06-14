import socket
import sqlite3
import json
db = sqlite3.connect("chart.sqlite")
cur = db.cursor()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("bitcoincharts.com", 27007))
try:
    started = False
    data = []
    while True:
        d = s.recv(1)

        if d == "{":
            started = True
        if started:
            data.append(d)
        if d == "}":
            started = False
            jdata = json.loads("".join(data))
            cur.execute("INSERT INTO chart (timestamp, price, volume, currency, tid, symbol) VALUES (?, ?, ?, ?, ?, ?)", (jdata['timestamp'], jdata['price'], jdata['volume'], jdata['currency'], jdata['tid'], jdata['symbol']))
            db.commit()
            print "".join(data)
            data = []
except KeyboardInterrupt:
    pass
