import datetime
import time
import shutil

from pathlib import Path
from dataclasses import dataclass

import bs4
import pytest

from requests import Session as RequestsSession

# duck-punch datetime.datetime.UTC support in versions older than Python 3.11
if __import__('sys').version_info[0:2] < (3, 11):
    datetime.UTC = datetime.timezone.utc

def pytest_addoption(parser):
    aoc = parser.getgroup('aoc')

    aoc.addoption('--aoc-year',         action='store', default=None,       help='year to download input files for')
    aoc.addoption('--aoc-input-dir',    action='store', default=None,       help='directory to store input files in')
    aoc.addoption('--aoc-session-id',   action='store', default=None,       help='session ID to use for retrieving input')
    aoc.addoption('--aoc-session-file', action='store', default=None,       help='file from which to read session ID')
    aoc.addoption('--aoc-sleep-time',   action='store', default=None,       help='time to sleep after downloading input')

    parser.addini('aoc_year', help='year to download input files for')
    parser.addini('aoc_input_dir', help='directory to store input files in')
    parser.addini('aoc_session_file', help='file from which to read session ID')
    parser.addini('aoc_sleep_time', help='time to sleep after downloading input')

def create_requests_session(session_id, session_file):
    session = RequestsSession()
    session.headers = {'User-Agent': 'https://pypi.org/project/pytest-aoc/ by jjm@j0057.nl'}
    if session_id:
        session.cookies.set('session', session_id, domain='adventofcode.com')
    elif session_file:
        with session_file.open('r') as f:
            session.cookies.set('session', f.read().strip(), domain='adventofcode.com')
    else:
        raise ValueError('neither session_id nor session_file are set')
    return session

def get_available_days(year, now):
    # don't worry, four unit tests prove that this works
    return [*range(1, min(25, (now - datetime.datetime(year, 11, 30, 5, 0, 0, 0, datetime.UTC)).days)+1)]

def reader_variants(name):
    yield f"{name}_raw", lambda f: f.read()
    yield f"{name}_text", lambda f: f.read().strip()
    yield f"{name}_lines", lambda f: [line.strip() for line in f]
    yield f"{name}_numbers", lambda f: [int(n) for n in f]
    yield f"{name}_number", lambda f: int(f.read())
    yield f"{name}_grid", lambda f: [row.split() for row in f]
    yield f"{name}_number_grid", lambda f: [[int(n) for n in row.split()] for row in f]

def create_fixtures(requests, year, day, input_file, sleep_time):
    def create_fixture(R):
        @pytest.fixture
        def fixture():
            if not input_file.exists():
                response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", stream=True)
                response.raise_for_status()
                time.sleep(sleep_time)
                with input_file.open('wb') as f:
                    shutil.copyfileobj(response.raw, f)
            with input_file.open('r') as f:
                return R(f)
        return fixture
    return {name: create_fixture(R) for (name, R) in reader_variants(f"day{day:02}")}

def create_examples(requests, year, day, input_path, sleep_time):
    def create_fixture(R):
        @pytest.fixture
        def fixture():
            def read(n):
                path = input_path / f"day{day:02}-ex{n}.txt"
                if not path.exists():
                    response = requests.get(f"https://adventofcode.com/2022/day/{day}", stream=True)
                    response.raise_for_status()
                    time.sleep(sleep_time)
                    soup = bs4.BeautifulSoup(response.raw, 'html5lib')
                    with path.open('w') as f:
                        example = soup.select('html body article pre>code')[n].text
                        f.write(example)
                with path.open('r') as f:
                    return R(f)
            return read
        return fixture
    return {name: create_fixture(R) for (name, R) in reader_variants(f"day{day:02}_ex")}

@dataclass
class Config:
    year: str
    input_path: Path
    session_id: str
    session_file: Path
    sleep_time: float

    @staticmethod
    def get_value(session, opt_name, ini_name, default=None):
        if opt_name and (result := session.config.getoption(opt_name)):
            return result
        if ini_name and (result := session.config.getini(ini_name)):
            return result
        return default

    @classmethod
    def load(cls, session):
        return cls(year=int(cls.get_value(session, 'aoc_year', 'aoc_year', 0)) or None,
                   input_path=Path(cls.get_value(session, 'aoc_input_dir', 'aoc_input_dir', 'input')),
                   session_id=cls.get_value(session, 'aoc_session_id', None),
                   session_file=Path(cls.get_value(session, 'aoc_session_file', 'aoc_session_file', '.cookie')),
                   sleep_time=float(cls.get_value(session, 'aoc_sleep_time', 'aoc_sleep_time', '2.5')))

    def __bool__(self):
        return self.year is not None

def pytest_sessionstart(session):
    if config := Config.load(session):
        requests = create_requests_session(config.session_id, config.session_file)
        config.input_path.mkdir(exist_ok=True)
        for day in get_available_days(config.year, datetime.datetime.now(datetime.UTC)):
            input_file = config.input_path / f"day{day:02}.txt"
            globals().update(create_fixtures(requests, config.year, day, input_file, config.sleep_time))
            globals().update(create_examples(requests, config.year, day, config.input_path, config.sleep_time))
