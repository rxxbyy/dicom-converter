# dicom2png
Convert DICOM format images to PNG using in Python in parallel using Message
Parsing Interface.

## Usage
```
$ mpiexec -np <number of processors> python3 dicom2png.py <dicom paths file> <output directory>
```
where `dicom paths file` contains paths to DICOM images, they can be generated
using the script `locate-dicom.sh

You can run
```
$ python3 dicom2png.py --help
```
to see all the options, and arguments that the script accepts.

The script `locate-dicom.sh` in `./scripts` will try to find all the DICOM images stored on a
directory and write its path to an output file.
```
$ ./scripts/locate-dicom.sh [-o output-path] <DICOM images directory>
```

### Example
Suppose we have the following DICOM images on a folder
```
$ ls example-dcm
case1_008.dcm  case1_016.dcm  case1_024.dcm  case1_032.dcm  case1_040.dcm  case1_048.dcm  case1_056.dcm  case1_064.dcm
case1_010.dcm  case1_018.dcm  case1_026.dcm  case1_034.dcm  case1_042.dcm  case1_050.dcm  case1_058.dcm  case1_066.dcm
case1_012.dcm  case1_020.dcm  case1_028.dcm  case1_036.dcm  case1_044.dcm  case1_052.dcm  case1_060.dcm  case1_068.dcm
case1_014.dcm  case1_022.dcm  case1_030.dcm  case1_038.dcm  case1_046.dcm  case1_054.dcm  case1_062.dcm
```
we can now run
```
$ ./scripts/locate-dicom.sh -o ./dcmpaths.dat ../example-dcm/
Successfully written 32 DICOM image paths to "./dcmpaths.dat"
```
Where, its contents look like
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
Now, you can run the program `dicom2png.py` as follows
```
mpiexec -np 2 python3 src/dicom2png.py -v -b 16 dcmpaths.dat out
[process 0] Saved image "case1_060.png" on "./out/example-dcm/case1_060.png".
[process 1] Saved image "case1_028.png" on "./out/example-dcm/case1_028.png".
[process 0] Saved image "case1_054.png" on "./out/example-dcm/case1_054.png".
[process 1] Saved image "case1_008.png" on "./out/example-dcm/case1_008.png".
[process 0] Saved image "case1_024.png" on "./out/example-dcm/case1_024.png".
[process 1] Saved image "case1_068.png" on "./out/example-dcm/case1_068.png".
[process 1] Saved image "case1_018.png" on "./out/example-dcm/case1_018.png".
[process 0] Saved image "case1_010.png" on "./out/example-dcm/case1_010.png".
[process 1] Saved image "case1_042.png" on "./out/example-dcm/case1_042.png".
[process 0] Saved image "case1_032.png" on "./out/example-dcm/case1_032.png".
[process 1] Saved image "case1_036.png" on "./out/example-dcm/case1_036.png".
[process 0] Saved image "case1_022.png" on "./out/example-dcm/case1_022.png".
...
[process 0] Saved image "case1_044.png" on "./out/example-dcm/case1_044.png".
[process 1] Saved image "case1_016.png" on "./out/example-dcm/case1_016.png".
[process 0] Saved image "case1_026.png" on "./out/example-dcm/case1_026.png".
[process 0] Saved image "case1_066.png" on "./out/example-dcm/case1_066.png".
```
It uses two processors (obviously you can try with the maximum of your system)
with verbose mode enabled and converting every DICOM image to 16-bit depth PNG images.

## Install dependencies
You can use PIP to install all the dependencies running
```
$ pip install -r requirements.txt
```
