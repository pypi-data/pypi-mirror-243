#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-11-03 16:30:48
LastEditors  : Kofi
LastEditTime : 2023-11-03 16:30:50
Description  : 
"""


class BaseCommand:
    def parameterSearch(self, parames, name, nameValue, types="value") -> any:
        """github copilt 优化代码"""
        try:
            ret = next(p for p in parames if p[name] == nameValue)
            if types:
                return ret.get(types)
            return ret
        except StopIteration:
            return None

    def parameterSearchByName(self, parames, nameValue, types="value"):
        return self.parameterSearch(parames, "name", nameValue, types)
