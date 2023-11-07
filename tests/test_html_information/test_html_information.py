import os

import pytest
import textwrap


@pytest.fixture()
def sample_test(testdir):
    testdir.makefile(
        ".feature",
        scenario=textwrap.dedent(
            """\
            Feature: Testing
                Scenario: Test scenario
                    Given I have a scenario
                    When I start the test
                    And I know it will fails
                    Then It fails
            """
        ),
    )

    testdir.makepyfile(
        textwrap.dedent(
            """\
        import pytest
        from pytest_bdd import given, when, then, scenario

        @scenario("scenario.feature", "Test scenario")
        def test_scenario():
            pass

        @given("I have a scenario")
        def _():
            pass

        @when("I start the test")
        def _():
            pass

        @when("I know it will fails")
        def _():
            pass

        @then('It fails')
        def _():
            assert False

        """
        )
    )

    return testdir


def test_arguments_in_help(testdir):
    res = testdir.runpytest("--help")
    res.stdout.fnmatch_lines(
        [
            "*bdd-report*",
        ]
    )


def test_create_html_report_file(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    assert (sample_test.tmpdir / "report.html").exists()


def test_create_html_report_file_with_directory(sample_test):
    sample_test.runpytest("--bdd-report=./reports/report.html")
    assert (sample_test.tmpdir / "./reports/report.html").exists()


def test_create_html_report_file_with_directory_name(sample_test):
    sample_test.runpytest("--bdd-report=results/report.html")
    assert (sample_test.tmpdir / "results/report.html").exists()


def test_create_html_report_file_with_directory_and_subdirectory(sample_test):
    sample_test.runpytest("--bdd-report=./reports/year/report.html")
    assert (sample_test.tmpdir / "./reports/year/report.html").exists()


def test_content_in_report(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    content = ""
    with open((sample_test.tmpdir / "report.html"), "r") as f:
        content = f.read()
    assert content != ""


def test_information_in_report(sample_test):
    sample_test.runpytest("--bdd-report=report.html")
    content = ""
    with open((sample_test.tmpdir / "report.html"), "r") as f:
        content = f.read()
    assert "Testing" in content
    assert "Test scenario" in content
    assert "I have a scenario" in content
    assert "I start the test" in content
    assert "I know it will fails" in content
    assert " It fails" in content
