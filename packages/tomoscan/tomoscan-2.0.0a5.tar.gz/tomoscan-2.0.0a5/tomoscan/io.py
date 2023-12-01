# coding: utf-8

"""Module dedicated to input / output utils"""

import errno
import logging
import os
import traceback
from contextlib import contextmanager

import h5py

from tomoscan.utils import SharedLockPool
from packaging.version import Version

if Version(h5py.__version__) >= Version("3.10.0"):
    HASSWMR = True
else:
    HASSWMR = h5py.version.hdf5_version_tuple >= h5py.get_config().swmr_min_hdf5_version
_logger = logging.getLogger(__name__)


class HDF5File(h5py.File):
    """File to secure reading and writing within h5py

    code originally from bliss.nexus_writer_service.io.nexus
    """

    _LOCKPOOL = SharedLockPool()

    def __init__(self, filename, mode, enable_file_locking=None, swmr=None, **kwargs):
        """
        :param str filename:
        :param str mode:
        :param bool enable_file_locking: by default it is disabled for `mode=='r'`
                                         and enabled in all other modes
        :param bool swmr: when not specified: try both modes when `mode=='r'`
        :param **kwargs: see `h5py.File.__init__`
        """
        if mode not in ("r", "w", "w-", "x", "a"):
            raise ValueError(f"invalid mode {mode}")

        with self._protect_init(filename):
            # https://support.hdfgroup.org/HDF5/docNewFeatures/SWMR/Design-HDF5-FileLocking.pdf
            if not HASSWMR and swmr:
                swmr = False
            libver = kwargs.get("libver")
            if swmr:
                kwargs["libver"] = "latest"
            if enable_file_locking is None:
                enable_file_locking = mode != "r"
            old_file_locking = os.environ.get("HDF5_USE_FILE_LOCKING", None)
            if enable_file_locking:
                os.environ["HDF5_USE_FILE_LOCKING"] = "TRUE"
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
            kwargs["track_order"] = True
            try:
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
                if mode != "r" and swmr:
                    # Try setting writing in SWMR mode
                    try:
                        self.swmr_mode = True
                    except Exception:
                        pass
            except OSError as e:
                if (
                    swmr is not None
                    or mode != "r"
                    or not HASSWMR
                    or not isErrno(e, errno.EAGAIN)
                ):
                    raise
                # Try reading with opposite SWMR mode
                swmr = not swmr
                if swmr:
                    kwargs["libver"] = "latest"
                else:
                    kwargs["libver"] = libver
                super().__init__(filename, mode=mode, swmr=swmr, **kwargs)
            if old_file_locking is None:
                del os.environ["HDF5_USE_FILE_LOCKING"]
            else:
                os.environ["HDF5_USE_FILE_LOCKING"] = old_file_locking

    @contextmanager
    def _protect_init(self, filename):
        """Makes sure no other file is opened/created
        or protected sections associated to the filename
        are executed.
        """
        lockname = os.path.abspath(filename)
        with self._LOCKPOOL.acquire(None):
            with self._LOCKPOOL.acquire(lockname):
                yield

    @contextmanager
    def protect(self):
        """Protected section associated to this file."""
        lockname = os.path.abspath(self.filename)
        with self._LOCKPOOL.acquire(lockname):
            yield


def isErrno(e, errno):
    """
    :param OSError e:
    :returns bool:
    """
    # Because e.__cause__ is None for chained exceptions
    return f"errno = {errno}" in "".join(traceback.format_exc())


def check_virtual_sources_exist(fname, data_path):
    """
    Check that a virtual dataset points to actual data.

    :param str fname: HDF5 file path
    :param str data_path: Path within the HDF5 file

    :return bool res: Whether the virtual dataset points to actual data.
    """
    with HDF5File(fname, "r") as f:
        if data_path not in f:
            _logger.error(f"No dataset {data_path} in file {fname}")
            return False
        dptr = f[data_path]
        if not dptr.is_virtual:
            return True
        for vsource in dptr.virtual_sources():
            vsource_fname = os.path.join(
                os.path.dirname(dptr.file.filename), vsource.file_name
            )
            if not os.path.isfile(vsource_fname):
                _logger.error(f"No such file: {vsource_fname}")
                return False
            elif not check_virtual_sources_exist(vsource_fname, vsource.dset_name):
                _logger.error(f"Error with virtual source {vsource_fname}")
                return False
    return True
