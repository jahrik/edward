import runpy
import sys
from unittest.mock import patch


def test_main_execution():
    with patch.object(sys, "argv", ["edward", "--help"]):
        try:
            runpy.run_module("edward", run_name="__main__")
        except SystemExit as e:
            assert e.code == 0


def test_main_import():
    with patch("edward.cli.cli") as mock_cli:
        mock_cli.assert_not_called()
