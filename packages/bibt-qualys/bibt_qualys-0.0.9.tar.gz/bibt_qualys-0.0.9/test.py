import json
import logging
import os
import sys

from bibt.qualys import Client

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    # filename="out.log",
    format=(
        "[%(asctime)s] "
        # '%(name)s | ' # logger name
        "%(levelname)s "
        "<%(module)s:%(funcName)s:%(lineno)s>:  "
        "%(message)s"
    ),
    force=True,
)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("google").setLevel(logging.WARNING)


def test_client(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        assert c.session
        c.close()
        assert not c.session


def test_list_scan_schedules(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        scans = c.list_scan_schedules()
        assert len(scans) > 0


def test_list_scans(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        scans = c.list_scans()
        assert len(scans) > 0


def test_get_scan_result(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        scan = c.get_scan_result(os.environ["TEST_SCAN_TITLE"], output_format="json")
        with open("test_json.json", "w+") as outfile:
            json.dump(scan, outfile, indent=2)


def test_list_reports(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        reports = c.list_reports()
        with open("reports.list.json", "w+") as outfile:
            json.dump(reports, outfile, indent=2)
        assert len(reports) > 0


def test_get_report_result(capsys):
    with capsys.disabled():
        c = Client(
            os.environ["QUALYS_USER"],
            os.environ["QUALYS_PASS"],
            os.environ["QUALYS_URL"],
        )
        output_format, report = c.get_report_result(os.environ["TEST_REPORT_TITLE"])
        with open(f"report.fetch.{output_format.lower()}", "w+") as outfile:
            outfile.write(report)
