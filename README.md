# dicom2png
Convert DICOM format images to PNG using in Python in parallel using Message
Parsing Interface.

## Usage
```
$ mpiexec -np <number of processors> python3 src/dicom2png.py <dicom paths file> <output directory>
```
where `dicom paths file` contains paths to DICOM images, they can be generated
using the script `scripts/locate-dicom.sh`

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
```
Now, to convert all of that DICOM images to PNG, run

```
$ mpiexec -np 2 python3 src/dicom2png.py -v -b -f ./dcmpaths.dat ./out
```

```
$ mpiexec -np 11 python dicom2png.py -b 8 -v -f PNG dcmpaths.dat Breast
[process 1] Saved image "case1_028.png" on "./.out/example-dcm/case1_028.png".
[process 0] Saved image "case1_060.png" on "./.out/example-dcm/case1_060.png".
[process 1] Saved image "case1_008.png" on "./.out/example-dcm/case1_008.png".
[process 0] Saved image "case1_054.png" on "./.out/example-dcm/case1_054.png".
[process 1] Saved image "case1_068.png" on "./.out/example-dcm/case1_068.png".
[process 1] Saved image "case1_018.png" on "./.out/example-dcm/case1_018.png".
[process 1] Saved image "case1_042.png" on "./.out/example-dcm/case1_042.png".
[process 0] Saved image "case1_024.png" on "./.out/example-dcm/case1_024.png".
[process 1] Saved image "case1_036.png" on "./.out/example-dcm/case1_036.png".
[process 0] Saved image "case1_010.png" on "./.out/example-dcm/case1_010.png".
[process 1] Saved image "case1_058.png" on "./.out/example-dcm/case1_058.png".
[process 1] Saved image "case1_040.png" on "./.out/example-dcm/case1_040.png".
[process 0] Saved image "case1_032.png" on "./.out/example-dcm/case1_032.png".
[process 0] Saved image "case1_022.png" on "./.out/example-dcm/case1_022.png".
[process 1] Saved image "case1_030.png" on "./.out/example-dcm/case1_030.png".
[process 0] Saved image "case1_056.png" on "./.out/example-dcm/case1_056.png".
[process 0] Saved image "case1_050.png" on "./.out/example-dcm/case1_050.png".
[process 0] Saved image "case1_064.png" on "./.out/example-dcm/case1_064.png".
[process 1] Saved image "case1_020.png" on "./.out/example-dcm/case1_020.png".
[process 0] Saved image "case1_052.png" on "./.out/example-dcm/case1_052.png".
[process 0] Saved image "case1_046.png" on "./.out/example-dcm/case1_046.png".
[process 0] Saved image "case1_038.png" on "./.out/example-dcm/case1_038.png".
[process 1] Saved image "case1_062.png" on "./.out/example-dcm/case1_062.png".
[process 0] Saved image "case1_034.png" on "./.out/example-dcm/case1_034.png".
[process 0] Saved image "case1_044.png" on "./.out/example-dcm/case1_044.png".
[process 0] Saved image "case1_026.png" on "./.out/example-dcm/case1_026.png".
[process 0] Saved image "case1_066.png" on "./.out/example-dcm/case1_066.png".
[process 1] Saved image "case1_014.png" on "./.out/example-dcm/case1_014.png".
[process 1] Saved image "case1_048.png" on "./.out/example-dcm/case1_048.png".
[process 1] Saved image "case1_012.png" on "./.out/example-dcm/case1_012.png".
[process 1] Saved image "case1_016.png" on "./.out/example-dcm/case1_016.png".
```
The above command uses `mpiexec` to run `dicom2png` using two processors. The
option `-v` enables verbose mode, and `-b 16` mean that the program will generate
16-bit depth PNG images

## Install dependencies
Create a virtual environment using virtualenv
```
$ virtualenv venv
```
then install all the dependencies running
```
$ pip install -r requirements.txt
```
---
Now, if you're in Ubuntu 24.x and the above process doesn't work, try
using APT.
```
$ sudo apt install python3-pydicom python3-opencv python3-mpi4py
```
