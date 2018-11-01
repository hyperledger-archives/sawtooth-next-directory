# Contributing to Hyperledger Sawtooth Hyper Directory

This document covers how to report issues and contribute code.

## Topics

* [Reporting Issues](#reporting-issues)
* [Contributing Code](#contributing-code)

# Reporting Issues

This is a great way to contribute. Before reporting an issue, please review
current open issues to see if there are any matches.

## How to Report an Issue

Issues should be reported to this project's Github Issues page: [https://github.com/hyperledger/sawtooth-hyper-directory/issues](https://github.com/hyperledger/sawtooth-hyper-directory/issues)

When reporting an issue, please provide as much detail as possible about how
to reproduce it. If possible, provide instructions for how to reproduce the
issue within the vagrant development environment.

Details are key. Please include the following:

OS version
Hyper Directory version
Environment details (virtual, physical, etc.)
Steps to reproduce
Actual results
Expected results


# Contributing Code

Hyperledger Sawtooth Hyper Directory is Apache 2.0 licensed and accepts
contributions via [GitHub](https://github.com/hyperledger/) pull requests.

## Ways to Contribute

Contributions by the community help grow and optimize the capabilities of
Hyperledger Sawtooth, and are the most effective method of having a positive
impact on the project.

## Different ways you can contribute

Bugs or Issues (issues or defects found when working with
    Sawtooth Hyper Directory)
Core Features & Enhancements (expanded capabilities or optimization)
New or Enhanced Documentation (improve existing documentation or create new)
Testing Events and Results (functional, performance or scalability)

## Commit Process

Hyperledger Sawtooth Hyper Directory is Apache 2.0 licensed and accepts
contributions via GitHub pull requests. When contributing code please do the
following:


Fork the repository and make your changes in a feature branch.
Please include unit and integration tests for any new features and updates to
existing tests.
Please ensure the unit and integration tests run successfully. Refer to the
Testing section in the [README.md](README.md) on how to run these
tests.

Please ensure that lint passes by running `./bin/run_lint`. The command should
produce no output if there are no lint errors. The linter requires all Python 
dependencies be installed locally (if not it'll throw import-errors). Install
dependencies locally by running `pip3 install -r requirements.txt` from the 
root project directory.

Pull Request Guidelines

Pull requests can contain a single commit or multiple commits. The most
important part is that a single commit maps to a single fix or enhancement.

Here are a few scenarios:

If a pull request adds a feature but also fixes two bugs, then the pull
request should have three commits, one commit each for the feature and two bug
fixes
If a PR is opened with 5 commits that was work involved to fix a single issue,
it should be rebased to a single commit
If a PR is opened with 5 commits, with the first three to fix one issue and
the second two to fix a separate issue, then it should be rebased to two
commits, one for each issue
Your pull request should be rebased against the current master branch. Please
do not merge the current master branch in with your topic branch, nor use the
Update Branch button provided by GitHub on the pull request page.

## Commit Messages

Commit messages should follow common Git conventions, such as the imperative
mood, separate subject lines, and a line-length of 72 characters. These rules
are well documented by Chris Beam in his [blog post on the subject](https://
chris.beams.io/posts/git-commit/).

Signed-off-by

Commits must include Signed-off-by in the commit message (git commit -s). This
indicates that you agree the commit satisfies the Developer Certificate of
Origin (DCO).

## Important GitHub Requirements

PLEASE NOTE: Pull requests can only be merged after they have passed all
status checks.

These checks are:

The PR must be approved by at least two reviewers and there cannot be
outstanding changes requested.
