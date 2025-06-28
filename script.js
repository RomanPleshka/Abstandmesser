document.addEventListener("DOMContentLoaded", function () {
    const tbody = document.getElementById("data");
    console.log(json_data);

    json_data.forEach(row => {
        const tr = document.createElement("tr");

        const tdDistance = document.createElement("td");
        tdDistance.textContent = row.distance;
        tr.appendChild(tdDistance);


        const tdTime = document.createElement("td");
        tdTime.textContent = row.time;
        tr.appendChild(tdTime);

        tbody.appendChild(tr);
    });
    // Daten für das Bubble Chart vorbereiten
    let data = json_data.map(entry => ({
        x: entry.distance,
        y: entry.distance,
        r: 5 // Radius der Blasen
    }));

    new Chart(
        document.getElementById('chart'),
        {
            type: 'bubble',
            data: {
                datasets: [
                    {
                        label: 'Distanz',
                        data: data,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                aspectRatio: 1,
                scales: {
                    x: {
                        min: 0, // Minimumwert für die x-Achse
                        max: 200, // Maximumwert für die x-Achse
                        ticks: {
                            callback: value => `${value} m`
                        },
                        title: {
                            display: true,
                            text: 'Distanz (Meter)'
                        }
                    },
                    y: {
                        min: 0, // Minimumwert für die y-Achse
                        max: 200, // Maximumwert für die y-Achse
                        ticks: {
                            callback: value => `${value} m`
                        },
                        title: {
                            display: true,
                            text: 'Distanz (Meter)'
                        }
                    }
                }
            }
        }
    );


});