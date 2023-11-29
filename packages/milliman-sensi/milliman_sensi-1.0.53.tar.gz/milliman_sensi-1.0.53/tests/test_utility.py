import inspect
import os
import shutil
import sys
import tempfile

import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import milliman_sensi.utility as su

TEST_DIR = os.path.join(
    os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/"), "data", "io"
).replace("\\", "/")


def test_read_json_successful():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    assert data is not None


def test_read_json_inexistent_file():
    with pytest.raises(FileNotFoundError):
        su.read_json_file("not_exists.json")


def test_read_json_invalid_file():
    with pytest.raises(ValueError):
        su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/invalid_settings.json")


############################################################################################################


def test_find_file_in_directory_successful():
    res = su.find_file_in_directory(
        "Sensi_config.csv",
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities",
    )
    assert res == f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config.csv"


def test_find_file_in_directory_with_file_inexistent():
    assert su.find_file_in_directory("inexistent_file.csv", ".") is None


def test_find_file_in_directory_with_target_dir_inexistent():
    assert su.find_file_in_directory("searched_file.csv", "inexistent_directory") is None


############################################################################################################


def test_read_csv_from_filepath_successful():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config.csv"
    assert isinstance(su.read_csv_from_filepath(sensi_config_input_csv), type(pd.DataFrame()))


def test_read_csv_from_filepath_with_inexistent_file():
    with pytest.raises(FileNotFoundError):
        su.read_csv_from_filepath("inexistent_file.csv")


def test_read_csv_from_filepath_with_non_allowed_extension():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_non_allowed_extension.txt"
    )
    with pytest.raises(ValueError):
        su.read_csv_from_filepath(csv_file_input)


def test_read_csv_from_filepath_with_file_containing_unallowed_characters():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_unallowed_characters.csv"
    )
    with pytest.raises(ValueError):
        su.read_csv_from_filepath(csv_file_input)


def test_read_csv_from_filepath_with_file_using_comma_as_delimiter():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_comma_as_delimiter.csv"
    )
    assert isinstance(su.read_csv_from_filepath(csv_file_input), type(pd.DataFrame()))


def test_read_csv_from_filepath_with_file_containing_semicolons_in_values():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_semicolons_in_values.csv"
    )
    res = su.read_csv_from_filepath(csv_file_input)
    assert res.iloc[1, 0] == "Sensi_1;"


############################################################################################################


def test_copy_dir_nested_files_and_subdirs():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir1 = os.path.join(base_rsrc_dir, "subdir1")
        temp_subdir2 = os.path.join(base_rsrc_dir, "subdir2")
        os.makedirs(temp_subdir1)
        os.makedirs(temp_subdir2)
        temp_file1 = os.path.join(base_rsrc_dir, "file1.txt")
        temp_file2 = os.path.join(temp_subdir1, "file2.txt")
        with open(temp_file1, "w") as f1, open(temp_file2, "w") as f2:
            f1.write("File 1 contents")
            f2.write("File 2 contents")

        su.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.exists(os.path.join(sensi_rsrc_dir, "file1.txt"))
        assert os.path.exists(os.path.join(sensi_rsrc_dir, "subdir1", "file2.txt"))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, "file1.txt"))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, "subdir1", "file2.txt"))
        assert os.path.isdir(os.path.join(sensi_rsrc_dir, "subdir2"))
    finally:
        shutil.rmtree(temp_dir)


@pytest.mark.skipif(sys.platform != "linux", reason="Symlinks only supported on Linux")
def test_copy_dir_symlink_point_to_dir():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(temp_subdir)
        temp_file = os.path.join(temp_subdir, "file1.txt")
        with open(temp_file, "w") as f:
            f.write("File 1 contents")

        temp_link = os.path.join(base_rsrc_dir, "symlink")
        os.symlink(temp_subdir, temp_link)

        su.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.exists(os.path.join(sensi_rsrc_dir, "symlink", "file1.txt"))

    finally:
        shutil.rmtree(temp_dir)


@pytest.mark.skipif(sys.platform != "linux", reason="Symlinks only supported on Linux")
def test_copy_dir_skip_dangling_symlink():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_link = os.path.join(base_rsrc_dir, "symlink")
        os.symlink("/path/to/nonexistent/target", temp_link)

        su.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert not os.path.exists(os.path.join(sensi_rsrc_dir, "symlink"))
    finally:
        shutil.rmtree(temp_dir)


def test_copy_dir_existing_destination():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_file = os.path.join(base_rsrc_dir, "file.txt")
        with open(temp_file, "w") as f:
            f.write("File contents")

        # Create an existing directory in the destination path
        os.makedirs(os.path.join(sensi_rsrc_dir, "existing_dir"))

        su.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.isdir(os.path.join(sensi_rsrc_dir, "existing_dir"))
        assert not os.path.isfile(os.path.join(sensi_rsrc_dir, "existing_dir", "file.txt"))
    finally:
        shutil.rmtree(temp_dir)


############################################################################################################


############################################################################################################


@pytest.fixture
def test_data():
    data = {
        "eco_1": {
            "name": "GBP",
            "driver_1": {
                "name": "IR",
                "data": {
                    "swaptions": {
                        "mkt": {
                            "filename": "file1.csv",
                            "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                        }
                    }
                },
            },
            "driver_2": {
                "name": "FX",
                "data": {
                    "swaptions": {
                        "mkt": {
                            "filename": "file2.csv",
                            "data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
                        }
                    }
                },
            },
        }
    }
    return data


def test_query_successful(test_data):
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    res = su.query(test_data, expression)
    assert res == ["file1.csv"]


def test_query_with_data_is_None():
    data = None
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    with pytest.raises(ValueError):
        su.query(data, expression)


def test_query_with_expression_is_None(test_data):
    expression = None
    with pytest.raises(ValueError):
        su.query(test_data, expression)


def test_query_expression_does_not_start_with_dollar_sign(test_data):
    expression = "..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    with pytest.raises(ValueError):
        su.query(test_data, expression)


def test_query_empty_result(test_data):
    expression = "$..*[@.name is 'GBP']..*[@.name is 'RI'].data.swaptions.mkt.filename"
    res = su.query(test_data, expression)
    assert res == []


def test_query_multiple_result(test_data):
    expression = "$..swaptions.mkt.filename"
    res = su.query(test_data, expression)
    assert res == ["file1.csv", "file2.csv"]


############################################################################################################


def test_get_input_file_path_successful():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Nominal_rates/GBP_Mkt_Swaptions_Vols.csv"
    )


def test_get_input_file_path_file_inexistent():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.option.tkm.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_with_wrong_field_in_expression():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.namefile"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_expression_without_eco():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*['driver_1'].data.swaptions.mkt.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_expression_has_inexistent_driver():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*['driver_100'].data.swaptions.mkt.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_inverted_order_of_driver_and_eco_in_expression():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'IR']..*['eco_1'].data.swaptions.mkt.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_driver_name_different_than_subclass():
    data = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    expression = "$..*[@.name is 'GBP']..*[@.name is 'EQ_1'].data.options.mkt.filename"
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Equity/FTSE100_Mkt_Implied_Vols.csv"
    )


def test_get_input_file_path_with_param_dependence():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.dependence.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Correlation/ESG_Correlation_Matrix.csv"
    )


def test_get_input_file_path_with_hist_corr_target_corr():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.hist_corr.target_corr.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Correlation/ESG_Target_Correlation_Matrix.csv"
    )


def test_get_input_file_path_with_param_table_format():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.table_format.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Formats/Format_BNP_2023_wMin.csv"
    )


def test_get_input_file_path_with_param_roll_forward_null_value():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.roll_forward.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_with_param_aom():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.aom.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Roll_Forward/AoM_23Q1_KVI_VA63.csv"
    )


def test_get_input_file_path_with_param_report_mt_weights():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mt.weights.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Report/MT_Weights.csv"
    )


def test_get_input_file_path_with_param_report_mt_asset_shares():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mt.asset_shares.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Report/Asset_Shares_Weights.csv"
    )


def test_get_input_file_path_with_param_report_mc_swaptions_weights():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.swaptions.weights.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Report/MC_Swaptions_Weights.csv"
    )


def test_get_input_file_path_with_param_report_mc_swaptions_thresholds():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.swaptions.thresholds.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Report/MC_Swaptions_Thresholds.csv"
    )


def test_get_input_file_path_with_param_report_mc_eq_re_options_weights():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.eq_re_options.weights.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    assert (
        su.get_input_file_path(data, expression, env_dir)
        == f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/Test_Param_File_Modif/RN_inputs/Report/MC_EQ_RE_Options_Weights.csv"
    )


def test_get_input_file_path_with_param_report_mc_eq_re_options_thresholds_null_value():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.eq_re_options.thresholds.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_with_param_report_mc_fx_options_weights_null_value():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.fx_options.weights.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)


def test_get_input_file_path_with_param_report_mc_fx_options_thresholds_null_value():
    data = su.read_json_file(
        f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539/resources/settings.json"
    )
    expression = "$.framework.sensi_1.param.report.mc.fx.options.thresholds.filename"
    env_dir = f"{TEST_DIR}/EIOPA_300623_Central_noVA_RN_Simulation_20230915_100539"
    with pytest.raises(RuntimeError):
        su.get_input_file_path(data, expression, env_dir)
