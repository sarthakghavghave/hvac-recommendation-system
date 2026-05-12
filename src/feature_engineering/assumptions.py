def get_assumptions(data):

    assumptions = []

    for feature, info in data.items():

        if info["source"] in ["inferred", "derived"]:

            assumptions.append({
                "feature": feature,
                "value": info["value"],
                "source": info["source"]
            })

    return assumptions