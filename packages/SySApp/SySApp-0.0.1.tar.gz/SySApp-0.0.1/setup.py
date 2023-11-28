from setuptools import *
from Cython.Build import *

to_pyc_module = ["sysapp/adv_module.py", "sysapp/dll.py"]

setup(
    name="SySApp",
    version="0.0.1",
    description="SyS App official module in Python. (Working in progress...)",
    author="Runkang Chen",
    author_email="help.informatic365@gmail.com",
    packages=["sysapp"],
    zip_save=False,
    ext_modules=cythonize(to_pyc_module)
)