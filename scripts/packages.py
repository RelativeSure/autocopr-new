#!/bin/env python3
import pathlib
from collections import namedtuple


def packagelist():
    dir_path = pathlib.Path(".")
    files = dir_path.glob("*.spec")
    sorted_files = sorted(files, key=lambda x: x.name)

    name_url_pairs = []

    for file in sorted_files:
        print(file)
        name = None
        url = None
        version = None
        with file.open("r", encoding="utf-8") as spec_file:
            for line in spec_file:
                if line.startswith("Name:"):
                    name = line.split(":", 1)[1].strip()
                elif line.startswith("URL:"):
                    url = line.split(":", 1)[1].strip()
                elif line.startswith("Version:"):
                    version = line.split(":", 1)[1].strip()
                if name and url and version:
                    break
        if name and url and version:
            name_url_pairs.append((name, url, version))
            print(
                f"Processed: {file.name} -> Name: {name}, Version: {version}, URL: {url}"
            )
    return name_url_pairs


Git_package = namedtuple("Git_package", ["name", "source_dict"])


def source_dict(
    clone_url=None,
    committish=None,
    subdirectory=None,
    specfile=None,
    source_build_method="rpkg",
):
    return {
        "clone_url": clone_url,
        "committish": committish,
        "subdirectory": subdirectory,
        "spec": specfile,
        "scm_type": "git",
        "source_build_method": source_build_method,
    }


def create_git_package(
    name, clone_url, committish, specfile, subdirectory=None, source_build_method="rpkg"
):
    return Git_package(
        name,
        source_dict(
            clone_url=clone_url,
            committish=committish,
            specfile=specfile,
            subdirectory=subdirectory,
            source_build_method=source_build_method,
        ),
    )._asdict()


def thirdparty_packages_dict():
    package_definitions = [
        ("dua-cli", "https://src.fedoraproject.org/rpms/rust-dua-cli", None, "rust-dua-cli.spec"),
        ("feh", "https://src.fedoraproject.org/rpms/feh", None, "feh.spec"),
        ("python-neovim", "https://github.com/agriffis/pynvim", "copr", None, None),
        ("rust-tealdeer", "https://src.fedoraproject.org/rpms/rust-tealdeer", "f44", "rust-tealdeer.spec"),
        ("utf8proc", "https://github.com/agriffis/utf8proc", "copr", None, None),
        ("wezterm", "https://github.com/wez/wezterm.git", None, None, None, "make_srpm"),
    ]
    thirdparty_packages = {
        "packages": [create_git_package(*pkg) for pkg in package_definitions]
    }
    return thirdparty_packages
