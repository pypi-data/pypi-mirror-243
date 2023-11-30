from __future__ import annotations

import datetime
import logging
import multiprocessing
import os
import time
from abc import ABC, abstractmethod
from multiprocessing import Process
from pathlib import Path
from typing import Set

from sapioseleniumlib.util.driver import BrowserType, SapioSeleniumDriver, SapioTestDriverFileManager
from sapioseleniumlib.widgets.do import Do

auto_run_id_accession: int = 1


class VeloxSeleniumScript(ABC):
    _browser_type: BrowserType
    _sapio_url: str
    _username: str
    _password: str
    _lab_name: str | None
    _headless: bool
    _driver: SapioSeleniumDriver
    _do: Do
    _file_man: SapioTestDriverFileManager
    _browser_binary_location: str | None

    def __init__(self, browser_type: BrowserType, sapio_url: str, username: str, password: str, headless: bool,
                 file_man: SapioTestDriverFileManager | None = None, run_id: str | None = None,
                 browser_binary_location: str | None = None, lab_name: str | None = None):
        global auto_run_id_accession
        if not run_id:
            run_id = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S' + "_") + str(auto_run_id_accession)
            auto_run_id_accession += 1
        if not file_man:
            path: str = os.path.join(Path.home(), 'sapio_selenium_runs', run_id)
            file_man = SapioTestDriverFileManager(path)
        self._file_man = file_man
        self._browser_type = browser_type
        self._headless = headless
        self._sapio_url = sapio_url
        self._username = username
        self._password = password
        self._lab_name = lab_name
        self._browser_binary_location = browser_binary_location

    @property
    def file_man(self) -> SapioTestDriverFileManager:
        """
        Sapio selenium testing file manager for file I/O.
        """
        return self._file_man

    @property
    def do(self) -> Do:
        return self._do

    @property
    def driver(self) -> SapioSeleniumDriver:
        return self._driver

    def screenshot(self, file_name: str):
        """
        Create a new screenshot file and store it under the directory managed by the script's file manager.
        """
        if not file_name.endswith(".png"):
            file_name = file_name + "-" + str(time.time())
        file_name = _slugify(file_name)
        file_name = file_name + ".png"
        file_path = os.path.join(self._file_man.screenshot_dir, file_name)
        success = self.driver.take_screenshot(file_path)
        if success:
            logging.info("Saved screenshot: " + file_path)
        else:
            logging.error("Failed to save screenshot: " + file_path)

    def run(self) -> None:
        self._before_setup()
        self._setup()
        try:
            self._run_selenium_script()
        except Exception as e:
            logging.exception("Error while running test script ", e)
            self.driver.take_screenshot("FAILURE")
        self._teardown()

    @abstractmethod
    def _run_selenium_script(self) -> None:
        """
        Implementations of this method should contain the logic for the script.
        """
        pass

    def _before_setup(self) -> None:
        """
        Optional method to override.  Runs before the setup logic of the run method.
        """
        pass

    def _before_teardown(self) -> None:
        """
        Optional method to override.  Runs after the teardown logic of the run method.
        """
        pass

    def _setup(self) -> None:
        """
        This is called before the run method to create driver object.
        """
        self._driver = SapioSeleniumDriver(self._browser_type, self._sapio_url, self._headless,
                                           self.file_man, self._browser_binary_location)
        if not self._headless:
            self._driver.selenium_driver.maximize_window()
        else:
            # headless runs in 4K?
            self._driver.selenium_driver.set_window_size(4096, 2160)
        self._do = Do(self._driver, 30, self._username, self._password, self._lab_name)

    # noinspection PyBroadException
    def _teardown(self):
        try:
            self._driver.selenium_driver.quit()
            self._file_man.on_stop()
        except Exception as e:
            pass


class SapioSeleniumMultiProcessResult:
    """
    The result of multi processing for a single process.
    """
    exit_code: int
    start_time: datetime.datetime
    end_time: datetime.datetime
    difference: datetime.timedelta

    def __init__(self, exit_code: int, start_time: datetime.datetime, end_time: datetime.datetime):
        self.exit_code = exit_code
        self.start_time = start_time
        self.end_time = end_time
        self.difference = end_time - start_time


class SeleniumScriptMultiProcessor:
    """
    Handles running multiple scripts concurrently.
    """
    _scripts: list[VeloxSeleniumScript]
    _processes: list[Process]
    _stagger_seconds: int

    def __init__(self, scripts: list[VeloxSeleniumScript], stagger_seconds: int = 20):
        """
        Create a new multiprocessor that handles running multiple scripts concurrently
        :param scripts: The script list to run concurrently.
        :param stagger_seconds: number of seconds to wait before launching another thread.
        """
        self._scripts = scripts
        # validates the paths in scripts are not identical
        paths: Set[str] = set()
        for script in scripts:
            path = script.file_man.storage_location_path
            if path in paths:
                raise ValueError("There are scripts that shares the same storage location path: " + path)
            paths.add(path)
        self._processes = []
        self._stagger_seconds = stagger_seconds

    def start(self) -> list[SapioSeleniumMultiProcessResult]:
        """
        Start all processes
        :return: a list of all time elapsed.
        """
        start_times: datetime = []
        num_total_processes: int = 0
        num_stopped_processes: int = 0
        num_error_processes: int = 0
        ret: list[SapioSeleniumMultiProcessResult] = []
        for script in self._scripts:
            process = multiprocessing.Process(target=script.run)
            self._processes.append(process)
            process.start()
            start_times.append(datetime.datetime.now())
            num_total_processes += 1
            logging.info("!!! STARTED " + script.__class__.__name__ + ". Total Processes: " + str(num_total_processes))
            time.sleep(self._stagger_seconds)

        for process, start_time in zip(self._processes, start_times):
            process.join()
            end_time = datetime.datetime.now()
            difference = end_time - start_time
            ret.append(SapioSeleniumMultiProcessResult(process.exitcode, start_time, end_time))
            minutes = divmod(difference.total_seconds(), 60)
            print("!!! Process elapsed " + str(minutes[0]) + " minutes and " + str(minutes[1]) + " seconds.")

            num_stopped_processes += 1
            logging.info("!!! " + str(num_stopped_processes) + "/" + str(num_total_processes) + " has completed.")
            if process.exitcode != 0:
                logging.error("!!! Process exited with abnormal status code " + str(process.exitcode))
        logging.info("!!! All Processes Finished. Number of processes with abnormal exit code: " +
                     str(num_error_processes) + "/" + str(num_total_processes))
        return ret


def _slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    import unicodedata
    import re
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
