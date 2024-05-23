def algorithms_context(request):
    algorithms = [
        {"key": "", "name": "Hill climber"},
        {"key": "hc_restarts", "name": "Hill climber with restarts"},
        {"key": "hc_larger_radii", "name": "Hill climber with larger search radii"}
    ]
    return {'algorithms': algorithms}
