from shutil import copytree, ignore_patterns
copytree("/input/match_results", "/output", dirs_exist_ok=True, ignore=ignore_patterns('dataset.csv'))
