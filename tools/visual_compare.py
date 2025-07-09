from typing import Any
from smolagents.tools import Tool
import base64
import requests
import os

class VisualIdentityCompareTool(Tool):
    name = "visual_identity_compare"
    description = (
        "Compares two images to determine if they show the same person. "
        "The comparison may use facial features, clothing, tattoos, or other visible cues. "
        "Requires a user-provided inference endpoint that accepts two images."
    )
    inputs = {
        'image1_path': {
            'type': 'string',
            'description': 'Path to the first image file.'
        },
        'image2_path': {
            'type': 'string',
            'description': 'Path to the second image file.'
        },
        'endpoint_url': {
            'type': 'string',
            'description': 'The inference endpoint URL that performs the visual identity comparison.'
        }
    }
    output_type = "string"

    def __init__(self, headers=None):
        super().__init__()
        self.headers = headers or {"Content-Type": "application/json"}

    def _load_base64(self, path: str) -> str:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image path not found: {path}")
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def forward(self, image1_path: str, image2_path: str, endpoint_url: str) -> str:
        img1 = self._load_base64(image1_path)
        img2 = self._load_base64(image2_path)

        payload = {
            "image1": img1,
            "image2": img2
        }

        try:
            response = requests.post(endpoint_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return str(response.json())  # Can customize formatting depending on endpoint output
        except requests.RequestException as e:
            return f"Request failed: {str(e)}"
