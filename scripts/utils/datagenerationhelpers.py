import glob

import pandas as pd
import logging

def generate_data_frame_with_relative_times(route):

    # Index(['tjobname', 'stage', 'COI-setup-start', 'COI-setup-end',
    #    'tjob-setup-start', 'tjob-setup-end', 'tjob-testexec-start',
    #    'tjob-testexec-end', 'tjob-teardown-start', 'tjob-teardown-end',
    #    'coi-teardown-start', 'coi-teardown-end'],

    df = pd.read_csv(route, delimiter=";")
    test_execution_start = min(df["COI-setup-start"])
    columns_to_substract = ['COI-setup-start', 'COI-setup-end',
                            'tjob-setup-start', 'tjob-setup-end', 'tjob-testexec-start',
                            'tjob-testexec-end', 'tjob-teardown-start', 'tjob-teardown-end',
                            'coi-teardown-start', 'coi-teardown-end']
    # Substract the initial time to have relative times
    for name_col in columns_to_substract:
        df[name_col] -= test_execution_start

    cols_to_concat = ['COI-setup', 'tjob-setup', 'tjob-testexec', 'tjob-teardown', 'coi-teardown']

    dataframe_duration_averages = pd.concat([df["tjobname"], df["stage"]], axis=1)
    for name in cols_to_concat:
        dataframe_duration_averages[name + '-avg'] = df[name + '-end'] - df[name + "-start"]

    return dataframe_duration_averages


def generatedatasetswithavgtimes(path):
    logging.debug("Generating the avg file using the .csv files of the path for: " + path)
    path = path + "/*.csv"

    is_first = True

    lifecycles = ['COI-setup-avg', 'tjob-setup-avg', 'tjob-testexec-avg', 'tjob-teardown-avg', 'coi-teardown-avg']
    current_dataframe = pd.DataFrame()
    number_files = 0
    output_dataframe = pd.DataFrame(columns=['tjobname', 'stage', 'COI-setup-start', 'COI-setup-end',
                                             'tjob-setup-start', 'tjob-setup-end', 'tjob-testexec-start',
                                             'tjob-testexec-end', 'tjob-teardown-start', 'tjob-teardown-end',
                                             'coi-teardown-start', 'coi-teardown-end'])
    files_directory = glob.glob(path)
    if len(files_directory) == 0:
        print("No .csv files found, please check the route: " + path + " the returned dataframe would be empty")
    else:
        for f_name in files_directory:
            number_files += 1
            if is_first:
                is_first = False
                current_dataframe = generate_data_frame_with_relative_times(f_name)

            else:
                next_dataframe = generate_data_frame_with_relative_times(f_name)
                for column in lifecycles:
                    current_dataframe[column] = current_dataframe[column] + next_dataframe[column]

        for column in lifecycles:
            current_dataframe[column] = current_dataframe[column].div(number_files)

        min_stage = 0
        max_stage = max(current_dataframe['stage'])
        start_stage = 0
        last_tjob_end = 0
        avg_teardown_coi = 0

        coi_setup_star_time = 0
        coi_setup_end_time = 0
        for i in range(min_stage, max_stage + 1):
            max_duration = 0
            stage_rows = current_dataframe.loc[current_dataframe['stage'] == i]
            for index, tjob_stage in stage_rows.iterrows():
                # ['COI-setup-avg', 'tjob-setup-avg', 'tjob-testexec-avg', 'tjob-teardown-avg', 'coi-teardown-avg']
                if i == 0:
                    coi_setup_end_time = tjob_stage['COI-setup-avg']
                    start_stage = coi_setup_end_time
                tjob_name_str = tjob_stage['tjobname']
                stage_str = tjob_stage['stage']
                coi_setup_start = coi_setup_star_time
                coi_setup_end = coi_setup_end_time
                tjob_setup_start = start_stage + 1
                tjob_setup_end = tjob_setup_start + tjob_stage['tjob-setup-avg']
                tjob_test_ex_start = tjob_setup_end + 1
                tjob_test_ex_end = tjob_test_ex_start + tjob_stage['tjob-testexec-avg']
                tjob_teardown_start = tjob_test_ex_end + 1
                tjob_teardown_end = tjob_teardown_start + tjob_stage['tjob-teardown-avg']
                coi_teardown_start = tjob_teardown_end
                coi_teardown_end = coi_teardown_start
                if tjob_teardown_end >= max_duration:
                    max_duration = tjob_teardown_end
                if tjob_teardown_end >= last_tjob_end:
                    last_tjob_end = tjob_teardown_end
                    avg_teardown_coi = tjob_stage['coi-teardown-avg']

                # Using pandas.concat() to add a row
                new_row = pd.DataFrame(
                    {'tjobname': tjob_name_str, 'stage': stage_str, 'COI-setup-start': coi_setup_start,
                     'COI-setup-end': coi_setup_end, 'tjob-setup-start': tjob_setup_start,
                     'tjob-setup-end': tjob_setup_end, 'tjob-testexec-start': tjob_test_ex_start,
                     'tjob-testexec-end': tjob_test_ex_end, 'tjob-teardown-start': tjob_teardown_start,
                     'tjob-teardown-end': tjob_teardown_end,
                     'coi-teardown-start': coi_teardown_start, 'coi-teardown-end': coi_teardown_end
                     },
                    index=[0])
                output_dataframe = pd.concat([new_row, output_dataframe.loc[:]]).reset_index(drop=True)

            start_stage = max_duration
        output_dataframe['coi-teardown-start'] = last_tjob_end
        output_dataframe['coi-teardown-end'] = last_tjob_end + avg_teardown_coi
        output_dataframe = output_dataframe.sort_values(by=["stage", "tjobname"], ascending=[True, True]).round(
            decimals=2)
    return output_dataframe


def generate_all_csv_with_avg_times(path_input, path_output):
    folders = glob.glob(path_input, recursive=True)
    if len(folders) == 0:
        print("There's no folders in this directory")
        return -1
    else:
        for f_name in folders:
            dataset_output = generatedatasetswithavgtimes(f_name)
            name_file_split = f_name.split("\\")
            namefile = str(name_file_split[len(name_file_split) - 1])
            dataset_output.to_csv(path_output + namefile + "_avg.csv", index=False, sep=";", decimal=",")
    return 0
