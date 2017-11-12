def backtrack(p, choose_configuration, expand_candidate, is_solution, dead_end):
    frontier = {(None, p)}  # frontier set of configurations
    while not len(frontier) == 0:
        x, y = choose_configuration(p, frontier)  # most promising configuration
        for candidate in expand_candidate(p, (x, y)):  # candidate extensions
            if is_solution(p, candidate):
                return candidate
            elif not dead_end(p, candidate):
                frontier |= candidate
    return None