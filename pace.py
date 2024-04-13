def run_pace_formatted(dist, t, formatted = True):
    # Calculate pace in minutes per mile
    pace_seconds = t / dist
    if not formatted:
        return pace_seconds / 60
    pace_minutes = pace_seconds // 60
    pace_seconds %= 60
    return "{:02d}:{:02d}".format(int(pace_minutes), int(pace_seconds))

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

    if not formatted:
        return pace
    
    pace_m = pace // 60
    pace_s = pace % 60
    # Format pace as MM:SS
    return "{:02d}:{:02d}".format(int(pace_m), int(pace_s))