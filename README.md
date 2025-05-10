# Merlin Monitor 🔭 ***IN DEVELOPMENT***

![Build Status](https://example.com/build/status.svg) ![PyPI](https://img.shields.io/pypi/v/merlin-monitor)

Merlin Monitor is a **lightweight**, **extensible**, and **open-source** Python tool for real-time system health tracking. It integrates seamlessly with CI/CD pipelines, automation workflows, and monitoring dashboards to provide actionable insights into your infrastructure’s performance and reliability. Designed with a modular architecture, Merlin Monitor simplifies the addition of new metrics and custom reporting sinks without requiring modifications to the core engine.

## Table of Contents

- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start Examples](#quick-start-examples)
- [Configuration File Structure](#configuration-file-structure)
- [Advanced Usage](#advanced-usage)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing & Code Style](#contributing--code-style)
- [License](#license)

## Key Features

Merlin Monitor offers a comprehensive set of capabilities aimed at both developers and operations teams:

- **Metrics Collection**: Pluggable checks covering CPU, RAM, Disk, GPU, Network, and OS-level metrics through a unified `Check` interface.
- **Flexible Reporting**: Supports rich console tables via `rich`, structured JSON outputs, and integration hooks for InfluxDB, Prometheus, Slack notifications, HTTP webhooks, and more.
- **Configurable Thresholds**: Define warning and critical thresholds per metric, with customizable polling intervals and output formats in YAML or JSON.
- **Scheduler Integration**: Built-in APScheduler support for cron-like job scheduling, backoff retries on failure, and clean shutdown handling for long-running deployments.
- **Advanced Logging**: Colorized, structured logs with configurable verbosity and file rotation, compatible with centralized log aggregators like ELK or Graylog.
- **Cross-Platform Support**: Automatically detects platform and uses `/proc`, sysfs, WMI, or platform-specific libraries to gather metrics on Linux, macOS, Windows, and containerized environments.
- **Extensibility & Plugins**: Easily add new metrics or reporters by dropping modules into `merlin/checks/` or `merlin/reporters/`—no core code changes required.
- **High Performance**: Optimized for minimal CPU and memory overhead, suitable for edge devices and large-scale clusters.

## Prerequisites

Before installing Merlin Monitor, ensure the following prerequisites are met:

- **Python 3.9+** installed and available in your system `PATH`.
- **pip** package manager for Python dependencies.
- **OS Access**:
  - Linux/macOS: Read access to `/proc`, sysfs, and device files for CPU, memory, disk, GPU, and thermal zones.
  - Windows: WMI (Windows Management Instrumentation) support; run as Administrator or grant necessary privileges.
- **Optional Requirements**:
  - **Docker** or **Kubernetes** for containerized deployments.
  - **InfluxDB** or **Prometheus** servers for metrics persistence.
  - **Slack** workspace or webhook endpoint for alert notifications.

## Installation

Follow these steps to install Merlin Monitor locally or in your environment:

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/merlin-monitor.git && cd merlin-monitor
````

2. **Verify Python version**

   ```bash
   python --version  # Expect 3.9 or above
   ```
3. **Set up and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Windows: venv\\Scripts\\activate
   ```
4. **Install core dependencies**

   ```bash
   pip install -r requirements.txt
   ```
5. **(Optional) Editable install for development**

   ```bash
   pip install -e .
   ```
6. **(Optional) Docker deployment**

   ```bash
   docker build -t merlin-monitor .
   docker run --rm merlin-monitor status --once
   ```
7. **(Optional) Kubernetes**

   * Use the provided `k8s/merlin-deployment.yaml` to deploy as a CronJob or DaemonSet.

## Quick Start Examples

### One-off Snapshot

Capture a single report of current system metrics:

```bash
merlin status --once
```

*Example Output:*

```
CHECK   STATUS  METRIC              VALUE    DETAILS
CPU     OK      usage_percent       12.3%    All cores normal
RAM     WARN    used_mb/total_mb    6144/8192 High memory usage
Disk    CRIT    free_percent        5.4%     Root partition low
Network OK      packet_loss         0.01%    Stable link
```

### Continuous Monitoring

Run Merlin every 30 seconds until interrupted:

```bash
merlin status --interval 30
```

Press **Ctrl+C** to stop. Logs are written to `merlin.log` by default.

### JSON Output

Useful for automated parsing or feeding into dashboards:

```bash
merlin status --once --output json > metrics.json
```

### Custom Configuration

Specify a custom configuration file and override poll interval:

```bash
merlin status --config ./config/prod.yaml --interval 15 --output json
```

## Configuration File Structure

Merlin supports both YAML and JSON formats for flexibility. Below is a sample YAML config demonstrating common settings:

```yaml
# config.yaml

enabled_checks:
  - cpu
  - ram
  - disk
  - network
  # - gpu  # Uncomment to enable GPU monitoring

thresholds:
  cpu:
    warn: 70    # % CPU usage to WARN
    crit: 90    # % CPU usage to CRIT
  ram:
    warn: 75    # % RAM usage to WARN
    crit: 90    # % RAM usage to CRIT
  disk:
    warn: 20    # % Free space to WARN
    crit: 10    # % Free space to CRIT
  network:
    warn: 1     # % Packet loss to WARN
    crit: 5     # % Packet loss to CRIT

poll_interval: 60       # Default polling interval in seconds
output_format: table    # Options: table | json
log_level: INFO         # DEBUG, INFO, WARNING, ERROR
webhook_url: https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX

# Advanced settings
retry_backoff: 5        # Seconds between retry attempts on failure
max_retries: 3          # Number of retry attempts per check
log_file: /var/log/merlin-monitor.log
persist: true           # Enable writing metrics to a local SQLite DB

```

## Advanced Usage

* **Webhook Alerts**: Configure `webhook_url` to POST JSON payloads on WARN or CRIT statuses. Use `curl` or native HTTP library support.
* **Persistence Layer**: Enable local SQLite storage or integrate with InfluxDB for historical data retention.
* **Custom Reporters**: Drop new reporter modules into `merlin/reporters/` and register them in your config under `reporters:` list.
* **Plugin Discovery**: Merlin automatically discovers any Python files in `merlin/plugins/`, enabling third-party extensions.

## Environment Variables

Merlin can also be configured via environment variables, which override settings in the config file:

| Variable              | Description                                     |
| --------------------- | ----------------------------------------------- |
| `ARGUS_CONFIG_PATH`   | Path to your config file                        |
| `ARGUS_POLL_INTERVAL` | Override polling interval (seconds)             |
| `ARGUS_OUTPUT`        | Default output format (`table` or `json`)       |
| `ARGUS_LOG_LEVEL`     | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `ARGUS_WEBHOOK_URL`   | Override webhook endpoint for alerts            |

## Troubleshooting

* **Permission Denied**: Ensure your user has read access to system metrics. On Linux, you may need `sudo`.
* **WMI Errors on Windows**: Run the CLI as Administrator or enable WMI service.
* **Missing Checks**: Verify `enabled_checks` matches filenames under `merlin/checks/` (without `.py`).
* **Docker Issues**: Ensure Docker daemon is running and image was built successfully.
* **Logging Missing Data**: Check `log_file` path and permissions.

## FAQ

**Q: Can I monitor remote servers?**
A: Yes, deploy Merlin on each server and aggregate metrics centrally via HTTP webhooks or InfluxDB.

**Q: How do I add a new metric?**
A: Create a Python file in `merlin/checks/` subclassing `base.Check` and implement the `run()` method.

**Q: How do I customize report output?**
A: Extend or override functions in `merlin/report.py`, or create a new reporter in `merlin/reporters/`.

## Contributing & Code Style

Contributions are highly encouraged:

1. **Fork** the repository and create a descriptive feature branch.
2. **Write tests** in the `tests/` directory and aim for high coverage.
3. **Format code** with Black and check with Flake8 & Mypy:

   ```bash
   black merlin tests
   flake8 merlin tests
   mypy merlin
   ```
4. **Run tests**:

   ```bash
   pytest --maxfail=1 --disable-warnings -q
   ```
5. **Open a Pull Request** against the `main` branch, describing changes and rationale.

Please adhere to the existing code style and include documentation updates for any new features.

## License

Distributed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.