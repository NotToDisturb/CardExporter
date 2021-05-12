import os
import csv
import json
import subprocess

LOCRES_CONFIG = "locres_config.json"
RELATIVE_LOCRES_PAK = os.path.normpath("\\live\\ShooterGame\\Content\\Paks\\en_US_Text-WindowsClient.pak")


class LocresExporter:
    def __init__(self):
        self.config = load_config()
        self.normalize_paths()

    def get_aes_key(self):
        with open(self.config["aes_path"], "rt") as aes_file:
            return str.encode(aes_file.read())

    def export_locres(self):
        locres_pak = self.config["valorant_path"] + RELATIVE_LOCRES_PAK
        exporter_process = subprocess.Popen([self.config["quickbms_path"], self.config["ut4_path"],
                                             locres_pak, self.config["working_path"]],
                                            stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        exporter_process.communicate(self.get_aes_key())
        exporter_process.wait()

    def locres_to_csv(self):
        locres_path = os.path.join(self.config["working_path"], "Game.locres")
        parser_process = subprocess.Popen([self.config["l2c_path"], locres_path],
                                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        parser_process.wait()
        os.remove(locres_path)

    def normalize_paths(self):
        for path, value in self.config.items():
            self.config[path] = os.path.normpath(os.path.abspath(value))

    def csv_to_json(self, json_path, force_overwrite=False):
        csv_path = os.path.join(self.config["working_path"], "Game.csv")
        with open(csv_path, "rt", encoding="utf-8") as csv_locres:
            csv_read = csv.DictReader(csv_locres, delimiter=",")
            json_dict = {}
            for index, line in enumerate(csv_read):
                add_child(json_dict, line["Key"].split("/"), line["Source"])

            self.__begin_json_parse_dump(json_path, json_dict, force_overwrite)
        os.remove(csv_path)

    @staticmethod
    def __begin_json_parse_dump(json_path, json_dict, force_overwrite):
        if os.path.exists(json_path):
            if not force_overwrite:
                print("[WARN] Target '" + json_path + "' already exists,")
                overwrite = input("       Overwrite it? (y/n) ")
            else:
                overwrite = "y"
            if overwrite.lower() == "y" or overwrite.lower() == "yes":
                LocresExporter.__dump_json_parse(json_path, json_dict, "wt")
        else:
            LocresExporter.__dump_json_parse(json_path, json_dict, "xt")

    @staticmethod
    def __dump_json_parse(json_path, json_dict, write_type):
        with open(json_path, write_type) as json_locres:
            json.dump(json_dict, json_locres, indent=4)


def load_config():
    if os.path.exists(LOCRES_CONFIG):
        try:
            with open(LOCRES_CONFIG, "rt") as config_file:
                return json.load(config_file)
        except OSError:
            print("[ERROR] Could not open '" + LOCRES_CONFIG + "'\n")
            exit()
        except ValueError:
            print("[ERROR] '" + LOCRES_CONFIG + "' has an invalid structure\n")
            exit()
    else:
        config_dict = {"quickbms_path": "", "ut4_path": "", "l2c_path": "",
                       "valorant_path": "", "working_path": ""}
        with open(LOCRES_CONFIG, "xt") as paths_file:
            json.dump(config_dict, paths_file, indent=4)
            print("[ERROR] Created '" + LOCRES_CONFIG + "', fill out before running again\n")
            exit()


def add_child(curr_dict, remaining_childs, child_contents):
    if len(remaining_childs) == 1:
        curr_dict[remaining_childs[0]] = child_contents
    else:
        next_dict = curr_dict.get(remaining_childs[0], {})
        curr_dict[remaining_childs[0]] = next_dict
        add_child(next_dict, remaining_childs[1:], child_contents)
