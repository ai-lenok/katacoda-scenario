#!/usr/bin/env python3

import os
import contextlib
import json
import pathlib
import subprocess
from pathlib import Path
import importlib.util
import sys
import logging
from importlib.machinery import SourceFileLoader


class Tester:

    def __init__(self):
        self.ignore_dirs = Tester.__read_ignore()
        self.root_dir = Path.cwd() / "temp_test"
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        self.m = object
        self.suite = {}
        self.dir_tests = Path
        self.checker = Path
        self.init = Path
        self.tear_down = Path

    @staticmethod
    def __read_ignore() -> set:
        file = Path(".testignore")
        if file.exists():
            with open(file) as f:
                return set(f.read().splitlines())
        else:
            return set()

    @staticmethod
    def __read_metadata(path: Path) -> dict:
        file_metadata = path / "test" / "test.json"
        metadata = {}
        with open(file_metadata) as f:
            metadata = json.load(f)
        return metadata

    def __run_script(self, path: Path):
        try:
            subprocess.run(['chmod', '+x', path])
            process = subprocess.run([path],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)

            stdout = process.stdout.strip()
            stderr = process.stderr.strip()
            return stdout, stderr
        except Exception as ex:
            self.log.error(ex)
            return "", ""

    def run_script(self, prefix: str, path: Path):
        if path.exists():
            stdout, stderr = self.__run_script(path)
            self.log.debug(f"{prefix}: {stdout}")

    def traverse(self):
        """Go through all folders with exercises and complete the checks"""
        for d in pathlib.Path(".").iterdir():
            if d.is_dir() and d.name not in self.ignore_dirs:
                dir_with_tests = d / "test"
                if dir_with_tests.is_dir():
                    self.run_suite(d)

    def run_suite(self, path: Path):
        """Run all exercise checks"""
        self.log.info(f"Run tests: {path}")

        metadata = self.__read_metadata(path)
        self.suite = metadata["results"]
        self.log.debug(self.suite)

        self.init_path_file(path)

        with self.working_directory(self.root_dir):
            self.run_script("Init", self.init)

            self.m = self.dynamic_module(self.checker)
            for script_name in self.suite:
                self.__run_test(script_name)

            self.run_script("Tear down", self.tear_down)

    def init_path_file(self, path: Path):
        self.dir_tests = path.absolute() / "test"
        self.checker = path.absolute() / "rules" / "finish.sh"
        self.init = self.dir_tests / "init.py"
        self.tear_down = self.dir_tests / "tearDown.py"

    def __run_test(self, script_name: str):
        script_path = self.dir_tests / "map" / script_name
        self.log.debug(script_path)
        checker = self.m.Checker(script_path)
        actual = checker.check()
        self.log.debug(f"Actual: {actual}")
        expected = self.suite[script_name]
        if expected != actual:
            self.log.warning(f"Script: {script_name}\nExpected: {expected}\n  Actual: {actual}")

    @staticmethod
    def dynamic_module(path: Path):
        """Dynamically load the module at the specified file path"""
        module_name = "Checker"
        loader = SourceFileLoader(module_name, str(path))
        spec = importlib.util.spec_from_loader(module_name, loader)
        module_obj = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module_obj
        spec.loader.exec_module(module_obj)
        return module_obj

    @contextlib.contextmanager
    def working_directory(self, path: Path):
        """Changes working directory and returns to previous on exit."""
        prev_cwd = Path.cwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(prev_cwd)


if __name__ == '__main__':
    tester = Tester()
    tester.traverse()
