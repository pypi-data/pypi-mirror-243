import os.path
import sys

from setuptools import find_packages, setup


def recursive_files(directory):
    paths = []
    for (path, _, filenames) in os.walk(directory):
        for filename in filenames:
            if not filename.endswith(".pyc") and filename != "registered.json":
                paths.append(os.path.join('..', path, filename))
    return paths

if sys.version_info < (3, 8):
    raise RuntimeError("turcar requires Python 3.8 or later")

setupdir = os.path.dirname(__file__)

with open(os.path.join(setupdir, "turcar", "VERSION"), encoding="ASCII") as f:
    version = f.read().strip()

requirements = []
for line in open(os.path.join(setupdir, "requirements.txt"), encoding="ASCII"):
    if line.strip() and not line.startswith("#"):
        requirements.append(line)

setup(
    name="turcar",
    version=version,
    description="Python IDE for beginners",
    long_description="turcar is a simple Python IDE with features useful for learning programming. See https://turcar.org for more info.",
    url="https://turcar.org",
    author="Aivar Annamaa and others",
    author_email="turcar@googlegroups.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: Freeware",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Software Development",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Text Editors",
    ],
    keywords="IDE education debugger",
    project_urls={
        "Source code": "https://github.com/turcar/turcar",
        "Bug tracker": "https://github.com/turcar/turcar/issues",
    },
    platforms=["Windows", "macOS", "Linux"],
    install_requires=requirements,
    python_requires=">=3.8",
    packages=find_packages(),
    package_data={
        "": ["VERSION", "defaults.ini", "res/*", "dbus/*"]
            + recursive_files("turcar/locale")
            + recursive_files("turcar/vendored_libs"),
        "turcar.plugins.help": ["*.rst"],
        "turcar.plugins.pi": ["res/**"],
        "turcar.plugins.printing": ["*.html"],
        "turcar.plugins.micropython": ["*api_stubs/**"],
        "turcar.plugins.circuitpython": ["*api_stubs/**"],
        "turcar.plugins.microbit": ["*api_stubs/**"],
        "turcar.plugins.rp2040": ["*api_stubs/**"],
        "turcar.plugins.ev3": ["*api_stubs/**"],
        "turcar.plugins.prime_inventor": ["*api_stubs/**"],
        "turcar.plugins.esp": ["*api_stubs/**"],
        "turcar.plugins.mypy": ["typeshed_extras/*.pyi"],
    },
    entry_points={"gui_scripts": ["turcar = turcar:launch"]},
)
