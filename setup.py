import os
import sys

from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = 'C:\\Users\\works\\Anaconda3\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\Users\\works\\Anaconda3\\tcl\\tk8.6'
packages = ["xlrd"]
build_exe_options = {"packages": packages}

base = None
if sys.platform == "win32":
        base = "Win32GUI"

directory_table = [
(
    "ProgramMenuFolder",
    "TARGETDIR",
    ".",
),
(
    "SampleFileGenerator",
    "ProgramMenuFolder",
    "Generator",
),
                ]

msi_data = {
    "Directory": directory_table,
}

setup(
    name = "sample_file_generator",
    version = "1.0.0",
    description = "My Calculator",
    options = {"build_exe": build_exe_options,
               'bdist_msi': { 'data': msi_data } },
    executables = [
        Executable(
            "sample_file_generator.py",
            base=base,
            shortcutName="Generator",
            shortcutDir="SampleFileGenerator",
            )
        ])
