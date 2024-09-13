#!/usr/bin/env bash

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

usage() {
    echo "usage: $0 [-o output-path] <DICOM images directory>" 1>&2
    exit 1
}

outpath=''
while getopts ":o:" opt; do
    case "${opt}" in
        o)
            outpath+="${OPTARG}"
        ;;
        *)
        ;;
    esac
done
shift $((OPTIND-1))


if [ -n "$1" ]; then
    dicomdir=$1
else
    usage
fi

if [ -z "$outpath" ]; then
    outpath+='dcmpaths.dat'
fi

locate_dicom() {
    find $dicomdir | grep -E '.dcm|.dicom' > $outpath
}

locate_dicom

numdcm=$(nl $outpath | tail -n 1 | awk '{print $1}')            # Total number of found DICOM images.
echo "Successfully written $numdcm DICOM image paths to \"$outpath\""
