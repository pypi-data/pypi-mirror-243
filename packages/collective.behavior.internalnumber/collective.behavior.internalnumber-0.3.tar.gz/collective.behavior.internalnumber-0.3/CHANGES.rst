Changelog
=========


0.3 (2023-11-27)
----------------

- Removed catalog metadata `internal_number`, added upgrade step to 1001.
  [gbastien]

0.2 (2023-05-31)
----------------

- Made compliant with Plone 4.3, 5.2 and 6.0
  [sgeulette]
- Ordered imports & improved docstring
  [sgeulette]
- Factorized increment/decrement functionnality in `settings.increment_nb_for`,
  `settings.decrement_nb_for` and `settings.decrement_if_last_nb` functions.
  Added helper function `settings.set_settings`.
  [gbastien]
- Fixed `ConnectionStateError` while setting `registry[TYPE_CONFIG]`
  in tests and profile is applied several times.
  [gbastien]

0.1 (2017-05-31)
----------------

- Initial release.
  [sgeulette]
