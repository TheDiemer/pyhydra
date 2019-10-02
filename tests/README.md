From the main Project directory, you can run the following to run the tests: 

``` 
pipenv run python -m unittest discover tests/
```

To run tests, you first need to create a test auth config in 'tests/test_config.cfg',
to interact with hydra using user cardentals.

```
[hydra]
username = rhn-support-USERNAME
password = NOPE
```

You can controll the test run behavior by using one of the following ENV variables

Example:
```
export DEBUG_TESTING=True
```

Variable for Controlling Test Behavior:

1. DEBUG_TESTING: options(True,False) - Used to turn on printing of data (not actual tests).
1. DEBUG_INDENT_NUMBER: option(# Numeric Value) - Number of Spaces to indent json (pretty printing).
1. DEBUG_ACCOUNT_NUMBER: optoin(# String Value) - Account Number to use in the tests.
1. DEBUG_CASE_NUMBER: option(# String Value) - Case Number to use in the tests.

