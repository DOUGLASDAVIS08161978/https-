#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""Dataplex Utils dbt reader
   2024 Google
"""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DBTReader:
    """A class to read and parse dbt artifacts."""

    def __init__(self, dbt_project_path: str):
        """Initializes the DBTReader."""
        self.dbt_project_path = Path(dbt_project_path)
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> dict:
        """Loads the dbt manifest.json file."""
        manifest_path = self.dbt_project_path / "target/manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"manifest.json not found in {manifest_path}")
        with open(manifest_path, "r") as f:
            return json.load(f)

    def get_model(self, model_name: str) -> dict:
        """Gets a specific model from the manifest."""
        model_key = f"model.{self.manifest['metadata']['project_id']}.{model_name}"
        model = self.manifest["nodes"].get(model_key)
        if not model:
            raise ValueError(f"Model '{model_name}' not found in dbt project.")
        return model

    def get_model_description(self, model_name: str) -> str:
        """Gets a model's description."""
        model = self.get_model(model_name)
        return model.get("description", "")

    def get_model_columns(self, model_name: str) -> dict:
        """Gets a model's columns and their descriptions."""
        model = self.get_model(model_name)
        return {
            col: details.get("description", "")
            for col, details in model.get("columns", {}).items()
        }
