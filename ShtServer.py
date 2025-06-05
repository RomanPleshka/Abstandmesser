import ESP8266WebServer as server
from WifiConnect import wifiConnect
import network
import machine
import json
from hcsr04_reading import returnDistance
import time



ssid = "gsog-iot"
password = "IOT_Projekt_BFK-S_2022"
#ssid = "POCO"
#password ="123456789"

wifiConnect(ssid, password)


def handleRoot(socket, _):
    try:
        distance = returnDistance()
        data = writeJson(distance)
        writeXML(data)
        page = """
            <!DOCTYPE HTML>
            <html>
            <head>
             <link rel="icon" href="favicon.ico" />
             <title>Abstandmesser</title>
             <link rel="stylesheet" href="style.css">
             <meta http-equiv="refresh" content="5">
            </head>
            <body>
              <h1>Hallo Wemos D1 mini</h1>
              <p>Distance: {0} cm;</p>
              <div class="files-container">
                  <div class="review_files">
                      <a target="_blank" href="#">Review HTML</a>
                      <a target="_blank" href="distance.json">Review JSON</a>
                      <a target="_blank" href="distance.xml">Review XML</a>
                  </div>
                  <div class="download_files">
                      <a href="#" download>Download HTML</a>
                      <a href="distance.json" download>Download JSON</a>
                      <a href="distance.xml" download>Download XML</a>
                  </div>
              </div>
            </body>
            </html>
            """.format(round(distance, 2))
        server.ok(socket, "200", "text/html", page)
    except Exception as e:
        server.err(socket, "500", "Internal Server Error")
        print("Exception in handleRoot:", e)

def writeJson(distance):
    try:
        try:
            with open("distance.json", "r") as f:
                data = json.load(f)
        except:
            data = []
            

        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*time.localtime()[:6])
        data.append({"distance": round(distance, 2), "time": timestamp})
        
        data = data[-10:]
        
        with open("distance.json", "w") as f:
            f.write("[\n")
            for i, entry in enumerate(data):
                f.write("    {\n")
                f.write('        "distance": {:.2f},\n'.format(entry["distance"]))
                f.write('        "time": "{}"\n'.format(entry["time"]))
                f.write("    }")
                if i < len(data) - 1:
                    f.write(",")
                f.write("\n")
            f.write("]\n")
            
            return data
        
    except Exception as e:
        print("Error writing JSON:", e)
                
def writeXML(data):
    try:
        with open("distance.xml", "w") as f:
            f.write("<distances>\n")
            for entry in data:
                f.write("  <entry>\n")
                f.write("    <distance>{:.2f}</distance>\n".format(entry["distance"]))
                f.write("    <time>{}</time>\n".format(entry["time"]))
                f.write("  </entry>\n")
            f.write("</distances>\n")
    except Exception as e:
        print("Error writing XML:", e)



def handleOnNotFound(socket):
    server.err(socket, "404", "File Not Found")

server.onNotFound(handleOnNotFound)
server.onPath("/", handleRoot)

server.begin()  


try:
    while True:
        server.handleClient()
except Exception as e:
    server.close()
