import datetime

import pytest
import time_machine

import pytest_aoc

@time_machine.travel('2018-12-01 04:59:59.999 +0000')
def test_get_available_days_before():
    assert pytest_aoc.get_available_days(2018, datetime.datetime.now(datetime.UTC)) == []

@time_machine.travel('2018-12-01 05:00:00.000 +0000')
def test_get_available_days_unlock():
    assert pytest_aoc.get_available_days(2018, datetime.datetime.now(datetime.UTC)) == [1]

@time_machine.travel('2014-12-18 16:16 +0100')
def test_get_available_days_during():
    assert pytest_aoc.get_available_days(2014, datetime.datetime.now(datetime.UTC)) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

@time_machine.travel('2018-08-14 19:26 +0200')
def test_get_available_days_after():
    assert pytest_aoc.get_available_days(2017, datetime.datetime.now(datetime.UTC)) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

@time_machine.travel('2022-12-05 20:39 +0200')
def test_download_input(testdir, responses):
    responses.add(responses.GET, 'https://adventofcode.com/2022/day/5/input', body='albatross')
    testdir.makepyfile(test_download_inputs='''
        import pytest_aoc
        def test_download_inputs(day05_text):
            assert day05_text == 'albatross'
    ''')
    testdir.runpytest('--aoc-session-id=abc', '--aoc-year=2022', '--aoc-input-dir=.', '--aoc-sleep-time=0').assert_outcomes(passed=1)

@time_machine.travel('2022-12-05 20:39 +0100')
def test_download_example(testdir, responses):
    responses.add(responses.GET, 'https://adventofcode.com/2022/day/5', body='''<!DOCTYPE html>
    <html>
        <body>
            <article>
                <pre><code>albatross</code</pre>
            </article>
        </body>
    </html>''')
    testdir.makepyfile(test_download_inputs='''
        import pytest_aoc
        def test_download_example(day05_ex_text):
            assert day05_ex_text(0) == 'albatross'
    ''')
    testdir.runpytest('--aoc-session-id=abc', '--aoc-year=2022', '--aoc-input-dir=.', '--aoc-sleep-time=0').assert_outcomes(passed=1)

@pytest.mark.parametrize('name,text,value', [
    ('text', 'spam ', '"spam"'),
    ('raw', 'spam ', '"spam "'),
    ('lines', 'spam\neggs\n', '["spam", "eggs"]'),
    ('numbers', '529\n127\n', '[529, 127]'),
    ('number', '529', '529'),
    ('grid', 'a b\nc d\n', '[["a", "b"], ["c", "d"]]'),
    ('number_grid', '1 2\n3 4\n', '[[1, 2], [3, 4]]')
])
@time_machine.travel('2018-12-01 05:00:00 +0000')
def test_fixture(testdir, name, text, value):
    with open('day01.txt', 'w') as f:
        f.write(text)
    testdir.makepyfile(test_fixture=f'def test_{name}(day01_{name}): assert day01_{name} == {value}')
    testdir.runpytest('--aoc-session-id=abc', '--aoc-year=2018', '--aoc-input-dir=.').assert_outcomes(passed=1)
