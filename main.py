import os
import re
import shutil
import subprocess
import json

from validate_paths import validate_paths_json


UMODEL_EXPORT = r"/Game/Personalization/PlayerCards/*"
UMODEL_SAVE = r"/Game/Personalization/PlayerCards/*/*_UIData.uasset"
DISPLAY_NAME_OFFSET = int("0x76", base=16)

image_paths = {}
uidata_paths = []
display_names = {}
associated_names = {}


def read_paths_json():
    if os.path.exists("paths.json"):
        try:
            with open("paths.json", "rt") as paths_file:
                return json.load(paths_file)
        except:
            print("[ERROR] Could not open 'paths.json'\n")
            exit()
    else:
        paths_dict = {"valorant_path": "", "umodel_path": "", "aes_path": "",
                      "locres_path": "", "extract_path": "", "target_path": ""}
        with open("paths.json", "xt") as paths_file:
            json.dump(paths_dict, paths_file, indent=4)
            print("[ERROR] Created 'paths.json', fill out before running again\n")
            exit()


def normalize_paths(paths_dict):
    for path, value in paths_dict.items():
        paths_dict[path] = os.path.normpath(os.path.abspath(value))


def umodel_extract(paths_dict):
    print("=== UModel extract ===")
    umodel_filename = os.path.basename(paths_dict["umodel_path"])
    os.chdir(os.path.dirname(paths_dict["umodel_path"]))
    print("Extracting playercards...")
    subprocess1 = subprocess.Popen([umodel_filename, "-path=\"" + paths_dict["valorant_path"] + "\"",
                                    "-game=ue4.24", "-aes=@" + paths_dict["aes_path"], "-export", UMODEL_EXPORT],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess2 = subprocess.Popen([umodel_filename, "-path=\"" + paths_dict["valorant_path"] + "\"",
                                    "-game=ue4.24", "-aes=@" + paths_dict["aes_path"], "-save", UMODEL_SAVE],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess1.wait()
    subprocess2.wait()
    print("Moving exports...")
    subprocess1 = subprocess.Popen(["robocopy", ".\\Exports\\Game\\Personalization\\PlayerCards\\",
                                    paths_dict["extract_path"], "/E", "/IS", "/MOVE"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess1.wait()
    print("Moving saves...\n")
    subprocess1 = subprocess.Popen(["robocopy", ".\\Saves\\Game\\Personalization\\PlayerCards\\",
                                    paths_dict["extract_path"], "/E", "/IS", "/MOVE"],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    subprocess1.wait()


def index_cards(cards_path):
    for entry in os.listdir(cards_path):
        norm_entry = os.path.join(cards_path, entry)
        if os.path.isdir(norm_entry):
            index_cards(norm_entry)
        elif entry.endswith("UIData.uexp"):
            uidata_paths.append(norm_entry)
        elif entry.endswith(".png"):
            image_array = image_paths.get(cards_path, [])
            image_array.append(entry)
            image_paths[cards_path] = image_array
        elif not entry.endswith(".uasset"):
            print("[WARN] Unexpected file type:", norm_entry)


def get_display_name_from_uidata(uidata_path):
    with open(uidata_path, 'rb') as hex_file:
        hex_file.seek(DISPLAY_NAME_OFFSET)
        display_name = ""
        while (current_read := hex_file.read(1)) != b'\x00':
            display_name += current_read.decode("utf-8")
        return display_name


def find_card_display_names(locres_path):
    with open(locres_path, "rt", encoding="utf-8") as csv_file:
        locres = json.load(csv_file)
        for outer_key, each_dict in locres.items():
            for key, value in each_dict.items():
                if "ercard" in key.lower():
                    display_names[key] = value


def print_uidata_name_associations():
    print("UIData count: " + str(len(uidata_paths)) + "\n\n")
    for index in range(len(uidata_paths)):
        uidata = get_display_name_from_uidata(uidata_paths[index])
        print("UIData path: " + uidata_paths[index])
        print("UIData: " + uidata)
        if uidata in display_names.keys():
            print("Name: " + display_names[uidata] + "\n")
        else:
            print("Name: NOT FOUND\n")


def name_to_readable(image_name, card_name, display_new_name):
    image_name = re.sub("_(L1|L2|L|large)\.", " - Large.", image_name)
    image_name = re.sub("_(S1|S2|S|small)\.", " - Small.", image_name)
    image_name = re.sub("_(W1|W2|W|wide)\.", " - Wide.", image_name)
    sub_index = -4 if " - " not in image_name else image_name.index(" - ")
    return display_new_name + image_name[sub_index:]


def name_clean_not_allowed(name):
    return name.replace("/", "").replace("?", "").replace(":", "")


def copy_named_cards(cards_path, target_path):
    for uidata_path in uidata_paths:
        card_name = re.sub("(_1|_2|)_UIData.uexp", "", os.path.basename(uidata_path))
        uidata = get_display_name_from_uidata(uidata_path)
        display_name = display_names[uidata]
        display_name = name_clean_not_allowed(display_name)
        path = os.path.dirname(uidata_path)
        relative_path = os.path.normpath(path.replace(cards_path, ""))
        relative_path = os.path.join(os.path.dirname(relative_path), display_name)
        images = image_paths[path]
        os.makedirs(target_path + relative_path)
        for image_name in images:
            new_image_name = name_to_readable(image_name, card_name, display_name)
            shutil.copyfile(os.path.join(path, image_name),
                            os.path.join(target_path + relative_path, new_image_name))
        image_paths.pop(path)


def copy_unnamed_cards(cards_path, target_path):
    for image_path, images in image_paths.items():
        relative_path = os.path.normpath(image_path.replace(cards_path, ""))
        os.makedirs(target_path + relative_path)
        for image_name in images:
            shutil.copyfile(os.path.join(image_path, image_name),
                            os.path.join(target_path + relative_path, image_name))


paths_json = read_paths_json()
normalize_paths(paths_json)
paths_validated = validate_paths_json(paths_json)
if paths_validated:
    print(paths_validated)
    exit()

umodel_extract(paths_json)

print("Cleaning previous export...\n")
shutil.rmtree(paths_json["target_path"], ignore_errors=True)
os.mkdir(paths_json["target_path"])

print("Cataloguing cards...")
index_cards(paths_json["extract_path"])

print("\nExporting display names...\n")
find_card_display_names(paths_json["locres_path"])

print("Copying and renaming cards...\n")
copy_named_cards(paths_json["extract_path"], paths_json["target_path"])
copy_unnamed_cards(paths_json["extract_path"], paths_json["target_path"])

print("Cleaning export...")
shutil.rmtree(paths_json["extract_path"], ignore_errors=True)



