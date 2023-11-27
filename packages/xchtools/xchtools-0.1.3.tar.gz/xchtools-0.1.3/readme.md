


# Config

In your own project, there should be a `settings.toml` and a `.env` file.

- `settings.toml` stores the common config.  
    - To use connections module, `[default.db]` is a must.
- `.env` stores secret things like passwords.

# Usage


## connections module

mysqldb connection example toml:

```toml
[default.db]
host = "replace with your host"
port = 3306
user = "root"
password = "@format {env[MYSQLDB_PASSWORD]}"
```

Usage in your code:

```python

from xchtools import XCHConnections
xc = XCHConnections(os.path.dirname(os.path.abspath(__file__)))
config = xc.settings
print(config.db)

xc.sql2df("show databases")
```





# For developer

## Build and Release

### TODO change to poetry
python setup.py sdist
python setup.py bdist_wheel

twine upload dist/*
pip install xchtools



参考 https://zhuanlan.zhihu.com/p/522865678

