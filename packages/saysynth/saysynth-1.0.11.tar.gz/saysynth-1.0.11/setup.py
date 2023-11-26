from pathlib import Path

from setuptools import find_packages, setup

from saysynth.version import VERSION

config = {
    "name": "saysynth",
    "version": VERSION,
    "packages": find_packages(),
    "include_package_data": True,
    "package_data": {
        "": ["cli/commands/demos/.*.yml", "*.md"],
    },
    "install_requires": [
        "charset-normalizer",
        "click",
        "mido",
        "midi-utils",
        "pyyaml",
        "g2p_en",
        "nltk",
        "hashids",
    ],
    "author": "Brian Abelson",
    "author_email": "hey@gltd.email",
    "description": "Make music with Mac's say command",
    "long_description": (Path(__file__).parent / "README.md").read_text(),
    "long_description_content_type": 'text/markdown',
    "url": "http://saysynth.org",
    "entry_points": {
        "console_scripts": [
            "saysynth=saysynth.cli:main",
            "sy=saysynth.cli:main",
        ]
    },
}

setup(**config)
