# -*- coding: utf-8 -*-
from typing import NamedTuple, Optional

__all__ = ["GCPContext"]


class GCPContext(NamedTuple):
    project_id: str = None
    cluster_name: str = None
    zone: str = None
    region: str = None
    parent: str = None

    def get_parent(self) -> Optional[str]:
        if self.parent:
            return self.parent

        parent = None
        if self.region:
            parent = f"project/{self.project_id}/locations/{self.region}"

        return parent

    def get_cluster_parent(self) -> Optional[str]:
        parent = self.get_parent()
        if parent and self.cluster_name:
            return f"{parent}/clusters/{self.cluster_name}"

    def get_operation_parent(self, op_name: str) -> str:
        return (
            f"projects/{self.project_id}/locations/{self.zone}"
            f"/operations/{op_name}"
        )
