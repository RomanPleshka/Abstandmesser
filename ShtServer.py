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
        data = write_data(distance)
        write_data(distance, "xml")

        with open("template.tpl", "r") as f:
            template = f.read()

        html = template("template.tpl", {"distance": distance, "data": data})
        f.write(html)
        print(html)

        server.ok(socket, "200", "text/html", page)

    except Exception as e:
        server.err(socket, "500", "Internal Server Error")
        print("Exception in handleRoot:", e)


def write_data(distance, format="json"):
    """Die Funktion write_data(distance, format) speichert einen gemessenen Abstand zusammen mit einem Zeitstempel entweder
    als JSON- oder XML-Datei. Sie prüft zunächst, ob bereits eine Datei mit dem gewünschten Format existiert, lädt deren Inhalt
    und fügt den neuen Messwert hinzu. Um Speicher zu sparen, werden nur die letzten zehn Einträge behalten. Anschließend wird
    die aktualisierte Liste wieder in die Datei geschrieben entweder im JSON-Format für einfache Datenverarbeitung
    oder im XML-Format für strukturierte Anwendungen."""
    filename = "distance." + format
    data = []

    # Vorhandene Datei laden (wenn vorhanden)
    try:
        with open(filename, "r") as f:
            if format == "json":
                data = json.load(f)
            elif format == "xml":
                # einfache XML-Zeilenweise-Auswertung
                lines = f.readlines()
                for i in range(1, len(lines) - 1, 5):
                    d = float(
                        lines[i + 1]
                        .strip()
                        .replace("<distance>", "")
                        .replace("</distance>", "")
                    )
                    t = (
                        lines[i + 2]
                        .strip()
                        .replace("<time>", "")
                        .replace("</time>", "")
                    )
                    data.append({"distance": d, "time": t})
    except:
        pass

    # Zeitstempel erzeugen
    timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        *time.localtime()[:6]
    )
    data.append({"distance": round(distance, 2), "time": timestamp})
    data = data[-10:]  # nur die letzten 10 Einträge behalten

    # Datei schreiben
    with open(filename, "w") as f:
        if format == "json":
            json.dump(data, f)
        elif format == "xml":
            f.write("<data>\n")
            for entry in data:
                f.write("  <entry>\n")
                f.write("    <distance>{:.2f}</distance>\n".format(entry["distance"]))
                f.write("    <time>{}</time>\n".format(entry["time"]))
                f.write("  </entry>\n")
            f.write("</data>\n")

    return data


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
