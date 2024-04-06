from grocery_shopper.archive_contents import archive_contents, create_archive_dir, copy_shopping_list
import os
from test_grocery_shopper import shopping_list_file


def test_create_archive_dir(tmp_path):
    recipe_paths: list[str] = [f"tests/{recipe_yaml}" for recipe_yaml in {"Testgericht_0.yaml", "Testgericht_1.yaml"}]
    archive_dir: str = create_archive_dir(recipe_paths, str(tmp_path))
    assert os.path.isdir(archive_dir)


def test_copy_shopping_list(tmp_path):
    recipe_paths: list[str] = [f"tests/{recipe_yaml}" for recipe_yaml in {"Testgericht_0.yaml", "Testgericht_1.yaml"}]
    archive_dir: str = create_archive_dir(recipe_paths, str(tmp_path))
    archived_shopping_list: str = copy_shopping_list(shopping_list_file,
                                                     archive_dir)
    assert os.path.isfile(archived_shopping_list)


def test_create_convenience_symlink():
    # Assert temp link was removed
    assert not os.path.islink('Selection.new')
    # Assert main link was created
    assert os.path.islink('Selection')


# @pytest.mark.skip(reason="Test needs PDF files of the recipes.")
def test_archive_contents(tmp_path):
    """
    Test function for archive_contents()
    """
    recipe_paths: list[str] = [
        f"/localhome/rost_ph/proj/grocery-shopper/tests/{recipe_yaml}" for recipe_yaml in ("Testgericht_0.yaml", "Testgericht_1.yaml")]
    symlinked_files = archive_contents(shopping_list_file, str(tmp_path), recipe_paths)

    # Check if symlinks were created
    assert all(os.path.islink(archived_file) for archived_file
               in symlinked_files)

    # Check if symlinks are valid, ie. if dst exists
    assert all(os.path.exists(os.readlink(archived_file)) for archived_file
               in symlinked_files)
