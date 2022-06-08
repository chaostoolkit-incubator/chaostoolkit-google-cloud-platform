# -*- coding: utf-8 -*-
from collections import namedtuple

__all__ = ["GCPContext"]


GCPContext = namedtuple(
    "GCPContext", ["project_id", "cluster_name", "zone", "region"]
)
# allows optional fields
GCPContext.__new__.__defaults__ = (None,) * len(GCPContext._fields)
