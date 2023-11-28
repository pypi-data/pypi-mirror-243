import os
from pathlib import Path

import pytest

import atomik
from atomik.errors import FileAlreadyExistsError

TPM_DIR = "./tests/TEST_DATA/.tmp"


def test__atomik_file_1(file_name: str, data: str) -> None:
    path = Path(file_name)
    with atomik.file(path, tmp_dir=TPM_DIR) as f:
        assert not path.exists()
        f.write(data)

    assert path.exists()
    with open(path) as f:
        assert f.read() == data


def test__atomik_folder(folder: str) -> None:
    file_1 = "data_1.csv"
    file_2 = "data_2.csv"
    with atomik.folder(Path(folder), tmp_dir=TPM_DIR) as path:
        path_1 = Path(path, file_1)
        with open(path_1, "w") as f:
            f.write("data_1")
        path_2 = Path(path, file_2)
        with open(path_2, "w") as f:
            f.write("data_2")

        assert not Path(folder, file_1).exists()
        assert not Path(folder, file_2).exists()

    assert Path(folder, file_1).exists()
    assert Path(folder, file_2).exists()

    with open(Path(folder, file_1)) as f:
        assert f.read() == "data_1"
    with open(Path(folder, file_2)) as f:
        assert f.read() == "data_2"

    assert not Path(path).exists()


def test_atomik_file_bytes(file_name: str, data: str) -> None:
    b_data = data.encode()
    path = Path(file_name)
    with atomik.file(path, mode=atomik.Mode.BYTES, tmp_dir=TPM_DIR) as f:
        assert not path.exists()
        f.write(b_data)

    assert path.exists()
    with open(path, "rb") as f:
        assert f.read() == b_data


def test__atomik_file__file_present__raise(file_name: str, data: str) -> None:
    path = Path(file_name)
    path.touch()
    with pytest.raises(FileAlreadyExistsError):
        with atomik.file(path, tmp_dir=TPM_DIR) as f:
            f.write(data)


def test__atomik_file__file_overwrite(file_name: str, data: str) -> None:
    path = Path(file_name)
    path.touch()
    with atomik.file(path, tmp_dir=TPM_DIR, overwrite=True) as f:
        f.write(data)
    with open(path) as f:
        assert f.read() == data


def test__atomik__folder_present__raise(folder: str, data: str) -> None:
    Path(folder).mkdir()

    with pytest.raises(FileAlreadyExistsError):
        with atomik.folder(folder, tmp_dir=TPM_DIR) as path:
            with open(Path(path, "test.txt"), "w") as f:
                f.write(data)

    assert os.listdir(folder) == []


def test__atomik__empty_folder_present__overwrite(folder: str, data: str) -> None:
    Path(folder).mkdir()
    file_1 = "test.txt"
    with atomik.folder(folder, tmp_dir=TPM_DIR, overwrite=True) as path:
        with open(Path(path, file_1), "w") as f:
            f.write(data)

    assert Path(folder).exists()
    with open(Path(folder, file_1)) as f:
        assert f.read() == data

    assert not Path(path).exists()


def test__atomik__folder_present__overwrite(folder: str, data: str) -> None:
    Path(folder).mkdir()
    file_1 = "test.txt"

    with open(Path(folder, file_1), "w") as f:
        f.write(data)

    with atomik.folder(folder, tmp_dir=TPM_DIR, overwrite=True) as path:
        with open(Path(path, file_1), "w") as f:
            f.write("another_data")

    assert Path(folder).exists()
    with open(Path(folder, file_1)) as f:
        assert f.read() == "another_data"

    assert not Path(path).exists()
