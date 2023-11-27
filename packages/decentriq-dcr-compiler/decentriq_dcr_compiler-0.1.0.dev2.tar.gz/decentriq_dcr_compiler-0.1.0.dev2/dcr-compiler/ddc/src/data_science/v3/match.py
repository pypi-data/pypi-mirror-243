"""
The purpose of this script is to perform an inner join on two tables.
If multiple matching columns are provided, the join is performed in a
"waterfall" fashion. That is, the first join is performed using the first
matching column pairs followed by additional joins using the remaining matching
columns. Positive matches at each stage are omited from the subsequent stages.
Columns that match on NULLs are disregarded and will remain in the datasets for
subsequent match stages.
"""

import pandas as pd
from pandas import DataFrame
import json, os, sys, csv, numpy
import decentriq_util
from decentriq_util.error import catch_safe_error, SafeError
from typing import List, Tuple, cast, TypedDict, Set, Dict


class MatchNodeError(SafeError):
    """
    Class for exceptions raised by this node that can be safely
    turned into a string which doesn't contain sensitive data.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def safe_str(self) -> str:
        """
        Return a safe string representation of this exception
        that does not include any sensitive data.
        """
        return str(self)


class MatchingComputeNodeConfig(TypedDict):
    query: List[str]
    round: int
    epsilon: int
    sensitivity: int
    dependency_paths: List[str]


class DataSet:
    dependency_path: str
    raw: bool
    dataframe: DataFrame
    match_columns: List[str]

    def __init__(self, dependency_path):
        self.raw = os.path.isfile(dependency_path)
        self.dependency_path = dependency_path
        self.dataframe = self.__init_dataframe(self.raw)

    def name(self) -> str:
        return os.path.basename(self.dependency_path)

    def get_dataframe(self) -> DataFrame:
        return self.dataframe

    def set_match_columns(self, match_columns: List[str]):
        self.match_columns = match_columns

    def get_match_columns(self) -> List[str]:
        return self.match_columns

    def __init_dataframe(self, raw: bool) -> DataFrame:
        if raw:
            return pd.read_csv(self.dependency_path)
        else:
            # We cannot just use `decentriq_util.sql.read_sql_data_from_dir()` here because
            # empty "int" values get dropped which affects the statistics that we generate
            # for the user. Instead, we manually construct the DataFrame ensuring that any
            # "int" columns are converted to the nullable int type "Int64".
            # Reference: https://stackoverflow.com/questions/21287624/convert-pandas-column-containing-nans-to-dtype-int

            data_file = os.path.join(self.dependency_path, "dataset.csv")
            schema_file = os.path.join(self.dependency_path, "types")
            types: List[
                Tuple[str, numpy.dtype]
            ] = decentriq_util.sql._get_numpy_dtypes_for_table_schema(schema_file)

            column_names = list(map(lambda t: t[0], types))
            df: DataFrame = pd.read_csv(data_file, names=column_names, dtype=str)
            for idx, (column_name, column_type) in enumerate(types):
                if pd.api.types.is_integer_dtype(column_type):
                    # Cast to a nullable int.
                    df[column_name] = df[column_name].astype("Int64")
            return df

    # Returns 'True' if all match columns are in the dataset
    def contains_match_columns(self, match_columns: List[str]) -> bool:
        dataset_columns = self.get_dataframe().columns
        return set(match_columns).issubset(dataset_columns)


class Naming:
    dataset_1_suffix = "_ds1"
    dataset_2_suffix = "_ds2"
    dataset_1_table_name = ""
    dataset_2_table_name = ""
    results_table_name = "results"

    def __init__(self, dataset_1_table_name: str, dataset_2_table_name: str) -> None:
        self.dataset_1_table_name = dataset_1_table_name
        self.dataset_2_table_name = dataset_2_table_name

    def get_dataset_1_suffix(self) -> str:
        return self.dataset_1_suffix

    def get_dataset_2_suffix(self) -> str:
        return self.dataset_2_suffix

    def get_dataset_1_table_name(self) -> str:
        return self.dataset_1_table_name

    def get_dataset_2_table_name(self) -> str:
        return self.dataset_2_table_name

    def get_results_table_name(self) -> str:
        return self.results_table_name


class MatchedRows:
    operation: str
    left_args: List[str]
    right_args: List[str]
    matched_rows: int

    def __init__(
        self,
        operation: str,
        left_args: List[str],
        right_args: List[str],
        rows: int,
        naming: Naming,
    ) -> None:
        self.operation = operation
        self.left_args = list(
            map(lambda arg: arg.removesuffix(naming.get_dataset_1_suffix()), left_args)
        )
        self.right_args = list(
            map(lambda arg: arg.removesuffix(naming.get_dataset_2_suffix()), right_args)
        )
        self.matched_rows = rows

    def get_query(self) -> str:
        assert len(self.left_args) == len(self.right_args)
        query = str()
        if self.operation == "and":
            for i in range(0, len(self.left_args)):
                query += f"{self.left_args[i]}={self.right_args[i]} AND "
            query = query.rsplit(" ", 2)[0]
        elif self.operation == "==":
            query += f"{self.left_args[0]}={self.right_args[0]}"
        else:
            raise MatchNodeError(f"MatchedRows does not support {self.operation} operation")
        return query

    def num_matched_rows(self) -> int:
        return self.matched_rows


class IOperation:
    def __init__(self) -> None:
        pass

    def get_match_columns(self) -> Tuple[List[str], List[str]]:
        pass

    def get_compound_keys(self) -> Tuple[List[List[str]], List[List[str]]]:
        pass

    def execute_query(
        self,
        left_dataset: DataFrame,
        right_dataset: DataFrame,
        naming: Naming,
    ) -> Tuple[DataFrame, DataFrame, DataFrame, List[MatchedRows]]:
        pass


class EqualsOp(IOperation):
    arg1: str
    arg2: str

    def __init__(self, arg1: str, arg2: str) -> None:
        super().__init__()
        self.arg1 = EqualsOp.__get_normalised_variable(arg1)
        self.arg2 = EqualsOp.__get_normalised_variable(arg2)

    def get_match_columns(self) -> Tuple[List[str], List[str]]:
        return ([self.arg1], [self.arg2])

    def get_compound_keys(self) -> Tuple[List[List[str]], List[List[str]]]:
        return ([[self.arg1]], [[self.arg2]])

    def execute_query(
        self,
        left_dataset: DataFrame,
        right_dataset: DataFrame,
        naming: Naming,
    ) -> Tuple[DataFrame, DataFrame, DataFrame, List[MatchedRows]]:
        match_column_left = list()
        match_column_right = list()
        match_column_left.append(self.arg1 + naming.get_dataset_1_suffix())
        match_column_right.append(self.arg2 + naming.get_dataset_2_suffix())
        (result, new_left_dataset, new_right_dataset) = execute_match(
            left_dataset,
            right_dataset,
            match_column_left,
            match_column_right,
            naming,
        )
        matched_rows = MatchedRows(
            "==", match_column_left, match_column_right, result.shape[0], naming
        )
        return (result, new_left_dataset, new_right_dataset, [matched_rows])

    def __get_normalised_variable(var: str) -> str:
        return var.split(".")[1]


class AndOp(IOperation):
    def __init__(self, query: str) -> None:
        super().__init__()
        self.operations = list()

        for sub_query in query:
            for operation in sub_query:
                if operation == "and":
                    self.operations.append(AndOp(sub_query[operation]))
                elif operation == "==":
                    self.operations.append(
                        EqualsOp(
                            sub_query[operation][0]["var"],
                            sub_query[operation][1]["var"],
                        )
                    )
                else:
                    raise MatchNodeError(f"Unsupported operation {operation}")

    def get_match_columns(self) -> Tuple[List[str], List[str]]:
        match_columns_left: List[str] = list()
        match_columns_right: List[str] = list()
        for op in self.operations:
            (match_left, match_right) = op.get_match_columns()
            match_columns_left.extend(match_left)
            match_columns_right.extend(match_right)
        return (match_columns_left, match_columns_right)

    def get_compound_keys(self) -> Tuple[List[List[str]], List[List[str]]]:
        compound_left = list()
        compound_right = list()
        for op in self.operations:
            (cl, cr) = op.get_compound_keys()
            for item in cl:
                compound_left.extend(item)
            for item in cr:
                compound_right.extend(item)
        return ([compound_left], [compound_right])

    def execute_query(
        self,
        left_dataset: DataFrame,
        right_dataset: DataFrame,
        naming: Naming,
    ) -> Tuple[DataFrame, DataFrame, DataFrame, List[MatchedRows]]:
        match_columns_left = list()
        match_columns_right = list()
        for op in self.operations:
            (left_args, right_args) = op.get_match_columns()
            for arg in left_args:
                match_columns_left.append(arg + naming.get_dataset_1_suffix())
            for arg in right_args:
                match_columns_right.append(arg + naming.get_dataset_2_suffix())
        (result, new_left_dataset, new_right_dataset) = execute_match(
            left_dataset,
            right_dataset,
            match_columns_left,
            match_columns_right,
            naming,
        )
        matched_rows = MatchedRows(
            "and", match_columns_left, match_columns_right, result.shape[0], naming
        )
        return (result, new_left_dataset, new_right_dataset, [matched_rows])


class OrOp(IOperation):
    operations: List[IOperation] = list()

    def __init__(self, query: str) -> None:
        super().__init__()
        for sub_query in query:
            for operation in sub_query:
                if operation == "and":
                    self.operations.append(AndOp(sub_query[operation]))
                elif operation == "==":
                    self.operations.append(
                        EqualsOp(
                            sub_query[operation][0]["var"],
                            sub_query[operation][1]["var"],
                        )
                    )
                else:
                    raise MatchNodeError(f"Unsupported operation {operation}")

    def get_match_columns(self) -> Tuple[List[str], List[str]]:
        match_columns_left: List[str] = list()
        match_columns_right: List[str] = list()
        for op in self.operations:
            (match_left, match_right) = op.get_match_columns()
            match_columns_left.extend(match_left)
            match_columns_right.extend(match_right)
        return (match_columns_left, match_columns_right)

    def get_compound_keys(self) -> Tuple[List[List[str]], List[List[str]]]:
        compound_left = list()
        compound_right = list()
        for op in self.operations:
            (cl, cr) = op.get_compound_keys()
            compound_left.extend(cl)
            compound_right.extend(cr)
        return (compound_left, compound_right)

    def execute_query(
        self,
        left_dataset: DataFrame,
        right_dataset: DataFrame,
        naming: Naming,
    ) -> Tuple[DataFrame, DataFrame, DataFrame, List[MatchedRows]]:
        result = pd.DataFrame()
        unmatched_ld = left_dataset
        unmatched_rd = right_dataset
        num_matched_rows: List[MatchedRows] = list()
        # Execute sub queries and append results
        for op in self.operations:
            (tmp_result, unmatched_ld, unmatched_rd, matched_rows) = op.execute_query(
                unmatched_ld, unmatched_rd, naming
            )
            result = pd.concat([result, tmp_result])
            num_matched_rows.extend(matched_rows)
        return (result, unmatched_ld, unmatched_rd, num_matched_rows)


class Query(IOperation):
    # A query has a single root operation.
    operation: IOperation

    def __init__(self, query: str) -> None:
        super().__init__()
        for operation in query:
            if operation == "or":
                op = OrOp(query[operation])
                self.operation = op
            elif operation == "and":
                self.operation = AndOp(query[operation])
            elif operation == "==":
                self.operation = EqualsOp(query["=="][0]["var"], query["=="][1]["var"])
            else:
                raise MatchNodeError(f"Unsupported operation {operation}")

    # The order of the match columns assumes that the UI always keeps the match
    # columns of the first dataset on the left of the query and the match columns
    # of the second dataset on the right of the query.
    def get_match_columns(self) -> Tuple[List[str], List[str]]:
        match_columns_left: List[str] = list()
        match_columns_right: List[str] = list()
        (match_left, match_right) = self.operation.get_match_columns()
        match_columns_left.extend(match_left)
        match_columns_right.extend(match_right)
        return (match_columns_left, match_columns_right)

    def get_compound_keys(self) -> Tuple[List[List[str]], List[List[str]]]:
        return self.operation.get_compound_keys()

    def execute_query(
        self, left_dataset: DataFrame, right_dataset: DataFrame, naming: Naming
    ) -> Tuple[DataFrame, DataFrame, DataFrame, List[MatchedRows]]:
        return self.operation.execute_query(left_dataset, right_dataset, naming)


def get_datasets(cfg: MatchingComputeNodeConfig) -> List[DataSet]:
    datasets = list()
    for dependency_path in cfg["dependency_paths"]:
        path = os.path.join("/input", dependency_path)
        assert os.path.exists(path)
        datasets.append(DataSet(path))
    return datasets


# Empty datasets are indicative of a dry run.
def is_dry_run(datasets: List[DataSet]) -> bool:
    for dataset in datasets:
        if os.path.isfile(dataset.dependency_path):
            if os.path.getsize(dataset.dependency_path) > 0:
                return False
        else:
            data_file = os.path.join(dataset.dependency_path, "dataset.csv")
            if os.path.getsize(data_file) > 0:
                return False
    return True


def get_overlapping_columns(columns1: List[str], columns2: List[str]) -> Set[str]:
    return set(columns1).intersection(columns2)


def rename_columns(
    df: DataFrame, overlapping_columns: Set[str], naming: Naming
) -> DataFrame:
    for column in overlapping_columns:
        df = df.rename(
            columns={
                f"{column}{naming.get_dataset_1_suffix()}": f"{column}_{naming.get_dataset_1_table_name()}"
            }
        )
        df = df.rename(
            columns={
                f"{column}{naming.get_dataset_2_suffix()}": f"{column}_{naming.get_dataset_2_table_name()}"
            }
        )
    df.columns = df.columns.str.removesuffix(naming.get_dataset_1_suffix())
    df.columns = df.columns.str.removesuffix(naming.get_dataset_2_suffix())
    return df


# Execute the matching logic.
# All matches, excluding NULL matches, are returned in the result.
# The non-matched rows are returned as the new "left" and "right" datasets. Which can
# be used for subsequent matches.
def execute_match(
    left_dataset: DataFrame,
    right_dataset: DataFrame,
    match_columns_left: List[str],
    match_columns_right: List[str],
    naming: Naming,
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    outer_join_result = pd.merge(
        left_dataset,
        right_dataset,
        how="outer",
        left_on=match_columns_left,
        right_on=match_columns_right,
        indicator=True,
    )
    match_result = outer_join_result.loc[outer_join_result["_merge"] == "both"].drop(
        "_merge", axis=1
    )

    unmatched_left_dataset = (
        outer_join_result.loc[outer_join_result["_merge"] == "left_only"]
        .drop("_merge", axis=1)
        .drop(
            list(outer_join_result.filter(regex=naming.get_dataset_2_suffix())), axis=1
        )
    )
    unmatched_right_dataset = (
        outer_join_result.loc[outer_join_result["_merge"] == "right_only"]
        .drop("_merge", axis=1)
        .drop(
            list(outer_join_result.filter(regex=naming.get_dataset_1_suffix())), axis=1
        )
    )

    # Filter out rows which have NULLs in their matching columns.
    # We only need to loop over "match_columns_left" because, if the value
    # is NULL, then it must be NULL in "match_columns_right" for the match
    # to have included it.
    null_match_results = DataFrame()
    for column in match_columns_left:
        null_match_results = pd.concat(
            [null_match_results, match_result.loc[match_result[column].isnull()]]
        )
        match_result = match_result.loc[match_result[column].notnull()]

    # Add the null rows back to the left and right datasets
    null_match_left = null_match_results.drop(
        list(null_match_results.filter(regex=naming.get_dataset_2_suffix())), axis=1
    )
    unmatched_left_dataset = pd.concat([unmatched_left_dataset, null_match_left])

    null_match_right = null_match_results.drop(
        list(null_match_results.filter(regex=naming.get_dataset_1_suffix())), axis=1
    )
    unmatched_right_dataset = pd.concat([unmatched_right_dataset, null_match_right])

    return (match_result, unmatched_left_dataset, unmatched_right_dataset)


# Ensure uniqueness of compound keys when matching.
def validate_input(dataset: DataSet, compound_keys: List[Tuple[str, str]]):
    dataframe = dataset.get_dataframe()
    for keys in compound_keys:
        df = dataframe.replace("", numpy.nan)
        keys_list = list(keys)
        non_null_dataframe = df.dropna(subset=keys_list)
        num_unique = non_null_dataframe[keys_list].drop_duplicates().shape[0]
        num_rows = non_null_dataframe.shape[0]
        if num_unique == 0:
            raise MatchNodeError(
                f"Table {dataset.name()}, Group ({get_compound_dict_keys(keys)}) has no unique values"
            )
        elif num_unique != num_rows:
            raise MatchNodeError(
                f"Table {dataset.name()}, Group ({get_compound_dict_keys(keys)}) included non-unique values."
            )


# Generate statistics related to the input datasets.
def generate_input_statistics(
    dataset: DataSet,
    compound_keys: List[Tuple[str, str]],
    table_name: str,
):
    dataframe = dataset.get_dataframe()
    match_columns = dataset.get_match_columns()

    statistics: List[str] = list()
    statistics.append(["", "Number of rows", dataframe.shape[0]])

    # Single key statistics
    for column in match_columns:
        non_null_column = dataframe[column].dropna()
        statistics.append([column, "Number of unique keys", non_null_column.nunique()])
        statistics.append(
            [column, "Number of keys without NULLs", len(non_null_column)]
        )

    # Compound key statistics
    dict_keys = list(map(lambda k: get_compound_dict_keys(k), compound_keys))
    compound_statistics: Dict[str, int] = dict.fromkeys(dict_keys, 0)
    for index, row in dataframe.iterrows():
        for keys in compound_keys:
            null_value = False
            for key in keys:
                if pd.isna(row[key]):
                    null_value = True
                    break
            # Count the number of non-NULL values
            if not null_value:
                key = get_compound_dict_keys(keys)
                compound_statistics[key] += 1

    compound_key_number = 1
    for k, v in compound_statistics.items():
        key = f"({k})"
        statistics.append(
            [f"Compound Key {compound_key_number} {key}", "Number of compound keys without NULLs", v]
        )
        compound_key_number += 1

    with open(f"/output/{table_name}_statistics.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(statistics)


def get_compound_dict_keys(values: List[List[str]]) -> str:
    return ",".join(map(str, values))


def generate_output_schema(dataset1: DataSet, dataset2: DataSet, naming: Naming):
    dataframe1 = dataset1.get_dataframe()
    dataframe2 = dataset2.get_dataframe()
    overlapping_columns = get_overlapping_columns(
        list(dataframe1.columns), list(dataframe2.columns)
    )

    for column in overlapping_columns:
        dataframe1 = dataframe1.rename(
            columns={column: f"{column}_{naming.get_dataset_1_table_name()}"}
        )
        dataframe2 = dataframe2.rename(
            columns={column: f"{column}_{naming.get_dataset_2_table_name()}"}
        )

    types = pd.concat([dataframe1, dataframe2])
    for column in types:
        # If the type is a nullable int, cast to a regular int.
        # `decentriq_utils` doesn't support nullable ints.
        if types[column].dtype == "Int64":
            types[column] = types[column].fillna(0).astype("int64")
    decentriq_util.sql.write_sql_data_to_dir(types, "/output")


def add_noise_and_round(value: int, config: MatchingComputeNodeConfig) -> int:
    round_value = config["round"]
    epsilon = config["epsilon"]
    sensitivity = config["sensitivity"]
    p = 1 - numpy.exp(-epsilon / sensitivity)
    noise = numpy.random.geometric(p) - numpy.random.geometric(p)
    return int(numpy.rint((value + noise) / round_value) * round_value)


def generate_result_outputs(
    dataset1: DataSet,
    dataset2: DataSet,
    query: Query,
    config: str,
    naming: Naming,
):
    dataframe1 = dataset1.get_dataframe()
    df1_suffix = dataframe1.add_suffix(naming.get_dataset_1_suffix())
    dataframe2 = dataset2.get_dataframe()
    df2_suffix = dataframe2.add_suffix(naming.get_dataset_2_suffix())

    matched_rows: List[MatchedRows] = list()
    # Add suffixes to the tables column names to ensure uniqueness between tables.
    # This prevents the merge from renaming the column headers automatically.
    (result, lhs, rhs, matched_rows) = query.execute_query(
        df1_suffix, df2_suffix, naming
    )

    # Ensure the input and output column types match.
    # Pandas join has a tendency to convert `int` columns to `float` columns.
    for column in df1_suffix.columns:
        if pd.api.types.is_integer_dtype(df1_suffix[column].dtypes):
            result[column] = result[column].fillna(0).astype("int64").to_frame()
    for column in df2_suffix.columns:
        if pd.api.types.is_integer_dtype(df2_suffix[column].dtypes):
            result[column] = result[column].fillna(0).astype("int64").to_frame()

    overlapping_columns = get_overlapping_columns(
        list(dataframe1.columns), list(dataframe2.columns)
    )

    # Output results table
    result = rename_columns(result, overlapping_columns, naming)
    decentriq_util.sql.write_sql_data_to_dir(result, "/output")

    # Output statistics
    statistics: List[str] = list()
    statistics.append(
        ["", "Approx. number of rows", add_noise_and_round(result.shape[0], config)]
    )

    for i in range(0, len(matched_rows)):
        statistics.append(
            [
                f"Group {i+1} ({matched_rows[i].get_query()})",
                "Approx. number of result rows matched by this condition",
                add_noise_and_round(matched_rows[i].num_matched_rows(), config),
            ]
        )
    with open(f"/output/results_statistics.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(statistics)


# Ensure the matching columns match to the correct dataframe.
def set_dataframes(
    datasets: List[DataSet], match_columns_1: List[str], match_columns_2: List[str]
) -> List[DataSet]:
    if datasets[0].contains_match_columns(match_columns_1):
        datasets[0].set_match_columns(match_columns_1)
        assert datasets[1].contains_match_columns(match_columns_2)
        datasets[1].set_match_columns(match_columns_2)
    else:
        assert datasets[0].contains_match_columns(match_columns_2)
        datasets[0].set_match_columns(match_columns_2)
        assert datasets[1].contains_match_columns(match_columns_1)
        datasets[1].set_match_columns(match_columns_1)
    return datasets


"""
Business Logic
"""

with catch_safe_error():
    with open("/input/matching_node_config.json", "r") as file:
        try:
            config: MatchingComputeNodeConfig = cast(
                MatchingComputeNodeConfig, json.loads(file.read())
            )
        except:
            raise MatchNodeError("Failed to parse JSON config for Match node")

    datasets = get_datasets(config)
    assert len(datasets) == 2

    naming = Naming(datasets[0].name().lower(), datasets[1].name().lower())

    if is_dry_run(datasets):
        generate_output_schema(datasets[0], datasets[1], naming)
        # Generate empty dataset.
        open("/output/dataset.csv", 'a').close()
    else:
        query = Query(config["query"])
        (match_columns_dataset1, match_columns_dataset2) = query.get_match_columns()

        datasets = set_dataframes(datasets, match_columns_dataset1, match_columns_dataset2)
        (compound_keys_left, compound_keys_right) = query.get_compound_keys()
        validate_input(datasets[0], compound_keys_left)
        validate_input(datasets[1], compound_keys_right)

        generate_input_statistics(
            datasets[0],
            compound_keys_left,
            naming.get_dataset_1_table_name(),
        )
        generate_input_statistics(
            datasets[1],
            compound_keys_right,
            naming.get_dataset_2_table_name(),
        )

        generate_result_outputs(datasets[0], datasets[1], query, config, naming)
