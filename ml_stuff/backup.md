def get_rms_data(delay, points, timestamp: datetime):
    rms = 0

    for point in points:
        rms += point ** 2

    rms = math.sqrt(rms)
    rms /= len(points)

    return [f"prediction current_rms={rms} {int(timestamp.timestamp() * 1e6)}000"]
