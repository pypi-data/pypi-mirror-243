import datetime
import json
from copy import copy
from os import listdir
from os.path import isfile, join

import pandas as pd
from rich.console import Console
from rich.progress import Progress

from stairsval.core.aggregator import Aggregator
from stairsval.core.database.DBWrapper import DBWrapper
from stairsval.core.dataset_processors.KSGDataset import KSGDataset
from stairsval.core.dataset_processors.PlanDataset import PlanDataset
from stairsval.core.dataset_processors.ValidationDataset import ValidationDataset
from stairsval.core.expert_metrics_estimator import ExpertMetricsEstimator
from stairsval.core.stats_calculator import StatisticCalculator
from stairsval.validation_checks.ResourcesChecker import ResourcesChecker
from stairsval.validation_checks.TimeChecker import TimeChecker
from stairsval.validation_checks.WorksChecker import WorksChecker
from stairsval.validators.BaseValidator import BaseValidator


class GPNPlanValidator:
    def __init__(
        self,
        plan,
        precalculated_brave: pd.DataFrame,
        links_history: pd.DataFrame,
        journal: dict,
        connector=None,
        level=None,
    ):
        self.console = Console()
        self.ksg_data = KSGDataset(
            ksg_data=plan, connector=connector, level=level
        ).collect()
        self.plan_dataset = PlanDataset(ksg_data=self.ksg_data)
        self.data_source = DBWrapper(connector=connector, level=level)
        self.aggregator = Aggregator()
        self.works_validator = WorksChecker()
        self.resources_validator = None
        self.statistic_calculator = None
        self.precalculated_brave = precalculated_brave
        self.links_history = links_history
        self.journal = journal
        self.time_validator = TimeChecker(journal=self.journal)

    def validate(self):
        with Progress(console=self.console) as progress:
            validation_task = progress.add_task("[cyan]Validating...", total=9)

            self.console.log("Collecting data")
            plan_df = self.plan_dataset.collect()
            act = self.plan_dataset.get_act_names()
            res = self.plan_dataset.get_res_names()

            pools = self.plan_dataset.get_pools()

            validation_df = ValidationDataset(
                self.data_source, pools, act, res
            ).collect()
            progress.advance(validation_task)

            self.console.log("Validating resources on log data")

            self.resources_validator = ResourcesChecker(
                res=[r + "_res_fact" for r in res], journal=self.journal
            )
            (
                df_perc_agg_res,
                df_final_volume_res,
                df_final_style_res,
                fig_dict_res,
                not_perc_res,
                norm_perc_res,
            ) = self.resources_validator.validate(plan_df, validation_df, act)
            progress.advance(validation_task)

            self.console.log("Validating resources on journal data")

            b = self.precalculated_brave

            (
                df_vedom,
                not_perc_vedom,
                norm_perc_vedom,
            ) = self.aggregator.get_res_ved_stat(b, self.ksg_data, plan_type="gpn")
            progress.advance(validation_task)

            self.console.log("Splitting data into window frames")
            _, df_wind_val = self.window_zero(validation_df)
            _, df_wind_model = self.window_zero(plan_df)
            for i in df_wind_val.index:
                for c in act:
                    df_wind_val.loc[i, c.split("_")[0] + "_real_time_act"] = (
                        df_wind_val.loc[i, "Window length"]
                        - df_wind_val.loc[i, c.split("_")[0] + "_act_fact_zero_lil"]
                        - df_wind_val.loc[i, c.split("_")[0] + "_act_fact_zero_big"]
                    )
            for i in df_wind_model.index:
                for c in act:
                    df_wind_model.loc[i, c.split("_")[0] + "_real_time_act"] = (
                        df_wind_model.loc[i, "Window length"]
                        - df_wind_model.loc[i, c.split("_")[0] + "_act_fact_zero_lil"]
                        - df_wind_model.loc[i, c.split("_")[0] + "_act_fact_zero_big"]
                    )
            progress.advance(validation_task)

            self.console.log("Validation of average daily work volumes")
            (
                df_volume_stat,
                dist_dict,
                norm_volume_perc,
                not_volume_perc,
            ) = self.works_validator.validate(
                plan_df, validation_df, act=[c + "_act_fact" for c in act]
            )
            progress.advance(validation_task)

            self.console.log("Validating time")
            (
                df_time_stat,
                time_plot_dict,
                norm_time_perc,
                not_time_perc,
            ) = self.time_validator.validate(
                df_wind_model, df_wind_val, act=[c + "_act_fact" for c in act]
            )
            progress.advance(validation_task)
            self.console.log("Validating sequences")
            (
                df_seq_stat,
                df_color_seq,
                norm_perc_seq,
                not_perc_seq,
            ) = self.aggregator.get_all_seq_statistic(self.links_history, self.ksg_data)
            progress.advance(validation_task)
            self.console.log(
                "Collecting general statistics on activities and resources"
            )
            self.statistic_calculator = StatisticCalculator(
                norm_perc_res,
                norm_perc_vedom,
                norm_volume_perc,
                norm_time_perc,
                norm_perc_seq,
                not_perc_res,
                not_perc_vedom,
                not_volume_perc,
                not_time_perc,
                not_perc_seq,
            )
            work_res_common_perc = (
                self.statistic_calculator.get_statistic_for_properties_and_all_stat()
            )
            plan_statistic = self.statistic_calculator.get_plan_statistic()
            progress.advance(validation_task)

        return (
            df_perc_agg_res,
            df_final_volume_res,
            df_final_style_res,
            fig_dict_res,
            df_vedom,
            df_volume_stat,
            dist_dict,
            df_time_stat,
            time_plot_dict,
            df_seq_stat,
            df_color_seq,
            work_res_common_perc,
            plan_statistic,
        )

    def common_validate(self):
        act = self.plan_dataset.get_act_names()
        res = self.plan_dataset.get_res_names()
        pools = self.plan_dataset.get_pools()
        validation_df_res = ValidationDataset(
            self.data_source, pools, act, res
        ).collect()
        val_data_time = self.data_source.get_time_data(act)
        (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
        ) = ResourcesChecker(res=res).common_validation(
            self.ksg_data, validation_df_res, plan_type="gpn"
        )
        df_vedom, not_perc_vedom, norm_perc_vedom = self.aggregator.get_res_ved_stat(
            self.precalculated_brave, self.ksg_data, plan_type="gpn"
        )
        (
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        ) = TimeChecker().common_validation(self.ksg_data, val_data_time, "gpn")
        return (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
            df_vedom,
            not_perc_vedom,
            norm_perc_vedom,
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        )

    @staticmethod
    def window_zero(df: pd.DataFrame, min_window: int = 2, max_window: int = 10):
        df = df.drop_duplicates()
        base = datetime.datetime.today()
        date_list = [
            (base + datetime.timedelta(days=x)).strftime("%d.%m.%Y")
            for x in range(df.shape[0])
        ]
        df.index = date_list
        """Function for making time windows of msg files

        Args:
            df (pd.DataFrame): input msg file
            min_window (int, optional): Min length of window. Defaults to 5.
            max_window (int, optional): Max length of window. Defaults to 31.

        Returns:
            DataFrame: msg files with windows
        """
        act_col = [var for var in df.columns if "_act_fact" in var]

        res_col = [var for var in df.columns if "_res_fact" in var]
        new_zero_lil = [act + "_zero_lil" for act in act_col]
        new_zero_big = [act + "_zero_big" for act in act_col]
        df_new = pd.DataFrame(
            columns=list(df.columns)
            + ["Start day", "Window length"]
            + new_zero_lil
            + new_zero_big
        )
        df_zero = pd.DataFrame(columns=act_col)
        for window_len in [7]:
            for start in range(0, len(df) - window_len + 1):
                new_row = (
                    df[act_col]
                    .iloc[start : start + window_len]
                    .sum(axis=0, skipna=True)
                )
                new_row = {
                    act: 1 if value == 0.0 else 0 for act, value in new_row.items()
                }
                start_day = datetime.datetime.strptime(df.index[start], "%d.%m.%Y")
                end_day = datetime.datetime.strptime(
                    df.index[start + window_len - 1], "%d.%m.%Y"
                )
                df_zero.loc[df.index[start]] = new_row

        window_list = list(range(min_window, max_window + 1))
        for window_len in window_list:
            for start in range(0, len(df) - window_len + 1):
                start_day = datetime.datetime.strptime(df.index[start], "%d.%m.%Y")
                end_day = datetime.datetime.strptime(
                    df.index[start + window_len - 1], "%d.%m.%Y"
                )
                if (end_day - start_day).days == window_len - 1:
                    new_row_act = (
                        df[act_col]
                        .iloc[start : start + window_len]
                        .sum(axis=0, skipna=True)
                    )
                    new_row_res = (
                        df[res_col]
                        .iloc[start : start + window_len]
                        .mean(axis=0, skipna=True)
                    )
                    new_row = copy(new_row_act)
                    new_row = pd.concat([new_row, new_row_res])

                    lil = {act + "_zero_lil": 0 for act in act_col}
                    big = {act + "_zero_big": 0 for act in act_col}
                    danger_date = [
                        df.index[ind] for ind in range(start, start + window_len)
                    ]

                    for act in act_col:
                        for i in range(start, start + window_len):
                            if df.iloc[i][act] == 0.0:
                                lil[act + "_zero_lil"] = lil[act + "_zero_lil"] + 1
                                if (
                                    (i < window_len - 6)
                                    and danger_date[i - start] in df_zero.index
                                    and df_zero.loc[danger_date[i - start]][act] == 1
                                ):
                                    if (i > start) and (
                                        df_zero.loc[danger_date[i - start - 1]][act]
                                        == 1
                                    ):
                                        big[act + "_zero_big"] = (
                                            big[act + "_zero_big"] + 1
                                        )
                                    else:
                                        big[act + "_zero_big"] = (
                                            big[act + "_zero_big"] + 7
                                        )
                    lil = {
                        act
                        + "_zero_lil": lil[act + "_zero_lil"]
                        - big[act + "_zero_big"]
                        for act in act_col
                    }

                    new_row = {
                        **new_row,
                        **lil,
                        **big,
                        "Start day": start_day,
                        "Window length": window_len,
                    }
                    df_new = pd.concat(
                        [df_new, pd.DataFrame(pd.Series(new_row)).transpose()],
                        ignore_index=True,
                    )

        return df_zero, df_new

    @staticmethod
    def _file_opener(mypath, validation_files, act):
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        for file in onlyfiles:
            msg_file = open(mypath + file, encoding="utf8")
            msg_data = json.load(msg_file)
            if len(msg_data["resource"]) != 0:
                for work in msg_data["work"]:
                    if work["work title"] in act:
                        validation_files.append(mypath + file)
                        break
        return validation_files

    @staticmethod
    def _save_json_file(label, json_file, new_plan_path):
        with open(new_plan_path + str(label) + ".json", "w") as outfile:
            json.dump(json_file, outfile)
        return new_plan_path + str(label) + ".json"


class GPNValidator(BaseValidator):
    """Validator for GPN plans."""

    def __init__(self, project_ksg, connector=None, level=None, history_adapter=None):
        super().__init__(project_ksg, history_adapter)
        self.connector = connector
        self.level = level
        self.plan_type = "gpn"

    def specific_validation(self):
        result_dict = dict()
        ksg_for_val_data = self.project_ksg
        regime = True
        for el in ksg_for_val_data["schedule"]["works"]:
            if (
                el["display_name"] == "Окончание работ по марке"
                or el["display_name"] == "Начало работ по марке"
            ):
                regime = False
                break
        if regime:
            (
                df_perc_agg_res,
                df_final_volume_res,
                df_final_style_res,
                fig_dict_res,
                df_vedom,
                df_volume_stat,
                dist_dict,
                df_time_stat,
                time_plot_dict,
                df_seq_stat,
                df_color_seq,
                work_res_common_perc,
                plan_statistic,
            ) = GPNPlanValidator(
                plan=self.project_ksg,
                connector=self.connector,
                level=self.level,
                precalculated_brave=self.history_adapter.get_precalculated_brave_coefficients(),
                links_history=self.history_adapter.get_links_history_messoyakha_with_new_granular_v2(),
                journal=self.history_adapter.get_journal_mapped(),
            ).validate()

            result_dict["Object 0"] = {
                "Resource to Work Ratio": df_perc_agg_res,
                "Work Pools Volumes": df_final_volume_res,
                "Work Pools Colors": df_final_style_res,
                "Data for Resource Charts": fig_dict_res,
                "Resource Journal": df_vedom,
                "Production Statistics": df_volume_stat,
                "Data for Production Charts": dist_dict,
                "Work Time Statistics": df_time_stat,
                "Data for Time Charts": time_plot_dict,
                "Connection Table": df_seq_stat,
                "Color Connection Table": df_color_seq,
                "Final Statistics for Work and Resources": work_res_common_perc,
                "Final Plan Statistics": plan_statistic,
            }
        else:
            json_files = []
            act_dict = dict()
            block_id = dict()
            ind_act = dict()
            label = 0
            for i, el in enumerate(ksg_for_val_data["schedule"]["works"]):
                act_dict[el["id"]] = el["display_name"]
                if el["display_name"] == "Окончание работ по марке":
                    label += 1
                elif el["display_name"] == "Начало работ по марке":
                    label += 1
                else:
                    block_id[el["id"]] = label
                    ind_act[el["id"]] = i
            block_id["0000000"] = label + 1
            json_file = {"schedule": {"works": []}, "wg": {"nodes": []}}
            label = block_id[list(block_id.keys())[0]]
            for k in block_id.keys():
                if block_id[k] == label:
                    ind_of_act = ind_act[k]
                    new_des_act = []
                    for el in ksg_for_val_data["wg"]["nodes"][ind_of_act][
                        "parent_edges"
                    ]:
                        if el[0] in block_id.keys():
                            if (
                                act_dict[el[0]] != "Окончание работ по марке"
                                and act_dict[el[0]] != "Начало работ по марке"
                            ):
                                if block_id[k] == block_id[el[0]]:
                                    new_des_act.append(el)
                    ksg_for_val_data["wg"]["nodes"][ind_of_act][
                        "parent_edges"
                    ] = new_des_act
                    json_file["schedule"]["works"].append(
                        ksg_for_val_data["schedule"]["works"][ind_of_act]
                    )
                    json_file["wg"]["nodes"].append(
                        ksg_for_val_data["wg"]["nodes"][ind_of_act]
                    )
                    label = block_id[k]
                else:
                    json_files.append(json_file)
                    if k == "0000000":
                        break
                    else:
                        json_file = {"schedule": {"works": []}, "wg": {"nodes": []}}
                        ind_of_act = ind_act[k]
                        new_des_act = []
                        for el in ksg_for_val_data["wg"]["nodes"][ind_of_act][
                            "parent_edges"
                        ]:
                            if el[0] in block_id.keys():
                                if (
                                    act_dict[el[0]] != "Окончание работ по марке"
                                    and act_dict[el[0]] != "Начало работ по марке"
                                ):
                                    if block_id[k] == block_id[el[0]]:
                                        new_des_act.append(el)
                        ksg_for_val_data["wg"]["nodes"][ind_of_act][
                            "parent_edges"
                        ] = new_des_act
                        json_file["schedule"]["works"].append(
                            ksg_for_val_data["schedule"]["works"][ind_of_act]
                        )
                        json_file["wg"]["nodes"].append(
                            ksg_for_val_data["wg"]["nodes"][ind_of_act]
                        )
                        label = block_id[k]
            for id_number, p in enumerate(json_files):
                plan = KSGDataset(
                    ksg_data=p, connector=self.connector, level=self.level
                ).collect()
                if len(plan["schedule"]["works"]) == 0:
                    continue
                else:
                    (
                        df_perc_agg_res,
                        df_final_volume_res,
                        df_final_style_res,
                        fig_dict_res,
                        df_vedom,
                        df_volume_stat,
                        dist_dict,
                        df_time_stat,
                        time_plot_dict,
                        df_seq_stat,
                        df_color_seq,
                        work_res_common_perc,
                        plan_statistic,
                    ) = GPNPlanValidator(
                        plan=p,
                        connector=self.connector,
                        level=self.level,
                        precalculated_brave=self.history_adapter.get_precalculated_brave_coefficients(),
                        links_history=self.history_adapter.get_links_history_messoyakha_with_new_granular_v2(),
                        journal=self.history_adapter.get_journal_mapped(),
                    ).validate()

                    result_dict["Object " + str(id_number)] = {
                        "Resource to Work Ratio": df_perc_agg_res,
                        "Work Pools Volumes": df_final_volume_res,
                        "Work Pools Colors": df_final_style_res,
                        "Data for Resource Charts": fig_dict_res,
                        "Resource Journal": df_vedom,
                        "Production Statistics": df_volume_stat,
                        "Data for Production Charts": dist_dict,
                        "Work Time Statistics": df_time_stat,
                        "Data for Time Charts": time_plot_dict,
                        "Connection Table": df_seq_stat,
                        "Color Connection Table": df_color_seq,
                        "Final Statistics for Work and Resources": work_res_common_perc,
                        "Final Plan Statistics": plan_statistic,
                    }
        return result_dict

    def calculate_expert_metrics(self):
        metrics_calculator = ExpertMetricsEstimator(self.project_ksg)
        metrics = metrics_calculator.calculate_metrics()
        formal_metrics = metrics_calculator.calculate_formal_metrics()
        return metrics, formal_metrics

    @staticmethod
    def _filter_activities(k, block_id, act_dict, ksg_for_val_data, ind_act):
        ind_of_act = ind_act[k]
        new_des_act = []
        for el in ksg_for_val_data["wg"]["nodes"][ind_of_act]["parent_edges"]:
            if el[0] in block_id.keys():
                if act_dict[el[0]] not in [
                    "Окончание работ по марке",
                    "Начало работ по марке",
                ]:
                    if block_id[k] == block_id[el[0]]:
                        new_des_act.append(el)
        ksg_for_val_data["wg"]["nodes"][ind_of_act]["parent_edges"] = new_des_act
        return ksg_for_val_data["schedule"]["works"][ind_of_act]

    def common_validation(self, cut_to_n_works: int = None):
        if cut_to_n_works:
            self._trim_plan_to_n_works(cut_to_n_works)

        (
            df_validation_table_res,
            fig_dict_res,
            norm_perc_res_val,
            not_perc_res_val,
            df_vedom,
            not_perc_vedom,
            norm_perc_vedom,
            df_validation_table_time,
            fig_dict_time,
            norm_perc_time,
            not_perc_time,
        ) = GPNPlanValidator(
            plan=self.project_ksg,
            connector=self.connector,
            level=self.level,
            precalculated_brave=self.history_adapter.get_precalculated_brave_coefficients(),
            links_history=self.history_adapter.get_links_history_messoyakha_with_new_granular_v2(),
            journal=self.history_adapter.get_journal_mapped(),
        ).common_validate()
        work_res_stat = dict()
        work_res_stat["Percentage of Normal Resource Volume Values"] = round(
            norm_perc_res_val
        )
        work_res_stat["Percentage of Atypical Resource Volume Values"] = 100 - round(
            norm_perc_res_val
        )
        work_res_stat["Percentage of Normal Resources According to Statements"] = round(
            norm_perc_vedom
        )
        work_res_stat[
            "Percentage of Atypical Resources According to Statements"
        ] = 100 - round(norm_perc_vedom)
        work_res_stat["Percentage of Normal Values Across All Resources"] = round(
            (
                work_res_stat["Percentage of Normal Resource Volume Values"]
                + work_res_stat[
                    "Percentage of Normal Resources According to Statements"
                ]
            )
            / 2
        )
        work_res_stat["Percentage of Atypical Values Across All Resources"] = (
            100 - work_res_stat["Percentage of Normal Values Across All Resources"]
        )
        work_res_stat["Percentage of Normal Work Time Values"] = round(norm_perc_time)
        work_res_stat["Percentage of Atypical Work Time Values"] = 100 - round(
            norm_perc_time
        )
        work_res_stat["Percentage of Normal Values Across All Works"] = round(
            norm_perc_time
        )
        work_res_stat["Percentage of Atypical Values Across All Works"] = 100 - round(
            norm_perc_time
        )
        work_res_stat["Percentage of Normal Plan Values"] = round(
            (
                work_res_stat["Percentage of Normal Values Across All Resources"]
                + work_res_stat["Percentage of Normal Values Across All Works"]
            )
            / 2
        )
        work_res_stat["Percentage of Atypical Plan Values"] = (
            100 - work_res_stat["Percentage of Normal Plan Values"]
        )
        work_res_stat["Percentage of Plan Values Not Covered by Validation"] = round(
            (not_perc_res_val + not_perc_vedom + not_perc_time) / 3
        )
        work_res_stat["Percentage of Plan Values Covered by Validation"] = 100 - round(
            (not_perc_res_val + not_perc_vedom + not_perc_time) / 3
        )

        result_dict = dict()
        result_dict["Common validation"] = {
            "Resources Validation Table": df_validation_table_res,
            "Data for Resource Charts": fig_dict_res,
            "Resource Journal": df_vedom,
            "Work Time Validation Table": df_validation_table_time,
            "Data for Time Charts": fig_dict_time,
            "Final Plan Statistics": work_res_stat,
        }
        return result_dict
