from flask import Flask, request, jsonify
from flask_cors import CORS
from bellman_ford import RobotGrid  

app = Flask(__name__)
CORS(app)

# New route for dynamic obstacle updates
@app.route('/update_grid', methods=['POST'])
def update_grid():
    data = request.json
    paths = data.get('paths')  # New set of paths with obstacles
    n = int(data.get('n'))
    robot_grid = RobotGrid(n, paths)
    return jsonify({"message": "Grid updated successfully!"}), 200

@app.route('/find_route', methods=['POST'])
def find_route():
    data = request.json
    start = int(data.get('start'))
    end = int(data.get('end'))
    max_stops = int(data.get('max_stops'))

    # Define the paths, make sure these are valid
    paths = [
        (0, 1, 100),
        (1, 2, 50),
        (0, 2, 200),
        (2, 3, 20),
        (1, 3, 70)
    ]
    
    robot_grid = RobotGrid(4, paths)
    energy_cost, path, error_message = robot_grid.find_least_expensive_route(start, end, max_stops)

    if error_message:
        return jsonify({"error": error_message}), 400

    return jsonify({
        "energy_cost": energy_cost,
        "path": path
    })

if __name__ == '__main__':
    app.run(debug=True)
