# pytest -v --capture=no  tests/test_bump_version.py

import os
import pytest
from cloudmesh.bumpversion.bumpversion import BumpVersion

@pytest.fixture
def setup_bump_version():
    # Create an instance of BumpVersion for testing
    bump_version = BumpVersion(file_path="./test_version")

    # Create a test version file
    with open("./test_version", "w") as test_file:
        test_file.write("1.2.3")

    yield bump_version

    # Remove the test version file after the test
    os.remove("./test_version")

def test_read_version_from_file(setup_bump_version):
    bump_version = setup_bump_version
    bump_version.read_version_from_file(file_path="./test_version")
    assert bump_version.version == {'major': 1, 'minor': 2, 'patch': 3}

def test_verify_version_format_valid(setup_bump_version):
    bump_version = setup_bump_version
    result = bump_version.verify_version_format("1.2.3")
    assert result is True

def test_verify_version_format_invalid(setup_bump_version):
    bump_version = setup_bump_version
    result = bump_version.verify_version_format("invalid_version")
    assert result is False

def test_update_version(setup_bump_version):
    bump_version = setup_bump_version
    bump_version.update_version("2.0.0")
    with open("./test_version", "r") as test_file:
        content = test_file.read()
    assert "2.0.0" in content

def test_update_version_in_file(setup_bump_version):
    bump_version = setup_bump_version
    bump_version.update_version_in_file("./test_version", "3.0.0")
    with open("./test_version", "r") as test_file:
        content = test_file.read()
    assert "3.0.0" in content

def test_incr_major(setup_bump_version):
    bump_version = setup_bump_version
    new_version = bump_version.incr("major", file_path="./test_version")
    assert new_version == "2.0.0"

def test_incr_minor(setup_bump_version):
    bump_version = setup_bump_version
    new_version = bump_version.incr("minor", file_path="./test_version")
    assert new_version == "1.3.0"

def test_incr_patch(setup_bump_version):
    bump_version = setup_bump_version
    new_version = bump_version.incr("patch", file_path="./test_version")
    assert new_version == "1.2.4"
