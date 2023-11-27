# Decentriq DCR Compiler (DDC)

## Publish

Whenever you change something in the data model exposted by DDC, run the
following command:

```
# generates schema json files
cargo build

# if run for the first time
poetry install

# generates typing files in python source dir
poetry run poe codegen-schema
```

Commit the schema files s.t. they will be included when the package
is published through CI.

Commits need to be tagged with e.g. `decentriq_dcr_compiler-v0.1.0`
for the CI pipeline to build the artifact.

## Debug mode

1. Go into your venv
2. `cd` into this directory
3. `maturin develop`
4. Maturin will now install the pacakge into your env
