# Contributing to Hyperledger Sawtooth Hyper Directory

This document covers how to report issues and contribute code.

## Topics

* [Reporting Issues](#reporting-issues)
* [Contributing Code](#contributing-code)

## Reporting Issues

This is a great way to contribute. Before reporting an issue, please review
current open issues to see if there are any matches.

### How to Report an Issue

Issues should be reported to this project's Github Issues page: [https://github.com/hyperledger/sawtooth-hyper-directory/issues](https://github.com/hyperledger/sawtooth-hyper-directory/issues)

When reporting an issue, please provide as much detail as possible about how
to reproduce it. If possible, provide instructions for how to reproduce the
issue within the vagrant development environment. There is a pre-built template for bug ticketing that can be used for reporting.  

Details are key. Please include the following:

* OS version
* Hyper Directory version
* Environment details (virtual, physical, etc.)
* Steps to reproduce
* Actual results
* Expected results

## Contributing Code

Hyperledger Sawtooth Hyper Directory is Apache 2.0 licensed and accepts
contributions via [GitHub](https://github.com/hyperledger/) pull requests.

### Ways to Contribute

Contributions by the community help grow and optimize the capabilities of
Hyperledger Sawtooth, and are the most effective method of having a positive
impact on the project.

#### Different ways you can contribute

* Bugs or Issues (issues or defects found when working with Sawtooth Hyper Directory)
* Core Features & Enhancements (expanded capabilities or optimization)
* New or Enhanced Documentation (improve existing documentation or create new)
* Testing Events and Results (functional, performance or scalability)

### Commit Process

Hyperledger Sawtooth Hyper Directory is Apache 2.0 licensed and accepts
contributions via GitHub pull requests. When contributing code please do the
following:

* Fork the repository and make your changes in a feature branch.
* Please include new or update existing PlantUML sequence/architecture diagrams
  that relate to your PR. See `./docs/diagrams/src/README.md` for details on how
  we maintain our diagrams)
* Please include unit and integration tests for any new features and update any
  existing tests that are impacted by the change. For more information on how to write tests please refer to [Testing Guidelines](#testing-guidelines) below.
* Please ensure the unit and integration tests run successfully. Refer to the
  Testing section in `/README.md` on how to run these tests.
* Please ensure that lint passes by running `./bin/run_lint`. The linter requires
  all Python dependencies be installed locally in a virtual environment, as detailed
  in the [developer setup](https://sawtooth-next-directory.readthedocs.io/en/latest/developer-setup.html)
  (if not it'll throw import-errors). Install dependencies locally by running
  `pip3 install -r requirements.txt` from the root project directory.

### Coding style & Standards (Python)

Please ensure that any contributions comply with the following:

* Our linter is set to comply with PEP 8, any Python contributions should follow
  the authoritative definitions [here](https://www.python.org/dev/peps/pep-0008/)
  * A friendlier version (though not authoritative) is available [here](https://realpython.com/python-pep8/).  
* Docstrings loosely follows Google's python styleguide which extends
  PEP 257. 
    * Docstrings should begin and end with triple quotes (""")
    * Summary and parameter definitions should be separated by a New Line
    * Args and Returns should be defined 
    * An example follows:
    ```
    def function(next_id):
    """ The function takes in a next_id and returns the next_id.
    
    Args:
     next_id:
          str: Id of a user in NEXT
    Returns:  string of a user's Id
    """
    return next_id
    ```
  * Details on Google's styleguide [here](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings).
  * Documentation of [PEP 257](https://www.python.org/dev/peps/pep-0257).

### Testing Guidelines

*  Docstrings will be formatted with a summary, a new line, and then args/returns. See the example in the above section.
* Internal testing folder structure will imitate the app so it is easy to locate tests for a specific file.
These are the folders below the top level folders. External testing folder (top level folders) structure to be as follows:
    ```
    tests
        | _ e2e
        | _ integration
        | _ unit
        | _ utilities
    ```
* Test file names will end in 's' (be plural). Example: role_api_tests.py.
* Where possible pytest parameterization will be used to be able to generalize the tests and increase unique use cases being tested in the system.
* Where possible, test cases will be limited to one per test (or test run if utilizing parameterization).
* There will be no additional annotation outside of doctrings for seperation or explanation purposes.
* Where possible tests will use pre-loaded data to decrease test run time of testing.
* Utilities will be split by use case and will have the following structure:
    ```
    utilities
        | _ creation
        | _ db_queries
        | _ deletion
        | _ fixtures
        | _ test_data
        | _ update
    ```
* Our goal is to get to and maintain 70% coverage over the project. Each pull request should have tests that test the new feature and gets to/maintains 70% or higher.
* If data manipulation occurs in a test, a tear down function must be used to reset the data before the start of the next test.
* __ init__.py files will not contain code

#### Pull Request Guidelines

Pull requests can contain a single commit or multiple commits. The most
important part is that **a single commit maps to a single fix or enhancement**.

Here are a few scenarios:

* If a pull request adds a feature but also fixes two bugs, then the pull
  request should have three commits, one commit each for the feature and two bug
  fixes.
* If a PR is opened with 5 commits that was work involved to fix a single issue,
  it should be rebased to a single commit.
* If a PR is opened with 5 commits, with the first three to fix one issue and
  the second two to fix a separate issue, then it should be rebased to two
  commits, one for each issue.
* Your pull request should be rebased against the current master branch. Please
  do not merge the current master branch in with your topic branch, nor use the
  Update Branch button provided by GitHub on the pull request page.

#### Commit Messages

Commit messages should follow common Git conventions, such as the imperative
mood, separate subject lines, and a line-length of 72 characters. These rules
are well documented by Chris Beam in his [blog post on the subject](https://chris.beams.io/posts/git-commit/)
and summarized by the 7 rules of a great git commit message:

```markdown
1. Separate subject from body with a blank line.
2. Limit the subject line to 50 characters.
3. Capitalize the subject line.
4. Do not end the subject line with a period.
5. Use the imperative mood in the subject line.
6. Wrap the body at 72 characters.
7. Use the body to explain what and why vs. how.
```

#### Signed-off-by

Commits must include Signed-off-by in the commit message (git commit -s). This
indicates that you agree the commit satisfies the Developer Certificate of
Origin (DCO).

#### Version Tracking

Each release to master includes a semantic version number in `/VERSION`.
As of Jan/9/2019 we use Semantic Versioning 2.0.0 as described [here](https://semver.org/).

A basic summary of Semantic Versioning is:

<pre>
Given a version number <b>MAJOR</b>.<b>MINOR</b>.<b>PATCH</b>, increment the:

  1. <b>MAJOR</b> version when you make incompatible API changes.
  2. <b>MINOR</b> version when you add functionality in a backwards-compatible manner.
  3. <b>PATCH</b> version when you make backwards-compatible bug fixes.

Additional labels for pre-release and build metadata are available as extensions
to the <b>MAJOR</b>.<b>MINOR</b>.<b>PATCH</b> format.
</pre>

### Important GitHub Requirements

**PLEASE NOTE**: Pull requests can only be merged after they have passed all
status checks.

These checks are:

* The PR must be approved by at least two reviewers and there cannot be
  outstanding changes requested.
* Travis must pass, meaning tests, formatting, and linting must pass
