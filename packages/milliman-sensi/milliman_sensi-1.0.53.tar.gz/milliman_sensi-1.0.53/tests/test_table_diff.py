import inspect
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import milliman_sensi.table_diff as table_diff

TEST_DIR = os.path.join(
    os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/"), "data", "table_diff"
).replace("\\", "/")


def convert_dataframe_column_types(df):
    """Converts first column and last two columns to object and the rest to string"""
    df.iloc[:, 0] = df.iloc[:, 0].astype("object")
    df.iloc[:, -2:] = df.iloc[:, -2:].astype("object")
    df.iloc[:, 1:-2] = df.iloc[:, 1:-2].astype("str")
    return df


def test_load_settings(settings_table_1):
    table_path = os.path.join(TEST_DIR, "table_1")

    tableHandler = table_diff.TableHandler(table_path)

    assert tableHandler.settings == settings_table_1


############################################################################################################


def test_load_table(settings_table_1):
    table_path = os.path.join(TEST_DIR, "table_1")

    tableHandler = table_diff.TableHandler(table_path)

    assert tableHandler.settings == settings_table_1

    assert tableHandler.data == {"data_1.csv": os.path.join(table_path, "resources", "data_1.csv")}


def test_load_table_empty_folder():
    table_path = os.path.join(TEST_DIR, "table_empty")

    tableHandler = table_diff.TableHandler(table_path)

    assert tableHandler.settings == {}
    assert tableHandler.data == {}


def test_load_data():
    table_path = os.path.join(TEST_DIR, "table_1")

    tableHandler = table_diff.TableHandler(table_path)

    assert tableHandler.data == {"data_1.csv": os.path.join(table_path, "resources", "data_1.csv")}


def test_load_data_with_subfolders():
    table_path = os.path.join(TEST_DIR, "table_2")

    tableHandler = table_diff.TableHandler(table_path)

    assert tableHandler.data == {
        "data_1.csv": os.path.join(table_path, "resources", "eco", "data_1.csv"),
        "data_2.csv": os.path.join(table_path, "resources", "eco", "data_2.csv"),
        "data_3.csv": os.path.join(table_path, "resources", "eco", "driver", "data_3.csv"),
    }


############################################################################################################


def test_filter_diff():
    diff = {
        "dictionary_item_added": {
            "root['gen_param']['input_format']['row_sep']": ",",
            "root['framework']['sensi_1']['param']['seed']": 789123,
        },
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "values_changed": {
            "root['gen_param']['name']": {"new_value": "test_2", "old_value": "test_1"},
            "root['gen_param']['path']": {"new_value": "/path/to/test_2", "old_value": "/path/to/test_1"},
            "root['framework']['sensi_1']['name']": {"new_value": "test_2", "old_value": "test_1"},
            "root['framework']['sensi_1']['folder_id']": {"new_value": "746573745F32", "old_value": "746573745F31"},
            "root['framework']['sensi_1']['param']['t0']": {"new_value": "2020/01/01", "old_value": "31/12/2019"},
        },
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list'][2]": 3},
    }

    fields_to_exclude = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
    ]

    expected_result = {
        "dictionary_item_added": {
            "root['gen_param']['input_format']['row_sep']": ",",
            "root['framework']['sensi_1']['param']['seed']": 789123,
        },
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "values_changed": {
            "root['framework']['sensi_1']['param']['t0']": {"new_value": "2020/01/01", "old_value": "31/12/2019"},
        },
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list'][2]": 3},
    }

    tableDiff = table_diff.TableDiff()
    result = tableDiff._filter_diff(diff, fields_to_exclude)

    assert result == expected_result


############################################################################################################


def test_merge_iterable_changes():
    diff = {
        "dictionary_item_added": {"root['gen_param']['input_format']['row_sep']": ","},
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "type_changes": {
            "root['framework']['sensi_1']['param']['n_s']": {
                "old_type": "<class 'int'>",
                "new_type": "<class 'str'>",
                "old_value": 1000,
                "new_value": "1000",
            }
        },
        "iterable_item_added": {
            "root['framework']['sensi_1']['param']['example_list'][2]": 3,
            "root['framework']['sensi_1']['param']['example_list'][3]": 4,
        },
    }

    expected_result = {
        "dictionary_item_added": {"root['gen_param']['input_format']['row_sep']": ","},
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "type_changes": {
            "root['framework']['sensi_1']['param']['n_s']": {
                "old_type": "<class 'int'>",
                "new_type": "<class 'str'>",
                "old_value": 1000,
                "new_value": "1000",
            }
        },
        "iterable_item_added": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3, "3": 4}},
    }

    tableDiff = table_diff.TableDiff()
    result = tableDiff._merge_iterable_changes(diff)

    assert result == expected_result


def test_merge_iterable_changes_items_added():
    diff = {
        "iterable_item_added": {
            "root['framework']['sensi_1']['param']['example_list'][2]": 3,
            "root['framework']['sensi_1']['param']['example_list'][3]": 4,
        }
    }

    expected_result = {
        "iterable_item_added": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3, "3": 4}}
    }

    tableDiff = table_diff.TableDiff()
    result = tableDiff._merge_iterable_changes(diff)

    assert result == expected_result


def test_merge_iterable_changes_items_removed():
    diff = {
        "iterable_item_removed": {
            "root['framework']['sensi_1']['param']['example_list'][2]": 3,
            "root['framework']['sensi_1']['param']['example_list'][3]": 4,
        }
    }

    expected_result = {
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3, "3": 4}}
    }

    tableDiff = table_diff.TableDiff()
    result = tableDiff._merge_iterable_changes(diff)

    assert result == expected_result


def test_merge_iterable_changes_no_items():
    diff = {}

    expected_result = {}

    tableDiff = table_diff.TableDiff()
    result = tableDiff._merge_iterable_changes(diff)

    assert result == expected_result


############################################################################################################


def test_compare_settings_files_in_table_diff():
    table_1 = table_diff.TableHandler(os.path.join(TEST_DIR, "table_1"))
    table_2 = table_diff.TableHandler(os.path.join(TEST_DIR, "table_2"))

    expected_result_without_type_changes = {
        "dictionary_item_added": {
            "root['gen_param']['input_format']['row_sep']": ",",
            "root['framework']['sensi_1']['param']['seed']": 789123,
        },
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "values_changed": {
            "root['framework']['sensi_1']['param']['t0']": {"new_value": "2020/01/01", "old_value": "31/12/2019"},
        },
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3}},
    }
    expected_keys_in_type_changes = ["root['framework']['sensi_1']['param']['n_s']"]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._compare_settings_files(table_1, table_2)
    # Pop the type_changes key as it contains
    # the type of the values which cannot be printed
    type_changes = result.pop("type_changes")

    assert result == expected_result_without_type_changes
    assert list(type_changes.keys()) == expected_keys_in_type_changes


def test_compare_settings_files_with_identical_settings():
    table_1 = table_diff.TableHandler(os.path.join(TEST_DIR, "table_1"))
    expected_result = {}

    tableDiff = table_diff.TableDiff()
    result = tableDiff._compare_settings_files(table_1, table_1)

    assert result == expected_result


def test_compare_settings_files_with_csv_files():
    table_1_with_csv = table_diff.TableHandler(os.path.join(TEST_DIR, "table_with_csv_1"))
    table_2_with_csv = table_diff.TableHandler(os.path.join(TEST_DIR, "table_with_csv_2"))

    expected_result_without_type_changes = {
        "values_changed": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": {
                "new_value": "Format_1.csv",
                "old_value": "Format_1",
            },
            "root['framework']['sensi_1']['param']['report']['mt']['weights']['filename']": {
                "new_value": "mt_weights_2.csv",
                "old_value": "mt_weights.csv",
            },
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['thresholds']['filename']": {
                "new_value": "sw_thresholds.txt",
                "old_value": "sw_thresholds.csv",
            },
            "root['framework']['sensi_1']['param']['report']['eco_1']['name']": {
                "new_value": "test_2",
                "old_value": "test_1",
            },
        },
        "csv_hash_mismatch": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": "Format_1 hash: FILE_NOT_FOUND => Format_1.csv hash: 63e031d105854601bf203ff7ba3eb3bba6eb9c50b9111a1480fc3e6fd7db376d",
            "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['weights']['filename']": "fx_weights.csv hash: FILE_NOT_FOUND => None hash: FILE_NOT_FOUND",
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['weights']['filename']": "sw_weights.csv hash: 8c2436be81ce8ff8b99948cfbf0852ee66779c1653134789eaffd580ced23a3a => sw_weights.csv hash: 34326c430da8553b121b4aec086d5a8e6a76e507c567c49ae38a0a2d510991bb",
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['thresholds']['filename']": "sw_thresholds.csv hash: 3bda6812fe714e221083c14b8d2623f1cf311b45315a2ea3bba2fde93837e53d => sw_thresholds.txt hash: 8fa30649357a41e7eff23e41e65e37f84156feb00c251341e16e357abce30996",
            "root['framework']['sensi_1']['param']['report']['eco_1']['driver_1']['data']['filename']": "driver_data.csv hash: FILE_NOT_FOUND => driver_data.csv hash: FILE_NOT_FOUND",
        },
    }
    expected_keys_in_type_changes = [
        "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['weights']['filename']",
        "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['weights']['resources_folder']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._compare_settings_files(table_1_with_csv, table_2_with_csv)
    # Pop the type_changes key as it contains
    # the type of the values which cannot be printed
    type_changes = result.pop("type_changes")

    assert result == expected_result_without_type_changes
    assert list(type_changes.keys()) == expected_keys_in_type_changes


############################################################################################################


def test_extract_paths_from_settings(settings_table_1):
    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._extract_paths_from_settings(settings_table_1)

    assert result == expected_result


def test_extract_paths_from_settings_with_empty_settings():
    settings_data = {}

    expected_result = []

    tableDiff = table_diff.TableDiff()
    result = tableDiff._extract_paths_from_settings(settings_data)

    assert result == expected_result


def test_extract_paths_from_settings_with_list_of_dicts():
    settings_data = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
            "input_format": {
                "dec_sep": ",",
            },
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "t0": "2020/01/01",
                    "n_s": "1000",
                    "M": 30,
                    "H": 40,
                    "example_list": [2, 4],
                    "seed": 789123,
                },
                "reports": [
                    {"name": "report_1", "type": "pdf"},
                ],
            }
        },
    }

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['example_list']",
        "root['framework']['sensi_1']['param']['seed']",
        "root['framework']['sensi_1']['reports']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._extract_paths_from_settings(settings_data)

    assert result == expected_result


def test_extract_paths_from_settings_with_dict_of_lists():
    settings_data = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
            "input_format": {
                "dec_sep": ",",
            },
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "t0": "2020/01/01",
                    "n_s": "1000",
                    "M": 30,
                    "H": 40,
                    "example_list": [2, 4],
                    "seed": 789123,
                },
                "mappings": {
                    "1": ["a", "b"],
                    "2": ["c", "d"],
                },
            }
        },
    }

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['example_list']",
        "root['framework']['sensi_1']['param']['seed']",
        "root['framework']['sensi_1']['mappings']['1']",
        "root['framework']['sensi_1']['mappings']['2']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._extract_paths_from_settings(settings_data)

    assert result == expected_result


def test_extract_paths_from_settings_with_eco_and_driver():
    settings_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {
                        "name": "driver_1",
                        "folder_id": "746573745F33",
                    },
                    "driver_2": {
                        "name": "driver_2",
                        "folder_id": "746573745F34",
                    },
                },
            }
        },
    }

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['name']",
        "root['framework']['sensi_1']['eco_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['folder_id']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._extract_paths_from_settings(settings_data)

    assert result == expected_result


############################################################################################################


def test_get_merged_paths_of_settings():
    settings_1_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {
                        "name": "driver_1",
                        "folder_id": "746573745F33",
                    },
                    "driver_2": {
                        "name": "driver_2",
                        "folder_id": "746573745F34",
                    },
                },
            }
        },
    }

    settings_2_data = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {"name": "driver_1", "folder_id": "746573745F33"},
                },
                "eco_2": {
                    "name": "eco_2",
                    "folder_id": "746573745F35",
                    "driver_1": {"name": "driver_2", "folder_id": "746573745F34"},
                },
            }
        },
    }

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['name']",
        "root['framework']['sensi_1']['eco_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['folder_id']",
        "root['framework']['sensi_1']['eco_2']['name']",
        "root['framework']['sensi_1']['eco_2']['folder_id']",
        "root['framework']['sensi_1']['eco_2']['driver_1']['name']",
        "root['framework']['sensi_1']['eco_2']['driver_1']['folder_id']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_merged_paths_of_settings(settings_1_data, settings_2_data)

    assert result == expected_result


def test_get_merged_paths_of_settings_with_empty_settings():
    settings_1_data = {}
    settings_2_data = {}

    expected_result = ["root"]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_merged_paths_of_settings(settings_1_data, settings_2_data)

    assert result == expected_result


def test_get_merged_paths_of_settings_with_identical_settings(settings_table_1):
    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_merged_paths_of_settings(settings_table_1, settings_table_1)

    assert result == expected_result


def test_get_merged_paths_of_settings_with_irregular_settings():
    settings_1_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {
                        "name": "driver_1",
                        "folder_id": "746573745F33",
                    },
                    "driver_3": {
                        "name": "driver_3",
                        "folder_id": "746573745F35",
                    },
                },
            }
        },
    }

    settings_2_data = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_2": {"name": "driver_2", "folder_id": "746573745F34"},
                },
            }
        },
    }

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['name']",
        "root['framework']['sensi_1']['eco_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_1']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_3']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_3']['folder_id']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['name']",
        "root['framework']['sensi_1']['eco_1']['driver_2']['folder_id']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_merged_paths_of_settings(settings_1_data, settings_2_data)

    assert result == expected_result


############################################################################################################


def test_filter_paths():
    paths = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    field_filters = ["folder_id", "name"]

    expected_result = [
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._filter_paths(paths, field_filters)

    assert result == expected_result


def test_filter_paths_with_empty_field_filters():
    paths = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    field_filters = []

    expected_result = [
        "root['gen_param']['name']",
        "root['gen_param']['path']",
        "root['gen_param']['input_format']['dec_sep']",
        "root['gen_param']['input_format']['col_sep']",
        "root['framework']['sensi_1']['name']",
        "root['framework']['sensi_1']['folder_id']",
        "root['framework']['sensi_1']['param']['t0']",
        "root['framework']['sensi_1']['param']['n_s']",
        "root['framework']['sensi_1']['param']['H']",
        "root['framework']['sensi_1']['param']['M']",
        "root['framework']['sensi_1']['param']['example_list']",
    ]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._filter_paths(paths, field_filters)

    assert result == expected_result


############################################################################################################


def test_get_value_from_path(settings_table_1):
    # gen_param
    path = "root['gen_param']['name']"
    expected_result = "test_1"

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result

    # param
    path = "root['framework']['sensi_1']['param']['t0']"
    expected_result = "31/12/2019"

    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_list(settings_table_1):
    # list
    path = "root['framework']['sensi_1']['param']['example_list']"
    expected_result = [1, 2, 3]

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_dict(settings_table_1):
    # dict
    path = "root['gen_param']['input_format']"
    expected_result = {"dec_sep": ".", "col_sep": ";"}

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_non_existing_data():
    # Not existing data
    settings_data = {}

    path = "root['gen_param']['name']"
    expected_result = None

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_data, path)

    assert result == expected_result


def test_get_value_from_path_with_non_existing_path(settings_table_1):
    # Not existing path
    path = "root['framework']['sensi_1']['param']['report']['mt']['asset_shares']['resources_folder']"
    expected_result = None

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_empty_path(settings_table_1):
    # Empty path
    path = ""
    expected_result = settings_table_1

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_missing_brackets(settings_table_1):
    # Path with missing brackets
    path = "root['gen_param'['name"
    expected_result = None

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_with_double_quotes(settings_table_1):
    # Path with double quotes
    path = 'root["gen_param"]["name"]'
    expected_result = "test_1"

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


def test_get_value_from_path_not_starting_with_root(settings_table_1):
    # Path not starting with root
    path = "['gen_param']['name']"
    expected_result = "test_1"

    tableDiff = table_diff.TableDiff()
    result = tableDiff._get_value_from_path(settings_table_1, path)

    assert result == expected_result


############################################################################################################


def test_interpret_diff(settings_table_1, settings_table_2):
    diff = {
        "dictionary_item_added": {"root['gen_param']['input_format']['row_sep']": ","},
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "type_changes": {
            "root['framework']['sensi_1']['param']['n_s']": {
                "old_type": "<class 'int'>",
                "new_type": "<class 'str'>",
                "old_value": 1000,
                "new_value": "1000",
            }
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [None, None, None],
                "Name": ["gen_param.input_format.col_sep", "gen_param.input_format.row_sep", "param.n_s"],
                "test_1/test_1": [";", None, 1000],
                "test_2/test_2": [None, ",", "1000"],
            }
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_table_1, settings_table_2, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_iterable_item_removed(settings_table_1, settings_table_2):
    diff = {
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3}},
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {"Type": [None], "Name": ["param.example_list"], "test_1/test_1": [[1, 2, 3]], "test_2/test_2": [[1, 2]]}
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_table_1, settings_table_2, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_iterable_item_added(settings_table_1, settings_table_2):
    diff = {
        "iterable_item_added": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3}},
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {"Type": [None], "Name": ["param.example_list"], "test_2/test_2": [[1, 2]], "test_1/test_1": [[1, 2, 3]]}
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_table_2, settings_table_1, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_empty_diff(settings_table_1):
    diff = {}

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(columns=["Type", "Name", "test_1/test_1", "test_1/test_1"])
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_table_1, settings_table_1, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_list_of_dicts_in_settings():
    settings_base_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "reports": [
                    {"name": "report_1", "type": "pdf"},
                    {"name": "report_2", "type": "pdf"},
                ],
            }
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "reports": [
                    {"name": "report_1", "type": "pdf2"},
                ],
            }
        },
    }

    diff = {
        "values_changed": {
            "root['framework']['sensi_1']['reports'][0]": {
                "new_value": {"name": "report_1", "type": "pdf2"},
                "old_value": {"name": "report_1", "type": "pdf"},
            },
        },
        "iterable_item_removed": {
            "root['framework']['sensi_1']['reports']": {"1": {"name": "report_2", "type": "pdf"}},
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [None],
                "Name": ["reports"],
                "test_1/test_1": [[{"name": "report_1", "type": "pdf"}, {"name": "report_2", "type": "pdf"}]],
                "test_2/test_1": [[{"name": "report_1", "type": "pdf2"}]],
            }
        )
    )
    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_dict_of_lists_in_settings():
    settings_base_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "mappings": {
                    "1": ["a", "b"],
                    "2": ["c", "d"],
                },
            }
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "mappings": {
                    "1": ["a", "b"],
                },
            }
        },
    }

    diff = {
        "dictionary_item_removed": {
            "root['framework']['sensi_1']['mappings']['2']": ["c", "d"],
        }
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame({"Type": [None], "Name": ["mappings.2"], "test_1/test_1": [["c", "d"]], "test_2/test_1": [None]})
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_eco_and_driver_in_settings():
    settings_base_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_1",
                    }
                },
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {
                        "name": "driver_1",
                        "folder_id": "746573745F33",
                    },
                    "driver_2": {
                        "name": "driver_2",
                        "folder_id": "746573745F34",
                    },
                },
            }
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_2",
                    }
                },
                "eco_1": {
                    "name": "eco_1",
                    "folder_id": "746573745F32",
                    "driver_1": {"name": "driver_1", "folder_id": "746573745F33"},
                },
                "eco_2": {
                    "name": "eco_2",
                    "folder_id": "746573745F35",
                    "driver_1": {"name": "driver_2", "folder_id": "746573745F34"},
                },
            }
        },
    }

    diff = {
        "dictionary_item_added": {
            "root['framework']['sensi_1']['eco_2']": {
                "name": "eco_2",
                "folder_id": "746573745F35",
                "driver_1": {"name": "driver_2", "folder_id": "746573745F34"},
            }
        },
        "dictionary_item_removed": {
            "root['framework']['sensi_1']['eco_1']['driver_2']": {"name": "driver_2", "folder_id": "746573745F34"}
        },
        "values_changed": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": {
                "new_value": "Format_2",
                "old_value": "Format_1",
            },
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [None, None, None, None],
                "Name": [
                    "param.table_format.filename",
                    "eco_1.driver_2.name",
                    "eco_2.name",
                    "eco_2.driver_1.name",
                ],
                "test_1/test_1": ["Format_1", "driver_2", None, None],
                "test_2/test_1": ["Format_2", None, "eco_2", "driver_2"],
            }
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_without_gen_param_name():
    settings_base_data = {
        "gen_param": {
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_1",
                    }
                },
            }
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_2",
                    }
                },
            }
        },
    }

    diff = {
        "values_changed": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": {
                "new_value": "Format_2",
                "old_value": "Format_1",
            },
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {"Type": [None], "Name": ["param.table_format.filename"], "Base": ["Format_1"], "Other": ["Format_2"]}
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_filename():
    settings_base_data = {
        "gen_param": {
            "path": "/path/to/test_1",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_1",
                    }
                },
            }
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
        },
        "framework": {
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "table_format": {
                        "filename": "Format_2",
                    }
                },
            }
        },
    }

    diff = {
        "values_changed": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": {
                "new_value": "Format_2",
                "old_value": "Format_1",
            },
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {"Type": [None], "Name": ["param.table_format.filename"], "Base": ["Format_1"], "Other": ["Format_2"]}
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


def test_interpret_diff_with_csv_hash_comparison():
    settings_base_data = {
        "gen_param": {
            "name": "test_1",
            "path": "/path/to/test_1",
            "input_format": {"dec_sep": ".", "col_sep": ";"},
        },
        "framework": {
            "name": "RN",
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "t0": "31/12/2019",
                    "n_s": 1000,
                    "H": 40,
                    "M": 30,
                    "table_format": {"filename": "Format_1"},
                    "report": {
                        "mt": {
                            "asset_shares": {
                                "filename": "mt_asset_shares.csv",
                                "resources_folder": "resources",
                            },
                            "weights": {
                                "filename": "mt_weights.csv",
                                "resources_folder": "resources",
                            },
                        },
                        "mc": {
                            "fx_options": {
                                "weights": {
                                    "filename": "fx_weights.csv",
                                    "resources_folder": "resources",
                                },
                                "thresholds": {"filename": None, "resources_folder": None},
                            },
                            "swaptions": {
                                "weights": {
                                    "filename": "sw_weights.csv",
                                    "resources_folder": "resources",
                                },
                                "thresholds": {
                                    "filename": "sw_thresholds.csv",
                                    "resources_folder": "resources",
                                },
                            },
                        },
                        "eco_1": {
                            "name": "test_1",
                            "folder_id": "746573745F31",
                            "driver_1": {
                                "name": "IR",
                                "folder_id": "746573745F31",
                                "data": {
                                    "filename": "driver_data.csv",
                                    "resources_folder": "resources",
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    settings_base_other = {
        "gen_param": {
            "name": "test_2",
            "path": "/path/to/test_2",
            "input_format": {"dec_sep": ".", "col_sep": ";"},
        },
        "framework": {
            "name": "RN",
            "sensi_1": {
                "name": "test_1",
                "folder_id": "746573745F31",
                "param": {
                    "t0": "31/12/2019",
                    "n_s": 1000,
                    "H": 40,
                    "M": 30,
                    "table_format": {"filename": "Format_1.csv"},
                    "report": {
                        "mt": {
                            "asset_shares": {
                                "filename": "mt_asset_shares.csv",
                                "resources_folder": "resources",
                            },
                            "weights": {
                                "filename": "mt_weights_2.csv",
                                "resources_folder": "resources",
                            },
                        },
                        "mc": {
                            "fx_options": {
                                "weights": {"filename": None, "resources_folder": None},
                                "thresholds": {"filename": None, "resources_folder": None},
                            },
                            "swaptions": {
                                "weights": {
                                    "filename": "sw_weights.csv",
                                    "resources_folder": "resources",
                                },
                                "thresholds": {
                                    "filename": "sw_thresholds.txt",
                                    "resources_folder": "resources",
                                },
                            },
                        },
                        "eco_1": {
                            "name": "test_2",
                            "folder_id": "746573745F31",
                            "driver_1": {
                                "name": "IR",
                                "folder_id": "746573745F31",
                                "data": {
                                    "filename": "driver_data.csv",
                                    "resources_folder": "resources",
                                },
                            },
                        },
                    },
                },
            },
        },
    }

    # old_type and new_type are removed from type_changes because they can't
    # be properly printed
    diff = {
        "type_changes": {
            "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['weights']['filename']": {
                "old_value": "fx_weights.csv",
                "new_value": None,
            },
            "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['weights']['resources_folder']": {
                "old_value": "resources",
                "new_value": None,
            },
        },
        "values_changed": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": {
                "new_value": "Format_1.csv",
                "old_value": "Format_1",
            },
            "root['framework']['sensi_1']['param']['report']['mt']['weights']['filename']": {
                "new_value": "mt_weights_2.csv",
                "old_value": "mt_weights.csv",
            },
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['thresholds']['filename']": {
                "new_value": "sw_thresholds.txt",
                "old_value": "sw_thresholds.csv",
            },
            "root['framework']['sensi_1']['param']['report']['eco_1']['name']": {
                "new_value": "test_2",
                "old_value": "test_1",
            },
        },
        "csv_hash_mismatch": {
            "root['framework']['sensi_1']['param']['table_format']['filename']": "Format_1 hash: FILE_NOT_FOUND => Format_1.csv hash: 63e031d105854601bf203ff7ba3eb3bba6eb9c50b9111a1480fc3e6fd7db376d",
            "root['framework']['sensi_1']['param']['report']['mc']['fx_options']['thresholds']['filename']": "None hash: FILE_NOT_FOUND => None hash: FILE_NOT_FOUND",
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['weights']['filename']": "sw_weights.csv hash: 8c2436be81ce8ff8b99948cfbf0852ee66779c1653134789eaffd580ced23a3a => sw_weights.csv hash: 34326c430da8553b121b4aec086d5a8e6a76e507c567c49ae38a0a2d510991bb",
            "root['framework']['sensi_1']['param']['report']['mc']['swaptions']['thresholds']['filename']": "sw_thresholds.csv hash: 3bda6812fe714e221083c14b8d2623f1cf311b45315a2ea3bba2fde93837e53d => sw_thresholds.txt hash: 8fa30649357a41e7eff23e41e65e37f84156feb00c251341e16e357abce30996",
            "root['framework']['sensi_1']['param']['report']['eco_1']['driver_1']['data']['filename']": "driver_data.csv hash: FILE_NOT_FOUND => driver_data.csv hash: FILE_NOT_FOUND",
        },
    }

    expected_df = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [
                    None,
                    "file::",
                    None,
                    None,
                    None,
                    None,
                    "file::",
                    None,
                    "file::",
                    None,
                    "file::",
                    None,
                    None,
                    "file::",
                ],
                "Name": [
                    "param.table_format.filename",
                    "param.table_format",
                    "param.report.mt.weights.filename",
                    "param.report.mc.fx_options.weights.filename",
                    "param.report.mc.fx_options.weights.resources_folder",
                    "param.report.mc.fx_options.thresholds.filename",
                    "param.report.mc.fx_options.thresholds",
                    "param.report.mc.swaptions.weights.filename",
                    "param.report.mc.swaptions.weights",
                    "param.report.mc.swaptions.thresholds.filename",
                    "param.report.mc.swaptions.thresholds",
                    "param.report.eco_1.name",
                    "param.report.eco_1.driver_1.data.filename",
                    "param.report.eco_1.driver_1.data",
                ],
                "test_1/test_1": [
                    "Format_1",
                    "FILE_NOT_FOUND",
                    "mt_weights.csv",
                    "fx_weights.csv",
                    "resources",
                    None,
                    "FILE_NOT_FOUND",
                    "sw_weights.csv",
                    "8c2436be81ce8ff8b99948cfbf0852ee66779c1653134789eaffd580ced23a3a",
                    "sw_thresholds.csv",
                    "3bda6812fe714e221083c14b8d2623f1cf311b45315a2ea3bba2fde93837e53d",
                    "test_1",
                    "driver_data.csv",
                    "FILE_NOT_FOUND",
                ],
                "test_2/test_1": [
                    "Format_1.csv",
                    "63e031d105854601bf203ff7ba3eb3bba6eb9c50b9111a1480fc3e6fd7db376d",
                    "mt_weights_2.csv",
                    None,
                    None,
                    None,
                    "FILE_NOT_FOUND",
                    "sw_weights.csv",
                    "34326c430da8553b121b4aec086d5a8e6a76e507c567c49ae38a0a2d510991bb",
                    "sw_thresholds.txt",
                    "8fa30649357a41e7eff23e41e65e37f84156feb00c251341e16e357abce30996",
                    "test_2",
                    "driver_data.csv",
                    "FILE_NOT_FOUND",
                ],
            }
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff._interpret_diff(settings_base_data, settings_base_other, diff)

    pd.testing.assert_frame_equal(result, expected_df)


############################################################################################################


def test_compare_two_tables():
    table_1_path = os.path.join(TEST_DIR, "table_1")
    table_2_path = os.path.join(TEST_DIR, "table_2")

    compare_result = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [None, None, None, None, None, None],
                "Name": [
                    "gen_param.input_format.col_sep",
                    "gen_param.input_format.row_sep",
                    "param.t0",
                    "param.n_s",
                    "param.example_list",
                    "param.seed",
                ],
                "test_1/test_1": [";", None, "31/12/2019", 1000, [1, 2, 3], None],
                "test_2/test_2": [None, ",", "2020/01/01", "1000", [1, 2], 789123],
            }
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff.compare(table_1_path, table_2_path)

    pd.testing.assert_frame_equal(result, compare_result)


def test_compare_two_tables_with_identical_tables():
    table_path = os.path.join(TEST_DIR, "table_1")

    compare_result = convert_dataframe_column_types(
        pd.DataFrame(columns=["Type", "Name", "test_1/test_1", "test_1/test_1"])
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff.compare(table_path, table_path)

    pd.testing.assert_frame_equal(result, compare_result)


def test_compare_two_tables_with_inexisting_table():
    table_1_path = os.path.join(TEST_DIR, "table_1")
    table_2_path = os.path.join(TEST_DIR, "table_3")

    compare_result = None

    tableDiff = table_diff.TableDiff()
    result = tableDiff.compare(table_1_path, table_2_path)

    assert result == compare_result


def test_compare_two_tables_without_csv_hash_comparison():
    table_1_path = os.path.join(TEST_DIR, "table_1")
    table_2_path = os.path.join(TEST_DIR, "table_2")

    compare_result = convert_dataframe_column_types(
        pd.DataFrame(
            {
                "Type": [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ],
                "Name": [
                    "gen_param.input_format.col_sep",
                    "gen_param.input_format.row_sep",
                    "param.t0",
                    "param.n_s",
                    "param.example_list",
                    "param.seed",
                ],
                "test_1/test_1": [";", None, "31/12/2019", 1000, [1, 2, 3], None],
                "test_2/test_2": [None, ",", "2020/01/01", "1000", [1, 2], 789123],
            }
        )
    )

    tableDiff = table_diff.TableDiff()
    result = tableDiff.compare(table_1_path, table_2_path, compare_csv_files=False)

    pd.testing.assert_frame_equal(result, compare_result)


def test_compare_two_tables_without_interpret_diff():
    table_1_path = os.path.join(TEST_DIR, "table_1")
    table_2_path = os.path.join(TEST_DIR, "table_2")

    compare_result = {
        "dictionary_item_added": {
            "root['gen_param']['input_format']['row_sep']": ",",
            "root['framework']['sensi_1']['param']['seed']": 789123,
        },
        "dictionary_item_removed": {"root['gen_param']['input_format']['col_sep']": ";"},
        "values_changed": {
            "root['framework']['sensi_1']['param']['t0']": {"new_value": "2020/01/01", "old_value": "31/12/2019"}
        },
        "iterable_item_removed": {"root['framework']['sensi_1']['param']['example_list']": {"2": 3}},
    }
    expected_keys_in_type_changes = ["root['framework']['sensi_1']['param']['n_s']"]

    tableDiff = table_diff.TableDiff()
    result = tableDiff.compare(table_1_path, table_2_path, interpret_diff=False)
    type_changes = result.pop("type_changes")

    assert result == compare_result
    assert all(key in expected_keys_in_type_changes for key in type_changes.keys())
