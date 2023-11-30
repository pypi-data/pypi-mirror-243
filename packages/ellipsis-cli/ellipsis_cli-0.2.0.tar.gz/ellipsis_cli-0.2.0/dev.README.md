### To test
```
virtualenv venv
. venv/bin/activate
pip install .
```
and then you can use commands like
```
bb ping
```
and when you're done
```
deactivate
```


### To publish
Increment the version in `ellipsis/cli.py:CLI_VERSION` and in `pyproject.toml`.  Then push your changes to master. Then
```
flit publish
```
Note: The GitHub workflow doesn't work at the moment.