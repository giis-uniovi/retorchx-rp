# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from scripts.model import capacitytypes
from scripts.model.capacity import Capacity
from scripts.utils.graphycalprofile import plot_usage_profile
from scripts.utils.profilegeneratorhelpers import generate_dataframe_with_capacities_usage, \
    generate_dataframe_aggregation_cloud_object


class ResourceProfileGenerators(unittest.TestCase):
    """Advanced test cases."""

    @staticmethod
    def test_generaResourceProfile():
        path_input="tests/resources/test-inputs/profilegraphgenerator/3parallel_avg_usageprofile_Container.csv"
        plot_usage_profile(path_input,capacitytypes.memory_name)



if __name__ == '__main__':
    unittest.main()
