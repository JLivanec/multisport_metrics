def run_pace_formatted(dist, t):
    # Calculate pace in minutes per mile
    pace_seconds = t / dist
    pace_minutes = pace_seconds // 60
    pace_seconds %= 60
    return "{:02d}:{:02d}".format(int(pace_minutes), int(pace_seconds))

def run_pace(dist, t):
    pace_seconds = t / dist
    return pace_seconds / 60

def mph(dist, t):
    t_hours = t / 3600
    mph = dist / t_hours
    return mph

def swim_pace(dist, t, meters = True, formatted = True):
    # Convert meters to yards
    if meters:
        dist = dist * 1.09361

    # Calculate pace per 100 yards
    pace = (t / dist) * 100
    
    pace_m = pace // 60
    pace_s = pace % 60
    # Format pace as MM:SS
    return "{:02d}:{:02d}".format(int(pace_m), int(pace_s))

# Example usage:
print(swim_pace(400, 6*60, meters = False, formatted = True))