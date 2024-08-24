from pathlib import Path

defaults_file: str = 'defaults.ini'
directories: dict[str, str] = {
    'recipe_dir': 'recipes',
    'misc_dir': 'misc',
    'resource_dir': '.resources',
    'archive_dir': '.archive',
}
RECIPE_DIR = Path('./recipes')
MISC_DIR = Path('./misc')
RESOURCE_DIR = Path('./.resources')
ARCHIVE_DIR = Path('./.archive')
