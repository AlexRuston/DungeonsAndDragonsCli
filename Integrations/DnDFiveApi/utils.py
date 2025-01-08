def unwrap(data):
    if not 'results' in data:
        return {}

    return data['results']