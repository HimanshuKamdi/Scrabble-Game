class AirportScheduler:
    def __init__(self):
        self.flights = ['AA123', 'BA456', 'CX789','FH234']
        self.time_slots = ['08:00', '09:30', '11:00','13:30']
        self.lanes = ['Lane1', 'Lane2', 'Lane3','Lane4']
        self.schedule = {}

        # Initialize schedule with empty slots
        for time_slot in self.time_slots:
            self.schedule[time_slot] = {lane: None for lane in self.lanes}

    def is_valid_assignment(self, flight, time_slot, lane):
        # Check if the assignment is valid based on constraints
        return (
            all(self.schedule[time_slot][other_lane] != flight for other_lane in self.lanes) and
            self.schedule[time_slot][lane] is None
        )

    def backtracking(self):
        return self.backtrack()

    def backtrack(self):
        # Find unassigned variable
        unassigned = self.find_unassigned_variable()
        if not unassigned:
            return True  # All variables are assigned, solution found

        time_slot, lane = unassigned

        for flight in self.flights:
            if self.is_valid_assignment(flight, time_slot, lane):
                # Assign value
                self.schedule[time_slot][lane] = flight

                # Recursively check the next variable
                if self.backtrack():
                    return True  # Solution found

                # If the assignment leads to failure, backtrack and try the next value
                self.schedule[time_slot][lane] = None

        return False  # No valid assignment found for the current variable

    def find_unassigned_variable(self):
        # Find the first unassigned variable
        for time_slot, lanes in self.schedule.items():
            for lane, flight in lanes.items():
                if flight is None:
                    return time_slot, lane
        return None

    def schedule_flight(self, flight, action, time_slot, lane):
        if action == 'arrival' or action == 'departure':
            if self.is_valid_assignment(flight, time_slot, lane):
                self.schedule[time_slot][lane] = flight
                print(f"Successfully scheduled {flight} {action} at {time_slot} in {lane}")
            else:
                print(f"Error: {flight} conflicts with another flight at {time_slot}")
        else:
            print("Error: Invalid action")

    def display_schedule(self):
        print("\nCurrent Schedule:")
        for time_slot, lanes in self.schedule.items():
            for lane, flight in lanes.items():
                print(f"{time_slot} - {lane}: {flight}" if flight else f"{time_slot} - {lane}: Empty")


def main():
    scheduler = AirportScheduler()

    while True:
        print("\n1. View Schedule\n2. Schedule Flight\n3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            scheduler.display_schedule()

        elif choice == '2':
            flight_number = input("Enter flight number: ")
            action = input("Enter action (arrival/departure): ")
            time_slot = input("Enter time slot (in 24hrs format): ")
            lane = input("Enter lane: ")

            scheduler.schedule_flight(flight_number, action, time_slot, lane)

        elif choice == '3':
            print("Finding optimal schedule using backtracking...")
            if scheduler.backtracking():
                print("Optimal schedule found!")
                scheduler.display_schedule()
            else:
                print("No solution found.")

            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()