````markdown
# Architecture Overview

Argus Monitor is architected as a **modular**, **layered**, and **plug-in**-based monitoring framework. This document delves into each architectural layer, illustrating how components interact, where to extend functionality, and the non-functional considerations that guide design decisions.

## 1. Overview

At its core, Argus Monitor follows the **separation of concerns** principle: CLI handling, scheduling orchestration, metric collection, and report generation are isolated into distinct layers. This approach enhances maintainability, testability, and ease of extension.

## 2. Layers and Components

Below is a detailed breakdown of each layer and its responsibilities:

### 2.1 CLI Layer (`argus/cli.py`)
- **Parsing & Validation**: Uses `click` to define commands (`status`, `checks`, `report`) and global options (`--config`, `--interval`, `--output`).
- **Initialization**: Loads configuration, sets up logging, and passes control to the Scheduler or Core.
- **Error Handling**: Validates CLI arguments and provides user-friendly error messages on invalid input.

### 2.2 Scheduler Layer (`argus/scheduler.py`)
- **Job Management**: Wraps APScheduler to schedule recurring jobs, cron jobs, or one-off tasks via `scheduler.add_job()`.
- **Lifecycle Hooks**: Registers signal handlers for SIGINT/SIGTERM to gracefully shutdown jobs and release resources.
- **Retry Logic**: Implements exponential backoff and retry counters for transient metric collection failures.

### 2.3 Core Layer (`argus/core.py`)
- **Discovery**: Dynamically discovers all subclasses of `base.Check` within `argus/checks/` using Python’s `importlib` and introspection.
- **Execution**: Instantiates each check with the appropriate configuration and invokes its `run()` method.
- **Aggregation**: Collects results into a standardized schema (`name`, `status`, `metrics`, `details`) and enriches with timestamp and host metadata.

### 2.4 Checks Layer (`argus/checks/*.py`)
- **Implementation**: Each metric check (e.g., `CPUCheck`, `RAMCheck`, `DiskCheck`, `GPUCheck`, `NetworkCheck`) subclasses `base.Check` and implements `run()`.
- **Utilities Integration**: Leverages helpers in `argus/utils/` for tasks like parsing `/proc`, interfacing with WMI, or normalizing raw data.
- **Threshold Evaluation**: Uses the `evaluate()` helper for WARN/CRIT status determination against configured thresholds.

### 2.5 Reporting Layer (`argus/report.py`)
- **Output Formats**: Renders aggregated results as rich console tables (`rich`), JSON dumps, or passes payloads to custom sinks.
- **Plugin Architecture**: Supports additional reporters (e.g., InfluxDB, HTTP webhook) by registering under a `reporters` registry in configuration.
- **Formatting Options**: Includes colorization, column alignment, and optional output paging.

## 3. Data Flow Diagram

```text
+-------+      +--------+      +-----------+      +-----------+      +-----------+
|       | ---> |        | ---> |           | ---> |           | ---> |           |
|  CLI  |      |Scheduler|      |   Core    |      |  Checks   |      | Reporter  |
|       | <--- |        | <--- |           | <--- |           | <--- |           |
+-------+      +--------+      +-----------+      +-----------+      +-----------+
      |                                                                          
      +-----------------+ Logging & Metrics Storage ----------------------------+
````

## 4. Non-Functional Requirements

* **Performance**: Minimal CPU/memory footprint to run on edge devices.
* **Reliability**: Automatic retries and error isolation so one failing check doesn’t halt the entire process.
* **Scalability**: Designed for both single-host and cluster-wide deployments; can be orchestrated via Kubernetes.
* **Security**: Runs with principle of least privilege, avoids storing sensitive data, and supports TLS for remote reporters.

## 5. Extension Points

* **Adding a New Check**: Create `argus/checks/<new_check>.py`, subclass `base.Check`, implement `run()`, and list the check name under `enabled_checks`.
* **Custom Reporters**: Drop a module under `argus/reporters/`, implement a `Reporter` class with `send(results)` method, and enable via `reporters:` config key.
* **Alternate Schedulers**: Replace APScheduler by providing a custom scheduler class in `argus/scheduler.py` and wiring via dependency injection in `cli.py`.

## 6. Cross-Cutting Concerns

* **Configuration Management**: Handled centrally in `argus/config.py`; supports YAML, JSON, and environment-variable overrides.
* **Logging**: Centralized logger in `argus/logger.py`, integrates with `rich.logging` for console output and Python’s `logging` for file handlers.
* **Testing**: Each layer has a dedicated test suite under `tests/`, using `pytest` fixtures and monkeypatch for simulating various OS states.

## 7. Dependency Summary

| Component         | Library                   | Purpose                |
| ----------------- | ------------------------- | ---------------------- |
| CLI               | `click`                   | Command parsing        |
| Scheduling        | `APScheduler`             | Job scheduling         |
| Metrics Fetching  | `psutil`, `wmi` (Windows) | Telemetry collection   |
| Console Rendering | `rich`                    | Pretty-printing tables |
| Config Parsing    | `PyYAML`, `json`          | Configuration loading  |
| Testing           | `pytest`, `pytest-mock`   | Automated test suite   |

```
```
