import os
import operator

from coala_quickstart.exts import exts


def get_popular_languages(file_paths):
    results = {}
    for ext in exts:
        results[exts[ext]] = 0
    results["Unknown"] = 0

    for file_path in file_paths:
        name, ext = os.path.splitext(file_path)
        if ext in exts:
            results[exts[ext]] += 1
        else:
            results["Unknown"] += 1
    if len(file_paths):
        for ext in results:
            results[ext] = (100.0 * results[ext]) / len(file_paths)

    languages = sorted(
        results.items(),
        key=operator.itemgetter(1),
        reverse=True)
    used_languages = []
    append_list = []
    for lang, percent in languages:
        if lang == "Unknown":
            append_list += [(lang, int(percent))]
            continue
        if int(percent) == 0:
            break
        else:
            used_languages += [(lang, int(percent))]

    return used_languages + append_list
