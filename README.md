# SSH config synchronisation for AWS

Generate `ssh_config` files, based on current EC2 state.

## Features

* Connect to one or more regions at once.
* Filter EC2 instances by name. Useful for including relevant nodes only or for creating separate config sets for the same environment (e.g. use a different `User` for different nodes).
* Identify hosts using tags or instance IDs:
    * Index duplicates (e.g. in autoscaling groups) using instance launch time.
    * Include a global name prefix and/or a region ID to identify the connection in a unique way.
* Use public or private IPs.
* Set various SSH params:
    * Skip strict host checking, if needed (e.g. internal autoscaling groups).
    * Provide a server alive interval to keep the connection from timing out.
    * Use custom identity files.
    * ...
* Write to `stdout` or a [master file with config-key substitution](#file-output). Useful for working with tools, that don't support the `Include` directive.

## Usage

Using a virtual [pipenv](https://github.com/pypa/pipenv) environment is recommended, but not strictly required. If you have all [dependencies](Pipfile) present, you can launch the script directly.

To get the full list of options:
```bash
pipenv run ./aws_ssh_sync.py --help
```

### Preview

The easiest way to get a **preview** of the current config in AWS is to print the output directly to `stdout`:

```bash
pipenv run ./aws_ssh_sync.py --profile <profile> --region <region>
```

### Utilising the 'Include' directive

If you want to **isolate** the generated config, you can write it to a dedicated file, and `Include` it in the main config. The base use-case is as follows:

```bash
pipenv run ./aws_ssh_sync.py --profile <profile> --region <region> > ~/.ssh/config.d/<some_file>
```

To extend your `~/.ssh/config`, add the following line:

```
Include config.d/*
```

### <a name="file-output"></a>Working with a single config file

Splitting config into multiple, small files keeps things elegant and clean - you should probably stick to that, if you can. 

Unfortunatelly, some tools may still have trouble with the `Include` directive itself. If you want to use a single file (e.g. `~/.ssh/config`) for keeping all configuration, then you can specify the `--output-file` together with a `--config-key`:

```bash
pipenv run ./aws_ssh_sync.py --profile <profile> --region <region> --config-key <key> --output-file <path>
``` 

Behaviour:

* Configuration is written to the `--output-file` rather than `stdout`.
* If the file doesn't exist, then it will be created.
* If a section identified by `--config-key` exists, then it will be replaced. 
* If no `--config-key` was found, then a new section will be appended to the file.
* **No backup file is created at the moment.**
