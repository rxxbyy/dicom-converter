# dicom2png
Convert DICOM format images to PNG using in Python in parallel using Message
Parsing Interface.

## Usage
```
$ mpiexec -np <number_processors> python3 dicom2PngNpy.py {input_directory} {output_directory} <bit_depth 8 or 16>
```

### Input Folder Structure
The input folder can contain subfolders, and the script will recursively process all files within the folder and its subfolders. 
The script will maintain the original folder hierarchy, so that the output files are organized in the same way as the input files.

```
input_folder/
  subfolder1/
    file1.dcm
    file2.dcm
  subfolder2/
    file3.dcm
    file4.dcm
  file5.dcm
  file6.dcm

```
### Output Folder Structure
After running the script, the output folder will have the same structure as the input folder, with the converted files in the corresponding new formats:
```
output_folder/
  subfolder1/
    file1.png
    file1.npy
    file2.png
    file2.npy
  subfolder2/
    file3.png
    file3.npy
    file4.png
    file4.npy
  file5.png
  file5.npy
  file6.png
  file6.npy

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

Now, to convert all of that DICOM images to PNG, run:
```
$ mpiexec -np 8 python3 dicom2PngNpy.py data dataconverted 8
```

```
Process 5: 439 files processed
Process 7: 481 files processed
Process 0: 533 files processed
Process 3: 425 files processed
Process 6: 495 files processed
Process 4: 439 files processed
Process 7: 482 files processed
Process 0: 534 files processed
Process 3: 426 files processed
Process 4: 440 files processed
Process 7: 483 files processed
Process 0: 535 files processed
Process 3: 427 files processed
Process 6: 496 files processed
Process 3: 428 files processed
Process 5: 440 files processed
Process 3: 429 files processed
Process 4: 441 files processed
Process 0: 536 files processed
Process 7: 484 files processed ....

```
The above command uses `mpiexec` to run `dicom2PngNpy.py` using two processors. The
option ` 16 or 8 ` mean that the program will generate 16-bit depth or 8-bit depth PNG images

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
