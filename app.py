from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class RobotGrid:
    def __init__(self, n, paths):
        self.n = n  # Number of stations
        self.paths = paths

    def find_least_expensive_route(self, start, end, max_stops):
        import sys

        # Validate start and end station
        if start < 0 or start >= self.n or end < 0 or end >= self.n:
            return -1, [], "Invalid station numbers."

        # Initialize energy costs and previous stations
        energy_costs = [sys.maxsize] * self.n
        energy_costs[start] = 0
        previous_stations = [-1] * self.n

        # Relaxation of edges up to max_stops + 1 times
        for _ in range(max_stops + 1):
            updated = False
            for from_i, to_i, cost in self.paths:
                # If we find a cheaper way to reach to_i
                if energy_costs[from_i] != sys.maxsize and energy_costs[from_i] + cost < energy_costs[to_i]:
                    energy_costs[to_i] = energy_costs[from_i] + cost
                    previous_stations[to_i] = from_i
                    updated = True

            # Debugging statement to track updates
            print(f"After {_ + 1} stops: {energy_costs}")

            if not updated:
                break

        # If no valid path found
        if energy_costs[end] == sys.maxsize:
            return -1, [], "No path found."

        # Backtrack to find the path
        path = []
        station = end
        while station != -1:
            path.append(station)
            station = previous_stations[station]
        path.reverse()

        return energy_costs[end], path, None


@app.route('/find_route', methods=['POST'])
def find_route():
    data = request.json
    start = int(data.get('start'))
    end = int(data.get('end'))
    max_stops = int(data.get('max_stops'))

    # Define the paths (make sure these are valid)
    paths = [
        (0, 1, 100),  # From station 0 to 1 costs 100 energy
        (1, 2, 50),   # From station 1 to 2 costs 50 energy
        (0, 2, 200),  # From station 0 to 2 costs 200 energy
        (2, 3, 20),   # From station 2 to 3 costs 20 energy
        (1, 3, 70)    # From station 1 to 3 costs 70 energy
    ]
    robot_grid = RobotGrid(4, paths)

    energy_cost, path, error_message = robot_grid.find_least_expensive_route(start, end, max_stops)

    # Debugging for better visibility of returned values
    print(f"Requested: Start: {start}, End: {end}, Max Stops: {max_stops}")
    print(f"Calculated: Energy Cost: {energy_cost}, Path: {path}, Error: {error_message}")

    if error_message:
        return jsonify({"error": error_message}), 400  # Return error with 400 (Bad Request) status

    return jsonify({
        "energy_cost": energy_cost,
        "path": path
    })


if __name__ == '__main__':
    app.run(debug=True)
