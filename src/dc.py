# Copyright (c) 2024 Manuel Rubio

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from typing import List, Any
import pydicom
import pydicom.multival
from mpi4py import MPI
from pathlib import Path, PosixPath
import os, sys
import argparse
import numpy as np
#import cupy as cp
import cv2
from pydicom.errors import InvalidDicomError
from PIL import Image

VERBOSE = False

def get_LUT_value(data, window, level):
    """Apply the RGB Look-Up Table for the given data and window/level value."""
    return np.piecewise(
        data,
        [
            data <= (level - 0.5 - (window - 1) / 2),
            data > (level - 0.5 + (window - 1) / 2),
        ],
        [
            0,
            255,
            lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0),
        ],
    )

def dicom2png(dicom_file : str, output_dir: str, bit_depth : int) -> int:
    """
    Convert a DICOM image to PNG.
    It will make the tree of directories from the `dicom_file` path in
    the `output_dir` directory.
    """
    result = 1
    try:
        dicom_file = dicom_file.strip()
        ds = pydicom.dcmread(os.path.abspath(dicom_file))

        if hasattr(ds, 'WindowWidth') and hasattr(ds, 'WindowCenter'):
            ww = ds.WindowWidth[0] if isinstance(ds.WindowWidth, pydicom.multival.MultiValue) else ds.WindowWidth
            wc = ds.WindowCenter[0] if isinstance(ds.WindowCenter, pydicom.multival.MultiValue) else ds.WindowCenter
            image_2d = get_LUT_value(ds.pixel_array, ww, wc)
        else:
            # Si no hay valores de ventana/centro, usar los datos tal cual
            image_2d = ds.pixel_array

        image = image_2d
        # If LUT value is present on `ds`, apply it before doing the conversion.
        assert image is not None, "dicom2png(): unsuported bit depth"

        # Normalize the image based on the bit depth
        image = (np.maximum(image, 0) / image.max()) * (float(1 << bit_depth) - 1)
        image_PIL = Image.fromarray(image)

        base_name = os.path.basename(dicom_file).replace('.dcm', '.png').replace('.dicom', '.png')

        path_segments = dicom_file.split('/')
        path_segments[0] = output_dir.replace('/', '')
        path_segments[-1] = base_name

        len_dirs = len(path_segments) - 1
        pathwobasename = [seg for idx, seg in enumerate(path_segments) if idx < len_dirs]

        path = Path(os.path.join('./', *pathwobasename))

        # Same behaviour as mkdir -p
        path.mkdir(parents=True, exist_ok=True)

        output_file = os.path.join('./', *path_segments)

        img = None
        if bit_depth == 8:
            img = image_PIL.convert("L")

        if bit_depth == 16:
            img = image_PIL.convert('I;16')

        if img is not None:
            img.save(output_file)

        if VERBOSE:
            print(f"Successfully saved PNG format image from \n\"{os.path.abspath(dicom_file)}\" to \"{output_file}\".")
        result = 0
    # If a DICOM image can't be converted (due to bad file encoding headers or if the
    # pixels can't be converted to pixel array as type uint16, etc.), ignore it since
    # we need the subprocess to continue running.
    #
    # Note: this is a naive solution, the code can be improved to handle this errors
    # without catching exceptions.
    except TypeError:
        pass
    except InvalidDicomError:
        pass
    except AttributeError:
        pass
    return result

def dicom2npy(dicom_file : str, output_dir: str, bit_depth : int) -> int:
    """Convert DICOM images to NPY format"""
    result = 1
    try:
        dicom_file = dicom_file.strip()
        ds = pydicom.dcmread(os.path.abspath(dicom_file))

        if hasattr(ds, 'WindowWidth') and hasattr(ds, 'WindowCenter'):
            ww = ds.WindowWidth[0] if isinstance(ds.WindowWidth, pydicom.multival.MultiValue) else ds.WindowWidth
            wc = ds.WindowCenter[0] if isinstance(ds.WindowCenter, pydicom.multival.MultiValue) else ds.WindowCenter
            image_2d = get_LUT_value(ds.pixel_array, ww, wc)
        else:
            # Si no hay valores de ventana/centro, usar los datos tal cual
            image_2d = ds.pixel_array

        image_2d = cp.asarray(image_2d, dtype=cp.float32)

        # Rescaling grey scale between 0-255
        image_2d_scaled = (cp.maximum(image_2d, 0) / cp.max(image_2d))

        # Normalize the image based on the bit depth
        normalized_image = (np.maximum(image_2d_scaled, 0) / image_2d_scaled.max()) * (float(1 << bit_depth) - 1)
        base_name = os.path.basename(dicom_file).replace('.dcm', '.npy').replace('.dicom', '.npy')

        path_segments = dicom_file.split('/')
        path_segments[0] = output_dir.replace('/', '')
        path_segments[-1] = base_name

        len_dirs = len(path_segments) - 1
        pathwobasename = [seg for idx, seg in enumerate(path_segments) if idx < len_dirs]

        path = Path(os.path.join('./', *pathwobasename))

        # Same behaviour as mkdir -p
        path.mkdir(parents=True, exist_ok=True)

        output_file = os.path.join('./', *path_segments)

        # Save as NumPy array
        np.save(output_file, cp.asnumpy(image_2d_scaled))

        if VERBOSE:
            print(f"Successfully saved PNG format image from \n\"{os.path.abspath(dicom_file)}\" to \"{output_file}\".")
        result = 0
    # If a DICOM image can't be converted (due to bad file encoding headers or if the
    # pixels can't be converted to pixel array as type uint16, etc.), ignore it since
    # we need the subprocess to continue running.
    #
    # Note: this is a naive solution, the code can be improved to handle this errors
    # without catching exceptions.
    except TypeError:
        pass
    except InvalidDicomError:
        pass
    except AttributeError:
        pass
    return result

def readicom(filepath: str) -> List[str]:
    """Read the file containing the DICOM image paths and return it as a list."""
    with open(filepath, 'r') as dcmf:
        lines = dcmf.readlines()
    return lines

def distribute_work(data: List[Any], size: int) -> List[Any]:
    """Split data into nearly equal chunks for distribution."""
    chunk_size = len(data) // size
    remainder = len(data) % size

    chunks = [data[i * chunk_size + min(i, remainder):(i + 1) * chunk_size + min(i + 1, remainder)] for i in range(size)]
    return chunks

def main(dcmpaths_filepath: str, output: str, bit_depth: int, formats: List[str]) -> int:
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        dcmpaths = readicom(dcmpaths_filepath)
        chunks = distribute_work(dcmpaths, size)
    else:
        chunks = []

    dcmpaths_chunk = comm.scatter(chunks, root=0)

    for dicom_img_path in dcmpaths_chunk:
        if VERBOSE:
            print(f"[process {rank}]", end=" ")

        if 'NPY' in formats:
            dicom2npy(dicom_img_path, output + '-npy', bit_depth)

        if 'PNG' in formats:
            dicom2png(dicom_img_path, output + '-png', bit_depth)

    all_images = comm.gather(chunks, root=0)

    if rank == 0:
        if all_images is None:
            print("Processed zero images.")
            return 0

            if VERBOSE:
                print(f"Successfully processed {len(all_images)} DICOM images.")

    MPI.Finalize()
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert DICOM format images to PNG,NPY format.')
    parser.add_argument('-b', '--bit-depth', type=int, nargs=1, help='Bit-depth of resulting images')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-f', '--formats', type=str, action='append', help='Conversion format')
    parser.add_argument('dcmpaths', type=str, nargs=1, help='Path to a file containing paths to DICOM images')
    parser.add_argument('outdir', type=str, nargs=1, help='Output directory')

    args = parser.parse_args()
    os.makedirs(args.outdir[0], exist_ok=True)

    if args.bit_depth is None:
        args.bit_depth = [8]

    if args.verbose:
        VERBOSE = True

    main(args.dcmpaths[0], args.outdir[0], args.bit_depth[0], args.formats)
