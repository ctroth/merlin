````markdown
# Usage Guide

A comprehensive reference for all Argus commands, flags, and examples, designed to help both beginners and advanced users integrate Argus Monitor into their workflows.

## Table of Contents

- [Global Options](#global-options)
- [CLI Commands](#cli-commands)
  - [status](#status)
  - [checks](#checks)
  - [report](#report)
  - [version](#version)
  - [completion](#completion)
- [Environment Variables](#environment-variables)
- [Exit Codes](#exit-codes)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)

## Global Options

These flags apply to most commands. They can also be set via environment variables as documented below.

| Flag                  | Description                                         | Default          | Env Var                 |
|-----------------------|-----------------------------------------------------|------------------|-------------------------|
| `-c, --config PATH`   | Path to configuration file (YAML or JSON)           | `config.yaml`    | `ARGUS_CONFIG_PATH`     |
| `-i, --interval SEC`  | Polling interval in seconds for continuous mode     | `60`             | `ARGUS_POLL_INTERVAL`   |
| `-o, --output FORMAT` | Output format: `table`, `json`, or `csv`            | `table`          | `ARGUS_OUTPUT`          |
| `-v, --verbose`       | Enable verbose logging (DEBUG level)                | off              | `ARGUS_LOG_LEVEL=DEBUG` |
| `-q, --quiet`         | Suppress non-critical output (only WARN/CRIT shown) | off              | —                       |

## CLI Commands

### status

Run all enabled checks and display results. By default, performs one-off checks unless `--interval` is specified.

```bash
# One-time snapshot of system health
argus status --once

# Poll every 30 seconds continuously
argus status --interval 30

# Include JSON output and verbose logs
argus status -i 15 -o json -v
````

**Key Options:**

* `--once`: Run checks exactly one time and exit.
* `--interval, -i`: Poll at the specified interval (seconds); disables `--once`.
* `--output, -o`: Choose from `table`, `json`, or `csv`.
* `--thresholds PATH`: Override thresholds file (YAML/JSON) separately.

### checks

Manage and inspect available metric checks.

```bash
# List all built-in checks by name\nargus checks --list

# Describe CPU check details and default thresholds\nargus checks describe cpu

# Enable a built-in check temporarily\nargus checks enable gpu --once
```

**Subcommands:**

* `list`: Show names of all checks in `argus/checks/`.
* `describe <name>`: Show metric names, units, and default warn/crit values.
* `enable <name>`: Temporarily enable a check for one run.

### report

Generate or export historical and one-off reports. Requires enabling persistence in config.

```bash
# Export JSON report for last 24 hours\nargus report --since 24h --output json > last_day.json

# Show human-readable report table for yesterday
argus report --since "2025-05-07" --until "2025-05-08"
```

**Key Options:**

* `--since`: Relative (e.g., `1h`, `24h`) or absolute (YYYY-MM-DD) start time.
* `--until`: Relative or absolute end time; defaults to now.
* `--output`: `table`, `json`, or `csv`.

### version

Display the installed Argus Monitor version and exit.

```bash
argus version
# Output: Argus Monitor v0.2.0
```

### completion

Generate shell completion scripts.

```bash
# Bash completion
eval "$(argus completion bash)"

# Zsh completion
eval "$(argus completion zsh)"
```

## Environment Variables

Override CLI defaults with these environment variables. Values take precedence over config file settings.

| Variable              | Description                          |
| --------------------- | ------------------------------------ |
| `ARGUS_CONFIG_PATH`   | Path to config file                  |
| `ARGUS_POLL_INTERVAL` | Default polling interval (seconds)   |
| `ARGUS_OUTPUT`        | Default output format (`table` etc.) |
| `ARGUS_LOG_LEVEL`     | Logging verbosity (`DEBUG`/`INFO`)   |
| `ARGUS_WEBHOOK_URL`   | Webhook endpoint for alerts          |

## Exit Codes

Argus returns specific exit codes to indicate overall status, useful for scripts and automation:

| Code | Meaning                                  |
| ---- | ---------------------------------------- |
| `0`  | All checks OK                            |
| `1`  | At least one check WARN but none CRIT    |
| `2`  | At least one check CRIT                  |
| `3`  | Invalid arguments or configuration error |
| `4`  | Runtime exception (unhandled error)      |

## Examples

### Logging to File

Append continuous logs to a timestamped file:

```bash
argus status --interval 60 >> /var/log/argus/$(date +%F_%T).log
```

### Filtering Critical Alerts

Use `jq` to filter CRIT statuses from JSON output:

```bash
argus status --once --output json | jq '.[] | select(.status == "CRIT")'
```

### Systemd Service

Create a service unit at `/etc/systemd/system/argus.service`:

```ini
[Unit]
Description=Argus Monitor Service
After=network.target

[Service]
ExecStart=/usr/local/bin/argus status --interval 60
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
systemctl enable argus
systemctl start argus
```

## Troubleshooting

* **Permission Denied**: On Linux, give read access to `/proc` or run as root.
* **Missing Checks**: Confirm `enabled_checks` in config matches filenames in `argus/checks/` (without `.py`).
* **WMI Errors**: On Windows, ensure WMI service is running and CLI is elevated.
* **Scheduler Failures**: Check logs for backoff/retry messages; adjust `retry_backoff` and `max_retries` settings.
* **Completion Scripts**: Ensure your shell is configured to load completion scripts on startup.

For more help, visit the [official documentation](https://github.com/yourusername/argus-monitor/wiki) or raise an issue on GitHub.

```
```
