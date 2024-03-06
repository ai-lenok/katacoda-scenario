#!/usr/bin/env python3

import os
import contextlib
import yaml
import subprocess
from pathlib import Path
import importlib.util
import sys
import logging
from importlib.machinery import SourceFileLoader


class Tester:

    def __init__(self):
        self.ignore_dirs = Tester.__read_ignore(Path(".kata-test-ignore"))
        self.root_dir = Path.cwd() / "temp_test"
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
        self.m = object
        self.metadata = {}
        self.dir_tests = Path
        self.checker = Path
        self.checker_new = Path
        self.init = {}
        self.tear_down = {}

    @staticmethod
    def __read_ignore(file: Path) -> set:
        if file.exists():
            with open(file) as f:
                return set(f.read().splitlines())
        else:
            return set()

    def __read_metadata(self, path: Path):
        path_metadata = path / "test" / "kata-test.yml"
        self.metadata = {}
        with open(path_metadata) as f:
            self.metadata = yaml.safe_load(f)

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
        for d in Path(".").iterdir():
            if d.is_dir() and d.name not in self.ignore_dirs:
                dir_with_tests = d / "test"
                if dir_with_tests.is_dir():
                    self.run_suite(d)

    def run_suite(self, path: Path):
        """Run all exercise checks"""
        self.log.info(f"Run tests: {path}")
        self.__read_metadata(path)
        self.__init_path_files(path)

        with self.working_directory(self.root_dir):
            self.m = self.dynamic_module(self.checker)
            for suite in self.metadata["suites"]:
                self.__run_test(suite)

            self.__after_all()

    def __init_path_files(self, path: Path):
        self.dir_tests = path.absolute() / "test"
        self.checker = path.absolute() / self.metadata.get("path-to-checking-script", "rules/finish.sh")

        if "script-before-each" in self.metadata:
            self.init = self.dir_tests / self.metadata["script-before-each"]
        if "script-after-all" in self.metadata:
            self.tear_down = self.dir_tests / self.metadata["script-after-all"]

    def __run_test(self, suite: dict):
        self.log.debug(f'Start "{suite["name"]}"')
        self.__before_each()
        self.__run_script_before_checker(suite)

        params = suite.get("params", {})
        params["checking_script"] = self.__get_path_to_script_for_putting_to_checker(suite)
        checker = self.m.Checker(**params)
        actual = checker.check()
        self.log.debug(f"Result: {actual}")
        expected = suite["result-text"]
        if expected != actual:
            self.log.warning(f'Script: {suite["name"]}\nExpected: {expected}\n  Actual: {actual}')

    def __get_path_to_script_for_putting_to_checker(self, suite):
        if "script-put-to-checker" in suite:
            path_script_test_case = self.dir_tests / "suites" / suite["script-put-to-checker"]
        else:
            path_script_test_case = "script.sh"
        return path_script_test_case

    def __run_script_before_checker(self, suite):
        if "script-run-before-checker" in suite:
            path = self.dir_tests / "suites" / suite["script-run-before-checker"]
            self.run_script("Run script", path)

    def __before_each(self):
        if self.init:
            self.run_script("Init", self.init)

    def __after_all(self):
        if self.tear_down:
            self.run_script("Tear down", self.tear_down)

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
