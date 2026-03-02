def evaluate_state(depth, is_defender):
    return depth if is_defender else -depth

def minimax(depth, is_defender):
    if depth == 0:
        return evaluate_state(depth, is_defender)

    if is_defender:

        return max(minimax(depth-1, False), minimax(depth-1, False))
    else:
 
        return min(minimax(depth-1, True), minimax(depth-1, True))


score = minimax(3, True)
print("Score is:", score)
