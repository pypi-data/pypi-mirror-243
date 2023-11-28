# Contributing to VCD for Python

The VCD for Python source code is managed using Git and is hosted on GitLab.

Clone using SSH (provided you have configured a SSH key in Gitlab):
```bash
git clone git@gitlab.com:vicomtech/v4/libraries/vcd/vcd-python.git
```
Clone using HTTPS (you will need to type your GitLab username and password):

```bash
git clone https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python.git
```

## Reporting Bugs and Asking Questions

If you think you have encountered a bug in VCD for Python or have an idea for a new feature? Great! We like to hear from you!

There are several options to participate:

- Send us an email to the project's official Service Desk email address: contact-project+vicomtech-v4-libraries-vcd-vcd-python-35661666-issue-@incoming.gitlab.com. Tell us your ideas or ask your questions.
- Look into our GitLab [issues](https://gitlab.com/vicomtech/v4/libraries/vcd/vcd-python/-/issues) tracker or open a new issue.

## Prerequisites
Before you make changes to the code, we would highly appreciate if you consider the following general requirements:

- Make sure your code adheres to the [Semantic Versioning](https://semver.org/) specification.
- To warranty the best code quality, the VCD for Python project has been configured to use different formatting, linting and code checks to try to reduce as much many common mistakes. To enable this tools please install the development requirements:

    ```bash
    pip install -r requirements-dev.txt
    ```
This will install [pre-commit](https://pre-commit.com/) package (among others) which needs to be activated in the VCD root folder:

```bash
pre-commit install
```

## Modifying the Code

### Repository Structure:
The repository uses two permanent branches:

- _master_: This branch allocates the released stable versions.
- _develop_: This branch contains the development code that will be integrated in future releases.

### Adding features:
We recommend the following workflow:

1. Clone the repository locally.
2. Checkout the _develop_ branch.
3. (Optional): Create a new temporal branch that must start by: _feature/_ or _hotfix/_. e.g. _feature/my-feature_.
4. Add all changes to the code and corresponding tests.
5. Check all [tests run](#running-the-test-suite) correctly.
5. Add change notes using the CHANGELOG [procedure](#adding-a-changelog-entry)
6. When finished, commit the changes to git.
7. Create a merge request (MR) to develop.
8. When the MR is accepted and integrated, if a branch was created, remove it.

## Running the Test Suite
We use [pytest](https://docs.pytest.org/) and [tox](https://tox.wiki/) to run tests against all supported Python versions. All test dependencies are resolved automatically.

We **HIGHLY** encourage you to add tests for all your new implemented features and run the tests if you have changed any functionality before submitting your work.

You can decide to run the complete test suite or only part of it:

- To run all tests, use:

    ```bash
    tox
    ```

    If you have not all Python interpreters installed on your system it will probably give you some errors (```InterpreterNotFound```). To avoid such errors, use:

    ```bash
    tox --skip-missing-interpreters
    ```

    It is possible to use one or more specific Python versions. Use the -e option and one or more abbreviations (py38 for Python 3.8, py39 for Python 3.9 etc.):

    ```bash
    tox -e py37
    tox -e py37,py38
    ```

    To get a complete list and a short description, run:

    ```bash
    tox -av
    ```

## Run the Code Analysis
This code is checked against formatting, style, type, and docstring issues ([black](), [flake8](), [pylint](), [mypy](), and [docformatter]()). It is recommended to run your tests in combination with ```pre-commit``` checks, for example:

```bash
pre-commit run --all
```

## Documenting VCD for Python
Documenting the features of VCD is very important. It gives our developers an overview what is possible with VCD, how it "feels", and how it is used efficiently.

### Building the documentation

To build the documentation locally use the following command:

$ tox -e docs

The built documentation is available in [docs/pdoc/vcd](.docs/pdoc/vcd/index.html).

A new feature is not complete if it isn't properly documented. A good documentation includes:

- A **docstring**

    Each docstring contains a summary line in imperative mode ending in a period, a linebreak, an optional directive, the description of its arguments, returns and raises in [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). The docstring is extracted and reused by [pdoc](https://pdoc3.github.io/pdoc/) to extract the API documentation.

    An appropriate docstring should look like this:

    ```python
    def sum(a: int, b: int) -> int:
        """
        Sum two int values:

        This function takes the two int values and sum its values.

        e.g.
        ```
        val_1 = 30
        val_2 = 45
        result = sum(val_1, val_2)
        ```

        Args:
            a (int): First attribute.
            b (int): Second attribute.

        Returns:
            (int): The result of the sum
        """
    ```

- **Type Annotations**

    To help the developers to know the use of the classes and functions. It is recommended to type annotate all the functions.

    The VCD library is designed to follow [PEP 604](https://peps.python.org/pep-0604/). Therefore the type annotations can be written as ```X | Y```.

## Adding a Changelog Entry

If you make any change to the VCD library it is mandatory to add an entry in the library CHANGELOG. To do this we have enabled a mechanism to add distributed changes using the tool [towncrier](https://github.com/twisted/towncrier).

This tools allows to create small files in the folder [.changelog.d](./.changelog.d) than can be committed and pushed to git to be shared by other developers. Then when a new release is prepared the maintainer of the Library can use towncrier to automatically collect and build the updated CHANGELOG.md file

For detailed instructions on how to add entries to the Changelog check [here](.changelog.d/README.md).
