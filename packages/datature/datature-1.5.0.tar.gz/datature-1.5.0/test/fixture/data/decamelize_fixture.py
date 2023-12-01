#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   decamelize_fixture.py
@Author  :   Raighne.Weng
@Version :   1.3.0
@Contact :   raighne@datature.io
@License :   Apache License 2.0
@Desc    :   Datature Decamelize Test Data
'''

project_response = {
    "id": "proj_cd067221d5a6e4007ccbb4afb5966535",
    "object": "project",
    "owner": "user_6323fea23e292439f31c58cd",
    "tier": "developer",
    "name": "New Test Name",
    "type": "object-detection",
    "createDate": 1673253800069,
    "localization": "MULTI",
    "tags": [
        "RBC",
        "WBC",
        "boat"
    ],
    "groups": [
        "main"
    ],
    "statistic": {
        "tagsCount": [
            {
                "name": "RBC",
                "count": 0
            },
            {
                "name": "WBC",
                "count": 0
            },
            {
                "name": "boat",
                "count": 1549
            }
        ],
        "assetTotal": 500,
        "assetAnnotated": 485,
        "annotationTotal": 1549
    }
}

decamelized_project_response = {
    "id": "proj_cd067221d5a6e4007ccbb4afb5966535",
    "object": "project",
    "owner": "user_6323fea23e292439f31c58cd",
    "tier": "developer",
    "name": "New Test Name",
    "type": "object-detection",
    "create_date": 1673253800069,
    "localization": "MULTI",
    "tags": [
        "RBC",
        "WBC",
        "boat"
    ],
    "groups": [
        "main"
    ],
    "statistic": {
        "tags_count": [
            {
                "name": "RBC",
                "count": 0
            },
            {
                "name": "WBC",
                "count": 0
            },
            {
                "name": "boat",
                "count": 1549
            }
        ],
        "asset_total": 500,
        "asset_annotated": 485,
        "annotation_total": 1549
    }
}

quota_response = {
    "limit": {
        "collaborator": 3,
        "image": 6000000,
        "compute": 60000,
        "artifact": 50,
        "artifactExport": 25,
        "intellibrush": 1000,
        "externalSource": 10,
        "octopodCpu": 24,
        "octopodGpu": 2
    },
    "usage": {
        "collaborator": 1,
        "image": 127365,
        "compute": 12784.25,
        "artifact": 11,
        "artifactExport": 12,
        "intellibrush": 0,
        "externalSource": 5,
        "octopodCpu": 0,
        "octopodGpu": 0
    }
}

decamelized_quota_response = {
    "limit": {
        "collaborator": 3,
        "image": 6000000,
        "compute": 60000,
        "artifact": 50,
        "artifact_export": 25,
        "intellibrush": 1000,
        "external_source": 10,
        "octopod_cpu": 24,
        "octopod_gpu": 2
    },
    "usage": {
        "collaborator": 1,
        "image": 127365,
        "compute": 12784.25,
        "artifact": 11,
        "artifact_export": 12,
        "intellibrush": 0,
        "external_source": 5,
        "octopod_cpu": 0,
        "octopod_gpu": 0
    }
}


asset_response = {
    "id": "asset_f16ddaa5-ef27-4fb9-9582-62ef24ec874b",
    "object": "asset",
    "filename": "boat180.png",
    "project": "proj_cd067221d5a6e4007ccbb4afb5966535",
    "createDate": 1698979252412,
    "metadata": {
        "fileSize": 186497,
        "mimeType": "image/png",
        "status": "annotated",
        "height": 243,
        "width": 400,
        "groups": [
            "main"
        ],
        "customMetadata": {
            "crameraId": "crameraId",
            "reviewed": True,
            "lat": 1.28
        }
    },
    "statistic": {
        "tagsCount": [
            {
                "name": "boat",
                "count": 1
            }
        ],
        "annotationTotal": 1
    },
}

decamelized_asset_response = {
    "id": "asset_f16ddaa5-ef27-4fb9-9582-62ef24ec874b",
    "object": "asset",
    "filename": "boat180.png",
    "project": "proj_cd067221d5a6e4007ccbb4afb5966535",
    "create_date": 1698979252412,
    "metadata": {
        "file_size": 186497,
        "mime_type": "image/png",
        "status": "annotated",
        "height": 243,
        "width": 400,
        "groups": [
            "main"
        ],
        "custom_metadata": {
            "crameraId": "crameraId",
            "reviewed": True,
            "lat": 1.28
        }
    },
    "statistic": {
        "tags_count": [
            {
                "name": "boat",
                "count": 1
            }
        ],
        "annotation_total": 1
    }
}


artifact_response = [
    {
        "id": "artifact_654461bac5f1057014134d46",
        "isTraining": False,
        "step": 5000,
        "flowTitle": "Yolov8 Workflow",
        "runId": "run_c05eeade-cd89-4daa-ba00-8a8f886c952a",
        "files": [
            {
                "name": "ckpt-23-datature-yolov8n.pt",
                "md5": "78e99ebf2ddd691d2ea4723c389c98b6"
            }
        ],
        "projectId": "proj_cd067221d5a6e4007ccbb4afb5966535",
        "artifact": "ckpt-23-datature-yolov8n",
        "createDate": 1698980282483,
        "metric": {
            "totalLoss": 12.071,
            "classificationLoss": 3.5076
        },
        "isDeployed": False,
        "exports": [
            "pytorch",
            "onnx"
        ],
        "modelName": "yolov8-nano-320x320",
        "modelType": "yolov8",
        "exportableFormats": [
            "pytorch",
            "onnx"
        ]
    }
]

decamelized_artifact_response = [
    {
        "id": "artifact_654461bac5f1057014134d46",
        "is_training": False,
        "step": 5000,
        "flow_title": "Yolov8 Workflow",
        "run_id": "run_c05eeade-cd89-4daa-ba00-8a8f886c952a",
        "files": [
            {
                "name": "ckpt-23-datature-yolov8n.pt",
                "md5": "78e99ebf2ddd691d2ea4723c389c98b6"
            }
        ],
        "project_id": "proj_cd067221d5a6e4007ccbb4afb5966535",
        "artifact": "ckpt-23-datature-yolov8n",
        "create_date": 1698980282483,
        "metric": {
            "total_loss": 12.071,
            "classification_loss": 3.5076
        },
        "is_deployed": False,
        "exports": [
            "pytorch",
            "onnx"
        ],
        "model_name": "yolov8-nano-320x320",
        "model_type": "yolov8",
        "exportable_formats": [
            "pytorch",
            "onnx"
        ]
    }
]
