"""Utility module for helpful functions"""
import logging
import zipfile

from fw_file.dicom import DICOMCollection
from fw_file.dicom.utils import sniff_dcm

from .fixers import is_dcm

log = logging.getLogger(__name__)


def calculate_decompressed_size(dicom_path: str) -> int:
    """Estimate size of decompressed file, to assist in calculating
    whether the container has enough memory available to successfully
    decompress without running afoul of the OOM killer.

    Args:
        dicom_path: Path to directory containing dicom files

    Returns:
        int: Estimated size of decompressed file in bytes
    """
    if sniff_dcm(dicom_path):
        dcms = DICOMCollection(dicom_path, filter_fn=is_dcm, force=True)
    elif zipfile.is_zipfile(str(dicom_path)):
        dcms = DICOMCollection.from_zip(dicom_path, filter_fn=is_dcm, force=True)
    else:
        raise RuntimeError(
            "Invalid file type passed in, not a DICOM nor a Zip Archive."
        )

    if len(dcms) > 1:
        frames = len(dcms)
    elif len(dcms) == 1:
        try:
            frames = dcms.get("NumberOfFrames")
        except AttributeError:
            try:
                frames = len(dcms.get("PerFrameFunctionalGroupsSequence"))
            except AttributeError:
                frames = 1
    else:  # len(dcms) == 0:
        # No valid dicoms is handled later on in dicom-fixer,
        # so for now, we're logging and moving on.
        log.warning(
            "Unable to estimate size of decompressed file; no valid dicoms found."
        )
        return 0

    try:
        total_bytes = (
            dcms.get("Rows")
            * dcms.get("Columns")
            * frames
            * dcms.get("SamplesPerPixel")
            * dcms.get("BitsAllocated")
            / 8  # convert from bits to bytes
        )
    except TypeError:
        # One or more tags needed to calculate size missing
        log.warning(
            "Unable to estimate size of decompressed file due to missing tags. Continuing."
        )
        return 0

    return total_bytes
