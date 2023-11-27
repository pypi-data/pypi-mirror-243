#!/usr/bin/env python

"""
 Module
     setup.py
 Copyright
     Copyright (C) 2023
"""

#from distutils.core import setup, Extension

from setuptools import setup, Extension, find_packages
import numpy as np
import os
import platform
import sys

__version__ = '1.1.5.7'

# CFLAGS etc
extra_compile_args = []

# Get the target platform
LINUX= platform.system() == 'Linux'
WIN= platform.system() == 'Windows'

if LINUX:
    extra_compile_args.append("-DLINUX")
elif WIN:
    extra_compile_args.append("-DWIN")
    
# header includes in Manifest.in src/*.h
OxySDK_module = Extension('_OxySDK',
                           sources=['OxySDK_wrap.c', 'src/OxyCoreLib_api.cpp', 'src/Decoder.cpp', 'src/DecoderAllMultiToneMode.cpp', 'src/DecoderAudibleMode.cpp', 'src/DecoderAudibleMultiToneMode.cpp', 'src/DecoderCompressionMultiToneMode.cpp', 'src/DecoderCustomMultiToneMode.cpp', 'src/DecoderNonAudibleMode.cpp', 'src/DecoderNonAudibleMultiToneMode.cpp', 'src/Encoder.cpp', 'src/EncoderAudibleMode.cpp', 'src/EncoderAudibleMultiToneMode.cpp', 'src/EncoderCompressionMultiToneMode.cpp', 'src/EncoderCustomMultiToneMode.cpp', 'src/EncoderNonAudibleMode.cpp', 'src/EncoderNonAudibleMultiToneMode.cpp', 'src/Globals.cpp', 'src/ReedSolomon.cpp', 'src/SpectralAnalysis.cpp'],
                           include_dirs=[np.get_include()],
                           extra_compile_args = extra_compile_args,
                        )
# Required libs
# sudo apt-get install python3-pip && python3-pyaudio

# Meta data
setup (name = 'OxySDK',
       version=__version__,
       author      = "OxySound",
       author_email="""support@oxycom.co.uk""",
       description = """OxySDK Python SDK""",
       long_description="""The OxySound Python SDK enables the user to send and receive data using the device’s microphone and speaker.""",
       license='License :: Other/Proprietary License',
       ext_modules = [OxySDK_module],
       install_requires=[
       'pyaudio', 'numpy',
       ],
       py_modules = ["OxySDK"],
       packages=find_packages(),
       )
