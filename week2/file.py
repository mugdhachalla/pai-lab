import heapq

# Define the state class to represent the current state of the jugs
class State:
    def __init__(self, jug1, jug2, parent=None, action="Initial"):
        self.jug1 = jug1
        self.jug2 = jug2
        self.parent = parent
        self.action = action
        self.f = 0  # heuristic value

    def __lt__(self, other):
        return self.f < other.f


# Heuristic function
# h = minimum distance from target in either jug
def h(jug1, jug2, target):
    return min(abs(jug1 - target), abs(jug2 - target))


# Evaluation function f = g + h
def evaluate(state, target):
    state.f = h(state.jug1, state.jug2, target)


# Retrieve solution path
def get_path(state):
    path = []
    while state:
        path.append((state.jug1, state.jug2, state.action))
        state = state.parent
    return path[::-1]


# Solve water jug problem
def solve_water_jug_problem(capacity1, capacity2, target):
    initial_state = State(0, 0)
    evaluate(initial_state, target)

    open_list = []
    heapq.heappush(open_list, initial_state)

    closed_set = set()

    while open_list:
        current_state = heapq.heappop(open_list)

        if current_state.jug1 == target or current_state.jug2 == target:
            return get_path(current_state)

        if (current_state.jug1, current_state.jug2) in closed_set:
            continue

        closed_set.add((current_state.jug1, current_state.jug2))

        jug1 = current_state.jug1
        jug2 = current_state.jug2

        # Fill jug1
        new_state = State(capacity1, jug2, current_state, "Fill jug1")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

        # Fill jug2
        new_state = State(jug1, capacity2, current_state, "Fill jug2")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

        # Empty jug1
        new_state = State(0, jug2, current_state, "Empty jug1")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

        # Empty jug2
        new_state = State(jug1, 0, current_state, "Empty jug2")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

        # Pour jug1 -> jug2
        pour_amount = min(jug1, capacity2 - jug2)
        new_state = State(jug1 - pour_amount, jug2 + pour_amount,
                          current_state, "Pour jug1 to jug2")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

        # Pour jug2 -> jug1
        pour_amount = min(jug2, capacity1 - jug1)
        new_state = State(jug1 + pour_amount, jug2 - pour_amount,
                          current_state, "Pour jug2 to jug1")
        evaluate(new_state, target)
        heapq.heappush(open_list, new_state)

    return None


# Main function
def main():
    capacity1 = 4
    capacity2 = 3
    target = 2

    solution = solve_water_jug_problem(capacity1, capacity2, target)

    if solution:
        print("Solution found in", len(solution) - 1, "steps:\n")
        for i, step in enumerate(solution):
            print(f"Step {i}: {step}")
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()