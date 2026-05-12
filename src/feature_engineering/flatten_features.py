def flatten_features(data):
    flattened = {}
    
    for feature, info in data.items():
        flattened[feature] = info["value"]

    return flattened