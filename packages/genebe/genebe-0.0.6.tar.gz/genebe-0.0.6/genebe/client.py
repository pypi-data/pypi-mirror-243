import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, List
import re
import json
import logging
import netrc
from tinynetrc import Netrc
from urllib.parse import urlparse
from importlib import metadata


# Read the version using importlib.metadata
try:
    __version__ = metadata.version("genebe")
except metadata.PackageNotFoundError:
    __version__ = "unknown"

# Set up the User-Agent header
user_agent = f"GeneBe/{__version__} (requests)"


def _save_credentials_to_netrc(machine, login, password):
    netrc = Netrc()
    netrc[machine]["login"] = login
    netrc[machine]["password"] = password
    netrc.save()


def _get_machine_name_from_endpoint(endpoint):
    """
    Extracts the machine name from an endpoint URL.

    Args:
        endpoint (str): The endpoint URL.

    Returns:
        str: The machine name extracted from the endpoint.
    """
    parsed_url = urlparse(endpoint)
    return parsed_url.netloc


def _read_netrc_credentials(endpoint):
    """
    Reads username and password from the .netrc file based on the machine name derived from the endpoint.

    Args:
        endpoint (str): The endpoint URL.

    Returns:
        tuple: A tuple containing (username, account, password). Returns (None, None, None) if no
        matching entry is found in the .netrc file.
    """
    machine_name = _get_machine_name_from_endpoint(endpoint)

    try:
        # Locate the .netrc file in the user's home directory
        netrc_file_path = netrc.netrc()

        # Get the authentication information for the specified machine
        login_info = netrc_file_path.authenticators(machine_name)

        if login_info:
            username, account, password = login_info
            return username, account, password
        else:
            return None, None, None

    except FileNotFoundError:
        print("Error: .netrc file not found.")
        return None, None, None


def _parse_variant_string(s):
    pattern = re.compile(r"^[^-]+-\d+-[ACGT]*-[ACGT]*$")
    if pattern.match(s):
        chr_, pos, ref, alt = s.split("-")
        pos = int(pos)
        return {"chr": chr_, "pos": pos, "ref": ref, "alt": alt}
    else:
        print(f"Error: Invalid format in {s}")
        return None


# Assuming you have a DataFrame named df with columns CHROM, POS, REF, ALT


# Function to annotate variants
def annotate_variants_list(
    variants: List[str],
    genome: str = "hg38",
    use_ensembl: bool = True,
    use_refseq: bool = True,
    flatten_consequences: bool = True,
    batch_size: int = 500,
    username: str = None,
    api_key: str = None,
    use_netrc: bool = True,
    endpoint_url: str = "https://api.genebe.net/cloud/api-public/v1/variants",
) -> List[Dict[str, object]]:
    """
    Annotates a list of genetic variants.

    Args:
        variants (List[str]): A list of genetic variants to be annotated.
            Format: chr-pos-ref-alt. Look at examples below.
        use_ensembl (bool, optional): Whether to use Ensembl for annotation.
            Defaults to True.
        use_refseq (bool, optional): Whether to use RefSeq for annotation.
            Defaults to True.
        genome (str, optional): The genome version for annotation (e.g., 'hg38').
            Defaults to 'hg38'.
        flatten_consequences (bool, optional): If set to False, return consequences as a list of objects.
            If set to True, only the most important consequence is returned in a flat form.
            Defaults to True.
        batch_size (int, optional): The size of each batch for processing variants.
            Defaults to 100. Must be smaller or equal 1000.
        username (str, optional): The username for authentication.
            Defaults to None.
        api_key (str, optional): The API key for authentication.
            Defaults to None.
        use_netrc (bool, optional): Whether to use credentials from the user's
            .netrc file for authentication. Defaults to True.
        endpoint_url (str, optional): The API endpoint for variant annotation.
            Defaults to 'https://api.genebe.net/cloud/api-public/v1/variants'.

    Returns:
        List[Dict[str, object]]: A list of dictionaries containing annotation information
        for each variant. The dictionary structure may vary. Check the current documentation
        on https://genebe.net/about/api

    Example:
        >>> variants = ["7-69599651-A-G", "6-160585140-T-G"]
        >>> annotations = annotate_variants_list(variants, use_ensembl=True,
        ...                                      use_refseq=False, genome='hg38',
        ...                                      batch_size=500, username="user123@example.com",
        ...                                      api_key="apikey456", use_netrc=False,
        ...                                      endpoint_url='https://api.genebe.net/cloud/api-public/v1/variants')
        >>> print(annotations)
        [{'chr': '7', 'pos':69599651 (...) }]

    Note:
        - The number of the elements in returned list is always equal to the number of queries.
    """

    if (use_refseq != True) and (use_ensembl != True):
        raise ValueError("use_refseq and use_ensembl cannot be both False")

    if (username is not None) and (api_key is not None):
        auth = (username, api_key)
        if use_netrc:
            _save_credentials_to_netrc(endpoint_url, username, api_key)
    elif use_netrc:
        username, _, api_key = _read_netrc_credentials(endpoint_url)
        if (username is not None) and (api_key is not None):
            auth = (username, api_key)
        else:
            auth = None
    else:
        auth = None

    # if username:
    if api_key == None:
        logging.warning(
            f"You are not logged in to GeneBe. We recommend using login function."
        )

    # input data validation
    # Convert the list of strings to list of dictionaries
    dict_list = [_parse_variant_string(s) for s in variants]
    logging.debug("I will query for " + json.dumps(dict_list))

    annotated_data = []

    for i in range(0, len(dict_list), batch_size):
        # Prepare data for API request
        api_data = dict_list[i : i + batch_size]

        logging.debug("Querying for " + json.dumps(api_data))

        params = {"genome": genome}
        # Make API request
        response = requests.post(
            endpoint_url,
            params=params,
            json=api_data,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": user_agent,
            },
            auth=auth,
        )

        # Check if request was successful
        if response.status_code == 200:
            api_results_raw = response.json()
            api_results = [element for element in api_results_raw["variants"]]

            logging.debug("Backend result is " + json.dumps(api_results))

            # Append API results to annotated_data
            annotated_data.extend(api_results)
        else:
            logging.error(
                f"Got response with code {response.status_code} with body "
                + json.dumps(response.json())
            )

    if flatten_consequences:
        for item in annotated_data:
            consequences_fields = None
            if item["transcript"]:  # check the ACMG chosen transcript
                if str(item["transcript"]).startswith("E"):
                    consequences_fields = "consequences_ensembl"
                else:
                    consequences_fields = "consequences_refseq"

                consequences_refseq = item[consequences_fields]
                if consequences_refseq:  # Check if the list is not empty
                    first_consequence = consequences_refseq[0]
                    for key in ["gene_symbol", "gene_hgnc_id", "transcript", "hgvs_c"]:
                        item[key] = first_consequence.get(key, None)
                    effects_list = first_consequence.get("consequences", None)
                    item["consequences"] = (
                        ",".join(
                            str(item) if item is not None else "None"
                            for item in effects_list
                        )
                        if effects_list is not None
                        else ""
                    )
            # Remove the 'consequences_refseq' field
            del item["consequences_ensembl"]
            del item["consequences_refseq"]

    return annotated_data


def annotate_variants_list_to_dataframe(
    variants: List[str],
    use_ensembl: bool = True,
    use_refseq: bool = True,
    genome: str = "hg38",
    batch_size: int = 100,
    flatten_consequences: bool = True,
    username: str = None,
    api_key: str = None,
    use_netrc: bool = True,
    endpoint_url: str = "https://api.genebe.net/cloud/api-public/v1/variants",
) -> pd.DataFrame:
    # Call the existing function
    result_list = annotate_variants_list(
        variants=variants,
        use_ensembl=use_ensembl,
        use_refseq=use_refseq,
        flatten_consequences=flatten_consequences,
        genome=genome,
        batch_size=batch_size,
        username=username,
        api_key=api_key,
        use_netrc=use_netrc,
        endpoint_url=endpoint_url,
    )

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(result_list)
    return df
