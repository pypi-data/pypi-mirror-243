from setuptools import setup, find_packages
from Cython.Build import cythonize

to_pyc_module = ["sysapp/adv_module.py", "sysapp/dll.py"]

setup(
    name="SySApp",
    version="0.0.4",
    description="SyS App official module in Python. (Work in progress...)",
    author="Runkang Chen",
    author_email="admin@sysapp.org",
    packages=find_packages(),
    zip_safe=False,
    ext_modules=cythonize(to_pyc_module),
    install_requires=[
        "Cython"
    ]
)