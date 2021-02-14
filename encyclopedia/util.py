import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    returns false.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return False
    else:
        #default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return True


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return markdown2.markdown(f.read().decode("utf-8"))
    except FileNotFoundError:
        return None

def search_entries(query):
    """
    searching directly
    """
    filename = f"entries/{query}.md"
    short_filename = f"{query}.md"
    if default_storage.exists(filename):
        return (re.sub(r"\.md$", "", short_filename))

def search_sim_entries(query):
    """
    searching similar
    """
    
    names_list = list_entries()
    found_list = []

    for x in names_list:
        if query.lower() in x.lower():
            found_list.append(x)
            found_list.sort()

    return found_list

def edit_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    returns false.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return True
    else:
        return False


