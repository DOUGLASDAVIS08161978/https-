#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright 2024 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""CLI interface to metadata wizard  API
   2024 Google
"""

# OS Imports
import argparse
import requests
import logging

logger = logging.getLogger(__name__)
# Set log level (optional)
logger.setLevel(logging.DEBUG) # or logging.INFO, logging.WARNING, etc.



def _call_api(
    service,
    scope,
    use_lineage_tables,
    use_lineage_processes,
    use_profile,
    use_data_quality,
    use_ext_documents,
    dataplex_project_id,
    llm_location,
    dataplex_location,
    documentation_uri,
    table_project_id,
    table_dataset_id,
    table_id,
    debug,
    documentation_csv_uri,
    strategy,
    **kwargs
):
    API_URL = f"https://{service}"
    API_URL_DEBUG = "http://localhost:8000"
    METADATA_TABLE_SCOPE_ROUTE = "/generate_table_description"
    METADATA_COLUMNS_SCOPE_ROUTE = "/generate_columns_descriptions"
    METADATA_DATASET_SCOPE_ROUTE = "/generate_dataset_tables_descriptions"
    METADATA_DBT_SCOPE_ROUTE = "/generate_dbt_model_description"

    if debug:
        API_URL = API_URL_DEBUG
    if scope == "table":
        url = API_URL + METADATA_TABLE_SCOPE_ROUTE
    elif scope == "columns":
        url = API_URL + METADATA_COLUMNS_SCOPE_ROUTE
    elif scope == "dataset":
        url = API_URL + METADATA_DATASET_SCOPE_ROUTE
    elif scope == "dbt":
        url = API_URL + METADATA_DBT_SCOPE_ROUTE

    params = {
        "client_options_settings": {
            "use_lineage_tables": use_lineage_tables,
            "use_lineage_processes": use_lineage_processes,
            "use_profile": use_profile,
            "use_data_quality": use_data_quality,
            "use_ext_documents": use_ext_documents,
        },
        "client_settings": {
            "project_id": dataplex_project_id,
            "llm_location": llm_location,
            "dataplex_location": dataplex_location
        },
        "table_settings": {
            "project_id": table_project_id,
            "dataset_id": table_dataset_id,
            "table_id": table_id,
            "documentation_uri": documentation_uri
        },
        "dataset_settings": {
            "project_id": table_project_id,
            "dataset_id": table_dataset_id,
            "documentation_csv_uri": documentation_csv_uri,
            "strategy": strategy
        },
        "dbt_settings": {
            "dbt_project_path": kwargs.get("dbt_project_path"),
            "model_name": kwargs.get("dbt_model_name")
        }
    }
    try:
        response = requests.post(url, json=params)
        response.raise_for_status()  
        print(response.json())
        logger.debug(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")


def _get_input_arguments():
    """Argparse helper."""
    parser = argparse.ArgumentParser(description="Call Metadata Wizard API.")
    parser.add_argument("--service",
                        dest="service",
                        required=True,
                        type=str
                        )
    parser.add_argument("--scope",
                        dest="scope",
                        required=True,
                        type=str
                        )
    parser.add_argument(
        "--use_lineage_tables",
        dest="use_lineage_tables",
        required=False,
        default=False,
        type=bool
    )
    parser.add_argument(
        "--use_lineage_processes",
        dest="use_lineage_processes",
        required=False,
        default=False,
        type=bool
    )
    parser.add_argument(
        "--use_profile",
        dest="use_profile",
        required=False,
        default=False,
        type=bool
        )
    parser.add_argument(
        "--use_data_quality",
        dest="use_data_quality",
        required=False,
        default=False,
        type=bool
    )
    parser.add_argument(
        "--use_ext_documents",
        dest="use_ext_documents",
        required=False,
        default=False,
        type=bool
    )
    parser.add_argument(
        "--dataplex_project_id",
        dest="dataplex_project_id",
        required=True,
        type=str
    )
    parser.add_argument(
        "--llm_location",
        dest="llm_location",
        required=True,
        type=str
    )
    parser.add_argument(
        "--dataplex_location",
        dest="dataplex_location",
        required=True,
        type=str
    )
    parser.add_argument(
        "--documentation_uri",
        dest="documentation_uri",
        required=False,
        default="",
        type=str
    )
    parser.add_argument(
        "--table_project_id",
        dest="table_project_id",
        required=True,
        type=str
    )
    parser.add_argument(
        "--table_dataset_id",
        dest="table_dataset_id",
        required=True,
        type=str
    )
    parser.add_argument(
        "--table_id",
        dest="table_id",
        required=True,
        type=str
        )   
    parser.add_argument(
        "--debug",
        dest="debug",
        required=False,
        type=bool,
        default=False
        )
    parser.add_argument(
        "--strategy",
        dest="strategy",
        required=False,
        type=str,
        default="1"
        )

    parser.add_argument(
        "--documentation_csv_uri",
        dest="documentation_csv_uri",
        required=False,
        type=str,
        default=""
        )
    return parser.parse_args()


def main():
    """The main function."""
    parser = argparse.ArgumentParser(
        description="CLI for the Metadata Wizard API."
    )
    subparsers = parser.add_subparsers(dest="scope", help="Execution scope")

    # Common arguments
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(
        "--service",
        type=str,
        default="127.0.0.1",
        help="The service to call.",
    )
    common_parser.add_argument(
        "--use_lineage_tables",
        dest="use_lineage_tables",
        required=False,
        default=False,
        type=bool
    )
    common_parser.add_argument(
        "--use_lineage_processes",
        dest="use_lineage_processes",
        required=False,
        default=False,
        type=bool
    )
    common_parser.add_argument(
        "--use_profile",
        dest="use_profile",
        required=False,
        default=False,
        type=bool
        )
    common_parser.add_argument(
        "--use_data_quality",
        dest="use_data_quality",
        required=False,
        default=False,
        type=bool
    )
    common_parser.add_argument(
        "--use_ext_documents",
        dest="use_ext_documents",
        required=False,
        default=False,
        type=bool
    )
    common_parser.add_argument(
        "--dataplex_project_id",
        dest="dataplex_project_id",
        required=True,
        type=str
    )
    common_parser.add_argument(
        "--llm_location",
        dest="llm_location",
        required=True,
        type=str
    )
    common_parser.add_argument(
        "--dataplex_location",
        dest="dataplex_location",
        required=True,
        type=str
    )
    common_parser.add_argument(
        "--documentation_uri",
        dest="documentation_uri",
        required=False,
        default="",
        type=str
    )
    common_parser.add_argument(
        "--table_project_id",
        dest="table_project_id",
        required=True,
        type=str
    )
    common_parser.add_argument(
        "--table_dataset_id",
        dest="table_dataset_id",
        required=True,
        type=str
    )
    common_parser.add_argument(
        "--table_id",
        dest="table_id",
        required=True,
        type=str
        )   
    common_parser.add_argument(
        "--debug",
        dest="debug",
        required=False,
        type=bool,
        default=False
        )
    common_parser.add_argument(
        "--strategy",
        dest="strategy",
        required=False,
        type=str,
        default="1"
        )

    common_parser.add_argument(
        "--documentation_csv_uri",
        dest="documentation_csv_uri",
        required=False,
        type=str,
        default=""
        )

    # Table parser
    table_parser = subparsers.add_parser("table", help="Generate metadata for a table.", parents=[common_parser])

    # Columns parser
    columns_parser = subparsers.add_parser("columns", help="Generate metadata for table columns.", parents=[common_parser])

    # Dataset parser
    dataset_parser = subparsers.add_parser("dataset", help="Generate metadata for a dataset.", parents=[common_parser])
    dataset_parser.add_argument(
        "--strategy",
        type=int,
        default=0,
        help="The strategy to use for generating metadata. 0 for NAIVE, 1 for RANDOM, 2 for ALPHABETICAL, 3 for DOCUMENTED, 4 for DOCUMENTED_THEN_REST",
    )

    # DBT parser
    dbt_parser = subparsers.add_parser("dbt", help="Generate metadata for a dbt model.", parents=[common_parser])
    dbt_parser.add_argument(
        "--dbt_project_path",
        type=str,
        required=True,
        help="The path to the dbt project.",
    )
    dbt_parser.add_argument(
        "--dbt_model_name",
        type=str,
        required=True,
        help="The name of the dbt model.",
    )


    args = parser.parse_args()

    _call_api(
        args.service,
        args.scope,
        args.use_lineage_tables,
        args.use_lineage_processes,
        args.use_profile,
        args.use_data_quality,
        args.use_ext_documents,
        args.dataplex_project_id,
        args.llm_location,
        args.dataplex_location,
        args.documentation_uri,
        args.table_project_id,
        args.table_dataset_id,
        args.table_id if hasattr(args, "table_id") else None,
        args.debug,
        args.documentation_csv_uri if hasattr(args, "documentation_csv_uri") else None,
        args.strategy if hasattr(args, "strategy") else None,
        **vars(args)
    )


if __name__ == "__main__":
    main()
