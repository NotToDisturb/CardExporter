import os
import json


def validate_nothing(path, value):
    pass


def validate_not_empty_path(path, value):
    if value == "":
        return "[ERROR] '" + path + "' cannot be empty"


def validate_standard_folder_path(path, value):
    if value == "":
        return "[ERROR] '" + path + "' cannot be empty"
    elif not os.path.exists(value):
        return "[ERROR] '" + path + "' does not exist"
    elif not os.path.isdir(value):
        return "[ERROR] '" + path + "' is not a folder"


def validate_standard_file_path(path, value):
    if value == "":
        return "[ERROR] '" + path + "' cannot be empty"
    elif not os.path.exists(value):
        return "[ERROR] '" + path + "' does not exist"
    elif not os.path.isfile(value):
        return "[ERROR] '" + path + "' is not a file"


def validate_locres_file_path(path, value):
    if value == "":
        return "[ERROR] '" + path + "' cannot be empty"
    elif not os.path.exists(value):
        return "[ERROR] '" + path + "' does not exist"
    elif not os.path.isfile(value):
        return "[ERROR] '" + path + "' is not a file"
    else:
        try:
            with open(value, "rt", encoding="utf-8") as json_file:
                json.load(json_file)
        except ValueError:
            return "[ERROR] Error found while opening '" + path + "'"


validator_hub = {"valorant_path": validate_standard_folder_path,
                 "umodel_path": validate_standard_file_path,
                 "aes_path": validate_standard_file_path,
                 "locres_path": validate_standard_file_path,
                 "extract_path": validate_not_empty_path,
                 "target_path": validate_not_empty_path}


def validate_paths_json(paths_dict):
    for path, value in paths_dict.items():
        validate_function = validator_hub.get(path, None)
        if validate_function:
            validate_result = validate_function(path, value)
            if validate_result:
                return validate_result
        else:
            print("[WARN] '" + path + "' is not an expected path")
