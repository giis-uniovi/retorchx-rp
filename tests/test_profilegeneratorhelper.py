# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from scripts.model import capacitytypes
from scripts.model.capacity import Capacity
from scripts.utils.profilegeneratorhelpers import generate_dataframe_with_capacities_usage, \
    generate_dataframe_aggregation_cloud_object


class ResourceProfileGenerators(unittest.TestCase):
    """Advanced test cases."""

    @staticmethod
    def test_generaResourceProfile():
        path_tjob_dataset = "tests/resources/test-inputs/profilegenerator/3parallel.csv"
        path_resource_instances = "tests/resources/test-inputs/profilegenerator/resourceinstances.json"
        dataframe_output = generate_dataframe_with_capacities_usage(path_tjob_dataset,
                                                                    path_resource_instances,
                                                                    "virtualmachineexample", time_period=3600,
                                                                    n_test_suite_executions=3)
        # dataframe_output.to_csv("tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile.csv", index=False,sep=";")
        expected_output_dataframe = pd.read_csv(
            "tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile.csv",
            header=0, sep=";")
        expected_output_dataframe = expected_output_dataframe.sort_values(by=["TJob", "Capacity", "Lifecycle"],
                                                                          ascending=[True, True, True])

        assert expected_output_dataframe.to_csv(index=False, sep=";") == dataframe_output.to_csv(index=False, sep=";")
        # For some reason use the default comparison of pandas doesn't work. The two dataframes are
        # identical, so it's related with the types of the indexes...
        # pandas._testing.assert_frame_equal(expected_output_dataframe, dataframe_output)


@staticmethod
def test_generateaggregation_container():
    dataframe_output = pd.read_csv(
        "tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile.csv",
        header=0, sep=";")
    dataframe_output = generate_dataframe_aggregation_cloud_object(dataframe_output=dataframe_output,
                                                                   cloud_object="Container",
                                                                   capacities_contracted={})

    # dataframe_output.to_csv("tests/resources/outputs/profilegenerator/profile3paralleloutputfile_container_agg.csv", index=False,sep=";")
    expected_output_dataframe = pd.read_csv(
        "tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile_container_agg.csv",
        header=0, sep=";")

    # assert expected_output_dataframe.to_csv(index=False, sep=";") == dataframe_output.to_csv(index=False, sep=";")
    # In this case the assert_equals of pandas works...
    pd._testing.assert_frame_equal(expected_output_dataframe, dataframe_output)


@staticmethod
def test_generateaggregation_vm():
    dataframe_output = pd.read_csv(
        "tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile.csv",
        header=0, sep=";")

    cap_vm_memory = Capacity(name=capacitytypes.memory_name, quantity=32)
    cap_vm_processor = Capacity(name=capacitytypes.processor_name, quantity=12)
    cap_vm_storage = Capacity(name=capacitytypes.storage_name, quantity=64)

    capacities_vm = {cap_vm_memory, cap_vm_processor, cap_vm_storage}
    dataframe_output = generate_dataframe_aggregation_cloud_object(dataframe_output=dataframe_output,
                                                                   cloud_object="VM",
                                                                   capacities_contracted=capacities_vm)

    dataframe_output.to_csv("tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile_vm_agg.csv",
                            index=False, sep=";")
    expected_output_dataframe = pd.read_csv(
        "tests/resources/test-outputs/profilegenerator/profile3paralleloutputfile_vm_agg.csv",
        header=0, sep=";")

    # assert expected_output_dataframe.to_csv(index=False, sep=";") == dataframe_output.to_csv(index=False, sep=";")
    # In this case the assert_equals of pandas works...
    pd._testing.assert_frame_equal(expected_output_dataframe, dataframe_output)


if __name__ == '__main__':
    unittest.main()
