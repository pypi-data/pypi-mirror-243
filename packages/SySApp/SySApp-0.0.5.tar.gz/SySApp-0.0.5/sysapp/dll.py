# -----------------------------------------------------------------------
# 
# © Copyright 2023 SyS App all rights reserved
# Powered By Runkang Chen
# email: help.informatic365@gmail.com
# Website: https://www.sysapp.org/
# 
# -----------------------------------------------------------------------

import os


class DLL:
    def create_file(filename_with_directory_path: str, write_mode: str, write_code):
        with open(filename_with_directory_path, write_mode)as create:
            create.write(write_code)

    def get_directory(file: any):
        try:
            result = os.path.dirname(os.path.realpath(file))
            return result
        except Exception as error:
            raise RuntimeError(error)