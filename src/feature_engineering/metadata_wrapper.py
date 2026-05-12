def create_feature(value, source):

    return {
        "value": value,
        "source": source
    }


def wrap_features(parsed_data):

    wrapped = {}

    for key, value in parsed_data.items():

        if value is None:

            wrapped[key] = create_feature(
                None,
                "missing"
            )

        else:

            wrapped[key] = create_feature(
                value,
                "user"
            )

    return wrapped