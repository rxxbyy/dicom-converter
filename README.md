# dicom2png
Convert DICOM format images to PNG using in Python in parallel using Message
Parsing Interface.

# Usage
```
$ mpiexec -np <number of processors> python3 dicom2png.py <dicom paths file> <output directory>
```
where `dicom paths file` contains paths to DICOM images, they can be generated
using the script `locate-dicom.sh

# Install dependencies
You can use PIP to install all the dependencies running
```
$ pip install -r requirements.txt
```
