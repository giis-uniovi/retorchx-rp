# -*- coding: utf-8 -*-
import logging
import unittest

import pandas as pd
import pandas._testing

from scripts.utils.datagenerationhelpers import generate_data_frame_with_relative_times, generatedatasetswithavgtimes


class DataframeGenerators(unittest.TestCase):
    """Advanced test cases."""

    @staticmethod
    def test_generateDataFromCSV():
        dataframe_output = generate_data_frame_with_relative_times(
            "tests/resources/test-inputs/datagenerator/sampleoutputJenkins.csv")

        expected_dataframe = pd.read_csv("tests/resources/test-outputs/datagenerator/outputgenerateDataFromCSV.csv",
                                         header=0)

        pandas._testing.assert_frame_equal(expected_dataframe.astype(str), dataframe_output.astype(str))

    @staticmethod
    def test_generateAvgDataframe():
        path_datasets = 'tests/resources/test-inputs/datagenerator'

        dataframe = generatedatasetswithavgtimes(path_datasets)
        # dataframe.to_csv("./outputavgdataframe.csv",sep=";",index=False)

        expected_output_dataframe = pd.read_csv('tests/resources/test-outputs/datagenerator/outputavgdataframe.csv',
                                                header=0,
                                                sep=";")
        expected_output_dataframe = expected_output_dataframe.reset_index(drop=True)
        dataframe = dataframe.reset_index(drop=True)
        pandas._testing.assert_frame_equal(expected_output_dataframe.astype(str), dataframe.astype(str))


if __name__ == '__main__':
    unittest.main()
