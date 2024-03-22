#!/usr/bin/env python3

import json
import shutil
from pathlib import Path


class LibraryUpdater:
    def __init__(self):
        self.folders = self.__read_folders_list(Path(".list-folder-library"))
        self.exercise_data = {}
        self.dir_lib = Path("ExerciseTester")
        self.file_name = "tester_lib.py"

    @staticmethod
    def __read_folders_list(file: Path) -> set:
        if file.exists():
            with open(file) as f:
                return set(f.read().splitlines())
        else:
            return set()

    def traverse(self):
        """Go through all folders with exercises and complete the checks"""
        for fold in self.folders:
            folder = Path(fold)
            if not folder.is_dir():
                break

            index_file = folder / "index.json"
            self.exercise_data = json.loads(index_file.read_text())

            self.__add_assets()
            index_file.write_text(json.dumps(self.exercise_data, indent=2, ensure_ascii=False))

            self.__put_file(folder)

    def __add_assets(self):
        if "assets" not in self.exercise_data["details"]:
            self.exercise_data["details"]["assets"] = {}
        if "host01" not in self.exercise_data["details"]["assets"]:
            self.exercise_data["details"]["assets"]["host01"] = []
        assets: list = self.exercise_data["details"]["assets"]["host01"]

        for file in self.dir_lib.iterdir():
            if file.is_file():
                self.__add_file_to_assets(assets, file)

    def __add_file_to_assets(self, assets: list, file: Path):
        lib = {"file": file.name, "target": f"/usr/local/lib/{self.dir_lib.name}", "chmod": "+x"}
        is_not_find = True
        for asset in assets:
            if asset["file"] == file.name:
                asset["target"] = lib["target"]
                asset["chmod"] = lib["chmod"]
                is_not_find = False
        if is_not_find:
            assets.append(lib)

    def __put_file(self, folder):
        dir_assets = folder / "assets"
        dir_assets.mkdir(parents=True, exist_ok=True)
        for file in self.dir_lib.iterdir():
            if file.is_file():
                shutil.copy(file, dir_assets / file.name)


if __name__ == '__main__':
    changer = LibraryUpdater()
    changer.traverse()
