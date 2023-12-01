#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   utils.py
@Author  :   Raighne.Weng
@Version :   1.5.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Utils Class module
'''

import os
import glob
from pathlib import Path
from os.path import isdir, isfile

import humps

from datature.error import Error

SUPPORTED_FILE_EXTENSIONS = [
    '*.jpg', '*.JPG', '*.png', '*.PNG', '*.jpeg', '*.JPEG', '*.mp4', '*.MP4',
    "*.dcm", "*.DCM", '*.nii', '*.NII'
]

ANNOTATION_FORMAT_EXTENSIONS_MAPPING = {
    "coco": ["*.json"],
    "csv_fourcorner": ["*.csv"],
    "csv_widthheight": ["*.csv"],
    "pascal_voc": ["*.xml"],
    "yolo_darknet": ["*.labels", "*.txt"],
    "yolo_keras_pytorch": ["*.txt"],
    "createml": ["*.json"],
    "polygon_coco": ["*.json"],
    "polygon_single": ["*.json"],
    "csv_classification": ["*.csv"],
    "keypoints_coco": ["*.json"],
}


def get_asset_metadata_limit_by_tier(tier: str) -> int:
    """Get asset limit by tier.

    :param tier: the tier of the project owner
    :return: limit in bytes
    """
    # professional tier 0.5kb
    if tier == "professional":
        return 500
    # developer tier 0.3kb
    if tier == "developer":
        return 300
    # free tier 0kb
    return 0


def find_all_assets(path: Path) -> [str]:
    """
    List all assets under folder, include sub folder.

    :param path: The folder to upload assets.
    :return: assets path list.
    """
    file_paths = []

    # find all assets under folder and sub folders
    for file_ext in SUPPORTED_FILE_EXTENSIONS:
        file_paths.extend(
            glob.glob(os.path.join(path, '**', file_ext), recursive=True))

    return file_paths


def find_all_annotations_files(path: Path, annotation_format: str) -> [str]:
    """
    List all annotations files under folder, include sub folder.

    :param path: The folder to upload annotations files.
    :param annotation_format: The format of the annotation type.
    :return: assets path list.
    """
    file_extensions = ANNOTATION_FORMAT_EXTENSIONS_MAPPING.get(
        annotation_format)

    if not file_extensions:
        raise Error("The annotation format is not valid")

    file_paths = []
    if isfile(path):
        file_paths.append(path)
    elif isdir(path):
        for file_ext in file_extensions:
            file_paths.extend(
                glob.glob(os.path.join(path, '**', file_ext), recursive=True))

    if len(file_paths) <= 0:
        raise Error("Could not find the annotation file")

    return file_paths


def get_exportable_annotations_formats(project_type: str) -> [str]:
    """
    Get the exported annotations formats by project type.

    :param project_type: The type of the project.
    :return: The exported annotations formats.
    """
    if project_type == "classification":
        return ["csv_classification", "classification_tfrecord"]

    if project_type == "keypoint":
        return ["keypoints_coco"]

    return ["coco", "csv_fourcorner", "csv_widthheight", "pascal_voc",
            "yolo_darknet", "yolo_keras_pytorch", "createml",
            "tfrecord", "polygon_single", "polygon_coco"]


def get_importable_annotations_formats(project_type: str) -> [str]:
    """
    Get the importable annotations formats by project type.

    :param project_type: The type of the project.
    :return: The importable annotations formats.
    """
    if project_type == "classification":
        return ["csv_classification"]

    if project_type == "keypoint":
        return ["keypoints_coco"]

    return ["coco", "csv_fourcorner", "csv_widthheight", "pascal_voc",
            "yolo_darknet", "yolo_keras_pytorch", "createml",
            "polygon_single", "polygon_coco"]


def selective_decamelize(data):
    """
    Decamelize a dict, but leave some keys unchanged.

    :param data: The json dict.
    :return: The decamelized data.
    """
    exclude_keys = ["customMetadata"]

    # If data is a dict, decamelize the keys
    if isinstance(data, dict):
        decamelized_data = {}
        for key, value in data.items():
            # Decamelize the key
            new_key = humps.decamelize(key)
            if key in exclude_keys:
                # If the key is the exclude key, decamelize it, but don't recurse into its value
                decamelized_data[new_key] = value
            elif isinstance(value, (dict, list)):
                # If the value is a dict and the key is not the exclude key, recurse into the value
                decamelized_data[new_key] = selective_decamelize(value)
            else:
                # Otherwise, just copy the value
                decamelized_data[new_key] = value
        return decamelized_data

    if isinstance(data, list):
        # If data is a list, apply the function to each item in the list if it's a dict, otherwise just copy the item
        return [selective_decamelize(item) if isinstance(item, dict) else item for item in data]

    return None
