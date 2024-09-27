document.getElementById('findRouteBtn').addEventListener('click', async function() {
    const startStation = document.getElementById('startStation').value;
    const endStation = document.getElementById('endStation').value;
    const maxStops = document.getElementById('maxStops').value;

    const data = {
        start: parseInt(startStation),
        end: parseInt(endStation),
        max_stops: parseInt(maxStops)
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/find_route', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            document.getElementById('result').innerHTML = 
                `Minimum Energy: ${result.energy_cost}<br>Path: ${result.path.join(' -> ')}`;
        } else {
            document.getElementById('result').innerHTML = `Error: ${result.error}`;
        }
    } catch (error) {
        console.error('Error occurred while finding the route:', error);
        document.getElementById('result').innerHTML = 'Error occurred while finding the route.';
    }
});
