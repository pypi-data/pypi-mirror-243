# `inferless`

Inferless - Deploy Machine Learning Models in Minutes.

See the website at https://inferless.com/ for documentation and more information
about running code on Inferless.

**Usage**:

```console
$ inferless [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`
* `--help`: Show this message and exit.

**Commands**:

* `deploy`: Deploy a model to Inferless
* `init`: Initialize a new Inferless model
* `log`: Inferless models logs (view build logs or...
* `login`: Login to Inferless
* `model`: Manage Inferless models (list , delete ,...
* `runtime`: Manage Inferless runtimes (can be used to...
* `secret`: Manage Inferless secrets (list secrets)
* `token`: Manage Inferless tokens
* `volume`: Manage Inferless volumes (can be used to...
* `workspace`: Manage Inferless workspaces (can be used...

## `inferless deploy`

Deploy a model to Inferless

**Usage**:

```console
$ inferless deploy [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless init`

Initialize a new Inferless model

**Usage**:

```console
$ inferless init [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless log`

Inferless models logs (view build logs or call logs)

**Usage**:

```console
$ inferless log [OPTIONS] [MODEL_ID]
```

**Arguments**:

* `[MODEL_ID]`: Model id or model import id

**Options**:

* `-i, --import-logs`: Import logs
* `-t, --type TEXT`: Logs type [BUILD, CALL]]  [default: BUILD]
* `--help`: Show this message and exit.

## `inferless login`

Login to Inferless

**Usage**:

```console
$ inferless login [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless model`

Manage Inferless models (list , delete , activate , deactivate , rebuild the models)

**Usage**:

```console
$ inferless model [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `activate`: activate a model.
* `deactivate`: deactivate a model.
* `delete`: delete a model.
* `info`: Get model details.
* `list`: List all models.
* `rebuild`: rebuild a model.

### `inferless model activate`

activate a model. 

**Usage**:

```console
$ inferless model activate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model deactivate`

deactivate a model. 

**Usage**:

```console
$ inferless model deactivate [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model delete`

delete a model.

**Usage**:

```console
$ inferless model delete [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model info`

Get model details.

**Usage**:

```console
$ inferless model info [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `--help`: Show this message and exit.

### `inferless model list`

List all models.

**Usage**:

```console
$ inferless model list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless model rebuild`

rebuild a model. (If you have a inferless.yaml file in your current directory, you can use the --local or -l flag to redeploy the model locally.)

**Usage**:

```console
$ inferless model rebuild [OPTIONS]
```

**Options**:

* `--model-id TEXT`: Model ID
* `-l, --local`: Local rebuild
* `--help`: Show this message and exit.

## `inferless runtime`

Manage Inferless runtimes (can be used to list runtimes and upload new runtimes)

**Usage**:

```console
$ inferless runtime [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all runtimes.
* `upload`: Upload a runtime.

### `inferless runtime list`

List all runtimes.

**Usage**:

```console
$ inferless runtime list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

### `inferless runtime upload`

Upload a runtime.

**Usage**:

```console
$ inferless runtime upload [OPTIONS]
```

**Options**:

* `-p, --path TEXT`: Path to the runtime
* `-n, --name TEXT`: Name of the runtime
* `--help`: Show this message and exit.

## `inferless secret`

Manage Inferless secrets (list secrets)

**Usage**:

```console
$ inferless secret [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `list`: List all secrets.

### `inferless secret list`

List all secrets.

**Usage**:

```console
$ inferless secret list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless token`

Manage Inferless tokens

**Usage**:

```console
$ inferless token [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `set`: Set account credentials for connecting to...

### `inferless token set`

Set account credentials for connecting to Inferless. If not provided with the command, you will be prompted to enter your credentials.

**Usage**:

```console
$ inferless token set [OPTIONS]
```

**Options**:

* `--token-key TEXT`: Account CLI key  [required]
* `--token-secret TEXT`: Account CLI secret  [required]
* `--help`: Show this message and exit.

## `inferless volume`

Manage Inferless volumes (can be used to list volumes and create new volumes)

**Usage**:

```console
$ inferless volume [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: create volume.
* `list`: List all volumes.

### `inferless volume create`

create volume.

**Usage**:

```console
$ inferless volume create [OPTIONS]
```

**Options**:

* `-n, --name TEXT`: Name of the volume
* `--help`: Show this message and exit.

### `inferless volume list`

List all volumes.

**Usage**:

```console
$ inferless volume list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `inferless workspace`

Manage Inferless workspaces (can be used to switch between workspaces)

**Usage**:

```console
$ inferless workspace [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `use`

### `inferless workspace use`

**Usage**:

```console
$ inferless workspace use [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
