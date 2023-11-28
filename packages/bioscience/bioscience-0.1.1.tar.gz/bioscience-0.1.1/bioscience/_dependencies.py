import argparse
from collections import defaultdict

NUMPY_MIN_VERSION = "1.26.0"
PANDAS_MIN_VERSION = "2.1.1"
SCIKIT_MIN_VERSION = "1.3.1"
NUMBA_MIN_VERSION = "0.58.0"
PYTEST_MIN_VERSION = "7.1.2"

dependent_packages = {
    "numpy": (NUMPY_MIN_VERSION, "build, install"),
    "pandas": (PANDAS_MIN_VERSION, "build, install"),
    "scikit-learn": (SCIKIT_MIN_VERSION, "build, install"),
    "numba": (NUMBA_MIN_VERSION, "build, install"),
    "pytest": (PYTEST_MIN_VERSION, "tests"),
    "pytest-cov": ("2.9.0", "tests"),
}

tag_to_packages: dict = defaultdict(list)
for package, (min_version, extras) in dependent_packages.items():
    for extra in extras.split(", "):
        tag_to_packages[extra].append("{}>={}".format(package, min_version))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get min dependencies for a package")
    parser.add_argument("package", choices=dependent_packages)
    args = parser.parse_args()
    min_version = dependent_packages[args.package][0]
    print(min_version)