import json
import logging
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

import milliman_sensi.syntax as syn
import milliman_sensi.utility as util

pd.options.mode.chained_assignment = None  # Used to suppress panda warning
SENSI_CONFIG_HEADER = ["Scenario", "Stress name", "Apply stress"]

logger = logging.getLogger(__name__)


def setup_syntax_logger(handler, level=None):
    """Sets up the syntax logger

    Args:
        handler (StreamHandler): The handler to use for the syntax logger
        level (int, optional): The level to log at. Defaults to None.
    """
    syn.logger.addHandler(handler)

    # To prevent setting the logger level multiple times
    if level:
        syn.logger.setLevel(level)


# Custom Exception class for sensi validation and modification
class SensiIOError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)

    def __str__(self):
        return self.msg


def sensi_config_is_valid(sensi_config):
    """Checks if the sensi config is valid

    Args:
        sensi_config (dataframe): The sensi config as a dataframe

    Raises:
        SensiIOError: If the sensi config is not a dataframe,
        if the header is not correct, if the number of columns is not correct
        or a value in 'Apply stress' is incorrect
    """
    logger.info(f"Validating sensi config")

    # Check if the sensi config is a dataframe
    if not isinstance(sensi_config, pd.DataFrame):
        logger.error(f"Sensi config is not a dataframe")
        raise SensiIOError(
            "Sensitivity configuration file cannot be validated. Please check the file is a valid csv file."
        )

    # Checking if the sensi config has the correct header
    logger.debug(f"Checking sensi config header")
    sensi_config_header = sensi_config.iloc[0].drop("_count_sep").dropna().values.tolist()
    if sensi_config_header != SENSI_CONFIG_HEADER:
        logger.error("Sensi config header is incorrect. " f"Expected {SENSI_CONFIG_HEADER}, got {sensi_config_header}")
        raise SensiIOError(
            "Sensitivity configuration file header is incorrect. "
            f"Expected {SENSI_CONFIG_HEADER}, got {sensi_config_header}"
        )

    # Checking if the sensi config has the correct number
    # of columns using the '_count_sep' column
    logger.debug(f"Checking sensi config number of columns")
    if not (sensi_config["_count_sep"] == len(SENSI_CONFIG_HEADER) - 1).all():
        rows_with_wrong_number_of_columns = sensi_config[
            sensi_config["_count_sep"] != len(SENSI_CONFIG_HEADER) - 1
        ].index.tolist()[1:]
        logger.error(
            "Sensi config has the wrong number of columns. "
            f"Rows with wrong number of columns: {rows_with_wrong_number_of_columns}"
        )
        raise SensiIOError(
            "Sensitivity configuration file has the wrong number of columns. "
            f"Rows with wrong number of columns: {rows_with_wrong_number_of_columns}"
        )

    # Checking if the 'Apply stress' column has the correct values
    logger.debug(f'Checking sensi config values in "Apply stress"')
    apply_stress_values = sensi_config.iloc[1:, SENSI_CONFIG_HEADER.index("Apply stress")]
    apply_stress_values_check = apply_stress_values.map(lambda x: isinstance(x, bool) or x.lower() in ["true", "false"])
    if not apply_stress_values_check.all():
        rows_with_wrong_apply_stress_values = apply_stress_values[~apply_stress_values_check].index.tolist()
        logger.error(
            "Sensi config has the wrong values in 'Apply stress'. "
            f"Rows with wrong values: {rows_with_wrong_apply_stress_values}"
        )
        raise SensiIOError(
            "Sensitivity configuration file has the wrong values in 'Apply stress'. "
            f"Rows with wrong values: {rows_with_wrong_apply_stress_values}"
        )


def validate_sensi_config(filepath):
    """Validates the sensi config file

    Args:
        filepath (str): Path to the sensi config file

    Returns:
        dict: The sensi config file as a dict
    """
    logger.info(f"Validating sensi config file {filepath}")

    # Read the sensi config file as a dataframe
    logger.debug(f"Reading sensi config file {filepath}")
    try:
        sensi_config = util.read_csv_from_filepath(filepath)
    except (FileNotFoundError, ValueError) as exc:
        # return the error message as a string
        logger.error(f"Error reading sensi config file {filepath}: {exc}")
        return str(exc)

    # Validate the sensi config file
    logger.debug(f"Validating sensi config file {filepath}")
    try:
        sensi_config_is_valid(sensi_config)
    except SensiIOError as exc:
        # return the error message as a string
        logger.error(f"Error validating sensi config file {filepath}: {exc}")
        return str(exc)

    # Drop the '_count_sep' column and use the first row as the header
    sensi_config = sensi_config.drop(columns="_count_sep")
    sensi_config.columns = sensi_config.iloc[0]
    sensi_config = sensi_config[1:]
    sensi_config.reset_index(drop=True, inplace=True)

    logger.debug(f"Returned sensi config: {sensi_config}")
    return sensi_config


def sensi_param_is_valid(sensi_param):
    """Validates the sensi param file

    Args:
        sensi_param (dataframe): The sensi param as a dataframe

    Raises:
        SensiIOError: If the sensi param is not a dataframe,
        if the first column is not the 'Name' column
        or if the sensi param has the wrong number of columns
    """
    logger.info(f"Validating sensi param")

    if not isinstance(sensi_param, pd.DataFrame):
        logger.error(f"Sensi param is not a dataframe")
        raise SensiIOError("Sensi param is not a dataframe")

    # Checking if the first column in the first row is the 'Name' column
    logger.debug(f"Checking sensi param first column")
    if not sensi_param.iloc[0, 0] == "Name":
        logger.error(f'Sensi param first column is not the "Name" column')
        raise SensiIOError('Sensitivity parameters file first column is not the "Name" column')

    # Checking if the sensi param has the correct number
    # of columns using the '_count_sep' column
    logger.debug(f"Checking sensi param number of columns")
    if not sensi_param["_count_sep"].nunique() == 1:
        # Get the rows with the wrong number of columns excluding the header
        rows_with_wrong_number_of_columns = sensi_param[
            sensi_param["_count_sep"] != sensi_param["_count_sep"].nunique()
        ].index.tolist()[1:]
        logger.error(
            "Sensi param has the wrong number of columns. "
            f"Rows with wrong number of columns: {rows_with_wrong_number_of_columns}"
        )
        raise SensiIOError(
            "Sensitivities parameters file has the wrong number of columns. "
            f"Rows with wrong number of columns: {rows_with_wrong_number_of_columns}"
        )


def validate_sensi_param(filepath):
    """Validates the sensi param file

    Args:
        filepath (str): Path to the sensi param file

    Returns:
        dict: The sensi param file as a dict
    """
    logger.info(f"Validating sensi param file {filepath}")

    # Read the sensi param file as a dataframe
    logger.debug(f"Reading sensi param file {filepath}")
    try:
        sensi_param = util.read_csv_from_filepath(filepath)
    except (FileNotFoundError, ValueError) as exc:
        # return the error message as a string
        return str(exc)

    # Validate the sensi param file
    logger.debug(f"Validating sensi param file {filepath}")
    try:
        sensi_param_is_valid(sensi_param)
    except SensiIOError as exc:
        # return the error message as a string
        return str(exc)

    # Drop the '_count_sep' column and use the first row as the header
    sensi_param = sensi_param.drop(columns="_count_sep")
    sensi_param.columns = sensi_param.iloc[0]
    sensi_param = sensi_param[1:]
    sensi_param.reset_index(drop=True, inplace=True)

    logger.debug(f"Returned sensi param: {sensi_param}")
    return sensi_param


def get_sensi_and_param_lists(sensi_config, sensi_param):
    """Gets the sensi and param lists
    from the sensi config and sensi param files

    Args:
        sensi_config (dataframe): The sensi config file as a dataframe
        sensi_param (dataframe): The sensi param file as a dataframe

    Raises:
        SensiIOError: If the sensi config and sensi param files
        do not have the same number of rows

    Returns:
        tuple: (sensi_list(dict), sensi_list_without_stress (list),
        param_list(dict))
    """
    logger.info(f"Getting sensi and param lists")

    logger.debug(f"Checking if sensi config and sensi param are valid")
    # Check if the values in the 'Stress name' column are a subset of
    # the columns in the sensi param file except the 'Name' column
    if not set(sensi_config["Stress name"]).issubset(set(sensi_param.columns.tolist()[1:])):
        # Get the values in the 'Stress name' column that are not a subset
        # of the columns in the sensi param file except the 'Name' column
        sensi_config_stress_names_not_in_sensi_param = set(sensi_config["Stress name"]) - set(
            sensi_param.columns.tolist()[1:]
        )
        logger.error(
            "Stress names in the sensi config file are not a subset of the stress names in the sensi param file. "
            f"Stress names not in the sensi param file: {sensi_config_stress_names_not_in_sensi_param}"
        )
        raise SensiIOError(
            "Stress names in the Sensitivity configuration file are not a subset "
            "of the stress names in the Sensitivity parameters file. Stress names "
            f"not in the Sensitivity parameters file: {sensi_config_stress_names_not_in_sensi_param}"
        )

    # Get the list sensi_list
    logger.debug(f"Getting sensi list")
    sensi_names = sensi_config["Scenario"].unique().tolist()
    sensi_list = {sensi_name: [] for sensi_name in sensi_names}
    for sensi_name in sensi_names:
        logger.debug(f"Adding the sensi {sensi_name} to the sensi list")
        # Get the dict of 'Stress name' for the sensi_name with 'Apply stress' as value
        stress_dict = (
            sensi_config[sensi_config["Scenario"] == sensi_name].set_index("Stress name")["Apply stress"].to_dict()
        )
        # Add keys from stress dict to sensi list if the value is True or 'true' (case insensitive)
        sensi_list[sensi_name] = [
            stress_name for stress_name, apply_stress in stress_dict.items() if apply_stress.lower() == "true"
        ]

    # Get the list sensi_list_without_stress
    logger.debug(f"Getting sensi list without stress")
    sensi_list_without_stress = [sensi_name for sensi_name, stress_list in sensi_list.items() if not stress_list]

    # Get the list param_list
    logger.debug(f"Getting unsorted param list")
    stress_names = list(sensi_param.columns)[1:]
    param_map_unsorted = {}
    for stress_name in stress_names:
        logger.debug(f"Adding the stress {stress_name} to the unsorted param list")
        # Select the rows where parameters are not null for the stress_name
        stress_df = sensi_param[sensi_param[stress_name] != ""]
        # Concatenate the stress name to the parameters
        stress_df = stress_df[["Name", stress_name]]
        stress_df[stress_name] = stress_df["Name"] + "=" + stress_df[stress_name].astype(str)
        # Add the stress name to the param map unsorted
        param_map_unsorted[stress_name] = stress_df.to_dict("list")[stress_name]

    # Get the list param_map
    logger.debug(f"Getting param map")
    # Sort the param map unsorted by the order of the stress names in the 'Stress name' column
    # of the sensi config file where 'Apply stress' is True or 'true' (case insensitive)
    param_map = {
        stress_name: param_map_unsorted[stress_name]
        for stress_name in sensi_config[sensi_config["Apply stress"].str.lower() == "true"]["Stress name"].tolist()
    }

    return sensi_list, sensi_list_without_stress, param_map


def read_sensitivities(env_dir):
    """Reads the sensitivities files

    Args:
        env_dir (str): Path to the environment directory

    Raises:
        SensiIOError: If either the sensi config
        or sensi param file is not valid

    Returns:
        tuple: (sensi_list(dict), sensi_list_without_stress (list),
        param_list(dict))
    """

    # 1. Read Sensi_config.csv & Sensi_param.csv in the /sensitivities directory (throw error if column does not match)
    # 2. Sanitary check for columns in both csv files
    # 3. Return two dict: sensi_list, param_map
    #    sensi_list: Name_in_config -> [List_of_Stress_in_config_in_order]
    #      eg: "Sensi_1" -> ["Stress_vol_1", "Stress_eq_vol_1"]
    #    param_map: Stress_in_param -> [List_of_Parameters_syntax_in_param]
    #      eg: "Stress_vol_1" -> ["param.H=(+100)","file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]=(+100)"]

    logger.info(f"Reading sensitivities from {env_dir}")

    # Read sensi_config.csv and validate using validate_sensi_config
    logger.debug(f"Reading sensi_config.csv")
    result = validate_sensi_config(util.find_file_in_directory("Sensi_config.csv", env_dir))
    if isinstance(result, str):
        logger.error(result)
        raise SensiIOError(result)
    sensi_config = result

    # Read sensi_param.csv and validate using validate_sensi_param
    logger.debug(f"Reading sensi_param.csv")
    result = validate_sensi_param(util.find_file_in_directory("Sensi_param.csv", env_dir))
    if isinstance(result, str):
        logger.error(result)
        raise SensiIOError(result)
    sensi_param = result

    # Construct sensi_list, sensi_list_without_stress and param_list
    logger.debug(f"Constructing sensi list, sensi list without stress and param list")
    sensi_list, sensi_list_without_stress, param_map = get_sensi_and_param_lists(sensi_config, sensi_param)

    return sensi_list, sensi_list_without_stress, param_map


def create_dir_for_one_sensi_from_base(sensi_name, sensi_path, base_dir):
    """Creates a directory for one sensitivity from the base directory

    Args:
        sensi_path (str): Path to the sensitivity directory
        base_dir (str): Path to the base directory

    Returns:
        (str or SensiIOError): Path to the sensitivity directory if successful, SensiIOError if not
    """
    logger.info(f"Creating directory for one sensitivity from base directory {base_dir}")
    sensi_path = sensi_path.replace("\\", "/")
    base_dir = base_dir.replace("\\", "/")

    logger.info(f"Creating directory {sensi_path} from base directory {base_dir}")

    # Check if the base directory exists
    if not os.path.exists(base_dir):
        logger.error(f"Base directory {base_dir} does not exist")
        return SensiIOError(f"Base directory does not exist")

    # Delete the sensi directory if it exists
    if os.path.exists(sensi_path):
        logger.debug(f"Deleting directory {sensi_path}")
        shutil.rmtree(sensi_path)

    # Copy 'resources' and 'resources_admin' from base directory to sensi directory
    logger.debug(f"Copying resources and resources_admin from base directory to sensi directory")
    try:
        sensi_rsrc_dir = os.path.join(sensi_path, "resources").replace("\\", "/")
        sensi_rsrc_admin_dir = os.path.join(sensi_path, "resources_admin").replace("\\", "/")
        base_rsrc_dir = os.path.join(base_dir, "resources").replace("\\", "/")
        base_rsrc_admin_dir = os.path.join(base_dir, "resources_admin").replace("\\", "/")

        if os.path.exists(sensi_rsrc_dir):
            shutil.rmtree(sensi_rsrc_dir)
        logger.info(f"Copying {base_rsrc_dir} to {sensi_rsrc_dir}")
        util.copy_dir(base_rsrc_dir, sensi_rsrc_dir)
        if os.path.exists(sensi_rsrc_admin_dir):
            shutil.rmtree(sensi_rsrc_admin_dir)
        logger.info(f"Copying {base_rsrc_admin_dir} to {sensi_rsrc_admin_dir}")
        util.copy_dir(base_rsrc_admin_dir, sensi_rsrc_admin_dir)
        logger.debug("Copy completed")

    except Exception as e:
        logger.error(f"Error copying resources and resources_admin from base directory to sensi directory: {e}")
        return SensiIOError(f"Error copying resources and resources_admin from base directory to sensi directory")

    # Delete 'settings_calibration.json' and 'settings_simulation.json' from sensi directory if they exist
    logger.debug(f"Deleting settings_calibration.json and settings_simulation.json from sensi directory if they exist")
    calib_settings_path = os.path.join(sensi_path, "resources", "settings_calibration.json").replace("\\", "/")
    sim_settings_path = os.path.join(sensi_path, "resources", "settings_simulation.json").replace("\\", "/")
    if os.path.exists(calib_settings_path):
        os.remove(calib_settings_path)
    if os.path.exists(sim_settings_path):
        os.remove(sim_settings_path)

    # Write values of the sensi to settings.json
    logger.debug(f"Writing values of the sensi to settings.json")
    try:
        settings_path = os.path.join(sensi_path, "resources", "settings.json").replace("\\", "/")
        settings_json = util.read_json_file(settings_path)
        settings_json["gen_param"]["name"] = "{}_{}".format(settings_json["gen_param"]["name"], sensi_name)
        settings_json["gen_param"]["path"] = sensi_path
        settings_json["framework"]["sensi_1"]["name"] = sensi_name
        # Save the settings.json file
        with open(settings_path, "w") as f:
            json.dump(settings_json, f, indent=4)
    except Exception as e:
        logger.error(f"Error writing values of the sensi to settings.json: {e}")
        return SensiIOError(f"Error writing values of the sensi to settings.json")

    return sensi_path


class SensiConfig:
    def __init__(self, env_dir):
        """The SensiConfig class

        Args:
            env_dir (str): The path to the environment directory

        Raises:
            SensiIOError: If the environment directory does not exist
        """
        logger.info(f"Creating SensiConfig object with env_dir: {env_dir}")
        if not os.path.exists(env_dir):
            logger.error(f"Failed to find Base table {env_dir}")
            raise SensiIOError("Base table {} does not exist".format(env_dir))

        self.base_dir = env_dir
        try:
            self.settings_json = util.read_json_file(f"{env_dir}/resources/settings.json")
            (
                self.sensi_list,
                self.sensi_list_without_any_stress,
                self.param_map,
            ) = read_sensitivities(self.base_dir)
        except Exception as e:
            logger.error(f"Error creating SensiConfig object: {e}")
            raise SensiIOError(f"Error creating SensiConfig object: {e}")

    def get_stress_desc(self, sensi_name):
        """Gets the stress description for a sensitivity

        Args:
            sensi_name (str): The name of the sensitivity

        Returns:
            str: The stress description
        """
        logger.info(f"Get stress description for sensi in {sensi_name}")
        param_list = self.sensi_list.get(sensi_name, [])
        return "".join([">>".join(self.param_map.get(p, [""])) for p in param_list])

    def create_tables(self, sensi_dirs={}):
        """Creates the sensitivity tables

        Args:
            sensi_dirs (dict, optional): The dictionary of sensitivity directories. Defaults to {}.

        Returns:
            dict: The dictionary of sensitivity directories processed or error messages
        """
        # For Seni_config.csv
        # To new create directory from the name of the Scenario
        # Copy env_dir to each directory of the name of the Scenario
        # Replace gen_param.name = name of the Scenario in the settings.json of the newly copied directory
        # Replace gen_param.path = newly created path
        # Input sensi_dirs can be provided by the API as dict { "<SENSI_NAME>":"<TABLE_ENV_PATH>" }
        # If sensi_dirs is provided, only the tables for the Sensi there are created
        # Else all the tables are created for every sensi in sensi_list
        # Dict that contains the list of sensi and their dirs
        logger.info(f"Creating sensitivity tables")

        processed_sensi_dirs = {}
        if len(self.sensi_list) <= 0:
            logger.info(f"No sensitivities found")
            return processed_sensi_dirs

        # Only create tables for the sensi in the sensi_dirs
        if len(sensi_dirs) > 0:
            logger.debug(f"Creating tables for sensi_dirs: {sensi_dirs}")
            for sensi in self.sensi_list.keys():
                # Checks that it is a sensi in the specified sensi lists (i.e. sensi_dirs)
                # or that there is at least one stress name to apply for it.
                if sensi in sensi_dirs.keys() and len(self.sensi_list[sensi]) > 0:
                    logger.debug(f"Creating table for sensi: {sensi}")
                    res = create_dir_for_one_sensi_from_base(sensi, sensi_dirs[sensi], self.base_dir)
                    processed_sensi_dirs[sensi] = res
        else:
            logger.debug(f"Creating tables for all sensi in sensi_list")
            path = Path(self.base_dir)
            parent_dir = path.parent
            for sensi in self.sensi_list.keys():
                if len(self.sensi_list[sensi]) > 0:
                    logger.debug(f"Creating table for sensi: {sensi}")
                    res = create_dir_for_one_sensi_from_base(sensi, os.path.join(parent_dir, sensi), self.base_dir)
                    processed_sensi_dirs[sensi] = res

        logger.info(f"Processed sensitivity directories: {processed_sensi_dirs.keys()}")
        return processed_sensi_dirs

    def _get_sensi_dirs_to_process(self, sensi_dirs={}):
        """Gets the sensitivity directories to process

        Args:
            sensi_dirs (dict): The dictionary of sensitivity directories

        Returns:
            dict: The dictionary of sensitivity directories to process
        """
        logger.info(f"Getting sensitivity directories to process")

        sensi_dirs_to_process = {}

        if len(sensi_dirs) > 0:
            logger.debug(f"Applying sensitivities to sensi_dirs: {sensi_dirs}")
            for sensi in self.sensi_list.keys():
                if sensi in sensi_dirs.keys():
                    logger.debug(f"Applying sensitivities to sensi: {sensi}")
                    sensi_dirs_to_process[sensi] = sensi_dirs[sensi].replace("\\", "/")
        else:
            logger.debug(f"Applying sensitivities to all sensi in sensi_list")
            path = Path(self.base_dir)
            parent_dir = path.parent
            for sensi in self.sensi_list.keys():
                logger.debug(f"Applying sensitivities to sensi: {sensi}")
                sensi_dirs_to_process[sensi] = os.path.join(parent_dir, sensi).replace("\\", "/")

        return sensi_dirs_to_process

    def _apply_stress_to_sensi(self, sensi_name, sensi_dirpath):
        """Applies the stress to the sensitivity

        Args:
            sensi_name (str): The name of the sensitivity
            sensi_dirpath (str): The path to the sensitivity directory

        Returns:
            (str or SensiIOError): The result of applying the stress
            to the sensitivity or an error message
        """
        logger.info(f"Applying stress to sensi: {sensi_name}")

        message = ""
        settings_modif_express = list()
        settings_modif_values = list()
        total_applied = 0

        for stress_name in self.sensi_list[sensi_name]:
            logger.debug(f"Applying stress: {stress_name}")
            counter = 0
            for command in self.param_map[stress_name]:
                logger.debug(f"Applying command: {command}")

                # Parse the command
                try:
                    logger.debug(f"Parsing command: {command}")
                    syntax = syn.parse_param(command)
                except syn.SensiSyntaxError as e:
                    logger.error(f"Error parsing command: {command} for stress {stress_name}: {e}")
                    message = SensiIOError(f"Unable to parse command {command} for stress {stress_name}")
                    break

                # Apply the command
                logger.debug(f"Applying expression: {syntax.expression}")
                if syntax.expression.startswith("$"):
                    path_to_file = None
                    logger.debug(f"Getting input file path for command: {command}")
                    try:
                        path_to_file = util.get_input_file_path(self.settings_json, syntax.expression, sensi_dirpath)
                    except RuntimeError as e:
                        logger.error(f"Error getting file for command {command} for stress {stress_name}: {e}")
                        message = SensiIOError(f"Unable to get file for command {command} for stress {stress_name}")
                        break

                    try:
                        applied = syn.apply_syntax_to_file(path_to_file, syntax, self.settings_json)
                        if applied:
                            counter += 1
                            logger.debug(
                                f'Applied "{syntax.expression}" with col: "{syntax.col}", '
                                f'condition: "{syntax.condition}" and value: "{syntax.value}" '
                                f"on input file {path_to_file}"
                            )
                            message = 'Applied "{}" modification(s) on input files of {}'.format(counter, sensi_name)
                        else:
                            logger.error(f'Unable to apply "{syntax.expression}" on input file {path_to_file}')
                            message = SensiIOError(f"Failed to apply {sensi_name} stress on {Path(path_to_file).name}")
                            break
                    except syn.SensiSyntaxError as e:
                        logger.error(f"Unable to apply {syntax.expression} on {path_to_file}: {e}")
                        message = SensiIOError("Unable to apply {} on {}".format(sensi_name, Path(path_to_file).name))
                        break

                else:
                    try:
                        settings_path = os.path.join(sensi_dirpath, "resources", "settings.json").replace("\\", "/")
                        settings_json = util.read_json_file(settings_path)
                        logger.debug(f"Querying settings.json for {syntax.expression}")
                        try:
                            table_name = util.query(settings_json, "$.framework.sensi_1.name")[0]
                        except ValueError as e:
                            logger.error(f"Error querying settings.json for {syntax.expression}: {e}")
                            raise syn.SensiSyntaxError(f"Unable to query settings.json for {syntax.expression}")
                        expression = (
                            syntax.expression
                            if syntax.expression.startswith("framework") or syntax.expression.startswith("gen_param")
                            else "framework.sensi[{}].{}".format(table_name, syntax.expression)
                        )
                        settings_modif_express.append(expression)
                        settings_modif_values.append(syntax.value)
                        message = f"Added settings modification to settings_modif of {sensi_name}"
                    except syn.SensiSyntaxError:
                        message = SensiIOError(f"Unable to add {syntax.expression} to settings_modif of {sensi_name}")
                        logger.error(f"Unable to add {syntax.expression} to settings_modif of {sensi_name}")
                        break

            total_applied = total_applied + counter
            logger.debug(f"Applied {counter} commands for stress {stress_name} to sensi {sensi_name}")

        # Saving settings_modif commands to settings_modif.csv
        if len(settings_modif_express) > 0 and len(settings_modif_values) > 0:
            logger.debug(f"Saving settings_modif commands to settings_modif.csv")
            total_applied = total_applied + len(settings_modif_express)
            settings_modif_pd = pd.DataFrame({"id": settings_modif_express, "value": settings_modif_values})
            settings_modif_pd.to_csv(
                os.path.join(sensi_dirpath, "resources/settings_modif.csv"),
                sep=";",
                index=False,
            )

        if not isinstance(message, SensiIOError):
            message = "Applied {} modification(s) on {}".format(total_applied, sensi_name)

        return message

    def apply(self, sensi_dirs={}):
        """Applies the sensitivities to the tables

        Args:
            sensi_dirs (dict, optional): The dictionary of sensitivity
            directories. Defaults to {}.

        Returns:
            dict: The dictionary of sensitivity directories processed
        """

        # For Sensi_param.csv
        # Iterate over sensi_list and apply the stress in the param_map
        # When interate param_map:
        # Build the good correct path from the json query
        # Call syntax.apply_sentax_to_file(path, syntax) in the syntax.py
        # Input sensi_dirs can be provided by the API as dict { "<SENSI_NAME>":"<TABLE_ENV_PATH>" }
        # If sensi_dirs is provided, only Sensi in sensi_dirs are stress applied
        # Else all the sensis are stress applied
        # Dict that contains the list of sensi and their dirs

        logger.info(f"Applying sensitivities to tables")

        processed_sensi_messages = {}

        if len(self.sensi_list) <= 0 or len(self.param_map) <= 0:
            logger.error(f"Sensi list or param map is empty")
            return {}

        sensi_dirs_to_process = self._get_sensi_dirs_to_process(sensi_dirs)

        # Applying the stress to the sensi
        for sensi_name, sensi_dirpath in sensi_dirs_to_process.items():
            if not os.path.exists(sensi_dirpath):
                logger.error(f"Sensitivity directory does not exist: {sensi_dirpath}")
                processed_sensi_messages[sensi_name] = SensiIOError("Sensitivity path does not exist")
                continue

            if self.settings_json is None:
                logger.error(f"No settings_json found for {sensi_name}")
                processed_sensi_messages[sensi_name] = SensiIOError("No settings file found")
                continue

            # Applying the stress to the sensi
            logger.debug(f"Applying stress to sensi: {sensi_name}")
            processed_sensi_messages[sensi_name] = self._apply_stress_to_sensi(sensi_name, sensi_dirpath)

        return processed_sensi_messages
