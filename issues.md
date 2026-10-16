# Static Analysis Issues: pet_shelter.py

Line numbers refer to the original file (before fixes).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| SQL injection (Bandit B608) | Security (Medium) | 10 | The INSERT query was built with `%` string formatting, so a crafted name such as `x'); DROP TABLE pets;--` could alter the query. Names with an apostrophe also broke it. | Replaced with a parameterized query: `VALUES (?, ?, ?, 0)` with a tuple of values. |
| Weak random generator (Bandit B311) | Security (Low) | 22 | `random.randint` is predictable and not suitable for codes that act like tokens. | Replaced with `secrets.randbelow(9000) + 1000`, keeping the same 1000-9999 range. |
| Try/except/pass and broad exception (Bandit B110, Pylint W0718) | Security (Low) / Bug | 36-37 | Any database error during delete was silently swallowed. | Catch `sqlite3.Error` specifically and print an error message instead of `pass`. |
| Mutable default argument (Pylint W0102) | Bug | 9 | `tags=[]` is created once and shared across calls, so tags leak between pets. | Changed the default to `None` and create a new list inside the function. |
| Bare `except` (Pylint W0702, Flake8 E722) | Bug / Style | 29 | Catches every error, including KeyboardInterrupt, and hid the case where no pet is available. | Removed the try/except and added an explicit `if row is None: return None` check. |
| Global statement and constant naming (Pylint W0603, C0103) | Design | 6, 16 | A mutable global counter was modified inside `adopt()`. | Removed the global counter. `shelter_status()` now counts adopted pets with `SELECT COUNT(*) ... WHERE adopted = 1`. |
| Function names not snake_case (Pylint C0103) | Style | 9, 21, 25, 33, 40 | `registerPet`, `adoptionCode`, `oldestAvailable`, `clearUnadopted`, `shelterStatus` violate PEP 8. | Renamed to `register_pet`, `adoption_code`, `oldest_available`, `clear_unadopted`, `shelter_status` and updated all callers. |
| Missing docstrings (Pylint C0114, C0116) | Style | 1, 9, 15, 21, 25, 33, 40, 45 | No module or function documentation. | Added a module docstring and a one-line docstring to every function. |
| Line too long (Flake8 E501, Pylint C0301) | Style | 5, 10, 27 | Lines were 103-116 characters, over the 79 (Flake8) and 100 (Pylint) limits. | Wrapped the CREATE TABLE string, the INSERT call and the SELECT query across multiple lines. |
| Multiple statements on one line (Flake8 E701, Pylint C0321) | Style | 41 | `if ...: return ...` was on a single line. | Moved the `return` onto its own indented line. |
| f-string suggestion (Pylint C0209) | Style | 10 | `%` formatting used for a string. | Resolved by switching to a parameterized query. |
| Blank-line spacing (Flake8 E302, E305) | Style | 11, 32, 69 (after fixes) | Top-level functions need exactly two blank lines around them. | Added the missing blank lines. |
| Missing `__main__` guard (not flagged by any tool) | Design | 54 | `main()` ran on import, so importing the module would execute the demo. | Wrapped the call in `if __name__ == "__main__":`. |
