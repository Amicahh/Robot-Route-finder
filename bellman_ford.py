import sys
import logging

class RobotGrid:
    def __init__(self, n, paths):
        self.n = n
        self.paths = paths
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

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
            return -1, []

        # Reconstruct the path from end to start using the previous_stations array
        path = []
        station = end
        while station != -1:
            path.append(station)
            station = previous_stations[station]

        # Reverse the path to go from start to end
        path.reverse()

        self.logger.info(f"Final path: {path} with energy cost: {energy_costs[end]}")
        return energy_costs[end], path
