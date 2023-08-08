import logging
import math

import jsonpickle
import pandas as pd

from scripts.model import capacitytypes
from scripts.model import lifecycles

def get_capacities_used(tjob_list, name):
    for i in tjob_list:
        if i.name == name:
            return i.get_capacities()


def get_start_end_time(tjob, lifecycle_phase, dataframe_data):
    row = dataframe_data.loc[dataframe_data['tjobname'] == tjob]
    start_time = float(row["tjob-" + lifecycle_phase + "-start"].iloc[0])
    end_time = float(row["tjob-" + lifecycle_phase + "-end"].iloc[0])
    return [start_time, end_time]


def get_certain_capacity(capacity_list, name):
    for i in capacity_list:
        if i.name == name:
            return i


def generate_dataframe_aggregation_cloud_object(dataframe_output, cloud_object, capacities_contracted):
    aggregation_dataframe = get_dataframe_aggregation_by_lifecycle_capacity(dataframe_output=dataframe_output)
    aggregation_dataframe = pd.concat([dataframe_output, aggregation_dataframe]).reset_index(drop=True)
    match cloud_object:
        case "VM":
            logging.debug("Generating the VM file")
            contracted_vm = dataframe_output.groupby(["Capacity", "Infrastructure"], as_index=False).sum()
            contracted_vm["TJob"] = "CONTRACTED"
            contracted_vm["Lifecycle"] = "All"
            for i in range(4, len(contracted_vm.columns), 1):
                for cap in capacities_contracted:
                    index_row = contracted_vm[contracted_vm['Capacity'] == cap.name].index[0]
                    contracted_vm.iloc[index_row, i] = cap.quantity
                    # contrated_vm.loc[contrated_vm['Capacity'] == cap.name, i] = cap.quantity
            dataframe_output = pd.concat([aggregation_dataframe, contracted_vm]).reset_index(drop=True)

        case "Container":
            logging.debug("Generating the Container file")
            contracted_container = get_dataframe_aggregation_by_lifecycle_capacity(dataframe_output=dataframe_output)
            contracted_container["TJob"] = "CONTRACTED"
            dataframe_output = pd.concat([aggregation_dataframe, contracted_container]).reset_index(drop=True)

    return dataframe_output


def get_dataframe_aggregation_by_lifecycle_capacity(dataframe_output):
    aggregated_dataframe = dataframe_output.groupby(["Lifecycle", "Capacity", "Infrastructure"], as_index=False).sum()
    aggregated_dataframe["TJob"] = "All"
    aggregated_dataframe = aggregated_dataframe.sort_values(by=["TJob", "Capacity", "Lifecycle"],
                                                            ascending=[True, True, True])
    return aggregated_dataframe


def generate_dataframe_with_capacities_usage(path_schedule, path_resources_used, cloud_object_name, time_period,
                                             n_test_suite_executions):
    dataframe_one_execution, dataframe_output, end_execution = generate_one_execution_resource_usage(cloud_object_name,
                                                                                                     path_resources_used,
                                                                                                     path_schedule)

    if (n_test_suite_executions * end_execution) > time_period:
        raise ValueError(
            'The number of test suite executions is not feasible for the time that the test suite is provisioned')
    else:
        logging.debug("Generating the Aggregated file of the scheduling: " + path_schedule)
        space_between_tasks = (calculate_time_interval(time_period, n_test_suite_executions) - end_execution)
        first_iter = True
        for i in range(0, n_test_suite_executions):
            if not first_iter:
                last_column_dataframe = dataframe_output.iloc[:, -1:]
                last_colum_label_seconds = int(last_column_dataframe.columns.values[0]) + 1
                list_new_dataframelabels = list(
                    range(last_colum_label_seconds, last_colum_label_seconds + end_execution + 1, 1))
                dataframe_one_execution.columns = [str(x) for x in list_new_dataframelabels]

            dataframe_output = pd.concat([dataframe_output, dataframe_one_execution], axis=1)
            dataframe_output = aggregate_dataframe_seconds_with_no_usage(dataframe_output,
                                                                         space_between_tasks - 1)
            first_iter = False

        last_column_dataframe = dataframe_output.iloc[:, -1:]
        last_colum_label_seconds = int(last_column_dataframe.columns.values[0])
        if last_colum_label_seconds < time_period:
            dataframe_output = aggregate_dataframe_seconds_with_no_usage(dataframe_output,
                                                                         time_period - last_colum_label_seconds)

        dataframe_output = dataframe_output.sort_values(by=["TJob", "Capacity", "Lifecycle"],
                                                        ascending=[True, True, True])

    return dataframe_output


def calculate_time_interval(total_seconds, num_tasks):
    interval_seconds = math.floor(total_seconds / num_tasks)
    return interval_seconds


def generate_one_execution_resource_usage(cloud_object_name, path_resources_used, path_schedule):
    dataframe_tjobs = pd.read_csv(path_schedule, delimiter=";", decimal=",")
    with open(path_resources_used, 'r') as file:
        json_string = file.read()
        plan = jsonpickle.decode(json_string)
    tjobs = plan.tjobs
    list_tjobs = list(tjobs)
    dataframe_output = pd.DataFrame()
    tjob_colum = []
    capacity_column = []
    infrastructure_column = []
    lifecycle_colum = []
    for tjob in dataframe_tjobs["tjobname"]:
        for phase in lifecycles.list_lifecycles:
            for capacity in capacitytypes.list_capabilities:
                tjob_colum.append(tjob)
                capacity_column.append(capacity)
                infrastructure_column.append(cloud_object_name)
                lifecycle_colum.append(phase)
    dataframe_output["TJob"] = tjob_colum
    dataframe_output["Capacity"] = capacity_column
    dataframe_output["Infrastructure"] = infrastructure_column
    dataframe_output["Lifecycle"] = lifecycle_colum
    dataframe_one_execution = pd.DataFrame()
    end_execution = int(dataframe_tjobs["coi-teardown-end"].get(1))
    for second in range(0, end_execution + 1, 1):
        row_resource_profile = []
        for index, row in dataframe_output.iterrows():
            tjob_resources = get_capacities_used(list_tjobs, row.TJob)
            start_time, end_time = get_start_end_time(row.TJob, row.Lifecycle, dataframe_tjobs)

            if float(start_time) < second < float(end_time):
                row_resource_profile.append(round(get_certain_capacity(tjob_resources, row.Capacity).quantity, 2))
            else:
                row_resource_profile.append(0.0)
        new_column = pd.Series(row_resource_profile)
        dataframe_one_execution = pd.concat([dataframe_one_execution, new_column.rename(second)], axis=1)

    return dataframe_one_execution, dataframe_output, end_execution


def aggregate_dataframe_seconds_with_no_usage(dataframe, num_seconds):
    height = len(dataframe.get("TJob"))
    lastcolumndataframe = dataframe.iloc[:, -1:]
    width_start = int(lastcolumndataframe.columns.values[0])
    width_end = width_start + num_seconds
    list_colum_labels = list(range(width_start + 1, width_end + 1, 1))
    list_colum_labels = [str(x) for x in list_colum_labels]
    dataframefullfill = pd.DataFrame(0.00, index=range(height), columns=list_colum_labels)

    dataframefullfill.index = dataframe.index

    dataframe = pd.concat([dataframe, dataframefullfill], axis=1)
    return dataframe
