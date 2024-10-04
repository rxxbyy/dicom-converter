# dicom-converter
Convert DICOM format images to PNG or NPY using in Python in parallel using Message
Parsing Interface.

## Usage
```
$ mpiexec -np <number of processors> python3 ./src/dc.py [-h] [-b BIT_DEPTH] [-v] [-f FORMATS] dcmpaths outdir

Convert DICOM format images to PNG or NPY format.

positional arguments:
  dcmpaths              Path to a file containing paths to DICOM images
  outdir                Output directory

options:
  -h, --help            show this help message and exit
  -b BIT_DEPTH, --bit-depth BIT_DEPTH
                        Bit-depth of resulting images
  -v, --verbose         Enable verbose mode
  -f FORMATS, --formats FORMATS
                        Conversion format
```

### Example
Suppose we have the following directory of DICOM images
```
$ ls example-dcm/
case1_008.dcm  case1_016.dcm  case1_024.dcm  case1_032.dcm  case1_040.dcm  case1_048.dcm  case1_056.dcm  case1_064.dcm
case1_010.dcm  case1_018.dcm  case1_026.dcm  case1_034.dcm  case1_042.dcm  case1_050.dcm  case1_058.dcm  case1_066.dcm
case1_012.dcm  case1_020.dcm  case1_028.dcm  case1_036.dcm  case1_044.dcm  case1_052.dcm  case1_060.dcm  case1_068.dcm
case1_014.dcm  case1_022.dcm  case1_030.dcm  case1_038.dcm  case1_046.dcm  case1_054.dcm  case1_062.dcm
```

We execute
```
$ ./scripts/locate-dicom.sh -o dcmpaths.dat ../example-dcm/
Successfully written 31 DICOM image paths to "dcmpaths.dat"
```
where the contents of `dcmpaths.dat` look like
```
$ head dcmpaths.dat
../example-dcm/case1_060.dcm
../example-dcm/case1_054.dcm
../example-dcm/case1_024.dcm
../example-dcm/case1_010.dcm
../example-dcm/case1_032.dcm
../example-dcm/case1_022.dcm
../example-dcm/case1_056.dcm
../example-dcm/case1_050.dcm
../example-dcm/case1_064.dcm
../example-dcm/case1_052.dcm
...
```
Now, to convert all of that DICOM images to PNG, run
```
$ mpiexec -np 2 python3 src/dc.py -v -b 8 -f PNG dcmpaths.dat example-png
```
where the output is
```
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_028.dcm" to "./example-png-png/example-dcm/case1_028.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_060.dcm" to "./example-png-png/example-dcm/case1_060.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_054.dcm" to "./example-png-png/example-dcm/case1_054.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_008.dcm" to "./example-png-png/example-dcm/case1_008.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_024.dcm" to "./example-png-png/example-dcm/case1_024.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_068.dcm" to "./example-png-png/example-dcm/case1_068.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_010.dcm" to "./example-png-png/example-dcm/case1_010.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_018.dcm" to "./example-png-png/example-dcm/case1_018.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_032.dcm" to "./example-png-png/example-dcm/case1_032.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_022.dcm" to "./example-png-png/example-dcm/case1_022.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_042.dcm" to "./example-png-png/example-dcm/case1_042.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_056.dcm" to "./example-png-png/example-dcm/case1_056.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_036.dcm" to "./example-png-png/example-dcm/case1_036.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_050.dcm" to "./example-png-png/example-dcm/case1_050.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_064.dcm" to "./example-png-png/example-dcm/case1_064.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_058.dcm" to "./example-png-png/example-dcm/case1_058.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_052.dcm" to "./example-png-png/example-dcm/case1_052.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_046.dcm" to "./example-png-png/example-dcm/case1_046.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_040.dcm" to "./example-png-png/example-dcm/case1_040.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_038.dcm" to "./example-png-png/example-dcm/case1_038.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_034.dcm" to "./example-png-png/example-dcm/case1_034.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_030.dcm" to "./example-png-png/example-dcm/case1_030.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_044.dcm" to "./example-png-png/example-dcm/case1_044.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_026.dcm" to "./example-png-png/example-dcm/case1_026.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_020.dcm" to "./example-png-png/example-dcm/case1_020.png".
[process 0] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_066.dcm" to "./example-png-png/example-dcm/case1_066.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_062.dcm" to "./example-png-png/example-dcm/case1_062.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_014.dcm" to "./example-png-png/example-dcm/case1_014.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_048.dcm" to "./example-png-png/example-dcm/case1_048.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_012.dcm" to "./example-png-png/example-dcm/case1_012.png".
[process 1] Successfully saved PNG format image from 
"/home/rxxbyy/programming/python/example-dcm/case1_016.dcm" to "./example-png-png/example-dcm/case1_016.png".
```
The above command uses `mpiexec` to run `dc` (dicom converter) using two processors. The
option `-v` enables verbose mode, `-f PNG` specifies to convert DICOM to the PNG format and
`-b 8` means that the program will generate 8-bit depth PNG format images.

## Install dependencies
Create a virtual environment using virtualenv
```
$ virtualenv venv
```
then install all the dependencies running
```
$ pip install -r requirements.txt
```
