""" This module contains the base classes that define the main properties of a dataset. """
import logging
import shutil

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Union, Any

from google.protobuf.json_format import MessageToJson

from resolv_data import utilities
from resolv_data.protobuf import DatasetIndex


@dataclass
class DatasetInfo:
    """A container for dataset metadata."""
    name: str
    version: str
    description: str
    homepage: str
    license_info: str
    citation: str


@dataclass
class RemoteSource:
    """The metadata for a remote file

    Attributes:
        filename (str): the remote file's basename
        url (str): the remote file's url
        checksum (str): the remote file's md5 checksum
        archive (bool)
    """
    filename: str
    url: str
    checksum: str
    checksum_type: str
    main_source: bool = False
    archive: bool = False
    has_archived_root: bool = False


class DirectoryDataset(ABC):

    def __init__(self, mode: str):
        """ Initializes the DirectoryDataset object with the specified parameters.

        Args:
            mode (str): The mode of the dataset.

        Raises:
            ValueError: If the mode is invalid.
        """
        self._root_dir = None
        if mode in self.remote_sources().keys():
            self._mode = mode
        else:
            raise ValueError(f"Invalid mode: {mode} for dataset {self}. Valid modes are: {self.remote_sources.keys()}")

    def __repr__(self) -> str:
        """ Returns a string representation of the DirectoryDataset object. """
        return f"{type(self).__name__}(root={self._root_dir})"

    @property
    @abstractmethod
    def info(self) -> DatasetInfo:
        """ Abstract property for accessing dataset information. """
        pass

    @staticmethod
    @abstractmethod
    def remote_sources() -> Dict[str, List[RemoteSource]]:
        """ Abstract property for accessing remote sources of the dataset. """
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """ Abstract property for accessing the version of the dataset."""
        pass

    @abstractmethod
    def _compute_index_internal(self, *args, **kwargs) -> DatasetIndex:
        """ Abstract method for computing the index of the dataset.

        Returns:
            (DatasetIndex): DatasetIndex proto representing the index of the dataset.
        """
        pass

    @property
    def root_dir(self) -> Path:
        """ Returns the path to the root directory of the dataset.

        Note: this will return None if the dataset has not been downloaded yet.

        """
        return self._root_dir

    @property
    def root_dir_name(self) -> str:
        """ Returns the root directory name for the dataset """
        return f'{self.info.name.replace(" ", "_").lower()}-v{self.version}-{self._mode}'

    def compute_index(self, *args, **kwargs) -> Any:
        """ Abstract method for computing the index of the dataset.
        It calls _compute_index_internal to compute the index of the concrete dataset, and then it serializes the proto
        message to disk, saving it in the root directory as index.json.

        Returns:
            (DatasetIndex): DatasetIndex proto representing the index of the dataset.
        """
        index = self._compute_index_internal(*args, **kwargs)
        json_data = MessageToJson(index)
        with open(self._root_dir / "index.json", 'w') as file:
            file.write(json_data)
        return index

    def download(self, output_path: Union[str, Path] = None, temp: bool = False, overwrite: bool = False,
                 cleanup: bool = True, allow_invalid_checksum: bool = False) -> Path:
        """ Downloads the dataset from remote sources and extracts it if necessary.

        The method will download all the sources of the dataset in the root directory of the dataset: the root directory
        is a temporary directory if temp is set to True, otherwise it can be specified during the object initialization
        or let empty, in that case a default location is used (see _default_path()).

        Only one source in the remote_sources property for the selected dataset mode must be specified as the main one.
        The path where this source is downloaded will be set as the root directory of the dataset. If the source is an
        archive the path where the archive is extracted will be set as the root directory.

        Args:
            output_path (Union[str, Path], optional): The path where the root directory of the dataset will be
                downloaded. Defaults to None. If not specified and temp is not True, the one specified by
                _default_path() will be used.
            temp (bool, optional): If True, use a temporary directory for download. Defaults to False.
            overwrite (bool, optional): If True, overwrite existing files during download. Defaults to False.
            cleanup (bool, optional): If True, cleanup temporary files after download. Defaults to True.
            allow_invalid_checksum (bool, optional): If True, allow invalid checksums during dataset download.
                Defaults to False.

        Returns:
            (Path): The path to the root directory of the downloaded dataset.

        Raises:
            ValueError: If more than one source is defined as the main one.
        """

        # Set the base output path according to the temp flag.
        base_output_path = None
        if not temp:
            base_output_path = Path(output_path) if output_path else self._default_path()
            root_dir_path = base_output_path / self.root_dir_name
            if root_dir_path.is_dir():
                if overwrite:
                    # Delete existing root directory is running in overwrite mode
                    shutil.rmtree(root_dir_path, ignore_errors=True)
                else:
                    logging.warning(f"Dataset already exists and has root directory: {self.root_dir}. Skipping download. "
                                    f"To overwrite it, call the download() method with overwrite=True.")
                    self._root_dir = root_dir_path
                    return self.root_dir
        else:
            if output_path:
                logging.warning(f"The given output path {output_path} will be ignored while downloading the dataset "
                                f"since the flag temp is True.")
            if overwrite:
                logging.warning(f"The flag overwrite is set to True but it will be ignored while downloading the "
                                f"dataset since also the flag temp is True.")

        # Download sources
        sources = self.remote_sources()[self._mode]
        # Exactly one of the sources must be identified as the main one for the dataset
        main_sources_count = sum(1 for x in sources if x.main_source)
        if main_sources_count != 1:
            raise ValueError(f"Exactly one source must be designed as the main one. Found {main_sources_count}.")
        # Sort sources to be sure that the main one is the first to be downloaded
        sources = sorted(sources, key=lambda x: x.main_source, reverse=True)
        for source in sources:
            # If current source is the main one set the output path according to tmp, otherwise set the output path to
            # the dataset root directory
            if source.main_source:
                source_output_path = base_output_path / source.filename if not temp else None
            else:
                source_output_path = self.root_dir / source.filename

            downloaded_sources_path = utilities.download(
                url=source.url,
                output_file_path=source_output_path,
                temp=temp if source.main_source else False,
                temp_suffix=source.filename,
                force_overwrite=overwrite,
                checksum=source.checksum,
                checksum_type=source.checksum_type,
                allow_invalid_checksum=allow_invalid_checksum
            )

            if source.archive:
                extraction_dir_name = self.root_dir_name if source.main_source else source.filename.split(".")[0]
                downloaded_sources_path = utilities.extract_archive(
                    archive_path=downloaded_sources_path,
                    output_path=downloaded_sources_path.parent / extraction_dir_name,
                    move_root_dir=source.has_archived_root,
                    cleanup=cleanup
                )
            elif source.main_source:
                root_dir_path = downloaded_sources_path.parent / self.root_dir_name
                utilities.move_content(downloaded_sources_path, root_dir_path, delete_src=True)

            # If current source is the main one set the root directory for the dataset to its path
            if source.main_source:
                logging.info(f"Setting dataset root directory to {downloaded_sources_path}...")
                self._root_dir = downloaded_sources_path

        return self.root_dir

    @staticmethod
    def _default_path() -> Path:
        """ Get the default path for the dataset

        Returns:
            (str): Local path to the dataset
        """
        return Path.home() / ".resolv" / "datasets"
