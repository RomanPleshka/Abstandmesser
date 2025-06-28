import json

distance = (234, 234, 324, 324)


def jakdhfskd(distance):
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
            print(data)
            data2 = json.dump(data, f)
            return data, data2

    except Exception as e:
        print("Error writing JSON:", e)
        data, data2 = jakdhfskd(distance)
