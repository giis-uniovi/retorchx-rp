import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scripts.model import capacitytypes


def plot_usage_profile(path_dataframe, capacity):
    daatframe_with_all_data = pd.read_csv(path_dataframe, header=0, sep=";")
    dataframe_used_cap = daatframe_with_all_data.loc[daatframe_with_all_data['TJob'] == "All"]
    dataframe_contrated_cap = daatframe_with_all_data.loc[daatframe_with_all_data['TJob'] == "CONTRACTED"]

    # set seaborn style
    sns.set_theme()

    x_Axis = list(map(float, dataframe_used_cap.columns.values[4:]))
    y_memory_used_setup = list(map(float, dataframe_used_cap.query(
        "Capacity == '" + capacity + "' & Lifecycle == 'setup'").iloc[0, :].values.flatten().tolist()[4:]))
    y_memory_used_testexec = list(map(float, dataframe_used_cap.query(
        "Capacity == '" + capacity + "' & Lifecycle == 'testexec'").iloc[0, :].values.flatten().tolist()[4:]))
    y_memory_used_teardown = list(map(float, dataframe_used_cap.query(
        "Capacity == '" + capacity + "' & Lifecycle == 'teardown'").iloc[0, :].values.flatten().tolist()[4:]))
    y_memory_contracted = list(map(float, dataframe_contrated_cap.query(
        "Capacity == '" + capacity + "'").iloc[0,
                                          :].values.flatten().tolist()[4:]))

    labels_set = [capacity + "-used-setup", capacity + "-used-test-execution", capacity + "-used-tear-down",
                  capacity + "-contracted"]
    color_map = ["yellow","orange","violet","blue"]
    # create seaborn area chart
    plt.stackplot(x_Axis, y_memory_used_setup, y_memory_used_testexec, y_memory_used_teardown, y_memory_contracted,
                  labels=labels_set,colors=color_map)
    print(daatframe_with_all_data)
