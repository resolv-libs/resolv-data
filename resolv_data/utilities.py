""" This module contains utility functions useful for datasets manipulation. """
import gzip
import hashlib
import logging
import lzma
import os
import requests
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union


_SUPPORTED_ARCHIVES = ['.zip', '.tar', '.tar.gz', '.tgz', '.tar.xz', '.txz', ".tbz", ".tar.bz", '.xz', '.gz']


def download(url: str,
             output_file_path: Union[str, Path] = None,
             temp: bool = False,
             temp_suffix: str = None,
             stream: bool = True,
             chunk_size: int = 1024 * 1024,
             force_overwrite: bool = False,
             checksum: str = None,
             checksum_type: str = "sha256",
             allow_invalid_checksum: bool = False) -> Path:
    """ Download a file from a given URL.

    Args:
        url (str): The URL from which to download the file.
        output_file_path (Union[str, Path], optional): The path where the downloaded file will be saved. If None,
            a temporary location will be used even if temp is False. Defaults to None.
        temp (bool, optional): If True, a temporary file will be used for downloading. Defaults to False.
        temp_suffix (str, optional): The suffix to be added to the temporary file name. Applied only if temp is True.
            Defaults to None.
        stream (bool, optional): If True, the download will be streamed. Defaults to True.
        chunk_size (int, optional): The chunk size for streaming the download, in bytes. Defaults to 1024 * 1024.
        force_overwrite (bool, optional): If True, existing files at the output path will be overwritten.
            Defaults to False.
        checksum (str, optional): The expected checksum of the downloaded file. Defaults to None.
        checksum_type (str, optional): The type of checksum to validate. Must be 'md5' or 'sha256'.
            Defaults to "sha256".
        allow_invalid_checksum (bool, optional): If True, the checksum validation will be skipped if it fails.
            Defaults to False.

    Returns:
        (Path): The path to the downloaded file.

    Raises:
        RuntimeError: If an existing file has a different checksum from the expected one.
    """
    # Set output file according to the temp flag.
    if not temp:
        # Check if file already exists.
        if output_file_path:
            if output_file_path.exists():
                if force_overwrite:
                    # Delete the file/dir if running in overwrite mode.
                    output_file_path.unlink() if output_file_path.is_file() else (
                        shutil.rmtree(output_file_path, ignore_errors=True))
                else:
                    if not allow_invalid_checksum and not validate_checksum(output_file_path, checksum, checksum_type):
                        raise RuntimeError(f"Existing file has a different {checksum_type} hash from the expected one.")
                    logging.info(f"Found existing downloaded file: {output_file_path}. Skipping download. To overwrite "
                                 f"it, use --force-overwrite flag.")
                    return Path(output_file_path)
            output_path_file_parent = Path(output_file_path).parent.absolute().expanduser()
            output_path_file_parent.mkdir(parents=True, exist_ok=True)
            output_file = open(output_file_path, mode='wb')
        else:
            output_file = NamedTemporaryFile(mode='wb', delete=False)
    else:
        output_file = NamedTemporaryFile(mode='wb', suffix=f'_{temp_suffix}', delete=False)
        if output_file_path:
            logging.warning(f"The given output path {output_file_path} will be ignored while downloading the dataset since "
                            f"the flag temp is True.")

    # Download and validate file.
    output_file_name = output_file.name
    logging.info(f"Downloading source: {url} to {output_file_name}...")
    with requests.get(url, stream=stream) as r:
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=chunk_size):
            if chunk:
                output_file.write(chunk)
        output_file.close()
        logging.info(f"Successfully downloaded source: {output_file_name}.")
        if not allow_invalid_checksum and not validate_checksum(output_file_name, checksum, checksum_type):
            raise RuntimeError(f"Downloaded file has a different {checksum_type} hash from the expected one.")
        return Path(output_file_name)


def compute_checksum(file_path: Union[str, Path],
                     checksum_type: str = "sha256",
                     chunk_size: int = 1024 * 1024) -> str:
    """ Compute the checksum of a given file.

    Args:
        file_path (Union[str, Path]): The path to the file.
        checksum_type (str, optional): The type of checksum to compute. Must be 'md5' or 'sha256'. Defaults to "sha256".
        chunk_size (int, optional): The chunk size for reading the file, in bytes. Defaults to 1024 * 1024.

    Returns:
        str: The computed checksum.

    Raises:
        ValueError: If the path is None or if the checksum type is not 'md5' or 'sha256'.
    """
    if file_path is None:
        raise ValueError("File path is None.")

    if checksum_type == "md5":
        hash_fn = hashlib.md5
    elif checksum_type == "sha256":
        hash_fn = hashlib.sha256
    else:
        raise ValueError(f"Checksum type must be 'md5' or 'sha256'. Type {checksum_type} not supported.")

    hash_out = hash_fn()
    with open(str(file_path), "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_out.update(chunk)
    return hash_out.hexdigest()


def validate_checksum(file_path: Union[str, Path],
                      checksum: str,
                      checksum_type: str = "sha256",
                      chunk_size: int = 1024 * 1024) -> bool:
    """ Validates whether a file's checksum matches the provided checksum.

    Args:
        file_path (Union[str, Path]): The path to the file.
        checksum (str): The expected checksum.
        checksum_type (str, optional): The type of checksum to validate. Must be 'md5' or 'sha256'.
            Defaults to "sha256".
        chunk_size (int, optional): The chunk size for reading the file, in bytes. Defaults to 1024 * 1024.

    Returns:
        bool: True if the checksum matches, False otherwise.
    """
    computed_checksum = compute_checksum(file_path, checksum_type, chunk_size)
    logging.debug(f'Original checksum: {checksum}. Computed checksum: {computed_checksum}.')
    return computed_checksum == checksum


def extract_archive(archive_path: Union[str, Path],
                    output_path: Union[str, Path] = None,
                    move_root_dir: bool = True,
                    kind: str = None,
                    cleanup: bool = False) -> Union[str, Path]:
    """ Extract an archive file to a specified output directory.

    Args:
        archive_path (Union[str, Path]): The path to the archive file.
        output_path (Union[str, Path], optional): The directory where the archive will be extracted. If None, the
            parent directory of the archive will be used. Defaults to None.
        move_root_dir (bool, optional): If True, moves the root directory of the extracted files to the output
            directory. Defaults to True.
        kind (str, optional): The type of archive. If None, it will be inferred from the file extension.
            Defaults to None.
        cleanup (bool, optional): If True, removes the source archive after extraction. Defaults to False.

    Returns:
        Union[str, Path]: The path to the extracted directory.

    Raises:
        ValueError: If the specified kind of archive is not supported.
    """
    def _infer_archive_type():
        for supported_ext in _SUPPORTED_ARCHIVES:
            if str(archive_path).endswith(supported_ext):
                return supported_ext
        return None

    archive_path = Path(archive_path)
    output_path = Path(output_path) if output_path is not None else archive_path.parent / archive_path.stem
    kind = _infer_archive_type() if kind is None else kind

    logging.info(f"Extracting archive : {archive_path} to {output_path}...")
    if kind in (".zip", ".tar", ".tgz", ".tar.gz", ".txz", ".tar.xz", ".tbz", ".tar.bz"):
        shutil.unpack_archive(archive_path, output_path)
    elif kind in (".gz", ".xz"):
        if kind == ".gz":
            with gzip.open(output_path, "rb") as f_in, open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        else:
            with lzma.open(output_path, "rb") as f_in_, open(output_path, "wb") as f_out:
                shutil.copyfileobj(f_in_, f_out)
    else:
        raise ValueError(f"Expect `kind` to be one of {','.join(_SUPPORTED_ARCHIVES)}, but got: {kind}.")

    logging.info(f"Successfully extracted archive: {archive_path} to {output_path}.")

    if cleanup:
        logging.info(f"Removing source archive: {archive_path}...")
        os.remove(archive_path)

    if move_root_dir:
        archive_root = next(output_path.iterdir())
        logging.info(f"Moving root directory: {archive_root} to {output_path}...")
        move_content(archive_root, output_path, delete_src=True)

    return output_path


def move_content(source_dir: Union[str, Path], destination_dir: Union[str, Path], delete_src: bool = False):
    """ Move the contents of a source directory to a destination directory.

    Args:
        source_dir (Union[str, Path]): The path to the source directory.
        destination_dir (Union[str, Path]): The path to the destination directory.
        delete_src (bool, optional): If True, deletes the source directory after moving its contents. Defaults to False.
    """
    source_directory = Path(source_dir)
    destination_directory = Path(destination_dir)
    for item in source_directory.iterdir():
        destination_path = destination_directory / item.name
        item.rename(destination_path)
    if delete_src:
        source_directory.rmdir()
