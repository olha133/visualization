def algorithms_context(request):
    algorithms = [
        {"key": "", "name": "Hill climbing", "description": "Simple algorithm that starts with an initial solution and then iteratively makes small changes to it in order to improve the solution."},
        {"key": "hc_restarts", "name": "Hill climbing with restarts", "description": "A technique for restarting an algorithm from a new initial state when it has found a local optimum."},
        {"key": "hc_larger_radii", "name": "Hill climbing with larger search radii", "description": "A technique that allows the algorithm to explore a larger neighborhood around the current solution to find the next step."}
    ]
    return {'algorithms': algorithms}
