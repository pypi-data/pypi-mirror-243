import sys

from Cython.Build import cythonize
from setuptools import Extension, setup

if sys.platform.startswith("linux"):
    cflags = ["-std=c++14", "-O2", "-mcx16"]  # ["-march=x86-64-v2"]
elif sys.platform == "win32":
    cflags = ["/std:c++14", "/O2"]
elif sys.platform == "darwin":
    cflags = ["-std=c++14", "-O2"]
else:
    cflags = []


cy_extensions = [
    Extension(
        "atomicarray.int",
        ["atomicarray/int.pyx"],
        extra_compile_args=cflags,
        language="c++",
    ),
]

compiler_directives = {
    "binding": False,
    "boundscheck": False,
    "wraparound": False,
    "annotation_typing": True,
    "warn.undeclared": True,
    "warn.unused": True,
    "warn.unused_arg": True,
    "warn.unused_result": True,
}

with open("README.md", encoding="utf-8") as fr:
    long_description = fr.read()

setup(
    name="atomicarray",
    version="0.0.1",
    description="Arrays with atomic operations",
    author="Dobatymo",
    author_email="Dobatymo@users.noreply.github.com",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8",
    url="https://github.com/Dobatymo/atomicarray",
    python_requires=">=3.8",
    install_requires=[],
    packages=["atomicarray"],
    ext_modules=cythonize(cy_extensions, language_level=3, compiler_directives=compiler_directives),
    extras_require={
        "test": ["genutility[test]"],
    },
)
