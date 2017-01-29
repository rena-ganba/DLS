from itertools import islice
import csv, sys
import copy
from transform import *


class Schema(object):
    def __init__(self, csv_file_path, header=False):
        self.csv_file_path = csv_file_path
        header_row = [col.strip() for col in Schema._read_n_rows(self.csv_file_path, 1)[0]]
        if header:
            duplicates = set([x for x in header_row if header_row.count(x) > 1])
            if len(duplicates) > 0:
                raise Exception("Should be no duplicates in CSV header: " + ", ".join([col for col in duplicates]))
            self._columns = [Schema.Column(item, [index]) for index, item in enumerate(header_row)]
        else:
            self._columns = [Schema.Column('col_' + str(index), [index]) for index in range(0, len(header_row))]

    @staticmethod
    def _read_n_rows(csv_file_path, rows_number):
        rows = []
        with open(csv_file_path, 'rb') as f:
            reader = csv.reader(f)
            try:
                for row in islice(reader, 0, rows_number):
                    rows.append(row)
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (csv_file_path, reader.line_num, e))

        return rows

    class Column(object):
        def __init__(self, name, columns_indexes):
            self._name = name
            # CSV corresponding columns indexes
            self._columns_indexes = columns_indexes

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            self._name = name

        @property
        def columns_indexes(self):
            return self._columns_indexes

        @columns_indexes.setter
        def columns_indexes(self, columns_indexes):
            self._columns_indexes = columns_indexes

    def __setitem__(self, old_name, new_name):
        columns = [c.name for c in self._columns]
        if old_name!= new_name and columns.count(new_name) > 0:
            raise Exception("Should be no duplicates in columns: " + new_name)
        for column in self._columns:
            if column.name == old_name:
                column.name = new_name.strip()

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, columns):
        l = len(columns)
        if (l > len(self._columns)) or (l < len(self._columns)):
            raise Exception("Passed columns number: %d is not compatible with Schema current columns number: %d"
                            % (l, len(self._columns)))
        duplicates = set([x for x in columns if columns.count(x) > 1])
        if len(duplicates) > 0:
            raise Exception("Should be no duplicates in columns: " + ", ".join([col for col in duplicates]))
        for index, item in enumerate(columns):
            self._columns[index].name = item.strip()

    def drop_column(self, column_name):
        for index, column in enumerate(copy.deepcopy(self._columns)):
            if column.name == column_name:
                self._columns.remove(self._columns[index])

    def merge_columns(self, new_column_name, columns_to_merge):
        if not isinstance(columns_to_merge, list):
            raise TypeError("Arg columns_to_merge should be list")
        columns_indexes = []
        for column in copy.deepcopy(self._columns):
            if column.name in columns_to_merge:
                columns_indexes.append(column.columns_indexes)
                self.drop_column(column.name)
        self._columns.append(Schema.Column(new_column_name, columns_indexes))

    def merge_columns_in_range(self, new_column_name, range=()):
        if not isinstance(range, tuple):
            raise TypeError("Arg range should be Tuple")
        if range[0] >= range[1]:
            raise Exception("Start index of the range can't be higher or equal than end index")
        if range[0] < 0 or range[1] >= len(self._columns):
            raise Exception("Range is out of length of schema, last schema index: %d" % (len(self._columns) - 1))
        columns_indexes = []
        for index, column in enumerate(copy.deepcopy(self._columns)):
            if range[0] <= index <= range[1]:
                columns_indexes.append(column.columns_indexes)
                self.drop_column(column.name)
        self._columns.append(Schema.Column(new_column_name, columns_indexes))

    def print_columns(self):
        print ", ".join([col.name for col in self._columns])

    def print_data(self):
        print "First 10 records:"
        for row in Schema._read_n_rows(self.csv_file_path, 10):
            print row


class Input(object):
    def __init__(self, schema):
        if not isinstance(schema, Schema):
            raise TypeError("Must be set to an Schema")
        self._schema = schema
        self._transforms = {}

    class Builder(object):
        def __init__(self, config):
            pass

        def build(self):
            pass

    class ColumnTransform(object):
        def __init__(self, column, pre_transforms, post_transforms, reader=None):
            self._column = column
            self._pre_transforms = pre_transforms
            self._post_transforms = post_transforms
            self._reader = reader

        @property
        def column(self):
            return self._column

        @property
        def pre_transforms(self):
            return self._pre_transforms

        @property
        def post_transforms(self):
            return self._post_transforms

        @property
        def reader(self):
            return self._reader

    def columns_transforms(self):
        return self._transforms

    def transform_column(self, column_name, pre_transforms=[], post_transforms=[], reader=None):
        column = self._find_column(column_name)
        if column is None:
            raise Exception("No column with such name %s" % (column_name))
        Input.check_transform_arg(pre_transforms, "pre_transforms")
        Input.check_transform_arg(post_transforms, "post_transforms")
        self._transforms[column_name] = Input.ColumnTransform(column, pre_transforms, post_transforms, reader)

    @staticmethod
    def check_transform_arg(transform_param, arg_name):
        if isinstance(transform_param, list):
            if not all(issubclass(t.__class__, Transform) for t in transform_param):
                raise Exception("Arg %s should be list of Transform class instances" % arg_name)
        elif not issubclass(transform_param.__class__, Transform):
            raise Exception("Arg %s should be Transform class instance" % arg_name)

    def _find_column(self, column_name):
        for column in self._schema.columns:
            if column.name == column_name:
                return column
        return None
