#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# @Time    : 2023/9/25
# @Author  : yanxiaodong
# @File    : model_api_modelstore.py
"""


def get_name(workspace_id: str, model_store_name: str):
    """
    get name
    """
    return "workspaces/" + workspace_id + "/modelstores/" + model_store_name