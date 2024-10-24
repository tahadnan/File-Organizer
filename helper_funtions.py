import os
import json
from typing import Dict, List, Set, Union
from constants import EXTENSION_MAP
from rich.console import Console,Theme
from rich.progress import Progress

message_theme = Theme({
    "other": "bright_cyan ",
    "info": "dim cyan italic",
    "success": "light_green bold",
    "error": "bold red"
})
console = Console(theme=message_theme)

def list_directory_files(directory_path: str = './') -> Union[List[str], str]:
    """List all files in the given directory."""
    if not (os.path.isdir(directory_path) and os.path.exists(directory_path)):
        return console.print(f"'{directory_path}' is invalid as a directory.", style="error")  
    return [
        file for file in os.listdir(directory_path)
        if os.path.isfile(os.path.join(directory_path, file))
    ]


def get_extension(file: str) -> str:
    """Get the extension of a file."""
    if os.path.isfile(file):
        _, file_extension = os.path.splitext(file)
        return file_extension
    return console.print(f"Error: '{file}' is not a valid file.", style="error")


def create_necessary_dirs(directory: str = './', extension_map: Dict = EXTENSION_MAP) -> None:
    """Create necessary directories based on file extensions."""
    files = list_directory_files(directory)
    extensions = {get_extension(f) for f in files if not f.startswith('Error')}
    needed_dirs: Set[str] = set()
    
    for category, ext_set in extension_map.items():
        for ext in extensions:
            if ext in ext_set:
                needed_dirs.add(category)
    
    created_dirs = []
    for dir_name in needed_dirs:
        os.makedirs(dir_name, exist_ok=True)
        created_dirs.append(dir_name)
    console.print("Succesfully created the following directories:",style="success")
    for idx, dir_name in enumerate(created_dirs,1):
        console.print(f"{idx}-[other]'{os.path.join(directory,dir_name)}'[/other]")


def get_file_category(extension: str, extension_map: Dict = EXTENSION_MAP) -> str:
    """Get the category of a file based on its extension."""
    for category, ext_set in extension_map.items():
        if extension.lower() in ext_set:
            return category
    return console.print(f"Error: No category found for '{extension}' extension",style="error")


def mv_file(source_file: str, destination_directory: str, verbose: bool = True) -> str:
    """Move a file to the specified destination directory."""
    filename = os.path.basename(source_file)
    destination = os.path.join(destination_directory, filename)
    
    try:
        os.rename(source_file, destination)
        if verbose:
            return console.print(f"Success: [other]{source_file}[/other] moved to [other]'{destination_directory}'[/other]",style="success")
    except FileExistsError:
        return console.print(f"Error: '{filename}' already exists in [other]'{destination_directory}'[/other]",style="error")
    except PermissionError:
        return f"Error: Permission denied while moving '{filename}'"

def map_validator(data: Dict) -> tuple[bool, str]:
    """Validate the structure and content of a user-provided extension mapping."""
    if not isinstance(data, dict):
        return False, "Extension map must be a dictionnary."
    
    for category, extensions in data.items():
        if not isinstance(category, str):
            return False, f"Category '{category}' must be a string."
        if isinstance(extensions, list):
            extensions = set(extensions)
        if not isinstance(extensions, set):
            return False, f"Extentions for '{category}' must be a set or list."
        for ext in extensions:
            if not isinstance(ext, str):
                return False, f"Extension '{ext}' in '{category}' MUST be a sting."
            if not ext.startswith('.'):
                return False, f"Extension '{ext}' in '{category}' must start with '.'"
    return True, "Valid extension map."


def user_map_reader(json_file: str) -> Dict[str, Set[str]]:
    """Read user mapping from a JSON file."""
    try:
        with open(json_file, 'r') as file:
            um = json.load(file)
        processed_map = {}
        for category, extensions in um.items():
            if isinstance(extensions, list):
                processed_map[category] = set(extensions)
            else:
                processed_map[category] = extensions
        is_valid, returned_msg = map_validator(processed_map)
        if not is_valid:
            print(f"Warning: Invalid extension map in '{json_file}': {error_msg}\nUsing the default extension map.")
            return {}
        return processed_map
    except FileNotFoundError as e:
        print(f"Warning: '{json_file}' not found. Using default extensions.\n{e}")
        return {}
    except json.JSONDecodeError as je:
        print(f"Warning: '{json_file}' is not a valid JSON file.\n{je}\nUsing default extensions.")
        return {}


def user_map(user_mapping: str, overwrite: bool = False) -> Dict[str, Set[str]]:
    """Combine user mapping with default extension map."""
    user_map = user_map_reader(user_mapping)
    if overwrite:
        return user_map

    combined_map: Dict[str, Set[str]] = {}
    for category, ext_set in EXTENSION_MAP.items():
        combined_map[category] = ext_set
        if category in user_map:
            combined_map[category].update(user_map[category])
    
    for category, ext_set in user_map.items():
        if category not in EXTENSION_MAP:
            combined_map[category] = ext_set
    
    return combined_map


def organize(directory: str, mapping_file: str = None, overwrite: bool = False, verbose: bool = True) -> None:
    extension_map = EXTENSION_MAP
    if mapping_file:
        extension_map = user_map(mapping_file, overwrite)
    
    if not os.path.exists(directory) or not os.path.isdir(directory):
        console.print(f"Error: [underline]'{directory}'[/underline] is not a valid directory",style="error")
        return 
    os.chdir(directory)
    create_necessary_dirs(directory, extension_map)
    
    if verbose:
        console.rule("[bold red]Processing and organizing files")

    files = list_directory_files(directory_path=directory)
    if isinstance(files, str):
        print(files)
        return 

    if verbose:
        for file in files:
            ext = get_extension(file)
            if ext.startswith('Error'):
                console.print(f"Skipping {file}: {ext}",style="error")
                continue

            category = get_file_category(ext, extension_map)
            if not category.startswith('Error'):
                mv_file(file, category)
            else:
                print(f"Skipping {file}: {category}")
    
    else:
        with Progress() as progress:
            task = progress.add_task("[cyan]Organizing files...", total=len(files))
            
            for file in files:
                ext = get_extension(file)
                if ext.startswith('Error'):
                    continue
                category = get_file_category(ext, extension_map)
                if not category.startswith('Error'):
                    mv_file(file, category, verbose=False)

                progress.update(task, advance=1)