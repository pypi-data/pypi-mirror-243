# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased
### Added
- `alphanumeric` and `alpha` methods. These replace `v1` method `string`.

### Removed
- **BREAKING**: `string` method.
- `ignore_max_length` option in the `string` and `integer` functions, the `length` option can now be as big as desired.

### Changed
- **BREAKING**: `integer` method renamed `numeric`.

## [1.0.0] - 2022-10-24
### Fixed
- `var` methods were not behaving the way they should.

### Added
- Short versions of date variables to `var` method.
- "var" function to generate a string based on a variable string that is passed as an argument.
- "var" method to "database" function.

### Changed
- `var` method in database will now add up until it's unique.
- Changed 'default_max_length' to 1000.

### Removed
- Removed "secret" function as it was depricated.
- Removed deprication warning when "string" function was given type "integer" instead of "numbers".

## [0.1.6] - 2022-03-08
### Added
- Arguments "lowercase_only" and "uppercase_only" to the "string" function.
- "string" function argument "type" will now take "all". It will then return a string containing both numbers and letters.

### Changed
- "string" function argument "type" will take "numbers" instead of "integer". This is deprecated in this version and will be removed in version 1.0.0.
- "secret" function split up into seperate "bytes", "hex" and urlsafe functions. This is deprecated in this version and will be removed in version 1.0.0.

### Removed
- Removed "colorama" dependency as it was unnecessary.

## [0.1.5] - 2022-02-27
### Fixed
- Issue where "database" function would fail if argument "method" was undefined.
- Issue where "integer" function failed because a variable was defined out of scope.

### Added
- Added exception that will raise when specified length is higher than 100000 if "ignore_max_length" argument is set to False.
- Added "type" argument to "string" function. This adds the option to create a string of numbers.

### Removed
- Removed unnecessary imports.
- Removed unnecessary code.

### Documentation
- Added information for "secret" function.

## [0.1.4] - 2022-02-17
### Fixed
- Issue where "integer" function will not be accurate when the randomly generated integer started with 0.
- Issue where "integer" and "string" functions would fail when no "prefix" was specified.

### Documentation
- Added information for "database" function.

[unreleased]: https://github.com/w-kuipers/simpleuid/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/w-kuipers/simpleuid/compare/v0.1.6...v1.0.0
[0.1.6]: https://github.com/w-kuipers/simpleuid/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/w-kuipers/simpleuid/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/w-kuipers/simpleuid/compare/v0.1.3...v0.1.4
[0.0.1]: https://github.com/w-kuipers/simpleuid/releases/tag/v0.0.1

