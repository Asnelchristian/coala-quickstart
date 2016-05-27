def comma_split(response):
    result = []
    for item in response.replace(" ", ",").split(","):
        if len(item):
            result.append(item)

    return result
