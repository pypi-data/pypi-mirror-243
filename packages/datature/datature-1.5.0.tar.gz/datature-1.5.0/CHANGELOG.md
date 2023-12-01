# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Workspace Authentication

## [1.5.0] - 2023-11

### Added

- Introduce new function `download_model` to download artifact models directly.

## [1.4.0] - 2023-10

### Added

- Support for key point projects.
- AnnotationExportFormat and AnnotationExportFormat enum types.

### Fixed

- CLI error exit during long/failed operation.

### Removed

- AnnotationFormat enum type.

## [1.3.2] - 2023-11-03

### Fixed

- Wrong dependency version
- Selective decamelize API response

## [1.3.0] - 2023-09-18

### Added

- Support for classification projects.
- Introduction of change logs.
- New function added to retrieve training confusion matrix. (#109).

### Changed

- Updated test cases to be compatible with Python 3.11.
