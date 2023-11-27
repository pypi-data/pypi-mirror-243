<h1 align="center">
<img width="300" hspace="2" valign="bottom" src="1.png">
  </br>
   </br>
Never be afraid to bet on yourself
  </h1>

## Intro

This is a python binding around the C++ SDK using SWIG to produce the interface between C++ and Python


## Compile source code

### Debug build
Builds the interface and then compiles a shared object and installs

```
swig -python OxySDK.i
CFLAGS='-Wall -O0 -g' python3 setup.py build_ext --inplace
```

### Release build
Builds the interface wrapper, source code and then using twine uploads the sdist to pypi.org

```
swig -python OxySDK.i
python3 setup.py sdist
python3 -m twine upload dist/*
```


Linux:

```
sudo apt-get install python3-pip python3-pyaudio portaudio19-dev
pip3 install numpy
```

Mac:

```
brew install portaudio
```

Windows:

```
See win_x86 for build instruction
```

## SWIG

SWIG has some issues generating pointers and c strings don't exist in python. The following is a fix.

```

/* OxySDK interface */
%module OxySDK

%include "stdint.i"


%{
#define SWIG_FILE_WITH_INIT
#include <stdio.h>

#include "src/OxyCoreLib_api.h"
%}

%include "numpy.i"

%init %{
import_array();
%}


%numpy_typemaps(audioBuffer, NPY_CFLOAT, int)

%apply (audioBuffer* INPLACE_ARRAY1, int DIM1) {(audioBuffer* data, unsigned int size)};

%include "src/OxyCoreLib_api.h"

%inline %{
PyObject* OXY_PyDecodeAudioBuffer (PyObject* obj, int size, void *oxyingObject) {
  const int dtype_obj = PyArray_ObjectType(obj, NPY_FLOAT);
  // the NPY_ARRAY_IN_ARRAY requirement flag
  // ensures that the data is a contiguous block in memory.
  PyArrayObject* arr = (PyArrayObject*) PyArray_FROM_OTF(obj, dtype_obj, NPY_ARRAY_IN_ARRAY);
  float* float_ptr = (float*) PyArray_BYTES(arr);
  int32_t result = OXY_DecodeAudioBuffer(float_ptr, size, oxyingObject);
  PyObject* result_py = PyLong_FromLong(result);
  /* printf("result=%d\n", result); */
  /* Py_INCREF(Py_None);
  return Py_None; */
  return result_py;
}

PyObject* OXY_PyGetDecodedData (void *oxyingObject) {
  /* printf("OXY_PyGetDecodedData\n"); */
  char stringDecoded[30];
  int32_t result = OXY_GetDecodedData(stringDecoded, oxyingObject);
  /* printf("OXY_PyGetDecodedData: result=%d\n", result); */
  PyObject* result_py = PyLong_FromLong(result);
  PyObject* result_decoded = PyUnicode_FromString(stringDecoded);
  PyObject* result_tuple = PyTuple_New(2);
  PyTuple_SetItem(result_tuple, 0, result_py);
  PyTuple_SetItem(result_tuple, 1, result_decoded);
  return result_tuple;
}

%}
```

## Install package

Install the SDK directly from PyPi.

```
pip3 install OxySDK==1.0.7
```

# Pipelines

[![Windows / MacOS](https://github.com/OxySound/pythonSDK/actions/workflows/x86.yml/badge.svg)](https://github.com/OxySound/pythonSDK/actions/workflows/x86.yml)
[![pypi deployer](https://github.com/OxySound/pythonSDK/actions/workflows/arch64.yml/badge.svg)](https://github.com/OxySound/pythonSDK/actions/workflows/arch64.yml)
[![Linux](https://github.com/OxySound/pythonSDK/actions/workflows/i686.yml/badge.svg)](https://github.com/OxySound/pythonSDK/actions/workflows/i686.yml)
