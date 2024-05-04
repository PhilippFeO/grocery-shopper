import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING
from grocery_shopper.vars import directories

if TYPE_CHECKING:
    from collections.abc import Iterable


def create_archive_dir(recipe_paths: 'Iterable[str]',
                       archive_location: str):
    """
    Helper function which creates the a directory 'yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/'.

    :recipe_paths: Iterable with the paths to the yaml files of the recipes.
    :archive_location: Directory, where recipes/, misc/ and .resources/ are
    :returns: The directory name as `str`.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Create subdirectory with the specified scheme
    recipe_names = [Path(recipe).stem for recipe in recipe_paths]
    archived_shopping_list_name = f'{"-".join((current_date, *recipe_names))}'
    archive_dir_path = os.path.join(archive_location,
                                    directories['archive_dir'],
                                    archived_shopping_list_name)
    os.makedirs(archive_dir_path, exist_ok=True)

    return archive_dir_path


def copy_shopping_list(shopping_list_file: str, archive_dir_path: str) -> str:
    """
    Copy shopping list into archive directory.
    """
    archive_dir_name = os.path.basename(archive_dir_path)
    shopping_list_dst = os.path.join(archive_dir_path, f'{archive_dir_name}.txt')
    shutil.copy(shopping_list_file, shopping_list_dst)
    logging.info(f"File '{shopping_list_file}' copied to '{shopping_list_dst}' successfully.")

    return shopping_list_dst


def create_convenience_symlink(archive_dir_path: str):
    """
    Creates a symlink 'Selection' in `recipe_dir` for convenience, ie. having direct access to the selected recipes and shopping list.
    """
    temp_link = (link_name := 'Selection') + ".new"
    try:
        os.remove(link_name)
    except FileNotFoundError as fnfe:
        logging.error(f'Error while removing link "{link_name}":\n\t{fnfe}')
    os.symlink(f'{archive_dir_path}', temp_link)
    os.rename(temp_link, link_name)


def archive_contents(shopping_list_file: str,
                     general_dir: str,
                     recipe_paths: 'Iterable[str]') -> list[str]:
    """
    Save shopping list to yyyy/yyyy-mm-dd-recipes[0]-...-recipes[n]/yyyy-mm-dd-recipes[0]-...-recipes[n].txt.
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
    archive_dir_path: str = create_archive_dir(recipe_paths=recipe_paths,
                                               archive_location=general_dir)
    copy_shopping_list(shopping_list_file,
                       archive_dir_path)
    create_convenience_symlink(archive_dir_path)

    # recipe_file scheme: file.ext
    symlinked_files: list[str] = []
    for recipe_file, recipe_path in zip((Path(recipe_path).name for recipe_path in recipe_paths),
                                        recipe_paths):
        dst_yaml = os.path.join(archive_dir_path,
                                recipe_file)
        dst_pdf = os.path.join(archive_dir_path,
                               (recipe_file_pdf := recipe_file.replace('yaml',
                                                                       'pdf')))
        try:
            os.symlink(recipe_path, dst_yaml)
            os.symlink(os.path.join(os.path.dirname(recipe_path),
                                    'pdf',
                                    recipe_file_pdf),
                       dst_pdf)
            symlinked_files.extend((dst_yaml, dst_pdf))
        except FileExistsError as fee:
            logging.error(f'Error Message: {fee}')

    return symlinked_files
