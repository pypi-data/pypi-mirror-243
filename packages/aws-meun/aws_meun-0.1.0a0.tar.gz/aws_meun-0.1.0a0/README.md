# aws-meun
CLI tool to unsubscribe from AWS Marketing Emails

## Quick start

```
❯ python -m pip install aws-meun
❯ aws-meun me@domain.org
Unsubscribed me@domain.org (HTTP 200)
```

## Quick tip

aws-meun can also read from STDIN for easy batch unsubscribe

```
❯ echo me@domain.org | aws-meun
Unsubscribed me@domain.org (HTTP 200)
```
