#!/bin/env python3
import pathlib
from collections import namedtuple

from packages import packagelist, thirdparty_packages_dict

package_array = packagelist()
thirdparty_package_array = []

Package = namedtuple("Git_package", ["name", "source_dict"])

thirdparty_pkgs_array = [
    Package(name=pkg["name"], source_dict=pkg["source_dict"])
    for pkg in thirdparty_packages_dict()["packages"]
]

for pkg in thirdparty_pkgs_array:
    name = pkg.name
    url = pkg.source_dict["clone_url"]
    print(name)
    print(url)
    if name and url:
        thirdparty_package_array.append((name, url))

readme_content = """# Autocopr-new

## Description

This COPR repo is for personal and work use. Please go ahead and use this copr repo, be aware that the repo might be abandoned at any point. Feel free to create a GitHub issue if there is any issue with the packages.

## List of packages from the repository root

### Status badges on COPR builds
"""

for name, url, version in package_array:
    readme_content += f"""
### [{name}]({name}.spec) v{version}

[Upstream]({url})

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)
"""

readme_content += """
## Following packages are from thirdparty sources

> [!WARNING]
> The list below contains packages from thirdparty sources.
"""

for name, url in thirdparty_package_array:
    readme_content += f"""
### {name}

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)

[Upstream]({url})
"""

readme_path = pathlib.Path("README.md")
with readme_path.open("w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

print("README.md file created successfully!")
