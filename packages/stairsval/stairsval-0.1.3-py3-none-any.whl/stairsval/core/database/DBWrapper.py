import pandas as pd

from stairsval.core.database.Adapter import DBAdapter
from stairsval.core.database.DataSource import DataSource


class DBWrapper(DataSource):
    def __init__(self, connector=None, level=None):
        # Default value for connector if not provided
        if connector is None:
            connector = DBAdapter
        # Default value for level if not provided
        if level is None:
            level = connector.GRANULARY

        self.adapter = connector
        self.level = level

    def get_data(self, pools, res_names):
        validation_dataset_list = []
        for df in self.adapter.get_works_by_pulls(
            work_pulls=pools,
            resource_list=res_names,
            key=self.level,
            res_key=self.adapter.GRANULARY,
        ):
            if df is not None:
                df.fillna(0, inplace=True)
            validation_dataset_list.append(df)
        return validation_dataset_list

    def get_act_names(self):
        df = self.adapter.get_all_works_name()
        return df

    def get_res_names(self):
        df = self.adapter.get_all_resources_name()
        return df

    def get_time_data(self, acts):
        frames = []
        for p in self.adapter.from_names(
            works=acts, key=self.level, objects_limit=-1, ceil_limit=-1
        ):
            frames.append(p)
        validation_dataset = pd.DataFrame()
        for df in frames:
            validation_dataset = pd.concat([validation_dataset, df])
        validation_dataset = validation_dataset[
            ["granulary_name", "physical_volume", "start_date", "finish_date"]
        ]
        validation_dataset.dropna(inplace=True)
        validation_dataset = validation_dataset.loc[
            validation_dataset["granulary_name"].isin(acts)
        ]
        validation_dataset.reset_index(inplace=True, drop=True)
        validation_dataset[["start_date", "finish_date"]] = validation_dataset[
            ["start_date", "finish_date"]
        ].apply(pd.to_datetime)
        validation_dataset["Time"] = (
            validation_dataset["finish_date"] - validation_dataset["start_date"]
        )
        validation_dataset["Time"] = validation_dataset["Time"].dt.days
        validation_dataset = validation_dataset.drop(
            columns=["start_date", "finish_date"]
        )
        validation_dataset.columns = ["Work", "Volume", "Time"]
        return validation_dataset
