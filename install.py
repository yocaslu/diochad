from sys import exit, stdout
from pathlib import Path
from os import symlink
from shutil import rmtree

CACHE_PATHS = [".local/state/nvim/", ".local/share/nvim/", ".config/nvim/"]

try:
    HOME_PATH = Path().home()
except RuntimeError as e:
    print(f'failed to get HOME environment variable due to: {e}')
    exit(1)

def remove_cache(cache_paths: list[str]) -> list[str]:
    removed_paths = []
    paths = [HOME_PATH.joinpath(x) for x in cache_paths]
    for cache_dir in paths:
        if not cache_dir.exists():
            print(f'{cache_dir.absolute()} does not exist. passing...')
            continue 

        answer = input(f'delete {cache_dir.absolute()} (y/N)? ') 
        if answer.lower() == 'y':
            try:
                if cache_dir.is_symlink() or cache_dir.is_file():
                    cache_dir.unlink()
                else: # is dir
                    rmtree(cache_dir.absolute())
                removed_paths.append(str(cache_dir.absolute()))

            except Exception as e:
                print(f"failed to remove {cache_dir.absolute()} due to: {e}")
        else:
            print('installation aborted. exiting...')
            exit(0)
    return removed_paths

def main():
    config_path = HOME_PATH / '.config/nvim'
    nvim_path = Path().joinpath('nvim')
    print(f'removed directories: {remove_cache(CACHE_PATHS)}')

    if not nvim_path.exists():
        print(f'could not find nvim folder in {nvim_path.absolute()}')
        exit(1)
    
    try:
        symlink(nvim_path.absolute(), config_path.absolute())
    except Exception as e:
        print(f'failed to link {nvim_path.absolute()} to {config_path.absolute()} due to: {e}')

if __name__ == "__main__":
    main()