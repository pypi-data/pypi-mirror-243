## Version 0.42.0 (2023-11-30)
### 🎉 New features

- nodes: use an explicit exception when we forgot to provide needed args in a rql query.
- run flynt on the code base to convert everything into f-strings

### 🤖 Continuous integration

- disable triggering cubicweb tests

### 🤷 Various changes

- avoid duplicated labels
- remove example `intersphinx_mapping` value
- remove references to deleted modules

## Version 0.41.0 (2022-10-26)
### 🎉 New features

- typing: declare that rql ship type annotations

## Version 0.40.1 (2022-10-18)
### 🤷 Various changes

- fix various deprecated warnings

## Version 0.40.0 (2022-10-11)
### 🎉 New features

- *BREAKING CHANGE* yams: remove warnings with version 0.48

### 👷 Bug fixes

- add missing methods to DummySchema (`ion_schema_for` and `entity_schema_for` replace rschema and eschema.)

## Version 0.39.0 (2022-09-07)
### 🎉 New features

- syntax: Add the possibility to call attribute or functions from projection attributes

### 🤖 Continuous integration

- add check-dependencies-resolution job
- add twine-check job

### 🤷 Various changes

- Exclude parser folder from flake8 check

## Version 0.38.2 (2022-05-18)
### 🤖 Continuous integration

- don't trigger CW pipeline if I'm trigger from another pipeline
- use native gitlab readthedocs integration
- use templates in .gitlab-ci.yml

## Version 0.38.1 (2022-03-29)
### 👷 Bug fixes

- stcheck: be sure we treat NOT EXISTS(X eid Y) as NOT(X eid Y) (https://forge.extranet.logilab.fr/cubicweb/cubicweb/-/issues/528)

## Version 0.38.0 (2022-01-13)
### 🎉 New features

- Change Python minimum version from 3.4 to 3.7
- don't use type vars where not necessary
- make internal types private
- move AnyStatement to stmts
- move Graph type to stmts
- move Solution and SolutionsList type aliases to stmts.py
- move some types in nodes.py
- Remove comparison feature
- remove import of BaseNode
- remove rqltypes.py
- remove TranslationFunction from rqltypes
- replace rqltypes.AnyStatementNode by stmts.AnyStatement
- Update Gitlab CI to run Cubicweb's tests with latest RQL's updates
- use explicit typing for children

### 👷 Bug fixes

- annotation: check Function children to detect potential aggragation. (https://forge.extranet.logilab.fr/cubicweb/cubicweb/-/issues/242)
- fix typo in test
- Install Yapps from Logilab's forge (#12)
- lint: make flake8 accept some monkeypatches
- move Graph to stmts and fix its definition
- remove conditional around Protocol import
- remove unused import to BaseNode

### 🤖 Continuous integration

- put linting job in the lint stage
- reorganize .gitlab-ci.yml jobs positions in the file to put linting jobs first
- start to migrate to open-source/gitlab-ci-templates
- uses our own docker image for python

### 🤷 Various changes

- Add types within stcheck.py module
- Begin adding type hints to rql/__init__
- feat! remove resolver_class argument to RQLHelper constructor
- feat!: remove unused index_path/go_to_index_path functions
- feat!: remove unused module rqlgen
- feat!: remove unused pygments_ext module
- Fix Argument 1 to "__call__" of "TranslationFunction" has incompatible type
- fix minor errors F821
- fix!: use patched version of yapps2
  *BREAKING CHANGE*: this shouldn't affect projects since updating rql will automacally install the new dependency.
- flake8: Fix [E301] expected 1 blank line, found 0
- flake8: Fix W293 blank line contains whitespace
- Improve function signature, remove unused type alias
- Improve type hint for RQLHelpher __init__ method
- Improve various type hints
- make get_nodes & iget_nodes more generic
- mypy: add IsASelectionManager protocol
- mypy: Add type hints for EtypeResolver class:
- mypy: Finish type-hints addition to stmts.py module
- mypy: Improve type aliases
- mypy: Improve type annotation for `_visit` method:
- mypy: Improve type annotation for set_limit method
- mypy: Improve type annotation for visit_insert & visit_delete
- mypy: Improve type hints for stmts.py module
- mypy: Improve type hints inside rql/stmts.py module
- mypy: Type RQLHelper's schema attribute as ISchema
- refactor: rename currently misleading name '_init_stmt' to '_init_scope_node'
- Replace mypy type:ignore comments that were moved by Black
- Type hint the undo module
- Update tox configuration
- Use protocol to declare type of translation function

## Version 0.37.0 (2021-05-04)
### 🎉 New features

- order: add support for order by NULLS LAST and NULLS FIRST
- typing: add partial typing

### 🤖 Continuous integration

- integrate pytest-deprecated-warnings
- mypy: enable mypy check on the ci
