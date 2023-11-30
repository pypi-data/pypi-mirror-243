## Version 0.7.1 (2023-11-30)
### 👷 Bug fixes

- setup.py: ensure we correctly shit the packages files

## Version 0.7.0 (2023-11-30)
### 🎉 New features

- run flynt on the code base to convert everything into f-strings

### 🤖 Continuous integration

- add safety job
- add twine-check job
- disable from forge and triggering other pipelines

### 🤷 Various changes

- add .readthedocs.yaml

## Version 0.6.2 (2022-06-07)
### 👷 Bug fixes

- check-manifest: include CHANGELOG.md

## Version 0.6.1 (2022-06-07)
### 👷 Bug fixes

- it's 2021 let's use utf-8
- rql repo has been moved

### 📝 Documentation

- licence: update licence dates

### 🤖 Continuous integration

- add .cube-doctor.yml
- add check-dependencies-resolution
- add pytest-caputre-deprecatedwarnings
- integrate pytest-deprecated-warnings
- make py3 jobs interruptible
- migrate to v2 of gitlab ci templates
- use templates
- add a gitlab-ci.yml based on tox
- add super basic tox.ini, project is broken anyway
- gitlab-ci/fix: forgot to pass TRIGGERED_FROM_OTHER_PROJECT variable to other pipelines
- gitlab-ci: add py3-from-forge pipeline
- gitlab-ci: makes curl fails on bad http code and display it
- gitlab-ci: refactor to use except:variables instead of bash if
- pkg: include __pkginfo__.py in sdist tarball
- tests: trigger rql builds from logilab-constraint if all other tests passed
- tox/fix: missing -U in pip install in from-forge
- use new gitlab syntax for triggering other pipeline