from abc import ABC, abstractmethod

from idbadapter.field_dev import FieldDevHistoryAdapter


class BaseValidator(ABC):
    """Abstract Base Validator class."""

    def __init__(self, project_ksg, history_adapter: FieldDevHistoryAdapter = None):
        self.project_ksg = project_ksg
        self.history_adapter = history_adapter

        self._preprocess_project()

    @abstractmethod
    def common_validation(self, *args, **kwargs):
        """Common validation logic for all plans."""
        pass

    @abstractmethod
    def specific_validation(self):
        """Method to be overridden for plan-specific validation."""
        pass

    def _preprocess_project(self):
        # Names to be removed
        names_to_remove = {"start of project", "start"}

        # Remove works with specified names from the schedule
        self.project_ksg["schedule"]["works"] = [
            work
            for work in self.project_ksg["schedule"]["works"]
            if work.get("name") not in names_to_remove
        ]

        # Get the IDs of the removed works
        removed_ids = {
            work["id"]
            for work in self.project_ksg["schedule"]["works"]
            if work.get("name") in names_to_remove
        }

        # Remove nodes with specified names from the wg graph
        self.project_ksg["wg"]["nodes"] = [
            node
            for node in self.project_ksg["wg"]["nodes"]
            if node.get("work_unit", {}).get("name") not in names_to_remove
        ]

        # Update parent_edges in the remaining nodes to remove references to deleted works
        for node in self.project_ksg["wg"]["nodes"]:
            if "parent_edges" in node["work_unit"]:
                node["work_unit"]["parent_edges"] = [
                    edge
                    for edge in node["work_unit"]["parent_edges"]
                    if edge["str"] not in removed_ids
                ]

    def _trim_plan_to_n_works(self, n):
        if n >= len(self.project_ksg["schedule"]["works"]):
            return  # No trimming needed as n is greater than or equal to the number of works

        # Step 1: Identify the IDs of the first N works to keep
        keep_ids = set(work["id"] for work in self.project_ksg["schedule"]["works"][:n])

        # Step 2: Keep only the first N works in the schedule
        self.project_ksg["schedule"]["works"] = self.project_ksg["schedule"]["works"][
            :n
        ]

        # Step 3: Keep only the first N nodes in the wg graph
        self.project_ksg["wg"]["nodes"] = [
            node
            for node in self.project_ksg["wg"]["nodes"]
            if node["work_unit"]["id"] in keep_ids
        ]

        # Step 4: Update parent_edges in the remaining nodes
        for node in self.project_ksg["wg"]["nodes"]:
            if "parent_edges" in node["work_unit"]:
                node["work_unit"]["parent_edges"] = [
                    edge
                    for edge in node["work_unit"]["parent_edges"]
                    if edge["str"] in keep_ids
                ]
