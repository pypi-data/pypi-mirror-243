# Copyright (c) 2023 Benjamin Mummery

import os
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from src.phone_footage_sorter.entry import main


class TestNullCases:
    @staticmethod
    def test_no_files(tmp_path: Path, cwd, mocker: MockerFixture):
        # GIVEN
        mocker.patch("sys.argv", ["stub_name", "stub title"])

        # WHEN
        with cwd(tmp_path):
            main()


@pytest.mark.parametrize("custom_name", ["Training Videos", "FOO"])
class TestFlatDir:
    @staticmethod
    def test_renames_single_file_correctly(
        tmp_path: Path, cwd, mocker: MockerFixture, custom_name: str
    ):
        # GIVEN
        filename = "20220202_222222.mp4"
        (tmp_path / filename).write_text("<sentinel>")
        mocker.patch("sys.argv", ["stub_name", custom_name])

        # WHEN
        with cwd(tmp_path):
            main()

        # THEN
        with open(tmp_path / f"{custom_name} - 2022-02-02.mp4", "r") as f:
            assert f.read() == "<sentinel>"

    @staticmethod
    def test_renames_multiple_files_for_same_day(
        tmp_path: Path, cwd, mocker: MockerFixture, custom_name: str
    ):
        # GIVEN
        for i, file in enumerate(["20220202_222222.mp4", "20220202_222223.mp4"]):
            (tmp_path / file).write_text(f"<{i} sentinel>")
        mocker.patch("sys.argv", ["stub_name", custom_name])

        # WHEN
        with cwd(tmp_path):
            main()

        # THEN
        for i, file in enumerate(
            [
                f"{custom_name} - 2022-02-02 - Part1.mp4",
                f"{custom_name} - 2022-02-02 - Part2.mp4",
            ]
        ):
            with open(tmp_path / file, "r") as f:
                assert f.read() == f"<{i} sentinel>"

    @staticmethod
    def test_ignores_non_matching_files(
        tmp_path: Path, cwd, mocker: MockerFixture, custom_name: str
    ):
        # GIVEN
        for file in [
            "20220202_222222.mp4",
            "20220202_222223.mp4",
            "not_a_matching_file.mp4",
        ]:
            (tmp_path / file).write_text("")
        mocker.patch("sys.argv", ["stub_name", custom_name])

        # WHEN
        with cwd(tmp_path):
            main()

        # THEN
        assert set(os.listdir(tmp_path)) == {
            f"{custom_name} - 2022-02-02 - Part1.mp4",
            f"{custom_name} - 2022-02-02 - Part2.mp4",
            "not_a_matching_file.mp4",
        }

    @staticmethod
    def test_reports_renamed_files(
        tmp_path: Path, cwd, mocker: MockerFixture, custom_name: str, capsys
    ):
        # GIVEN
        files = [
            "20220202_222222.mp4",
            "20220202_222223.mp4",
        ]
        outfiles = [
            f"{custom_name} - 2022-02-02 - Part1.mp4",
            f"{custom_name} - 2022-02-02 - Part2.mp4",
        ]
        for file in files:
            (tmp_path / file).write_text("")
        mocker.patch("sys.argv", ["stub_name", custom_name])

        # WHEN
        with cwd(tmp_path):
            main()

        # THEN
        out = capsys.readouterr().out
        assert out.startswith("Renaming files:")
        for i, file in enumerate(files):
            assert f"{file} --> {outfiles[i]}" in out
