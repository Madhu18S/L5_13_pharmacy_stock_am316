# Static Code Analysis Report

## Overview

Static analysis was performed on `pharmacy_system.py` using:

- Pylint
- Flake8
- Bandit

---

# Pylint Findings

Initial Pylint Score: **6.90/10**

## Issues Identified

| Issue Type | Line(s) | Description |
|------------|---------|-------------|
| Missing module docstring | 1 | File has no module-level documentation |
| Missing function docstrings | Multiple | Several functions lack documentation |
| Line too long | 36 | Exceeds recommended length |
| Dangerous default value | 24 | Mutable list used as default argument |
| Bare except | 38, 58 | Catches all exceptions without specifying type |
| Unspecified encoding | 50, 57 | Files opened without explicit encoding |
| Resource leak risk | 50, 57 | Files not handled using context manager |
| Global statement | 55 | Uses global variable |
| Invalid function name | 61 | Function name does not follow snake_case |
| Unused import | 3 | Imported `os` module is not used |
| Old string formatting | 21 | Could use safer formatting mechanism |

---

# Flake8 Findings

## Issues Identified

| Error Code | Description |
|------------|-------------|
| F401 | Unused import `os` |
| E302 | Expected two blank lines between functions |
| E501 | Line exceeds maximum length |
| E722 | Bare except clause used |
| E305 | Expected two blank lines after function definition |

---

# Bandit Security Findings

## Issue 1: Potential SQL Injection

**Severity:** Medium

Problematic code:

```python
query = "SELECT id, allergy FROM patients WHERE name = '%s'" % name
```

Reason:

User input is directly inserted into the SQL query, making the application vulnerable to SQL injection attacks.

Recommended fix:

```python
query = "SELECT id, allergy FROM patients WHERE name = ?"
cur.execute(query, (name,))
```

---

## Issue 2: try-except-pass Pattern

**Severity:** Low

Problematic code:

```python
except:
    pass
```

Reason:

Exceptions are silently ignored, making debugging difficult and potentially hiding serious problems.

Recommended fix:

```python
except Exception as error:
    print(error)
```

---

# Fixes Implemented

1. Removed unused import `os`.
2. Added module docstring.
3. Added function docstrings.
4. Replaced SQL string formatting with parameterized query.
5. Replaced mutable default argument with `None`.
6. Replaced bare exception handlers with specific exception handling.
7. Added explicit UTF-8 encoding to file operations.
8. Used `with open(...)` context managers for file handling.
9. Renamed functions to follow snake_case conventions.
10. Corrected formatting and spacing issues reported by Flake8.

---

# Conclusion

Static code analysis successfully identified code quality, maintainability, and security issues. Implementing these fixes improved readability, reduced potential runtime errors, and removed security vulnerabilities from the application.