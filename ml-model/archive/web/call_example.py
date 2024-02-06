import requests

# to send result back to front-end

URL = "http://3.94.25.91/api/result"
json = {
    "file":"ex1.pdf",
    "coords":"0 0.3392857142857143 0.17142857142857146 0.30952380952380953 0.12698412698412698 1 0.32242063492063494 0.4380952380952381 0.26785714285714285 0.08888888888888889"
}

res = requests.get(URL, json=json)

res = print(res) # OK = 200