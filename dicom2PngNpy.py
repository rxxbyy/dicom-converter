import os
import sys
import psutil
import time
import cupy as cp
import pydicom
from PIL import Image
from pydicom import dcmread
from pydicom.errors import InvalidDicomError
from pydicom.misc import is_dicom
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import mpi4py
from mpi4py import MPI

error_log = "conversion_errors.log"

def readicom(filepath):
    """ Custom function to read DICOM file as binary. """
    with open(filepath, 'rb') as dcmf:
        lines = dcmf.read()
    return lines

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

def mri_to_png(mri_file_path, npy_file_path, png_file_path, bit_depth):
    """ Function to convert from a DICOM image to both.npy and.png using GPU for faster processing.
        Allows selection between 8-bit and 16-bit depth.
    """
    try:
        # Leer el archivo DICOM
        plan = dcmread(mri_file_path)

        # Asegurarse de que el archivo DICOM contiene datos de píxeles
        if 'PixelData' not in plan:
            raise ValueError(f'File "{mri_file_path}" does not contain pixel data.')

        # Verificar si WindowWidth y WindowCenter están presentes y son válidos
        if hasattr(plan, 'WindowWidth') and hasattr(plan, 'WindowCenter'):
            ww = plan.WindowWidth[0] if isinstance(plan.WindowWidth, pydicom.multival.MultiValue) else plan.WindowWidth
            wc = plan.WindowCenter[0] if isinstance(plan.WindowCenter, pydicom.multival.MultiValue) else plan.WindowCenter
            image_2d = get_LUT_value(plan.pixel_array, ww, wc)
        else:
            # Si no hay valores de ventana/centro, usar los datos tal cual
            image_2d = plan.pixel_array
        
        # Convertir la imagen a CuPy (GPU) para escalado
        image_2d = cp.asarray(image_2d, dtype=cp.float32)

        # Rescaling grey scale between 0-255
        image_2d_scaled = (cp.maximum(image_2d, 0) / cp.max(image_2d))

        # Convert to 8-bit or 16-bit
        if bit_depth == 8:
            image_2d_scaled = (image_2d_scaled * 255).astype(cp.uint8)
        else:  # Default is 16-bit
            image_2d_scaled = (image_2d_scaled * 65535).astype(cp.uint16)

        # Save as NumPy array
        np.save(npy_file_path, cp.asnumpy(image_2d_scaled))

        # Convert to CPU for saving as PNG
        image_2d_scaled_cpu = cp.asnumpy(image_2d_scaled)

        # Save as PNG
        img = Image.fromarray(image_2d_scaled_cpu)
        if bit_depth == 8:
            img = img.convert("L")  # 8-bit grayscale
        else:
            img = img.convert("I;16")  # 16-bit grayscale
        img.save(png_file_path)

    except (InvalidDicomError, AttributeError, TypeError, ValueError, FileNotFoundError) as e:
        # Log the error to the file and return failure result
        with open(error_log, 'a') as log:
            log.write(f"Error processing {mri_file_path}: {str(e)}\n")
        raise

def convert_file(mri_file_path, npy_file_path, png_file_path, bit_depth, output_type):
    """ Function to convert an MRI DICOM file to both NumPy (.npy) and PNG (.png) image files.
    """
    if not os.path.exists(mri_file_path):
        raise FileNotFoundError(f'File "{mri_file_path}" does not exist')

    if os.path.exists(npy_file_path) or os.path.exists(png_file_path):
        raise FileExistsError(f'File "{npy_file_path}" or "{png_file_path}" already exists')

    # Validar si el archivo es un archivo DICOM
    if not is_dicom(mri_file_path):
        raise InvalidDicomError(f'File "{mri_file_path}" is not a valid DICOM file')

    if output_type == 'npy':
        mri_to_png(mri_file_path, npy_file_path, None, bit_depth)
    elif output_type == 'png':
        mri_to_png(mri_file_path, None, png_file_path, bit_depth)
    elif output_type == 'ambas':
        mri_to_png(mri_file_path, npy_file_path, png_file_path, bit_depth)
    else:
        raise ValueError(f'Invalid output type: {output_type}')

def convert_folder(mri_folder, output_folder, bit_depth=16, output_type='ambas', max_workers=os.cpu_count()):
    os.makedirs(output_folder, exist_ok=True)

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Proceso maestro
        # Lee la lista de archivos a procesar
        files = []
        for mri_sub_folder, subdirs, files_in_subdir in os.walk(mri_folder):
            files.extend([os.path.join(mri_sub_folder, file) for file in files_in_subdir])

        # Divide la lista de archivos entre los procesos
        chunk_size = len(files) // size
        chunks = [files[i*chunk_size:(i+1)*chunk_size] for i in range(size)]

        # Envía la lista de archivos a cada proceso
        for i in range(1, size):
            comm.send(chunks[i], dest=i, tag=0)

    else:
        # Procesos esclavos
        # Recibe la lista de archivos del proceso maestro
        files = comm.recv(source=0, tag=0)

    processed_files = 0
    for file in files:
        # Procesa el archivo
        rel_path = os.path.relpath(file, mri_folder)
        output_sub_folder = os.path.join(output_folder, os.path.dirname(rel_path))
        os.makedirs(output_sub_folder, exist_ok=True)
        npy_file_path = os.path.join(output_sub_folder, os.path.basename(file).replace('.dcm', '.npy'))
        png_file_path = os.path.join(output_sub_folder, os.path.basename(file).replace('.dcm', '.png'))
        convert_file(file, npy_file_path, png_file_path, bit_depth, output_type)
        processed_files += 1
        print(f'Proceso {rank}: {processed_files} archivos procesados')

    comm.Barrier()
    MPI.Finalize()

if __name__ == "__main__":
    mri_folder = sys.argv[1]
    output_folder = sys.argv[2]
    bit_depth = int(sys.argv[3]) if len(sys.argv) > 3 else 16  # Default to 16 bits if not specified
    output_type = sys.argv[4] if len(sys.argv) > 4 else 'ambas'  # Default to ambas if not specified
    convert_folder(mri_folder, output_folder, bit_depth=bit_depth, output_type=output_type)
