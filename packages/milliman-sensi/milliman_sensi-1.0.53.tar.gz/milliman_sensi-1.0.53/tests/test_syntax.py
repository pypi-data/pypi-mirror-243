import inspect
import os
import sys

import pandas as pd
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import milliman_sensi.syntax as syn
import milliman_sensi.utility as su

TEST_DIR = os.path.join(
    os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/"), "data", "syntax"
).replace("\\", "/")


def test_extract_value_from_equal_successful():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]=(+100)"
    res = syn.extract_value_from_equal(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]", "(+100)")


def test_extract_value_from_equal_without_equal():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1] (+100)"
    with pytest.raises(syn.SensiSyntaxError):
        syn.extract_value_from_equal(param_string)


def test_extract_value_from_equal_with_two_equals():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1].where('COL1'==0,10,20)=(+100)"

    res = syn.extract_value_from_equal(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt[*,1].where('COL1'==0,10,20)", "(+100)")


def test_extract_value_from_equal_with_leading_and_trailing_spaces():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[*,1] = (+100)"

    res = syn.extract_value_from_equal(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt[*,1]", "(+100)")


############################################################################################################


def test_extract_target_column_successful():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3]"
    res = syn.extract_target_column(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt", "3,3")


def test_extract_target_column_empty_column():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[]"
    with pytest.raises(syn.SensiSyntaxError):
        syn.extract_target_column(param_string)


def test_extract_target_column_missing_bracket():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3"
    with pytest.raises(syn.SensiSyntaxError):
        syn.extract_target_column(param_string)


def test_extract_target_column_multiple_brackets():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3][3]"
    res = syn.extract_target_column(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt[3,3]", "3")


def test_extract_target_column_leading_and_trailing_spaces():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[ 3,3 ] "

    res = syn.extract_target_column(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt", "3,3")


def test_extract_target_column_duplicate_closing_bracket():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3]]"
    res = syn.extract_target_column(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt", "3,3]")


def test_extract_target_column_multiple_column_brackets():
    param_string = "file::eco[GBP].driver[IR].data.swaptions.mkt[3,3,3]"
    res = syn.extract_target_column(param_string)
    assert res == ("file::eco[GBP].driver[IR].data.swaptions.mkt", "3,3,3")


############################################################################################################


def test_parse_param_successful():
    param_string = (
        """"file::eco[GBP].driver_1.data.swaptions.mkt['COL3'].where('COL1'==0,10,20 && 'COL2'>0 || 'COL4'<0)"=(+100)"""
    )
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*['driver_1'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3'"
    assert syntax.condition == "('COL1'==0,10,20 && 'COL2'>0 || 'COL4'<0)"
    assert syntax.value == "(+100)"


def test_parse_param_without_file_mark():
    param_string = "eco[GBP].driver[IR].data.swaptions.mkt['COL3']=500"
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "eco[GBP].driver[IR].data.swaptions.mkt['COL3']"
    assert syntax.col == ""
    assert syntax.condition == ""
    assert syntax.value == "500"


def test_parse_param_with_multiple_file_mark():
    param_string = "file::file::eco[GBP].driver[IR].data.swaptions.mkt['COL3']=500"
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3'"
    assert syntax.condition == ""
    assert syntax.value == "500"


def test_parse_param_without_where():
    param_string = """"file::eco[GBP].driver[IR].data.swaptions.mkt['ROW3','COL3']"=100"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    assert syntax.col == "'ROW3','COL3'"
    assert syntax.condition == ""
    assert syntax.value == "100"


def test_parse_param_with_an_empty_condition():
    param_string = """"file::eco[GBP].driver[IR].data.swaptions.mkt['COL3'].where()"=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3'"
    assert syntax.condition == "()"
    assert syntax.value == "(+100)"


def test_parse_param_with_multiple_conditions():
    param_string = """"file::eco[GBP].driver[IR].data.swaptions.mkt['COL3'].where('COL1'==0,10,20).where('COL2'>0 || 'COL4'<0)"=(+100)"""
    with pytest.raises(syn.SensiSyntaxError):
        syn.parse_param(param_string)


def test_parse_param_without_col():
    param_string = """"file::eco[GBP].driver[IR].data.swaptions.mkt"=(+100)"""

    with pytest.raises(syn.SensiSyntaxError):
        syn.parse_param(param_string)


def test_parse_param_eco_and_driver_without_brackets():
    param_string = """"file::eco_1.driver_1.data.swaptions.mkt['COL3', 1]"=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*['eco_1']..*['driver_1'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3', 1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_mixed_eco_and_driver_syntax():
    param_string = """"file::eco[GBP].driver_1.data.swaptions.mkt['COL3', 1]"=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*['driver_1'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3', 1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_eco_and_driver_inverted_with_brackets():
    param_string = """"file::driver[IR].eco[GBP].data.swaptions.mkt['COL3', 1]"=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3', 1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_eco_and_driver_inverted_without_brackets():
    param_string = """"file::driver_1.eco_1.data.swaptions.mkt['COL3', 1]"=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$..*['eco_1']..*['driver_1'].data.swaptions.mkt.filename"
    assert syntax.col == "'COL3', 1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_dependence_successful():
    param_string = """"file::param.dependence['EUR_IR_LMMP_FACTOR_1',2]=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$.framework.sensi_1.param.dependence.filename"
    assert syntax.col == "'EUR_IR_LMMP_FACTOR_1',2"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_table_format_successful():
    param_string = """"file::param.table_format['type',4]=spreads"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$.framework.sensi_1.param.table_format.filename"
    assert syntax.col == "'type',4"
    assert syntax.condition == ""
    assert syntax.value == "spreads"


def test_parse_param_aom_successful():
    param_string = """"file::param.aom['EUR_IR',1]=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$.framework.sensi_1.param.aom.filename"
    assert syntax.col == "'EUR_IR',1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


def test_parse_param_report_mt_weights_successful():
    param_string = """"file::param.report.mt.weights['EUR_ASSET_SHARE',1]=(+100)"""
    syntax = syn.parse_param(param_string)
    assert syntax.expression == "$.framework.sensi_1.param.report.mt.weights.filename"
    assert syntax.col == "'EUR_ASSET_SHARE',1"
    assert syntax.condition == ""
    assert syntax.value == "(+100)"


############################################################################################################


@pytest.fixture
def test_dataframe():
    dataframe = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50],
            "Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3],
            "Volatility": [
                0.002121,
                0.002833,
                0.003342,
                0.004941,
                0.005789,
                0.006,
                0.006529,
                0.005569,
                0.003737,
                0.004129,
            ],
            "Strike": [0, 0, 0, -0.02, 0.015, -0.005, 0.01, 0.01, 0.02, -0.02],
            "Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1],
            "p_y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        }
    )
    return dataframe


def test_get_selection_from_dataframe_successful(test_dataframe):
    selection = "[3, 3]"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Volatility": [0.003342]}).set_index([pd.Index([2])])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_thats_empty():
    selection = "[3, 3]"
    dataframe = pd.DataFrame()
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.empty


def test_get_selection_from_dataframe_with_selection_no_brackets(test_dataframe):
    selection = "3, 3"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Volatility": [0.003342]}).set_index([pd.Index([2])])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_with_selection_missing_bracket(test_dataframe):
    selection = "3, 3]"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_col_and_row_numbers(test_dataframe):
    selection = "[3,3]"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Volatility": [0.003342]}).set_index([pd.Index([2])])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_with_col_star_and_row_number(test_dataframe):
    selection = "[*, 1]"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {"Maturity": [1], "Tenor": [1], "Volatility": [0.002121], "Strike": [0.0], "Weigth": [1], "p_y": [1]}
    ).set_index([pd.Index([0])])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_with_col_number_row_star(test_dataframe):
    selection = "[1, *]"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Maturity": [1, 1, 2, 2, 20, 20, 25, 30, 50, 50]}).set_index([pd.Index(range(10))])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_with_col_name_existent(test_dataframe):
    selection = "['Weigth']"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Weigth": [1, 1, 0, 1, 1, 0, 0, 1, 0, 1]}).set_index([pd.Index(range(10))])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_with_col_name_inexistent(test_dataframe):
    selection = "['Height']"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_row_name(test_dataframe):
    selection = "['Tenor','ROW3']"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_high_col_number(test_dataframe):
    selection = "[1000]"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_with_negative_col(test_dataframe):
    selection = "[-2]"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


def test_get_selection_from_dataframe_missing_row(test_dataframe):
    selection = "['Tenor',]"
    dataframe = test_dataframe
    expected = pd.DataFrame({"Tenor": [1, 2, 3, 4, 5, 6, 7, 1, 2, 3]}).set_index([pd.Index(range(10))])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_missing_col(test_dataframe):
    selection = "[,1]"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {"Maturity": [1], "Tenor": [1], "Volatility": [0.002121], "Strike": [0.0], "Weigth": [1], "p_y": [1]}
    ).set_index([pd.Index([0])])
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_empty(test_dataframe):
    selection = "[]"
    dataframe = test_dataframe
    expected = dataframe
    res = syn.get_selection_from_dataframe(selection, dataframe)
    assert res.equals(expected)


def test_get_selection_from_dataframe_extra_field(test_dataframe):
    selection = "[1,2,3]"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.get_selection_from_dataframe(selection, dataframe)


############################################################################################################


def test_select_from_dataframe_successful(test_dataframe):
    condition = "'Maturity'==1"
    operation = "=="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    )
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_equal_multi_values(test_dataframe):
    condition = "'Maturity'==1,2"
    operation = "=="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 2],
            "Tenor": [1, 2, 3, 4],
            "Volatility": [0.002121, 0.002833, 0.003342, 0.004941],
            "Strike": [0, 0, 0, -0.02],
            "Weigth": [1, 1, 0, 1],
            "p_y": [1, 1, 1, 1],
        }
    )
    assert (
        pd.concat([syn.select_from_dataframe(condition, operation, dataframe), expected])
        .drop_duplicates(keep=False)
        .empty
    )


def test_select_from_dataframe_equal_no_right_value(test_dataframe):
    condition = "'Maturity'==,"
    operation = "=="
    dataframe = test_dataframe
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.empty


def test_select_from_dataframe_equal_no_left_value(test_dataframe):
    condition = "==1"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_equal_different_types(test_dataframe):
    condition = "'Maturity'=='Example'"
    operation = "=="
    dataframe = test_dataframe
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.empty


def test_select_from_dataframe_invalid_operation(test_dataframe):
    condition = "'Maturity'!!1"
    operation = "!!"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_missing_operation(test_dataframe):
    condition = "'Maturity'1"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_duplicated_operation(test_dataframe):
    condition = "'Maturity'==1==2"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_operation_not_in_condition(test_dataframe):
    condition = "'Maturity'!=1"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_right_value_not_number(test_dataframe):
    condition = "'Maturity'==Example"
    operation = "=="
    dataframe = test_dataframe
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.empty


def test_select_from_dataframe_right_value_empty(test_dataframe):
    condition = "''==1"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_missing_right_value(test_dataframe):
    condition = "'Maturity'=="
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_missing_left_value(test_dataframe):
    condition = "==1"
    operation = "=="
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.select_from_dataframe(condition, operation, dataframe)


def test_select_from_dataframe_equal_with_bools(test_dataframe):
    condition = "'Maturity'==TRUE"
    operation = "=="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    )
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_equal_with_floats(test_dataframe):
    condition = "'Maturity'==1.0"
    operation = "=="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    )
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_less_than(test_dataframe):
    condition = "'Tenor'<3"
    operation = "<"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 30, 50],
            "Tenor": [1, 2, 1, 2],
            "Volatility": [0.002121, 0.002833, 0.005569, 0.003737],
            "Strike": [0.0, 0.0, 0.01, 0.02],
            "Weigth": [1, 1, 1, 0],
            "p_y": [1, 1, 1, 1],
        }
    ).set_index([pd.Index([0, 1, 7, 8])])
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_less_than_equal(test_dataframe):
    condition = "'Tenor'<=3"
    operation = "<="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 30, 50, 50],
            "Tenor": [1, 2, 3, 1, 2, 3],
            "Volatility": [0.002121, 0.002833, 0.003342, 0.005569, 0.003737, 0.004129],
            "Strike": [0.0, 0.0, 0.0, 0.01, 0.02, -0.02],
            "Weigth": [1, 1, 0, 1, 0, 1],
            "p_y": [1, 1, 1, 1, 1, 1],
        }
    ).set_index([pd.Index([0, 1, 2, 7, 8, 9])])
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_greater_than(test_dataframe):
    condition = "'Tenor'>3"
    operation = ">"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [2, 20, 20, 25],
            "Tenor": [4, 5, 6, 7],
            "Volatility": [0.004941, 0.005789, 0.006, 0.006529],
            "Strike": [-0.020, 0.015, -0.005, 0.010],
            "Weigth": [1, 1, 0, 0],
            "p_y": [1, 1, 1, 1],
        }
    ).set_index([pd.Index([3, 4, 5, 6])])
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_greater_than_equal(test_dataframe):
    condition = "'Tenor'>=3"
    operation = ">="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [2, 2, 20, 20, 25, 50],
            "Tenor": [3, 4, 5, 6, 7, 3],
            "Volatility": [0.003342, 0.004941, 0.005789, 0.006, 0.006529, 0.004129],
            "Strike": [0.0, -0.020, 0.015, -0.005, 0.010, -0.020],
            "Weigth": [0, 1, 1, 0, 0, 1],
            "p_y": [1, 1, 1, 1, 1, 1],
        }
    ).set_index([pd.Index([2, 3, 4, 5, 6, 9])])
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_not_equal(test_dataframe):
    condition = "'Tenor'!=3"
    operation = "!="
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 20, 20, 25, 30, 50],
            "Tenor": [1, 2, 4, 5, 6, 7, 1, 2],
            "Volatility": [0.002121, 0.002833, 0.004941, 0.005789, 0.006, 0.006529, 0.005569, 0.003737],
            "Strike": [0.0, 0.0, -0.020, 0.015, -0.005, 0.010, 0.010, 0.020],
            "Weigth": [1, 1, 1, 1, 0, 0, 1, 0],
            "p_y": [1, 1, 1, 1, 1, 1, 1, 1],
        }
    ).set_index([pd.Index([0, 1, 3, 4, 5, 6, 7, 8])])
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.equals(expected)


def test_select_from_dataframe_empty_selection(test_dataframe):
    condition = "'Maturity'<=0"
    operation = "<="
    dataframe = test_dataframe
    res = syn.select_from_dataframe(condition, operation, dataframe)
    assert res.empty


############################################################################################################


def test_interpret_condition_successful(test_dataframe):
    condition = "'Maturity'==1,2"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 2],
            "Tenor": [1, 2, 3, 4],
            "Volatility": [0.002121, 0.002833, 0.003342, 0.004941],
            "Strike": [0, 0, 0, -0.02],
            "Weigth": [1, 1, 0, 1],
            "p_y": [1, 1, 1, 1],
        }
    )
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_different(test_dataframe):
    condition = "'Maturity'!=1,2,20,30,50,50"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {"Maturity": [25], "Tenor": [7], "Volatility": [0.006529], "Strike": [0.01], "Weigth": [0], "p_y": [1]}
    ).set_index([pd.Index([6])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_greater_or_equal(test_dataframe):
    condition = "'Maturity'>=50"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [50, 50],
            "Tenor": [2, 3],
            "Volatility": [0.003737, 0.004129],
            "Strike": [0.02, -0.02],
            "Weigth": [0, 1],
            "p_y": [1, 1],
        }
    ).set_index([pd.Index([8, 9])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_greater(test_dataframe):
    condition = "'Maturity'>30"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [50, 50],
            "Tenor": [2, 3],
            "Volatility": [0.003737, 0.004129],
            "Strike": [0.02, -0.02],
            "Weigth": [0, 1],
            "p_y": [1, 1],
        }
    ).set_index([pd.Index([8, 9])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_less_or_equal(test_dataframe):
    condition = "'Maturity'<=1"
    dataframe = test_dataframe

    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    ).set_index([pd.Index([0, 1])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_less(test_dataframe):
    condition = "'Maturity'<2"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    ).set_index([pd.Index([0, 1])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_invalid(test_dataframe):
    condition = "'Maturity'!!1"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.interpret_condition(condition, dataframe)


def test_interpret_condition_multiple_values(test_dataframe):
    condition = "'Maturity'==1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1, 2, 2, 20, 20],
            "Tenor": [1, 2, 3, 4, 5, 6],
            "Volatility": [0.002121, 0.002833, 0.003342, 0.004941, 0.005789, 0.006],
            "Strike": [0.0, 0.0, 0.0, -0.02, 0.015, -0.005],
            "Weigth": [1, 1, 0, 1, 1, 0],
            "p_y": [1, 1, 1, 1, 1, 1],
        }
    ).set_index([pd.Index([0, 1, 2, 3, 4, 5])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_duplicate_values(test_dataframe):
    condition = "'Maturity'==1,1,1"
    dataframe = test_dataframe
    expected = pd.DataFrame(
        {
            "Maturity": [1, 1],
            "Tenor": [1, 2],
            "Volatility": [0.002121, 0.002833],
            "Strike": [0.0, 0.0],
            "Weigth": [1, 1],
            "p_y": [1, 1],
        }
    ).set_index([pd.Index([0, 1])])
    res = syn.interpret_condition(condition, dataframe)
    assert res.equals(expected)


def test_interpret_condition_duplicate_operator(test_dataframe):
    condition = "'Maturity'==1==2"
    dataframe = test_dataframe
    with pytest.raises(syn.SensiSyntaxError):
        syn.interpret_condition(condition, dataframe)


############################################################################################################


def test_apply_value_to_selection_successful():
    value = "(+100)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "101.0"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_sub():
    value = "(-200)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "-199.0"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_multiply():
    value = "(*0.000000000005)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "5.0e-12"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_div():
    value = "(/4.0000001)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "0.24999999375"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_replace_value():
    value = "100"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "100"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_replace_value2():
    value = "-100"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "-100"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_string():
    value = "MIN(33.3)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "MIN(33.3)"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_wrong_types():
    value = "(+100)"
    selected_dict = {"Maturity": {1: "test"}}
    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_scientific_notation():
    value = "(-5,000001E-04)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "0.9994999999"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_decimal_with_comma():
    value = "(+0,00247)"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "1.00247"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_single_parentheses():
    value = "(-100"
    selected_dict = {"Maturity": {1: "1"}}
    expected = {"Maturity": {1: "(-100"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_empty_value():
    value = ""
    selected_dict = {"Maturity": {1: 1}}
    assert syn.apply_value_to_selection(value, selected_dict) == selected_dict


def test_apply_value_to_selection_empty_value_in_dict():
    value = "(+100)"
    selected_dict = {"Maturity": {1: ""}}
    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_null_value():
    value = "(- )"
    selected_dict = {"Maturity": {1: 1}}
    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_multiple_whitespaces():
    value = "(+ 100   )"
    selected_dict = {"Maturity": {1: 1}}
    expected = {"Maturity": {1: "101.0"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_bool_value():
    value = "True"
    selected_dict = {"Maturity": {1: "1"}}
    expected = {"Maturity": {1: True}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_apply_with_string():
    value = "(+test)"
    selected_dict = {"Maturity": {1: "1"}}
    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


def test_apply_value_to_selection_apply_with_no_operation():
    value = "(10)"
    selected_dict = {"Maturity": {1: "1"}}
    expected = {"Maturity": {1: "11.0"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_replace_with_string():
    value = "test"
    selected_dict = {"Maturity": {1: "1"}}
    expected = {"Maturity": {1: "test"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_undefined_operation():
    value = "(%10)"
    selected_dict = {"Maturity": {1: 1}}
    with pytest.raises(syn.SensiSyntaxError):
        syn.apply_value_to_selection(value, selected_dict)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("+0.99999998", "10.99999998"),
        ("+0.99999999", "10.99999999"),
        ("+1.00000000", "11.0"),
        ("+1.00000001", "11.00000001"),
        ("+1.00000002", "11.00000002"),
        ("-0.99999998", "9.00000002"),
        ("-0.99999999", "9.00000001"),
        ("-1.00000000", "9.0"),
        ("-1.00000001", "8.99999999"),
        ("-1.00000002", "8.99999998"),
    ],
)
def test_apply_value_to_selection_with_precision(value, expected):
    value = f"({value})"
    selected_dict = {"Maturity": {1: "10"}}
    expected = {"Maturity": {1: expected}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_precision_with_int():
    value = "(-50)"
    selected_dict = {"Maturity": {1: "148.2092901"}}
    expected = {"Maturity": {1: "98.2092901"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


def test_apply_value_to_selection_precision_with_float():
    value = "(-49.99999999991)"
    selected_dict = {"Maturity": {1: "148.2092901"}}
    expected = {"Maturity": {1: "98.20929010009"}}
    res = syn.apply_value_to_selection(value, selected_dict)
    assert res == expected


############################################################################################################


def test_apply_syntax_to_file_successful():
    input_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/ceF89BNhvJRc9WHMS/Nominal_rates/GBP_Mkt_Swaptions_Vols.csv"
    syntax = syn.Syntax("$..*[@.name is 'GBP']..*[@.name is 'IR'].data.swaptions.mkt.filename", "*,1", "", "(+0)")
    settings_json = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    assert syn.apply_syntax_to_file(input_path, syntax, settings_json) is True


def test_apply_syntax_to_file_with_row_index():
    input_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/Central/RN_inputs/Correlation/ESG_Correlation_Matrix.csv"
    syntax = syn.Syntax(
        "$.framework.sensi_1.param.dependence.filename", "'USD_IR_DDLMM_FACTOR_1','USD_IR_DDLMM_FACTOR_1'", "", "(+0)"
    )
    settings_json = su.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    assert syn.apply_syntax_to_file(input_path, syntax, settings_json) is True
