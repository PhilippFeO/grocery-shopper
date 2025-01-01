import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

from grocery_shopper.vars import ARCHIVE_DIR

if TYPE_CHECKING:
    from grocery_shopper.recipe import Recipe


class YamlPdf(NamedTuple):
    yaml_path: Path
    pdf_path: Path


def create_archive_dir(
    recipes: list['Recipe'],
    archive_location: str,
) -> Path:
    """Create the a directory 'yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/'.

    Helper function.

    :recipe_paths: Iterable with the paths to the yaml files of the recipes.
    :archive_location: Directory, where recipes/, misc/ and .resources/ are
    :returns: The directory name as `str`.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Create subdirectory with the specified scheme
    recipe_names = [recipe.name_with_underscore for recipe in recipes]
    archived_shopping_list_name = f'{"-".join((current_date, *recipe_names))}'
    archive_dir_path = Path(
        archive_location,
        ARCHIVE_DIR,
        archived_shopping_list_name,
    )
    archive_dir_path.mkdir(parents=True)

    return archive_dir_path


def copy_shopping_list(
    shopping_list_file: Path,
    archive_dir_path: Path,
) -> Path:
    """Copy shopping list into archive directory."""
    shopping_list_dst = Path(archive_dir_path, f'{archive_dir_path.name}.txt')
    shutil.copy(shopping_list_file, shopping_list_dst)
    msg = (
        f"File '{shopping_list_file}' copied to '{shopping_list_dst}' successfully.",
    )
    logging.info(msg)

    return shopping_list_dst


def create_convenience_symlink(archive_dir_path: Path):
    """Create a symlink 'Selection' in `recipe_dir` for convenience, ie. having direct access to the selected recipes and shopping list."""
    link_name = 'Selection'
    link = Path(f'{link_name}')
    temp_link = Path(f'{link_name}.new')
    try:
        link.unlink()
    except FileNotFoundError as fnfe:
        msg = f'Error while removing link "{link}":\n\t{fnfe}'
        logging.exception(msg)
    # TODO(Philipp): Maybe doesn't work <01-01-2025>
    os.symlink(f'{archive_dir_path}', temp_link)
    temp_link.rename(link_name)


def archive_contents(
    shopping_list_file: Path,
    general_dir: str,
    recipes: list['Recipe'],
) -> list[YamlPdf]:
    """Save shopping list to yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/yyyy-mm-dd-recipes[0]-...-recipes[n].txt.

    Create sym links of the used recipes next to it to have all resources close at hand.

    :param shopping_list_file: Name of the shopping list file.
    :param archive_location: Location where the archive directory, ie. yyyy/, is created.
    :param recipe_paths: Paths to the recipes which will be archived.
    :returns: List of the created symlinks.

    Reminder: `general_dir` parameter because importing from main doesn't work due to circular import.
    """
    # TODO: I dont like how the whole paths are assembled <06-04-2024>
    #   fi: Path(recipe_path).name
    #       Second symlink (symlink to the pdf)
    archive_dir_path: Path = create_archive_dir(
        recipes=recipes,
        archive_location=general_dir,
    )
    copy_shopping_list(shopping_list_file, archive_dir_path)
    create_convenience_symlink(archive_dir_path)

    symlinked_files: list[YamlPdf] = []
    for recipe in recipes:
        dst_yaml = Path(archive_dir_path, recipe.name_with_underscore)
        dst_pdf = Path(
            archive_dir_path,
            (recipe_file_pdf := str(recipe.path).replace('yaml', 'pdf')),
        )
        try:
            os.symlink(recipe.path, dst_yaml)
            os.symlink(
                Path(recipe.path.parent, 'pdf', recipe_file_pdf),
                dst_pdf,
            )
            symlinked_files.append(
                YamlPdf(dst_yaml, dst_pdf),
            )
        except FileExistsError as fee:
            msg = f'Error Message: {fee}'
            logging.exception(msg)

    return symlinked_files
