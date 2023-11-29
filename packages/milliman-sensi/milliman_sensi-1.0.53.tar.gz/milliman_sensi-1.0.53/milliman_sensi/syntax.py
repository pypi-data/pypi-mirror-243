import logging
import os
import re

import pandas as pd
from mpmath import mp

from milliman_sensi.utility import FILE_MARK

PRECISION = 13

mp.dps = PRECISION
mp.pretty = False

logger = logging.getLogger(__name__)


# Custom Exception class for sensi validation
class SensiSyntaxError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)

    def __str__(self):
        return self.msg


class Syntax:
    def __init__(self, expression="", col="", condition="", value=""):
        """Initialize a Syntax object

        Args:
            expression (str, optional): The expression to be evaluated.
            col (str, optional): The column name.
            condition (str, optional): The condition to be evaluated.
            value (str, optional): The value to be evaluated.
        """
        self.expression = expression
        self.col = col
        self.condition = condition
        self.value = value

    def __str__(self):
        return f"Syntax(expression={self.expression}, col={self.col}, condition={self.condition}, value={self.value})"


def extract_value_from_equal(param_string):
    """Extracts syntax and value from param_string if param_string contains =

    Args:
        param_string (str): string to be parsed

    Raises:
        SensiSyntaxError: if param_string does not contain =

    Returns:
        tuple: (syntax (str), value (str))
    """
    logger.info(f"Extracting value from {param_string}")

    if not "=" in param_string:
        logger.error(f'Incorrect syntax in param. Unable to find "=" in {param_string}')
        raise SensiSyntaxError('Incorrect syntax in param. Unable to find "="')

    logger.debug(f"Extracting syntax and value from {param_string}")
    equal_char_position = param_string.rindex("=")
    syntax = param_string[:equal_char_position].strip('"').strip()
    value = param_string[equal_char_position + 1 :].strip()

    logger.debug(f"Returned {syntax} and {value}.")
    return syntax, value


def extract_target_column(param_string):
    """Extracts column from param_string if param_string contains
    [ and ends with ]

    Args:
        param_string (str): string to be parsed

    Raises:
        SensiSyntaxError: if param_string does not contain [ and ends with ]

    Returns:
        tuple: (syntax (str), column (str))
    """
    logger.info(f"Extracting target column from {param_string}")
    param_string = param_string.strip('"').strip()

    if not "[" in param_string or not param_string.endswith("]"):
        logger.error(f'Incorrect syntax in param. Unable to find "[" or "]" in {param_string}')
        raise SensiSyntaxError('Incorrect syntax in param. Unable to find "[" or "]"')

    logger.debug(f"Extracting target column from {param_string}")
    right_quote_position = param_string.rindex("]")
    left_quote_position = param_string.rindex("[")
    syntax = param_string[:left_quote_position].strip('"').strip()
    column = param_string[left_quote_position + 1 : right_quote_position].strip()

    if column == "":
        logger.error(f"Incorrect input syntax. Column cannot be empty")
        raise SensiSyntaxError("Incorrect input syntax. Column cannot be empty")

    logger.debug(f"Returned {syntax} and {column}.")
    return syntax, column


def parse_param(input_syntax):
    """Parses input syntax and returns Syntax object

    Args:
        input_syntax (str): input syntax

    Raises:
        SensiSyntaxError: if input_syntax is invalid

    Returns:
        Syntax: Syntax object
    """
    logger.info(f"Parsing param: {input_syntax}")

    if not input_syntax:
        logger.error("Empty input_syntax parameter passed to the parse_param function.")
        raise SensiSyntaxError("Empty input_syntax in parse_param function")

    logger.debug(f"Extracting syntax and value from {input_syntax}")
    param_string, param_value = extract_value_from_equal(input_syntax)

    # Check if param_string contains FILE_MARK
    if not FILE_MARK in param_string:
        logger.debug(f"param_string does not contain {FILE_MARK}.")
        logger.debug(f"Returning Syntax object with expression: {param_string}, value: {param_value}")
        return Syntax(expression=param_string, value=param_value)

    logger.debug(f"Input syntax contains {FILE_MARK}.")

    # Remove FILE_MARK from param_string
    param_string = param_string.replace(FILE_MARK, "").strip()

    logger.debug(f"Checking if param_string contains condition")
    # Checks if '.where' exists in param_string
    if ".where" in param_string:
        logger.debug(f".where exists in param_string.")
        if param_string.count(".where") > 1:
            logger.error(f'Incorrect input_syntax. Multiple ".where" in {param_string}')
            raise SensiSyntaxError('Incorrect input_syntax. Multiple ".where"')
        param_expression, param_condition = param_string.split(".where")
    else:
        logger.debug(f".where does not exist in param_string.")
        param_expression, param_condition = param_string, ""

    # Gets the column in the param_expressions
    logger.debug(f"Extracting target column from {param_expression}")
    param_expression, param_col = extract_target_column(param_expression)

    if "eco" in param_expression and "driver" in param_expression:
        # Construct the query for input file extraction under eco and driver
        logger.debug(f"Extracting economy from {param_expression}")
        eco_pattern = ""
        if re.search(r"eco_\d+\.", param_expression):
            eco_pattern = r"eco_\d+\."
            eco = re.search(r"eco_\d+(?=\.)", param_expression).group()  # Gets the 123 from "eco_123."
        elif re.search(r"eco\[\w+?\]\.", param_expression):
            eco_pattern = r"eco\[\w+?\]\."
            eco = re.search(r"(?<=eco\[)\w+(?=\]\.)", param_expression).group()  # Gets the EUR from "eco[EUR]."
        else:
            raise SensiSyntaxError("Unable to find a valid eco in the expression")

        logger.debug(f"Extracting driver from {param_expression}")
        driver_pattern = ""
        if re.search(r"driver_\d+\.", param_expression):
            driver_pattern = r"driver_\d+\."
            driver = re.search(r"driver_\d+(?=\.)", param_expression).group()  # Gets the 123 from "driver_123."
        elif re.search(r"driver\[\w+?\]\.", param_expression):
            driver_pattern = r"driver\[\w+?\]\."
            driver = re.search(r"(?<=driver\[)\w+(?=\]\.)", param_expression).group()  # Gets the IR from "driver[IR]"
        else:
            raise SensiSyntaxError("Unable to find a valid driver in the expression")

        # Remove eco and driver from param_expression
        param_expression = re.sub(eco_pattern, "", param_expression)
        param_expression = re.sub(driver_pattern, "", param_expression)

        result = (
            "$"
            + (f"..*['{eco}']" if "eco" in eco else f"..*[@.name is '{eco}']")
            + (f"..*['{driver}']" if "driver" in driver else f"..*[@.name is '{driver}']")
            + f".{param_expression}.filename"
        )
    else:
        # Construct the query for input file extraction under sensi_1
        result = f"$.framework.sensi_1.{param_expression}.filename"
    logger.debug(f"Constructed query for input file extraction: {result}")

    logger.debug(
        f"Returning Syntax object with expression: {result}, value: {param_value}, "
        f"column: {param_col}, condition: {param_condition}"
    )
    return Syntax(result, param_col, param_condition, param_value)


def select_with_column_and_row(dataframe, column=None, row=None):
    """Selects a column and row from a dataframe

    Args:
        dataframe (pd.dataframe): dataframe to select from
        column (str, optional): column to select. Defaults to None.
        row (str, optional): row to select. Defaults to None.

    Raises:
        SensiSyntaxError: if any of the queries fail

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Selecting column: {column} and row: {row} from dataframe")

    if dataframe is None or dataframe.empty:
        return dataframe

    logger.debug(f"Selecting column: {column}")
    if column is not None:
        column = column.strip()
        if column == "":
            pass
        elif column.isdigit():
            column = int(column)
            if column < 1 or column > len(dataframe.columns):
                logger.error(f"Column index out of range: {column}")
                raise SensiSyntaxError(f"Column index out of range: {column}")
            dataframe = dataframe[[dataframe.columns[column - 1]]]
        elif column.startswith("'") and column.endswith("'"):
            column = column.strip("'")
            if column not in dataframe.columns:
                logger.error(f"Column not found: {column}")
                raise SensiSyntaxError(f"Column not found: {column}")
            dataframe = dataframe[[column]]
        elif column == "*":
            pass
        else:
            logger.error(f"Invalid column: {column}")
            raise SensiSyntaxError(f"Invalid column: {column}")

    if row is not None:
        row = row.strip()
        if row == "":
            pass
        elif row.isdigit():
            row = int(row)
            if row < 1 or row > len(dataframe):
                logger.error(f"Row index out of range: {row}")
                raise SensiSyntaxError(f"Row index out of range: {row}")
            dataframe = dataframe.iloc[[row - 1], :]
        elif row.startswith("'") and row.endswith("'"):
            row = row.strip("'")
            if row not in dataframe.index:
                logger.error(f"Row not found: {row}")
                raise SensiSyntaxError(f"Row not found: {row}")
            dataframe = dataframe.loc[[row]]
        elif row == "*":
            pass
        else:
            logger.error(f"Invalid row: {row}")
            raise SensiSyntaxError(f"Invalid row: {row}")

    return dataframe


def get_selection_from_dataframe(selection, dataframe):
    """Gets the selection from the dataframe

    Args:
        selection (str): selection to get
        dataframe (pd.dataframe): dataframe to get selection from

    Raises:
        SensiSyntaxError: if selection is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Getting selection from dataframe: {selection}")

    # Check if the dataframe is not empty
    if dataframe is None or dataframe.empty:
        return dataframe

    # Strip spaces and remove brackets from selection if present
    selection = selection.strip()
    if selection.startswith("[") and selection.endswith("]"):
        selection = selection[1:-1]

    logger.debug(f"Getting column and row from selection: {selection}")
    if selection.count(",") == 1:
        column, row = selection.split(",")
        column = column.strip()
        row = row.strip()
    else:
        column = selection.strip()
        row = None

    logger.debug(f"Getting column and row from dataframe: {column}, {row}")
    try:
        return select_with_column_and_row(dataframe, column, row)
    except SensiSyntaxError as e:
        logger.error(f"Unable to get selection from dataframe: {e}")
        raise SensiSyntaxError("Unable to get selection from dataframe")


def convert_value_to_true_type(value):
    """Parses the value for selection

    Args:
        value (str): value to parse

    Returns:
        int, float, str, bool, None: parsed value
    """
    logger.info(f"Parsing value for selection: {value}")

    real_value = None
    if value is None:
        logger.debug(f"Value is None")
        pass
    elif value.lower() in ["true", "false"]:
        logger.debug(f"Value is boolean")
        real_value = value.lower() == "true"
    else:
        try:
            logger.debug(f"Value is integer")
            real_value = int(value)
        except ValueError:
            try:
                logger.debug(f"Value is float")
                real_value = float(value)
            except ValueError:
                logger.debug(f"Value is string")
                real_value = value.strip("'")
    return real_value


def select_from_dataframe(condition, operation, dataframe):
    """Selects from the dataframe based on the condition and operation

    Args:
        condition (str): condition to select
        operation (str): operation to select
        dataframe (pd.dataframe): dataframe to select from

    Raises:
        SensiSyntaxError: if condition or operation is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Selecting from dataframe: {condition}, {operation}")

    try:
        lvalue, rvalue = condition.split(operation)
    except ValueError:
        logger.error(f"Invalid condition: {condition}")
        raise SensiSyntaxError("Condition must be in the form of 'lvalue operation rvalue'")
    logger.debug(f"Parsed condition: {lvalue}, {rvalue}")

    if lvalue is None or lvalue.strip() == "":
        logger.error(f"lvalue from condition is empty: {condition}")
        raise SensiSyntaxError("lvalue from condition is empty")
    lvalue = lvalue.strip()

    logger.debug(f"Getting selection from dataframe: {lvalue}")
    selected = get_selection_from_dataframe(lvalue, dataframe)

    if selected is not None and not selected.empty:
        logger.debug("Converting non empty selection to numeric")
        selected = selected.apply(pd.to_numeric, errors="ignore")

        if rvalue is None or rvalue.strip() == "":
            logger.error(f"rvalue from condition is empty: {condition}")
            raise SensiSyntaxError("rvalue from condition is empty")
        values = rvalue.strip().split(",")

        # Parse all elements in the list 'values' to their respective types
        values = [convert_value_to_true_type(value) for value in values]

        logger.debug("Using condition and values to select from dataframe")
        try:
            if operation == "==":
                dataframe = dataframe[selected.T.iloc[0].isin(values)]
            elif operation == "!=":
                dataframe = dataframe[~selected.T.iloc[0].isin(values)]
            elif operation == ">=":
                dataframe = dataframe[selected.T.iloc[0] >= values[0]]
            elif operation == ">":
                dataframe = dataframe[selected.T.iloc[0] > values[0]]
            elif operation == "<=":
                dataframe = dataframe[selected.T.iloc[0] <= values[0]]
            elif operation == "<":
                dataframe = dataframe[selected.T.iloc[0] < values[0]]
            else:
                logger.error(f"{operation} is unsupported by this tool.")
                raise SensiSyntaxError("{} is an unsupported Operation!".format(operation))
        except Exception as e:
            logger.error(f"Selection failed using {operation}: {e}")
            raise SensiSyntaxError(f"Failed to execute selection with {operation}")
    else:
        logger.warning(f"Selection from dataframe using condition {condition} is empty")
        dataframe = pd.DataFrame()

    return dataframe


def interpret_condition(condition, dataframe):
    """Interprets the condition and returns the selected dataframe

    Args:
        condition (str): condition to interpret
        dataframe (pandas.dataframe): dataframe to select from

    Raises:
        SensiSyntaxError: if condition is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Interpreting condition: {condition}")

    if condition.strip() and not dataframe.empty:
        condition = condition.strip()
        logger.debug(f"Choosing selection method using correct operator in condition")
        if condition.count("==") == 1:
            dataframe = select_from_dataframe(condition, "==", dataframe)
        elif condition.count("!=") == 1:
            dataframe = select_from_dataframe(condition, "!=", dataframe)
        elif condition.count(">=") == 1:
            dataframe = select_from_dataframe(condition, ">=", dataframe)
        elif condition.count(">") == 1:
            dataframe = select_from_dataframe(condition, ">", dataframe)
        elif condition.count("<=") == 1:
            dataframe = select_from_dataframe(condition, "<=", dataframe)
        elif condition.count("<") == 1:
            dataframe = select_from_dataframe(condition, "<", dataframe)
        else:
            logger.error(f"Incorrect condition '{condition}'.")
            raise SensiSyntaxError(f"'{condition}' is not a correct condition")

    return dataframe


def apply_value_to_selection(value, selected_dict):
    """Applies the value to the selected dataframe

    Args:
        value (str): value to apply
        selected_dict (dict): dictionary of selected data

    Raises:
        SensiSyntaxError: if value is invalid or unable to apply value to selection

    Returns:
        dict: dictionary of selected data with value applied
    """
    logger.info(f"Applying value to selection: {value}")

    applying_operation = False

    value = value.strip('"').replace(" ", "")
    if value.startswith("(") and value.endswith(")"):
        logger.debug(f"Operation {value} is inclosed in parentheses.")
        value = value.strip("()")
        applying_operation = True

    if value:
        if not applying_operation:
            if str(value).lower() in ["true", "false"]:
                value = value.lower() == "true"

            logger.debug(f"Replacing selection with value: {value}")
            for column in selected_dict.keys():
                selected_dict[column] = {k: value for k in selected_dict[column].keys()}
        else:
            logger.debug(f"Applying operation to selection")

            operation = ""
            if value[0] in ("+", "-", "*", "/"):
                operation, value = value[0], value[1:]
            try:
                value = mp.mpf(value.replace(",", "."))
                logger.debug(f"Converted value to {type(value)} .")
            except ValueError:
                logger.error(f"Invalid value: {value}")
                raise SensiSyntaxError(f"'{value}' is not a correct value")
            try:
                logger.debug(f"Applying operation: {operation}")
                # We use the mpmath module to execute operations with maximum of precision (currently 13)
                if operation == "+":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) + value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "-":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) - value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "*":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) * value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "/":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) / value, PRECISION) for k, v in selected_dict[column].items()
                        }
                else:
                    logger.debug("Applying a + as the default operation")
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) + value, PRECISION) for k, v in selected_dict[column].items()
                        }

            except Exception as exc:
                logger.error(
                    f"Failed to execute operation: {operation} between {selected_dict} and {value}: {str(exc)}"
                )
                raise SensiSyntaxError(
                    "Unable to execute operation '{}' between '{}' and '{}'".format(operation, selected_dict, value)
                )

    logger.debug(f"Returned dict:\n {selected_dict}")
    return selected_dict


def apply_syntax_to_file(input_path, syntax, settings_json):
    """Applies the syntax to the input file

    Args:
        input_path (str): path to the input file
        syntax (str): syntax to apply
        settings_json (dict): settings to use

    Raises:
        SensiSyntaxError: if failed to apply syntax to file

    Returns:
        boolean: True if syntax was applied successfully, False otherwise
    """
    logger.info(f"Applying syntax to file: {input_path}")

    try:
        if input_path is None:
            logger.error("No input file specified.")

        if syntax is None:
            logger.error("No syntax specified.")
            raise SensiSyntaxError("No syntax specified.")

        if syntax.col is None or syntax.col == "":
            logger.error("No column specified.")
            raise SensiSyntaxError("No column specified.")

        if syntax.value is None:
            logger.error("No value specified.")
            raise SensiSyntaxError("No value specified.")

        if settings_json is None:
            logger.error("No settings specified.")
            raise SensiSyntaxError("No settings specified.")

        logger.debug(f"Getting separators from settings.json:\n {settings_json}")
        seps = settings_json.get("gen_param").get("input_format")
        if seps is None:
            logger.error("No separators specified in settings.json.")
            raise SensiSyntaxError("No separators specified in settings.json.")
        try:
            dec_sep = seps["dec_sep"]
            col_sep = seps["col_sep"]
            logger.debug(f"Found dec_sep: {dec_sep} and col_sep: {col_sep}")
        except KeyError as e:
            logger.error(f"Missing separator in settings.json: {e}")
            raise SensiSyntaxError(f"Missing separator in settings.json: {e}")

        if not os.path.isfile(input_path):
            logger.error(f"Input file not found: {input_path}")
            raise SensiSyntaxError(f"Input file not found: {input_path}")

        logger.debug(f"Reading input file: {input_path}")
        # convert all columns to string to avoid losing leading zeros
        # (uses converters because dtype=str does not work)
        # then, check if first cell is empty, if so, set index to first column
        input_df = pd.read_csv(input_path, sep=col_sep, header=None, converters={i: str for i in range(100)})
        first_cell = input_df.iloc[0, 0]
        input_df.columns = input_df.iloc[0]
        input_df.drop(0, inplace=True)
        if first_cell == "":
            input_df.set_index(input_df.columns[0], inplace=True)

        # Select from dataframe using conditions inside .where("...")
        df_selected_with_condition = input_df.copy()
        if syntax.condition:
            logger.debug(f"Selecting from dataframe: {syntax.condition}")
            condition = syntax.condition.strip("()")
            or_conditions = condition.split("||")
            logger.debug(f"Applying conditions separated by ||: {or_conditions}")
            df_indexes_list_or = []
            for or_cond in or_conditions:
                logger.debug(f"Applying {or_cond}")
                if or_cond.strip():
                    and_conditions = or_cond.split("&&")
                    logger.debug(f"Applying conditions separated by &&: {and_conditions}")
                    df_indexes_list_and = []
                    for and_cond in and_conditions:
                        logger.debug(f"\tApplying {and_cond}")
                        selected_df = interpret_condition(and_cond, input_df)
                        df_indexes_list_and.append(set(selected_df.index))

                        logger.debug(f"Appended result of and_condition to the list.")

                    df_common_indexes = set.intersection(*df_indexes_list_and)
                    df_indexes_list_or.append(df_common_indexes)
                    logger.debug(f"Appended result of or_condition to the list.")

            df_total_indexes = set().union(*df_indexes_list_or)
            df_selected_with_condition = input_df.iloc[list(df_total_indexes)]

        # Select from dataframe using columns
        dict_selected_with_col = {}
        logger.debug(f"Selecting data using {syntax.col} .")
        try:
            selected_df = get_selection_from_dataframe(syntax.col, df_selected_with_condition)
        except SensiSyntaxError as err:
            logger.error(f"{err.msg} in file {input_path}")
            raise err

        selected_dict = selected_df.to_dict()  # {"Nom_column": {"Index de ligne": "valeur associé"}}
        logger.debug(f"Converted selected_df to dict:\n {selected_dict}")

        try:
            dict_selected_with_col = apply_value_to_selection(syntax.value, selected_dict)
        except SensiSyntaxError as err:
            logger.error(f"{err.msg} in file {input_path}")
            raise err

        for column, indexes in dict_selected_with_col.items():
            for index in indexes:
                logger.debug(f"Replacing value at [{index},{column}] with {indexes[index]}")
                input_df.loc[index, column] = indexes[index]

        logger.debug(f"Dataframe types are:\n {input_df.dtypes}")
        os.remove(input_path)
        if first_cell == "":
            # reset index back to first column
            input_df.reset_index(inplace=True)
        input_df.to_csv(input_path, sep=col_sep, index=False, float_format="%.18g")
        logger.debug(f"Saved to {input_path}:\n" + "\t" + input_df.to_string().replace("\n", "\n\t"))
        return True

    except Exception as exc:
        logger.error(f"Failed to apply syntax to file: {input_path}: {exc}")
        return False
