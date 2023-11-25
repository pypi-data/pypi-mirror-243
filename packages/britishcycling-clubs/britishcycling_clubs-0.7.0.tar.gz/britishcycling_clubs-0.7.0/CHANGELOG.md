# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Historic and pre-release versions aren't necessarily included.


## [0.7.0] - 2023-11-24

### Added

- Logging for Playwright operations in `get_private_member_counts()` 


## [0.6.0] - 2023-11-21

### Added

- Support Python 3.12 in CI workflow

### Changed

- `get_private_member_counts()`: raise exception if zero 'active members' would be returned.

- Update dev/test dependencies: mypy, ruff


## [0.5.0] - 2023-11-09

### Added

- Optional page load delay in `get_private_member_counts()` 

### Changed

- Update dev/test dependencies: black, ruff


## [0.4.2] - 2023-10-23

### Changed

- Update dependencies: requests, playwright

- Update dev/test dependencies: black, mypy, ruff, types-requests


## [0.4.1] - 2023-09-27

### Fixed

- Missing/outdated/broken package metadata

### Changed

- Update dev/test dependencies: ruff


## [0.4.0] - 2023-09-25

### Added

- PEP 561 typing compatibility

- Documentation: Explain how to install playwright system dependencies

### Changed

- Update dev/test dependencies: ruff


## [0.3.0] - 2023-09-21

### Added

- This changelog

- Documentation: Describe public functions in README 

- Dev/test dependencies: ruff

- Enforce linting with isort, black, ruff and static type checking with mypy in CI 
  using GitHub Actions

### Fixed

- Reliability issues when getting data from Club Manager pages with
 `get_private_member_counts()`. See 'Changed'

- Use of `assert` in production code

### Changed

- **BREAKING CHANGE**: Simplify package structure.
 
  `import britishcycling-clubs.main` should be replaced with `import 
  britishcycling-clubs`

- Use [Playwright](https://playwright.dev/python/) instead of Selenium when getting 
  data from Club Manager pages with `get_private_member_counts()`

  This makes deployment easier, as Playwright simplifies browser installation and
  updates, and a separate driver executable is no longer required. README updated to 
  cover this

- Update dev/test dependencies: black, mypy, pytest, types-requests, 
  types-beautifulsoup4

### Removed

- Trivial test which didn't have any real value

- Dev dependencies: pylint


## [0.2.5] - 2023-05-30

### Changed

- Minor code, type hinting and docstring improvements

- Update dev dependencies: mypy, pylint, test, types-requests, types-beautifulsoup4


[0.7.0]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.2.5...v0.3.0
[0.2.5]: https://github.com/elliot-100/britishcycling-clubs/compare/v0.2.3...v0.2.5
