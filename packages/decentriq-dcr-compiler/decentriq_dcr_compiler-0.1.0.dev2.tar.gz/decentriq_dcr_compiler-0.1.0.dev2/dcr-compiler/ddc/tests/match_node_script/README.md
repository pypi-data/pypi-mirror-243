The match node tests are designed to test the validity of the matching script; which is executed inside a Docker container.

The tests can be run using the command:
```bash
poetry run pytest test_match.py
```

The following occurs when a test run is initiated using the above command:

1. The Docker container is built from the provided Dockerfile.
2. The Docker container is run with the `input` and `output` directories mounted into it.
3. The match script is executed inside the Docker container and the results are written into the `output` directory.

The contents of the output directory are evaluated for correctness by the relevant tests.