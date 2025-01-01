from pathlib import Path

import pytest
from test_grocery_shopper import shopping_list_file

from grocery_shopper.archive_contents import (
    archive_contents,
    copy_shopping_list,
    create_archive_dir,
)


def test_create_archive_dir(tmp_path, recipes):
    archive_dir: Path = create_archive_dir(recipes, str(tmp_path))
    assert archive_dir.is_dir()


def test_copy_shopping_list(tmp_path, recipes):
    archive_dir: Path = create_archive_dir(recipes, str(tmp_path))
    archived_shopping_list: Path = copy_shopping_list(shopping_list_file, archive_dir)
    assert archived_shopping_list.is_file()


def test_create_convenience_symlink():
    # Assert temp link was removed
    assert not Path('Selection.new').is_symlink()
    # Assert main link was created
    assert Path('Selection').is_symlink()


@pytest.mark.skip(reason='Test needs PDF files of the recipes.')
def test_archive_contents(tmp_path, recipes):
    """Test function for `archive_contents()`."""
    symlinked_files = archive_contents(shopping_list_file, str(tmp_path), recipes)

    # Check if symlinks were created
    assert all(
        archived_file.yaml_path.is_symlink() for archived_file in symlinked_files
    )

    # Check if symlinks are valid, ie. if dst exists
    assert all(
        archived_file.yaml_path.readlink().exists() for archived_file in symlinked_files
    )
