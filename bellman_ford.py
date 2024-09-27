import sys
import logging

class RobotGrid:
    def __init__(self, n, paths):
        self.n = n
        self.paths = paths
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def update_paths(self, new_paths):
        """Function to update grid with new paths (e.g., dynamic obstacles)."""
        self.paths = new_paths
        self.logger.info("Grid paths updated.")

    def find_least_expensive_route(self, start, end, max_stops):
        # Initialize costs with infinity, except for the start node
        energy_costs = [sys.maxsize] * self.n
        energy_costs[start] = 0

        # To track the stations visited to reconstruct the path later
        previous_stations = [-1] * self.n

        # Bellman-Ford-like logic with a focus on stopping when max_stops is reached
        for iteration in range(max_stops + 1):  # +1 to allow up to the max stops
            updated = False
            for from_i, to_i, cost in self.paths:
                # Only update if the cost from the source station isn't infinity
                if energy_costs[from_i] != sys.maxsize and energy_costs[from_i] + cost < energy_costs[to_i]:
                    energy_costs[to_i] = energy_costs[from_i] + cost
                    previous_stations[to_i] = from_i
                    updated = True  # Mark that we updated a value in this iteration
            
            # Log the intermediate energy costs for debugging
            self.logger.info(f"Energy costs after iteration {iteration}: {energy_costs}")
            
            # If no update was made in this iteration, break early to save computation
            if not updated:
                self.logger.info(f"No updates in iteration {iteration}, stopping early.")
                break

        # If there's no valid path to the end station, return -1
        if energy_costs[end] == sys.maxsize:
            self.logger.info(f"No valid route found from {start} to {end} within {max_stops} stops.")
            return -1, [], "No valid path found."

        # Reconstruct the path from end to start using the previous_stations array
        path = []
        station = end
        while station != -1:
            path.append(station)
            station = previous_stations[station]

        # Reverse the path to go from start to end
        path.reverse()

        # Smoothing the path to remove unnecessary nodes (simplified for this example)
        smoothed_path = self.smooth_path(path)

        self.logger.info(f"Final path: {smoothed_path} with energy cost: {energy_costs[end]}")
        return energy_costs[end], smoothed_path, None

    def smooth_path(self, path):
        """Optional path smoothing to simplify the final route."""
        # Logic to remove unnecessary points (simplified version)
        if len(path) < 3:
            return path  # No smoothing needed for small paths
        smoothed = [path[0]]  # Start from the first point
        for i in range(1, len(path) - 1):
            # Compare if we can skip a point (this logic can be expanded)
            if path[i] != path[i-1] + path[i+1]:
                smoothed.append(path[i])
        smoothed.append(path[-1])  # Ensure the end point is always included
        return smoothed
