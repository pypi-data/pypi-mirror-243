from typing import TypedDict, List, cast, Dict
import json, csv, subprocess, pandas, faker, numpy, random, pytest
from pandas import DataFrame

simpleQuery = {"==": [{"var": "123.email"}, {"var": "456.email"}]}
compoundQuery = {
    "and": [
        {"==": [{"var": "123.address"}, {"var": "456.address"}]},
        {"==": [{"var": "123.postcode"}, {"var": "456.postcode"}]},
    ]
}


class MatchingComputeNodeConfig(TypedDict):
    query: List[str]
    round: int
    epsilon: int
    sensitivity: int
    dependency_paths: List[str]


def parameterise_cfg(round: int, epsilon: int, sensitivity: int, query=compoundQuery):
    config = MatchingComputeNodeConfig()
    config["query"] = query
    config["round"] = round
    config["epsilon"] = epsilon
    config["sensitivity"] = sensitivity
    config["dependency_paths"] = ["/input/table1", "/input/table2"]

    with open("./input/matching_node_config.json", "w") as file:
        file.write(json.dumps(config))


fake = faker.Faker()


def fake_int():
    # helper function to convert binary faker functionality to an int
    return int(fake.sha1()[0:7], 16)


"""
A mapping that allows us to get a function capable of generating fake data
of the correct type given an english description
"""
mask_functions = {
    "Generic Int": fake_int,
    "Generic String": fake.sha1,
    "Name": fake.name,
    "Address": fake.street_address,
    "Postcode": fake.postcode,
    "Phone Number": fake.phone_number,
    "Social Security Number": fake.ssn,
    "Email": fake.ascii_email,
    "Date": fake.date,  # TODO: allow different formats
    "Timestamp": fake.unix_time,
    "IBAN": fake.iban,
}


def gen_table(size=0, cols=None) -> DataFrame:
    df = pandas.DataFrame()
    for col_name, col_func in cols.items():
        df[col_name] = [col_func() for _i in range(size)]
    return df


def gen_input_tables(
    overlap_size=0,
    left_size=0,
    right_size=0,
    join_keys=None,
    left_cols=None,
    right_cols=None,
):
    # TODO: none of these will handle name collisions correctly
    left_table = gen_table(size=left_size - overlap_size, cols=join_keys | left_cols)
    right_table = gen_table(size=right_size - overlap_size, cols=join_keys | right_cols)
    overlap_rows = gen_table(size=overlap_size, cols=join_keys | right_cols | left_cols)
    left_table = left_table.append(overlap_rows[list(left_table.columns)])
    right_table = right_table.append(overlap_rows[list(right_table.columns)])
    return {
        "left": left_table.sample(frac=1).reset_index(drop=True),
        "right": right_table.sample(frac=1).reset_index(drop=True),
    }


def setup_module():
    rc = subprocess.call("./build.sh")
    assert rc == 0


def run(input_tables: Dict[str, DataFrame]):
    input_tables["left"].to_csv("./input/table1", index=False)
    input_tables["right"].to_csv("./input/table2", index=False)
    rc = subprocess.call("./run.sh")
    assert rc == 0


def test_results_statistics_rounding():
    dataset_sizes = [10, 20, 50, 100]
    epsilon = 20
    expected_results = {}
    for size in dataset_sizes:
        overlap_size = random.randint(0, size)
        round = int(size / 2)
        input_tables = gen_input_tables(
            overlap_size=overlap_size,
            left_size=int(size / 2),
            right_size=size,
            join_keys={
                "email": fake.ascii_email,
                "address": fake.street_address,
                "postcode": fake.postcode,
            },
            left_cols={"account_number": fake_int},
            right_cols={"product_code": fake.iban},
        )

        # Expected result.
        expected_num_rows = int(numpy.rint(overlap_size / round) * round)
        expected_results["Number of rows"] = expected_num_rows
        expected_results[
            "Number of result rows matched by this condition"
        ] = expected_num_rows

        # Set noise (epsilon) to zero so we only test the rounding is correct.
        parameterise_cfg(round, epsilon, 1)
        run(input_tables)

        # Verify statistics
        with open("./output/results_statistics.csv", "r") as file:
            rdr = csv.reader(file)
            for row in rdr:
                assert int(row[2]) == expected_results[row[1]]


def test_results_statistics_noise():
    input_tables = gen_input_tables(
        overlap_size=5,
        left_size=20,
        right_size=40,
        join_keys={
                "email": fake.ascii_email,
                "address": fake.street_address,
                "postcode": fake.postcode,
            },
        left_cols={"account_number": fake_int},
        right_cols={"product_code": fake.iban},
    )

    parameterise_cfg(1, 10, 10)

    results: Dict[List[int]] = {
        "Number of rows": [],
        "Number of result rows matched by this condition": [],
    }
    for i in range(0, 5):
        run(input_tables)
        with open("./output/results_statistics.csv", "r") as file:
            rdr = csv.reader(file)
            for row in rdr:
                results[row[1]].append(int(row[2]))

    for result in results.values():
        # Check that the result has a number of values due to
        # the addition of noise.
        # The conversion to a set ensures unique values.
        assert len(set(result)) > 1


def test_input_statistics():
    table_sizes = [10, 20, 50, 100]
    join_keys = {
        "email": fake.ascii_email,
        "address": fake.street_address,
        "postcode": fake.postcode,
    }
    expected_results_table_left = {}
    expected_results_table_right = {}
    for size in table_sizes:
        input_tables = gen_input_tables(
            overlap_size=5,
            left_size=int(size / 2),
            right_size=size,
            join_keys=join_keys,
            left_cols={"account_number": fake_int},
            right_cols={"product_code": fake.iban},
        )

        table_left: DataFrame = input_tables["left"]
        table_right: DataFrame = input_tables["right"]

        # Expected results.
        expected_results_table_left["Number of rows"] = table_left.shape[0]
        expected_results_table_right["Number of rows"] = table_right.shape[0]
        for key in join_keys:
            expected_results_table_left["Number of unique keys"] = table_left[
                key
            ].nunique()
            expected_results_table_left["Number of keys without NULLs"] = len(
                table_left[key].dropna()
            )
            expected_results_table_left[
                "Number of compound keys without NULLs"
            ] = len(table_left[key].dropna())

            expected_results_table_right["Number of unique keys"] = table_right[
                key
            ].nunique()
            expected_results_table_right["Number of keys without NULLs"] = len(
                table_right[key].dropna()
            )
            expected_results_table_right[
                "Number of compound keys without NULLs"
            ] = len(table_right[key].dropna())

        # Parameterisation doesn't affect the input statistics.
        parameterise_cfg(5, 20, 1)
        run(input_tables)

        # Verify statistics.
        with open("./output/table1_statistics.csv", "r") as file:
            rdr = csv.reader(file)
            for row in rdr:
                assert int(row[2]) == expected_results_table_left[row[1]]

        with open("./output/table2_statistics.csv", "r") as file:
            rdr = csv.reader(file)
            for row in rdr:
                assert int(row[2]) == expected_results_table_right[row[1]]
