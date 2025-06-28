import http.client
import json
import time

while (True):
    try:
        # Connection zu IP von ESP
        connection = http.client.HTTPConnection('10.1.230.185', 80)
        connection.request('GET', '/distance.json')

        response = connection.getresponse()
        data = response.read()
        connection.close()

        if data:
            jsonData = json.loads(data)
            print(json.dumps(jsonData[-1], indent=4))

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(5);