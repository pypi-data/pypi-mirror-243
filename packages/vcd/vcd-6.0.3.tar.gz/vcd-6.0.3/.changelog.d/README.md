# How to generate the VCD Changelog

A "Changelog" is a record of all notable changes made to a project. Such a changelog, in our case the `CHANGELOG.md`, is read by the users. Therefore, any description should be aimed to users instead of describing internal changes which are only relevant to developers.

To avoid merge conflicts, we use the [Towncrier](https://github.com/twisted/towncrier) package to manage our changelog.

The directory [.changelog.d](../.changelog.d) contains "newsfragments" which are short Markdown-formatted files. On release, those news fragments are compiled into the [CHANGELOG.md](../CHANGELOG.md) file.

You don't need to install towncrier yourself, use the `tox` command to call the tool.

We recommend to follow the steps to make a smooth integration of your changes:

1. After you have created a GitLab Issue, add a new file into the directory [.changelog.d](../.changelog.d). Each filename follows the syntax:

    ```
    <ISSUE>.<TYPE>.md
    ```

    where `<ISSUE>` is the GitLab issue number. `<TYPE>` is one of:

    - `added`: for new features.
    - `changed`: for changes in existing functionality.
    - `deprecated`: for soon-to-be removed features.
    - `removed`: for now removed features.
    - `fixed`: for any bug fixes.
    - `security`: in case of vulnerabilities.
    - `other`: for other changes.

    For example: `123.added.md`, `233.removed.md`, `456.fixed.md` etc.

    For orphan news fragments (those that don’t need to be linked to any Issue ID), start the file name with +.
    The content will still be included in the release notes, at the end of the category corresponding to the file extension

    For example: `+anything.added.md`, `+anything.removed.md`, `+anything.fixed.md` etc

2. Create the new file with the command:

    ```bash
    tox -e changelog -- create 123.added.md
    ```

    The file is created int the [.changelog.d](../.changelog.d) directory.

3. Open the file and describe your changes in Markdown format.

    - Wrap symbols like modules, functions, or classes into double backticks so they are rendered in a monospace font.
    - Prefer simple past tense or constructions with "now".

4. Check your changes with:

    ```bash
    tox -e changelog -- check
    ```

5. Optionally, build a draft version of the changelog file with the command:

    ```bash
    tox -e changelog
    ```
6. Commit all your changes and push it.

## Release Changelog

On release, the maintainer compiles a new `CHANGELOG.md` file by running:

```bash
tox -e changelog -- build  --version <new_version>
```

This will remove all newsfragments inside the [.changelog.d](../.changelog.d) directory, making it ready for the next release.
