## 1.0.0 (2025-11-27)

### BREAKING CHANGE

- replace add_pid with no_prefix in testing helpers

### Fix

- **plugin**: guard against nested test context usage
- **testingsystem**: generate unique prefixes and rename flag
- **plugin**: set funcnodes config dir to temp base in pytest

## 0.4.2 (2025-11-25)

### Fix

- **pytest-funcnodes**: harden decorators and test context handling

## 0.4.1 (2025-11-13)

### Fix

- **testingsystem**: simplify get_in_test call in setup function
- **testingsystem**: update deprecation warning import for consistency

## 0.4.0 (2025-11-13)

### Feat

- **pytest-funcnodes**: expand __all__ to include testing system functions

## 0.3.0 (2025-11-13)

### Feat

- **pytest-funcnodes**: isolate funcnodes tests per temp context

## 0.2.0 (2025-11-13)

### Feat

- **pytest-funcnodes**: add async funcnodes_test decorator
