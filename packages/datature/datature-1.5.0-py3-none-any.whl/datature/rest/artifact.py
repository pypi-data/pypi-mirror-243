#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   artifact.py
@Author  :   Raighne.Weng
@Version :   1.5.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Artifact API
'''

import zipfile
import tempfile
from pathlib import Path

import requests

from datature import error
from datature.http.resource import RESTResource


class Artifact(RESTResource):
    """Datature Artifact API Resource."""

    @classmethod
    def list(cls, show_models=False) -> dict:
        """Lists all artifacts in the project.

        :param show_models: The boolean indication on whether to return the exported models.
        :return: A list of dictionaries containing the artifact metadata with the following structure:

                .. code-block:: json

                        [
                            {
                                "id": "artifact_63bd140e67b42dc9f431ffe2",
                                "object": "artifact",
                                "is_training": false,
                                "step": 3000,
                                "flow_title": "Blood Cell Detector",
                                "run_id": "run_63bd08d8cdf700575fa4dd01",
                                "files": [
                                    {
                                        "name": "ckpt-13.data-00000-of-00001",
                                        "md5": "5a96886e53f98daae379787ee0f22bda"
                                    }
                                ],
                                "project_id": "proj_cd067221d5a6e4007ccbb4afb5966535",
                                "artifact_name": "ckpt-13",
                                "create_date": 1673335822851,
                                "metric": {
                                    "total_loss": 0.548,
                                    "classification_loss": 0.511,
                                    "localization_loss": 0.006,
                                    "regularization_loss": 0.03
                                },
                                "is_deployed": false,
                                "exports": [],
                                "model_type": "efficientdet-d1-640x640"
                            }
                        ]

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Artifact.list()
        """
        if show_models:
            return cls.request("GET",
                               "/artifact/list?models=true")

        return cls.request("GET", "/artifact/list")

    @classmethod
    def retrieve(cls, artifact_id: str, show_models=False) -> dict:
        """Retrieves a specific artifact using the artifact ID.

        :param artifact_id: The ID of the artifact as a string.
        :param show_models: The boolean indication on whether to return the exported models.
        :return: A dictionary containing the specific artifact metadata with the following structure:

                .. code-block:: json

                            {
                                "id": "artifact_63bd140e67b42dc9f431ffe2",
                                "object": "artifact",
                                "is_training": false,
                                "step": 3000,
                                "flow_title": "Blood Cell Detector",
                                "run_id": "run_63bd08d8cdf700575fa4dd01",
                                "files": [
                                    {
                                        "name": "ckpt-13.data-00000-of-00001",
                                        "md5": "5a96886e53f98daae379787ee0f22bda"
                                    }
                                ],
                                "project_id": "proj_cd067221d5a6e4007ccbb4afb5966535",
                                "artifact_name": "ckpt-13",
                                "create_date": 1673335822851,
                                "metric": {
                                    "total_loss": 0.548,
                                    "classification_loss": 0.511,
                                    "localization_loss": 0.006,
                                    "regularization_loss": 0.03
                                },
                                "is_deployed": false,
                                "exports": [],
                                "model_type": "efficientdet-d1-640x640"
                            }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Artifact.retrieve("artifact_63bd140e67b42dc9f431ffe2")
        """
        if show_models:
            return cls.request("GET",
                               f"/artifact/{artifact_id}?models=true")

        return cls.request("GET", f"/artifact/{artifact_id}")

    @classmethod
    def list_exported(cls, artifact_id: str) -> dict:
        """Lists all exported models of a specific artifact.

        :param artifact_id: The ID of the artifact as a string.
        :return: A list of dictionaries with the exported model metadata with the following structure:

                .. code-block:: json

                        [
                            {
                                "id": "model_d15aba68872b045e27ac3db06a401da3",
                                "object": "model",
                                "status": "Finished",
                                "format": "tensorflow",
                                "create_date": 1673336054173,
                                "download": {
                                    "method": "GET",
                                    "expiry": 1673339505871,
                                    "url": "https://storage.googleapis.com/exports.datature.ioa2d89"
                                }
                            }
                        ]

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Artifact.list_exported("artifact_63bd140e67b42dc9f431ffe2")
        """
        return cls.request(
            "GET",
            f"/artifact/{artifact_id}/models",
        )

    @classmethod
    def export_model(cls, artifact_id: str, model_format: str) -> dict:
        """Exports an artifact model in a specific model format.

        :param artifact_id: The ID of the artifact as a string.
        :param model_format: The export format of the model.

        :return: A dictionary containing the operation metadata of the model export with the following structure:

                .. code-block:: json

                            {
                                "id": "model_d15aba68872b045e27ac3db06a401da3",
                                "object": "model",
                                "status": "Running",
                                "format": "tensorflow",
                                "create_date": 1673336054173,
                            }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Artifact.export_model(
                            "artifact_63bd140e67b42dc9f431ffe2", "tensorflow")
        """
        return cls.request("POST",
                           f"/artifact/{artifact_id}/export",
                           request_body={"format": model_format})

    @classmethod
    def download_model(cls, model_id: str, path=None) -> dict:
        """Exports an artifact model in a specific model format.

        :param model_id: The ID of the artifact exported model.
        :param path: The download path for the model, default current path.

        :return: A dictionary containing the download path of the model:

                .. code-block:: json

                        {
                            "download_path": "/Volumes/Coding",
                            "model_filename": "datature-yolov8l.pt",
                            "label_filename": "label_map.pbtxt"
                        }

        :example:
                .. code-block:: python

                        import datature

                        datature.secret_key = "5aa41e8ba........"
                        datature.Artifact.download_model("model_63bd140e67b42dc9f431ffe2")
        """
        artifacts = cls.request("GET", "/artifact/list?models=true")

        if path:
            download_path = Path(path)
            # Create directory if it doesn't exist
            download_path.mkdir(parents=True, exist_ok=True)
        else:
            download_path = Path.cwd()

        for artifact in artifacts:
            if 'models' in artifact:
                for model in artifact['models']:
                    if model_id in (model['id'], model['id'].split('_')[1]):
                        url = model['download']['url']

                        resp = requests.get(url,
                                            stream=True,
                                            timeout=(60, 3600))

                        # Download the file
                        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                            for data in resp.iter_content(chunk_size=1024):
                                temp_file.write(data)

                        # Unzip the file
                        model_files = []
                        with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
                            zip_ref.extractall(download_path)

                            for file_name in zip_ref.namelist():
                                # Check if the file ends with the desired extension
                                if any(file_name.endswith(ext) for ext in [".onnx", ".tflite", ".pt"]):
                                    model_files.append(file_name)

                        return {
                            "download_path": str(download_path),
                            "model_filename": "saved_model/" if model['format'] == 'tensorflow' else model_files[0],
                            "label_filename": "label.txt" if model['format'] == 'tflite' else "label_map.pbtxt",
                        }

        # If didn't find the model key in the artifacts, raise an 404 error
        raise error.NotFoundError(
            f"Model with id {model_id} not found, please export model first."
        )
