# `compass_data_challenge`: Repository for Compass Pokemon Data Challenge, 11/23/2019

## Environment Prerequisites

-   UNIX-like operating system
-   Installation of `docker` (I am testing with `docker` version 19.03.5, build
    633a0ea)
-   Installation of `git` (I am testing with `git` version 2.14.3)

## Getting Started

1.  `git` clone the directory to local filesystem:

    ```bash
    git clone https://github.com/yingw787/compass_data_challenge /path/to/compass_data_challenge/
    cd /path/to/compass_data_challenge/
    ```

2.  Execute the runfile to generate results:

    ```bash
    source ./run.sh
    ```

## Notes

-   Explanations on problem understanding and how I arrived at a particular
    conclusion are present within module docstrings.

## Design Principles

-   **Reproducible, Hermetic Builds**: I used Docker to reduce any discrepancies
    in correctness behavior due to environment shifts. I also used an
    `environment.yaml` lockfile with strict versioning in order to guarantee
    versioning compatibility, especially with dependency resolution.

    If this was an enterprise setting, it may be appropriate to lock down the
    image ID hashcode and build out additional tooling / infrastructure around
    updating the hash based on what is available on the remote Docker images
    repository.

-   **Lean Environments**: I used native libraries where possible, and paid
    attention to which dependencies were critically necessary to the
    satisfaction of problem requirements. Having fewer dependencies means faster
    versioning and better alignment with the latest generally available
    dependency builds, fewer correctness issues due to dependency errors and
    less need to upstream changes and communicate with third parties, and leaner
    build sizes which may improve resource utilization.

    If this was an enterprise setting, I might compartmentalize which
    dependencies were necessary for different staging environments, such as
    dev/test/alpha/beta/canary/prod, along with other improvements.

-   **Optimizing for Read Load**: Since the data is ingested once, and since
    multiple queries may be run on this data, I structured the data to make each
    request as cheap as possible in order to amortize read load, while also
    sticking to the data representation in the third-party API when necessary.

    If this was an enterprise setting, I might apply materialized views on top
    of query results for OLAP workloads, and let the database stream results to
    a client. This may involve using a query explainer tool to examine how the
    view refreshes, which may change the optimum data model.

-   **Value Simplicity**: I designed the data model to answer the questions
    directly, trading off simplicity for extensibility where not needed may
    count as premature optimization. When possible, I avoid usage of magic
    strings/numbers and make the code as self-documenting and the mental model
    as semantic as possible. I could apply a process pool and parallelize the
    query execution and HTTP requests as the ingest pipeline is heavily
    I/O-bound, however this may make debugging trickier and complicate the error
    model, as runtime-based scheduling results in non-determinism.
