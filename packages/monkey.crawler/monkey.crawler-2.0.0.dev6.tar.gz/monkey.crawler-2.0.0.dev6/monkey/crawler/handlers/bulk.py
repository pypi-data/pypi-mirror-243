# -*- coding: utf-8 -*-
import collections.abc
from monkey.crawler.op_codes import OpCode
from monkey.crawler.processor import Handler


class BulkInjector(Handler):
    """Injects a key/value map into records.
    """

    def __init__(self, field_map: dict):
        """Initializes the handler.
        :param field_map: a key/value map to inject
        """
        super().__init__()
        self.field_map: dict = {} if field_map is None else field_map

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the evaluation of the expression and store the formatted value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the evaluated value in the target field
        :return: the operation code depending on the expression evaluation
        """
        rec = record.copy()
        BulkInjector._merge_data(rec, self.field_map)
        return rec, op_code

    @staticmethod
    def _merge_data(d, u):
        result = d.copy()
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                result[k] = BulkInjector._merge_data(d.get(k, {}), v)
            else:
                result[k] = v
        return result


class FieldValueMapper(Handler):
    """Injects or replaces a field value into handled record regarding a value map for specified field. The handler can
    update the operation code depending on the specified field has a match in the value map or not.
    """

    def __init__(self, field_name: str, value_map: dict, result_field_name: str = None, use_default_value: bool = False,
                 default_value=None, on_match_op_code: OpCode = None, on_no_match_op_code: OpCode = None):
        """Initializes the handler.
        :param field_name: the name of the field to inspect to lookup for a value match
        :param value_map: the value map
        :param result_field_name: the name of the field that will store the matching value. If name is None, the value
        will replace the original one in the inspected field.
        :param use_default_value: indicates whether the default value should be used on no match
        :param default_value: the default value to use in case of no match
        :param on_match_op_code: the operation code to return if there is a match in the value table
        :param on_no_match_op_code: the operation code to return if no match is found
        """
        super().__init__()
        self.field_name: str = field_name
        self.value_map: dict = value_map
        self.result_field_name = result_field_name
        self.use_default_value = use_default_value
        self.default_value = default_value
        self.on_match_op_code = on_match_op_code
        self.on_no_match_op_code = on_no_match_op_code

    def handle(self, record: dict, op_code: OpCode = None) -> (dict, OpCode):
        """Performs the evaluation of the expression and store the formatted value in the specified target field.
        :param record: the record to validate
        :param op_code: the operation code computed by any previous operation
        :return: a copy of the provided record that contains the evaluated value in the target field
        :return: the operation code depending on the expression evaluation
        """
        rec = record.copy()
        value = self.default_value
        matched = False
        try:
            key = rec[self.field_name]
            value = self.value_map[key]
            matched = True
            op_code = op_code if self.on_match_op_code is None else self.on_match_op_code
        except KeyError:
            op_code = op_code if self.on_no_match_op_code is None else self.on_no_match_op_code
        if matched or (not matched and self.use_default_value):
            if self.result_field_name is not None:
                rec[self.result_field_name] = value
            else:
                rec[self.field_name] = value
        return rec, op_code