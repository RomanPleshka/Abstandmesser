import ESP8266WebServer as server
from WifiConnect import wifiConnect
import network
import machine
import json
from hcsr04_reading import returnDistance
import time


# ssid = "gsog-iot"
# password = "IOT_Projekt_BFK-S_2022"
# ssid = "POCO"
# password ="123456789"
ssid = "Jaron"
password = "12345678"

wifiConnect(ssid, password)


def handleRoot(socket, _):
    """
    Behandelt HTTP-Anfragen an die Root-URL.

    Ruft die aktuelle Distanz vom Sensor ab, speichert sie im JSON- und XML-Format,
    und liefert eine HTML-Seite mit dem aktuellen Messwert zurück.

    Args:
        socket: Der Socket, über den die HTTP-Verbindung läuft.
    """
    try:
        distance = returnDistance()
        data = writeJson(distance)
        writeXML(data)

        with open("template.tpl", "r") as f:
            template = f.read()
        for key, value in distance.items():
            template = template.replace("{{ " + data + " }}", distance)

        html = template("template.tpl", {"distance": distance, "data": data})
        f.write(html)
        print(html)

        server.ok(socket, "200", "text/html", page)

    except Exception as e:
        server.err(socket, "500", "Internal Server Error")
        print("Exception in handleRoot:", e)


def writeJson(distance):
    """
    Schreibt die aktuelle Distanz in eine JSON-Datei und speichert die letzten 10 Einträge.

    Falls bereits eine JSON-Datei existiert, wird sie geladen und aktualisiert.
    Die Daten enthalten Zeitstempel und werden formatiert gespeichert.

    Args:
        distance (float): Der gemessene Abstand in Zentimetern.

    Returns:
        list: Die aktualisierte Liste der Messdaten.
    """
    try:
        try:
            with open("distance.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
            *time.localtime()[:6]
        )
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
    """
    Schreibt die aktuelle Distanz in eine XML-Datei und speichert die letzten 10 Einträge.

    Falls bereits eine XML-Datei existiert, wird sie geladen und aktualisiert.
    Die Daten enthalten Zeitstempel und werden formatiert gespeichert.

    Args:
        data (list): Eine Liste von Dictionaries mit den Feldern "distance" (float) und "time" (str).
    """
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
