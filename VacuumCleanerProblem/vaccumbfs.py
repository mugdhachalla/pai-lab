from collections import deque

# Define initial state
initial_state = ('A', 'Dirty', 'Dirty')

# Goal test
def is_goal(state):
    return state[1] == 'Clean' and state[2] == 'Clean'

# Actions
def successors(state):
    loc, rA, rB = state
    result = []
    
    # SUCK action
    if loc == 'A' and rA == 'Dirty':
        result.append((('A','Clean',rB), 'Suck'))
    if loc == 'B' and rB == 'Dirty':
        result.append((('B',rA,'Clean'), 'Suck'))
    
    # Move actions
    if loc == 'A':
        result.append((('B',rA,rB), 'MoveRight'))
    else:
        result.append((('A',rA,rB), 'MoveLeft'))
    
    return result

def bfs_search(initial):
    queue = deque([(initial, [])])
    visited = set([initial])
    
    while queue:
        state, path = queue.popleft()
        
        if is_goal(state):
            return path
        
        for (next_state, action) in successors(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [action]))
    return None

solution = bfs_search(initial_state)
print("Solution:", solution)
