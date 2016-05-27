import os


def write_coafile(project_dir, settings):
    with open(os.path.join(project_dir, ".coafile"), "w") as coafile:
        for section in settings:
            coafile.write("[" + section + "]\n")
            for key in settings[section]:
                coafile.write(key + "=" + settings[section][key] + "\n")
            coafile.write("\n")
