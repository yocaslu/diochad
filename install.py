from sys import exit
from pathlib import Path
from os import symlink
from shutil import rmtree
from sys import stdout

from rich import print
from rich.prompt import Confirm
from rich.traceback import install; install(show_locals=True)

from loguru import logger
logger.remove()
logger.add(stdout)

CACHE_PATHS = [".local/state/nvim/", ".local/share/nvim/", ".config/nvim/"]

try:
    HOME_PATH = Path().home()
except RuntimeError as e:
    logger.error(f'failed to get HOME environment variable due to: {e}')
    exit(1)

def remove_cache(cache_paths: list[str]) -> list[str]:
    removed_paths = []
    paths = [HOME_PATH.joinpath(x) for x in cache_paths]
    for cache_dir in paths:
        if not cache_dir.exists():
            logger.info(f'{cache_dir.absolute()} does not exist. passing...')
            continue

        if Confirm.ask(f'delete {cache_dir.absolute()}', default=False):
            try:
                if cache_dir.is_symlink() or cache_dir.is_file():
                    cache_dir.unlink()
                else: # is dir
                    rmtree(cache_dir.absolute())
                removed_paths.append(str(cache_dir.absolute()))

            except Exception as e:
                logger.error(f"failed to remove {cache_dir.absolute()} due to: {e}")
        else:
            print('installation aborted. exiting...')
            exit(0)
    return removed_paths

def main():
    config_path = HOME_PATH / '.config/nvim'
    nvim_path = Path().joinpath('nvim')
    logger.info(f'removed directories: {remove_cache(CACHE_PATHS)}')

    if not nvim_path.exists():
        logger.critical(f'could not find nvim folder in {nvim_path.absolute()}')
        exit(1)
    
    try:
        symlink(nvim_path.absolute(), config_path.absolute())
        logger.info(f'linked {nvim_path.absolute()} to {config_path.absolute()}.')

    except Exception as e:
        logger.critical(f'failed to link {nvim_path.absolute()} to {config_path.absolute()} due to: {e}')

if __name__ == "__main__":
    main()
