import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_articles():
    """
    Returns a list of all names of lacrosse articles.
    """
    _, filenames = default_storage.listdir("articles")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_article(title, content):
    """
    Saves an article, given its title and Markdown
    content. If an existing article with the same title already exists,
    it is replaced.
    """
    filename = f"articles/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_article(title):
    """
    Retrieves an article by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"articles/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search(query):
    """
    Returns a list of all names of articles containing the search query
    """
    _, filenames = default_storage.listdir("articles")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md") and query in filename.lower()))
