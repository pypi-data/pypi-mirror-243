import csv
import json
import os
import re
import shutil

import pandas as pd
from objectpath import Tree
from pandas.errors import EmptyDataError, ParserError

FILE_MARK = "file::"

MODEL_DIR_NAMES = {
    "IR": "Nominal_rates",
    "RIR": "Real_rates",
    "EQ": "Equity",
    "RE": "Real_estate",
    "CRED": "Credit",
    "FX": "FX_rate",
}

PARAM_KEYS_FOLDERS_MAPPING = {
    "param.dependence": "Correlation",
    "hist_corr.target_corr": "Correlation",
    "param.table_format": "Formats",
    "param.roll_forward": "Roll_Forward",
    "param.aom": "Roll_Forward",
    "param.report.mt.weights": "Report",
    "param.report.mt.asset_shares": "Report",
    "param.report.mc.swaptions.weights": "Report",
    "param.report.mc.swaptions.thresholds": "Report",
    "param.report.mc.eq_re_options.weights": "Report",
    "param.report.mc.eq_re_options.thresholds": "Report",
    "param.report.mc.fx_options.weights": "Report",
    "param.report.mc.fx_options.thresholds": "Report",
}


def read_json_file(file_path):
    """Reads a json file and returns a dict

    Args:
        file_path (str): Path to the json file

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is not a json file

    Returns:
        dict: The json file as a dict
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist. Unable to read json")

    with open(file_path, "r") as json_file:
        try:
            json_data = json.load(json_file)
        except ValueError as exc:
            raise ValueError(f"{file_path} is not a valid json file. {str(exc)}")

        return json_data


def find_file_in_directory(filename, dir):
    """Finds a file in a directory

    Args:
        filename (str): The name of the file to find
        dir (str): The directory to search

    Returns:
        str: The path to the file if found, None otherwise
    """
    if not os.path.exists(dir):
        return None

    for root, _, files in os.walk(dir):
        if filename in files:
            return os.path.join(root, filename).replace("\\", "/")

    return None


def read_csv_from_filepath(filepath):
    """Reads a csv file and returns a dataframe

    Args:
        filepath (str): Path to the csv file

    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file is empty or not valid

    Returns:
        dataframe: The csv file as a dataframe
    """
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError("File does not exist. Unable to read csv")

    # Reads the content of the csv file to a single column and applies
    # a mapping to replace all ; inside "" to _SEMI_COL
    # .squeeze("columns") turns a dataframe with a single column
    # to a Series that which we verify is the result's type
    try:
        # Read the csv file as a series using '~' as the delimiter
        # which should not be present in the csv file
        sensi_file = pd.read_csv(filepath, sep=r"~", header=None, quoting=csv.QUOTE_NONE).squeeze("columns")
        if not isinstance(sensi_file, pd.Series):
            raise ValueError('File contains the delimiter "~" which is not allowed in sensi csv files')
    except EmptyDataError:
        raise ValueError("File is empty")
    except ParserError:
        raise ValueError("File is not a valid csv file")

    # Replace all ; inside "" with _SEMI_COL and replace all " with nothing
    # And then split the whole csv using the remaining ; as delimiter
    # And add a '_count_sep' column to count the number of ; in each row
    try:
        # TODO: Check what to do with _SEMI_COL after parsing
        sensi_file = sensi_file.map(lambda x: re.sub(r'"([^"]*)"', lambda m: re.sub(r";", "_SEMI_COL", m.group()), x))
        sensi_file = sensi_file.map(lambda x: re.sub(r'"', "", x))
        sensi_file = pd.concat(
            [
                sensi_file.str.split(";", expand=True),
                sensi_file.str.count(";").rename("_count_sep"),
            ],
            axis=1,
        )
        # Replace back all _SEMI_COL with ;
        sensi_file = sensi_file.replace("_SEMI_COL", ";", regex=True)
    except:
        raise ValueError("File is not a valid csv file")

    return sensi_file


def copy_dir(base_rsrc_dir, sensi_rsrc_dir):
    """
    Copy the contents of base_rsrc_dir to sensi_rsrc_dir,
    recursively copying any linked directories.
    """
    for root, dirs, files in os.walk(base_rsrc_dir):
        for item in dirs + files:
            path = os.path.join(root, item)
            real_path = os.path.realpath(path) if os.path.islink(path) else path

            # If the path is a symlink but doesn't point to an existing file/folder, skip it
            if not os.path.exists(real_path):
                continue

            dest_path = os.path.join(sensi_rsrc_dir, os.path.relpath(path, base_rsrc_dir))

            if os.path.islink(path) and os.path.isdir(real_path):
                # Recursive call to copy the linked directory
                os.makedirs(dest_path, exist_ok=True)
                copy_dir(real_path, dest_path)
            else:
                copy_file_or_directory(path, dest_path)


def copy_file_or_directory(src_path, dest_path):
    if os.path.isdir(src_path):
        os.makedirs(dest_path, exist_ok=True)
    else:
        shutil.copy2(src_path, dest_path)


def query(data, expression):
    """Queries data using expression

    Args:
        data (json): data to query from
        expression (str): expression to query with

    Raises:
        ValueError: if data is empty
        or expression is invalid or the query fails

    Returns:
        list: list of results (or a single result)
    """

    if data is None or expression is None:
        raise ValueError("Incorrect input. data or expression is None")

    expression = expression.strip()
    if not expression.startswith("$"):
        raise ValueError("Expression does not start with $")

    result = []
    try:
        tree = Tree(data)
        query_result = tree.execute(expression)
        if query_result:
            if isinstance(query_result, str):
                # Convert string to a list with one element
                result = query_result.split(None, -1)
            else:
                result = list(query_result)

    except Exception as e:
        raise ValueError(f"Failed to query for data")

    return result


def get_input_file_path(data, expression, env_dir):
    """Gets the input file path from the data using the expression

    Args:
        data (dict): data to query from
        expression (str): expression to query with
        env_dir (str): environment directory where the input file is located

    Raises:
        RuntimeError: if any of the queries fail

    Returns:
        str: input file path
    """
    # Query for input file
    try:
        filename = query(data, expression)[0]
    except (ValueError, IndexError) as e:
        raise RuntimeError("Error occurred while fetching input file path")

    if re.search(r"\[@\.name is '\w+'\]", expression) or re.search(r"\['\w+'\]", expression):
        # Query for eco and driver
        matches = re.findall(r"(?<=')\w+(?=')", expression)
        if len(matches) != 2:
            raise RuntimeError("Unable to get eco and driver from expression")

        eco_name, driver_name = matches[0], matches[1]

        # Get the eco_name using 'eco_123' or 'eco[EUR]'
        # Then use the eco_name to get the eco_folder_id
        try:
            if eco_name.startswith("eco_"):
                eco_name = query(data, f"$..*['{eco_name}'].name")[0]
            else:
                eco_name = query(data, f"$..*[@.name is '{eco_name}'].name")[0]

            eco_folder_id = query(data, f"$..*[@.name is '{eco_name}'].folder_id")[0]
        except (ValueError, IndexError) as e:
            raise RuntimeError("Unable to get eco_folder_id")

        # Get the driver_data using 'driver_123' or 'driver[IR]'
        try:
            if driver_name.startswith("driver_"):
                driver_data = query(data, f"$..*['{driver_name}']")[0]
            else:
                driver_data = query(data, f"$..*[@.name is '{driver_name}']")[0]
            driver_name = driver_data.get("class", driver_data.get("subclass", None))
        except (ValueError, IndexError) as e:
            raise RuntimeError(f"Exception occurred while getting driver_name from data")

        # TODO: Check how to get driver_folder_id correctly
        driver_folder_id = MODEL_DIR_NAMES.get(driver_name, None)
        if driver_folder_id is None:
            raise RuntimeError(f"Unable to find driver_folder_id for driver_name: {driver_name}")

        # Get the local path of the input file
        local_filepath = "/".join([eco_folder_id, driver_folder_id, filename])

    else:
        # Remove the $.framework.sensi_1 and .filename from the expression
        expression = expression.replace(".filename", "").replace("$.framework.sensi_1.", "")

        # Use the KEY_FOLDER_MAPPING and construct the local path of the input file
        folder_name = PARAM_KEYS_FOLDERS_MAPPING.get(expression, None)
        if folder_name is None:
            raise RuntimeError(f"The key from the expression provided is not recognized")

        local_filepath = "/".join([folder_name, filename])

    # Get the framework name, sensi_1 folder id
    try:
        framework_name = query(data, "$.framework.name")[0]
        input_folder = framework_name + "_inputs"
        folder_name = query(data, "$.framework.sensi_1.name")[0]
    except (ValueError, IndexError) as e:
        raise RuntimeError("Unable to get framework.name or framework.sensi_1.name from data")

    # Get the full path of the input file
    global_filepath = os.path.join(env_dir, "resources", folder_name, input_folder, local_filepath).replace("\\", "/")
    if not os.path.exists(global_filepath):
        try:
            folder_id = query(data, "$.framework.sensi_1.folder_id")[0]
        except (ValueError, IndexError) as e:
            raise RuntimeError("Unable to get framework.sensi_1.folder_id from data")
        global_filepath = os.path.join(env_dir, "resources", folder_id, input_folder, local_filepath).replace("\\", "/")
        if not os.path.exists(global_filepath):
            raise RuntimeError("Input file path does not exist")

    return global_filepath
