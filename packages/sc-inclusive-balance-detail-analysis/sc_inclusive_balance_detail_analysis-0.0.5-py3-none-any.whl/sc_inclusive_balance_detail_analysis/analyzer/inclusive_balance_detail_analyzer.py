#  The MIT License (MIT)
#
#  Copyright (c) 2023. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import logging

import numpy as np
import pandas as pd
from config42 import ConfigManager

from sc_inclusive_balance_detail_analysis.manifest_utils import ManifestUtils
from .base_analyzer import BaseAnalyzer


class InclusiveBalanceDetailAnalyzer(BaseAnalyzer):
    """
    普惠相关数据余额明细分析
    """

    def __init__(self, *, config: ConfigManager, excel_writer: pd.ExcelWriter):
        self._client_adjustments = dict()
        super().__init__(config=config, excel_writer=excel_writer)
        self._key_enabled = "inclusive.balance_detail.enabled"
        self._key_business_type = "inclusive.balance_detail.business_type"
        self._key_export_column_list = "inclusive.balance_detail.sheet_config.export_column_list"

    def _read_config(self, *, config: ConfigManager):
        self._src_filepath = config.get("inclusive.balance_detail.source_file_path")
        adjustments_config = config.get("inclusive.balance_detail.client_adjustments")
        if adjustments_config is not None and type(adjustments_config) == list:
            for adjustment in adjustments_config:
                result = [x.strip() for x in adjustment.split(':')]
                if len(result) != 3:
                    continue
                client_no = result[0]
                manager_a = result[1]
                manager_b = result[2]
                if client_no not in self._client_adjustments:
                    self._client_adjustments[client_no] = dict()
                self._client_adjustments[client_no][manager_a] = manager_b

        self._header_row = config.get("inclusive.balance_detail.sheet_config.header_row")
        # 客户编号列索引
        self._client_no_column = self._calculate_column_index_from_config(
            config, "inclusive.balance_detail.sheet_config.client_no_column"
        )
        # 客户经理列索引
        self._name_column = self._calculate_column_index_from_config(
            config, "inclusive.balance_detail.sheet_config.name_column"
        )
        # 考核口径普惠贷款列索引
        self._is_inclusive_column = self._calculate_column_index_from_config(
            config, "inclusive.balance_detail.sheet_config.is_inclusive_column"
        )
        # 考核口径普惠贷款列过滤值
        self._is_inclusive_column_value = config.get(
            "inclusive.balance_detail.sheet_config.is_inclusive_column_value"
        )
        # 是否过滤贷款业务品种
        filter_loan_product_config = config.get(
            "inclusive.balance_detail.sheet_config.is_filter_loan_product"
        )
        self._is_filter_loan_product = False if filter_loan_product_config is None else filter_loan_product_config
        # 贷款业务品种列索引
        self._loan_product_column = self._calculate_column_index_from_config(
            config, "inclusive.balance_detail.sheet_config.loan_product_column"
        )
        # 贷款业务品种列过滤值（列出需要保留的贷款业务品种）
        loan_product_list_config = config.get(
            "inclusive.balance_detail.sheet_config.loan_product_list"
        )
        self._loan_product_list = list()
        if loan_product_list_config is not None and type(loan_product_list_config) == list:
            self._loan_product_list.extend(loan_product_list_config)
        # 广州分行公共名称
        self._gz_common_account = config.get("branch.gz_common_account")
        # 需要统计的列的索引与输出列名对
        key = "inclusive.balance_detail.sheet_config.value_column_pairs"
        self._init_value_column_config(config, key)

    def _read_src_file(self) -> pd.DataFrame:
        logging.getLogger(__name__).info("读取源文件：{}".format(self._src_filepath))
        data = pd.read_csv(self._src_filepath, header=self._header_row)
        self._client_no_column_name = data.columns[self._client_no_column]
        self._name_column_name = data.columns[self._name_column]
        self._is_inclusive_column_name = data.columns[self._is_inclusive_column]
        self._loan_product_column_name = data.columns[self._loan_product_column]
        self._init_value_column_pairs(data)
        data[self._client_no_column_name] = data[self._client_no_column_name].apply(lambda x: x.replace("'", ""))
        return data

    def _add_export_column_manifest_branch(self, origin_data: pd.DataFrame):
        if origin_data is None or origin_data.empty:
            return origin_data
        # 与花名册整合，添加花名册所在部门一列
        data = origin_data.merge(
            ManifestUtils.get_name_branch_data_frame(),
            how="left",
            left_on=[self._name_column_name],
            right_on=[ManifestUtils.get_name_column_name()]
        )
        return data

    def _rename_target_columns(self, *, data: pd.DataFrame) -> pd.DataFrame:
        return data.rename(columns=self._value_column_pairs)

    def _pre_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        # 过滤考核口径普惠贷款
        criterion1 = data[self._is_inclusive_column_name].map(lambda x: x == self._is_inclusive_column_value)
        data = data[criterion1].copy()
        # 过滤贷款业务品种
        if self._is_filter_loan_product:
            criterion2 = data[self._loan_product_column_name].map(lambda x: x in self._loan_product_list)
            data = data[criterion2].copy()

        # 做客户对应的客户经理的替换
        for row_i, row in data.iterrows():
            client_no = row[self._client_no_column_name]
            if client_no not in self._client_adjustments.keys():
                continue
            manager_pair_dict = self._client_adjustments[client_no]
            manager_name = row[self._name_column_name]
            if manager_name not in manager_pair_dict.keys():
                continue
            data.at[row_i, self._name_column_name] = manager_pair_dict[manager_name]
            logging.getLogger(__name__).info("第 {} 行，客户号 {} 的客户经理从 {} 改为了 {}".format(
                row_i + 1,
                client_no,
                manager_name,
                manager_pair_dict[manager_name],
            ))
        return data

    def _pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        index_columns = [self._name_column_name]
        value_columns = self._get_value_columns()
        logging.getLogger(__name__).info("按{} 透视数据项：{}".format(
            index_columns,
            value_columns,
        ))
        if data.empty:
            return pd.DataFrame(columns=index_columns + value_columns)
        table = pd.pivot_table(
            data,
            values=value_columns,
            index=index_columns,
            aggfunc=np.sum,
            fill_value=0
        )
        return table

    def _after_pivot_table(self, *, data: pd.DataFrame) -> pd.DataFrame:
        return data.reset_index()

    def _merge_with_manifest(self, *, manifest_data: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
        logging.getLogger(__name__).info("与花名册合并...")
        merge_result = ManifestUtils.merge_with_manifest(
            manifest_data=manifest_data, data=data,
            name_column_name=self._name_column_name
        )
        return merge_result

    def _drop_duplicated_columns(self, *, data: pd.DataFrame) -> pd.DataFrame:
        return data.drop(columns=[self._name_column_name])

    def _add_target_columns(self) -> None:
        self._add_value_pair_target_columns()
