import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="FairFRU",
    version="0.2",
    author="Lisa Koutsoviti, Gonzalo Napoles",
    packages=["FairFRU"],
    description="A bias measure using the fuzzy rough set theory",
    long_description= long_description,
    long_description_content_type='text/markdown'
)