import os
import functools
import json
import pandas as pd
import gc

SEGMENTS = "segments"
MATCHING = "matching"
EMBEDDINGS = "embeddings"
DEMOGRAPHICS = "demographics"

USER_ID_COLUMN = "user_id"
MATCHING_ID_COLUMN = "matching_id"
SEGMENT_COLUMN = "segment"
AGE_COLUMN = "age"
GENDER_COLUMN = "gender"
SCOPE_COLUMN = "scope"

CONFIG_PATH = os.environ["PDS_CONFIG_PATH"] if 'PDS_CONFIG_PATH' in os.environ else "/input/datalab_config.json"
RESULT_PATH = os.environ["PDS_RESULT_PATH"] if 'PDS_RESULT_PATH' in os.environ else "/output/statistics.json"

NA = "n/a"
ALL_USERS = "all"
SERIALIZATION_SEP = "||" # used to convert tuple keys into string keys for JSON serialization

def load_single(table, path):
    try:
        # In Data Lab the datasets are exposed as a table nodes
        import decentriq_util
        df = decentriq_util.read_tabular_data(path)
        n_cols = df.shape[1]
    except Exception as e:
        with open(path, 'r') as f:
          first_row = f.readline().strip()
          n_cols = len(first_row.split(','))
        if table == EMBEDDINGS:
            columns = [USER_ID_COLUMN, SCOPE_COLUMN] + ["v" + str(i) for i in range(n_cols-2)]
            usecols = [USER_ID_COLUMN]
        elif table == MATCHING:
            columns = [USER_ID_COLUMN, MATCHING_ID_COLUMN]
            usecols = [USER_ID_COLUMN]
        elif table == DEMOGRAPHICS:
            columns = [USER_ID_COLUMN, AGE_COLUMN, GENDER_COLUMN]
            usecols = columns
        elif table == SEGMENTS:
            columns = [USER_ID_COLUMN, SEGMENT_COLUMN]
            usecols = columns
        else:
            raise Exception("Unexpected table") 
        dtype = {c: str for c in columns}
        df = pd.read_csv(path, header=None, na_values=[], names=columns, dtype=dtype, usecols=usecols)

    return df, n_cols

def load_data(paths):
  
    dfs = { table: load_single(table, path)[0] for table, path in paths.items() if not table == EMBEDDINGS }

    # Drop all the embeddings data as it's unneeded
    if EMBEDDINGS in paths.keys():
        df_embeddings, n_cols = load_single(EMBEDDINGS, paths[EMBEDDINGS])
        # We test EMBEDDINGS to have user_id, scope, embeddings[] schema. Hence the way we compute n_embeddings below.
        n_embeddings = n_cols-2
        df_embeddings = df_embeddings[[USER_ID_COLUMN]]
        dfs[EMBEDDINGS] = df_embeddings
    else:
        n_embeddings = None
    
    return dfs, n_embeddings

def compute_unique_users(dfs):
    unique_users = { table: set(df[USER_ID_COLUMN]) for table, df in dfs.items() }
    unique_users[ALL_USERS] = functools.reduce(lambda s1, s2: s1.union(s2), unique_users.values())
    return unique_users

# Potential for suboptimal memory usage
def filter_dfs(dfs, considered_users):
    for k in dfs.keys():
        dfs[k] = dfs[k][dfs[k][USER_ID_COLUMN].isin(considered_users)]
    return dfs

def check_errors(dfs, n_embeddings, test_config):
    errors = []
    if SEGMENTS in dfs.keys():
        n_segments = dfs[SEGMENTS][SEGMENT_COLUMN].nunique()
        if n_segments > test_config["max_segments"]:
            s = "ERROR: At most {} distinct segments are supported, found {}.".format(test_config["max_segments"], n_segments)
            errors.append(s)
        if n_segments < test_config["min_segments"]:
            s = "ERROR: At least {} distinct segments are required, found {}.".format(test_config["min_segments"], n_segments)
            errors.append(s)
    else:
        errors.append("ERROR: Require Segment data.")

    if not MATCHING in dfs.keys():
        errors.append("ERROR: Require Matching data.")

    if DEMOGRAPHICS in dfs.keys():
        n_age_values = dfs[DEMOGRAPHICS][AGE_COLUMN].nunique()
        n_gender_values = dfs[DEMOGRAPHICS][GENDER_COLUMN].nunique()
        if n_age_values > test_config["max_age_values"]:
            s = "ERROR: At most {} distinct age values are supported, found {}.".format(test_config["max_age_values"], n_age_values)
            errors.append(s)
        if n_gender_values > test_config["max_gender_values"]:
            s = "ERROR: At most {} distinct gender values are supported, found {}.".format(test_config["max_gender_values"], n_gender_values)
            errors.append(s)

    if EMBEDDINGS in dfs.keys():
        if n_embeddings > test_config["max_embeddings"]:
            s = "ERROR: At most {} distinct embeddings are supported, found {}.".format(test_config["max_embeddings"], n_embeddings)
            errors.append(s)
        if n_embeddings < test_config["min_embeddings"]:
            s = "ERROR: At least {} distinct embeddings are required, found {}.".format(test_config["min_embeddings"], n_embeddings)
            errors.append(s)

    return errors

def compute_distributions(dfs, considered_users, digits):
    # Compute number of segments per user distribution for all considered users and only the matchable (and considered) users. Returns a dictionary
    # - keys: number_of_segments_per_user
    # - values: (share_of_all_users, share_of_matchable_users)
    def segments_per_user_distribution(dfs, considered_users):
        # 1) Compute distribution for all considered users
        n_considered_users = len(considered_users)
        spu = {number_of_segments_per_user: float(number_of_occ)/n_considered_users
               for number_of_segments_per_user, number_of_occ in dfs[SEGMENTS][USER_ID_COLUMN].value_counts().value_counts().items()}

        # These are the users that are considered, but do not appear in segments -> They appear in the 0 bucket
        spu[0] = 1 - sum(spu.values())

        keys = list(spu.keys())
        for i in range(1, max(keys)):
            if i not in keys:
                spu[i] = 0.0

        # 2) Compute distribution for matchable (and considered) users
        considered_matchable_users = dfs[MATCHING][USER_ID_COLUMN].unique()
        n_considered_matchable_users = len(considered_matchable_users)
        df_segments_matchable = dfs[SEGMENTS][dfs[SEGMENTS][USER_ID_COLUMN].isin(considered_matchable_users)]
        spu_auth = {number_of_segments_per_user: float(number_of_occ)/n_considered_matchable_users
                    for number_of_segments_per_user, number_of_occ in df_segments_matchable[USER_ID_COLUMN].value_counts().value_counts().items()}

        # These are the users that are matchable, but do not appear in segments -> They appear in the 0 bucket
        spu_auth[0] = 1 - sum(spu_auth.values())

        # 3) Combine (note that every key in spu_auth is guaranteed to be in spu by construction)
        spu_final = {}
        for k, v in spu.items():
            spu_final[k] = (round(v, digits), round(spu_auth[k], digits) if k in spu_auth.keys() else 0.0)

        return spu_final

    def share_of_users_per_segment(dfs):
        n_users = len(considered_users)
        sups = {segment: round(float(number_of_users)/n_users, digits)
                for segment, number_of_users in dfs[SEGMENTS][SEGMENT_COLUMN].value_counts().items()}
        return sups

    # Compute demographics distribution for all considered users and only the matchable (and considered) users. Returns a dictionary
    # keys: (age_value, gender_value)
    # values: (share_of_all_users, share_of_matchable_users)
    def demographics_distribution(dfs, considered_users):

        # 1) Compute distribution for all considered users
        n_considered_users = len(considered_users)
        ags = {(k[0] if len(k[0])>0 else NA, k[1] if len(k[1])>0 else NA): float(v)/n_considered_users
               for k, v in dfs[DEMOGRAPHICS][[AGE_COLUMN, GENDER_COLUMN]].value_counts().items()}

        # These are the users that are considered, but do not appear in demographics -> They appear in the (NA, NA) bucket
        ags[(NA, NA)] = 1 - sum(ags.values())

        # 2) Compute distribution for matchable (and considered) users
        considered_matchable_users = set(dfs[MATCHING][USER_ID_COLUMN])
        n_considered_matchable_users = len(considered_matchable_users)
        df_demographics_matchable = dfs[DEMOGRAPHICS][dfs[DEMOGRAPHICS][USER_ID_COLUMN].isin(considered_matchable_users)]
        ags_auth = {number_of_segments_per_user: float(number_of_occ)/n_considered_matchable_users
                    for number_of_segments_per_user, number_of_occ in df_demographics_matchable[[AGE_COLUMN, GENDER_COLUMN]].value_counts().items()}

        # These are the users that are matchable, but do not appear in demographics -> They appear in the (NA, NA) bucket
        ags_auth[(NA, NA)] = 1 - sum(ags_auth.values())

        # 3) Combine (note that every key in ags_auth is guaranteed to be in ags by construction)
        ags_final = {}
        for k, v in ags.items():
            ags_final[k] = (round(v, digits), round(ags_auth[k], digits) if k in ags_auth.keys() else 0.0)

        return ags_final

    spu = segments_per_user_distribution(dfs, considered_users)
    sups = share_of_users_per_segment(dfs)
    ags = demographics_distribution(dfs, considered_users) if DEMOGRAPHICS in dfs.keys() else None

    return spu, sups, ags

def compute_statistics(paths, test_config):
    # Load data for the provided paths
    dfs, n_embeddings = load_data(paths)

    # Compute the original unique users
    original_unique_users = compute_unique_users(dfs)
    original_number_of_unique_users = {k: len(v) for k, v in original_unique_users.items()}

    # Select the considered users (see Notion for the rationale). This is a bit an ugly recompute but allows original_unique_users (hopefully) to be gc'ed (otherwise it probably keeps a reference count, apparently even with .copy())
    considered_users = set(dfs[EMBEDDINGS][USER_ID_COLUMN]) if EMBEDDINGS in original_unique_users.keys() else set(dfs[SEGMENTS][USER_ID_COLUMN])
    
    del original_unique_users # This is a big object, let's get rid of it
    gc.collect()
    
    # Filter to keep only the considered users. Inplace modification for memory.
    dfs = filter_dfs(dfs, considered_users)

    # Compute the filtered unique users
    filtered_unique_users = compute_unique_users(dfs)
    filtered_number_of_unique_users = {k: len(v) for k, v in filtered_unique_users.items()}
    
    del filtered_unique_users  # This is a big object, let's get rid of it
    gc.collect()
    
    # If errors is non-empty, we should stop here
    errors = check_errors(dfs, n_embeddings, test_config)

    # Compute segment and demographics distributions
    spu, sups, ags = compute_distributions(dfs, considered_users, digits=4) if len(errors) == 0 else (None, None, None)

    # Build result JSON object
    return {
        "errors": errors,
        "original_number_of_unique_users": original_number_of_unique_users,
        "filtered_number_of_unique_users": filtered_number_of_unique_users,
        "segments_per_user_distributions": spu if spu else None,
        "share_of_users_per_segment_distribution": sups if sups else None,
        "demographics_distributions": {f"{k[0]}{SERIALIZATION_SEP}{k[1]}": v for k, v in ags.items()} if ags else None # JSON cannot deal with tuple-keys    
      }



if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("No data lab config provided")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

paths = {
    SEGMENTS: config["dataset_segments"]["path"],
    MATCHING: config["dataset_users"]["path"]
}

if "dataset_embeddings" in config:
    paths[EMBEDDINGS] = config["dataset_embeddings"]["path"]
if "dataset_demographics" in config:
    paths[DEMOGRAPHICS] = config["dataset_demographics"]["path"]

statistics_config = {
    "max_age_values": 20,
    "max_gender_values": 5,
    "max_segments": 2000,
    "min_segments": 10,
    "max_embeddings": 200,
    "min_embeddings": 10,
}

result = compute_statistics(paths, statistics_config)

with open(RESULT_PATH, "w") as f:
    f.write(json.dumps(result))
