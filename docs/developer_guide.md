# Developer Guide for Building Argus (Deep Dive)

A comprehensive, step-by-step guide to designing, developing, testing, and deploying Argus Monitor. This document provides detailed instructions, best practices, and code examples to help you build a robust, maintainable, and extensible system monitoring tool.

---

## 1. Environment & Tools Setup

Before writing any code, prepare your development environment to ensure consistency across systems.

1. **Install Python 3.9+**

   * Use your OS package manager (`apt`, `brew`) or `pyenv` to install and manage Python versions.
   * Verify with:

     ```bash
     python3 --version  # Expected: 3.9.x or above
     ```
2. **Create and Activate Virtual Environment**

   * Isolates dependencies per-project:

     ```bash
     python3 -m venv venv
     source venv/bin/activate   # Windows: venv\\Scripts\\activate
     ```
   * Confirm:

     ```bash
     which python            # Should point to venv
     pip list                # Empty or minimal packages
     ```
3. **Install Core Libraries**

   * Fundamental runtime dependencies:

     ```bash
     pip install click apscheduler psutil rich PyYAML
     ```
   * Verify installation:

     ```bash
     pip show psutil rich
     ```
4. **Set Up Development & QA Tools**

   * For testing, linting, formatting, and type checking:

     ```bash
     pip install pytest pytest-cov flake8 mypy black pre-commit
     ```
   * Initialize pre-commit hooks to enforce code quality:

     ```bash
     pre-commit install
     ```
5. **Optional Tooling**

   * **Docker**: Containerize development environment and runtime.
   * **IDE Extensions**: Install Python linting/formatting plugins for VS Code or PyCharm.
   * **CI Runner**: Configure local GitHub Actions runner for faster iteration.

---

## 2. Project Scaffolding & Structure

Create a standardized layout to separate concerns and facilitate growth.

```text
argus-monitor/
├── README.md
├── LICENSE
├── pyproject.toml        # Build config and metadata
├── requirements.txt      # Pin exact versions for reproducibility
├── config/               # Default and example config files
│   ├── config.yaml
│   └── config.example.json
├── argus/                # Main package
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── logger.py
│   ├── scheduler.py
│   ├── core.py
│   ├── report.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── metrics.py   # Parsing & normalization functions
│   │   └── platform.py  # OS-specific helpers
│   └── checks/
│       ├── __init__.py
│       ├── base.py      # Abstract Check interface
│       ├── cpu_check.py
│       ├── ram_check.py
│       ├── disk_check.py
│       ├── network_check.py
│       └── gpu_check.py
├── tests/                # Test suite
│   ├── conftest.py      # Shared fixtures & mocks
│   ├── test_cpu_check.py
│   ├── test_ram_check.py
│   ├── ...
├── docs/                 # Supplementary documentation
│   ├── architecture.md
│   ├── usage.md
│   └── developer_guide.md
└── .github/              # CI/CD workflows
    └── workflows/
        ├── lint.yml
        ├── test.yml
        └── release.yml
```

* **Modularity**: Separate CLI, config, core logic, checks, and utils to minimize coupling.
* **Testability**: Align test files with modules to simplify coverage analysis.
* **Documentation**: Keep docs in sync with code; use markdown for clarity.

---

## 3. Designing the Base Check Interface

Define a clear contract for all metric checks.

```python
# argus/checks/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Check(ABC):
    """
    Base class for all Argus checks.

    Attributes:
      name:            Unique check name used in config and reporting.
      categories:      Optional list of classification tags (e.g., ['performance', 'resource']).
    """
    name: str = "base"
    categories: Optional[list] = None

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """
        Execute the check logic and return a result dict:
          - name: str
          - status: 'OK' | 'WARN' | 'CRIT' | 'UNKNOWN'
          - metrics: Dict[str, float|str]
          - details: Optional[str]
        """
        raise NotImplementedError()

    def evaluate(self, metric: str, value: float) -> str:
        """
        Compare metric value against thresholds in config.
        Returns status string.
        """
        thresh = self.config.get('thresholds', {}).get(self.name, {})
        warn = thresh.get('warn', float('inf'))
        crit = thresh.get('crit', float('inf'))
        if value >= crit:
            return 'CRIT'
        if value >= warn:
            return 'WARN'
        return 'OK'
```

**Extendability**: Future checks like `temperature_check.py` can subclass `Check` and leverage `evaluate()`.

---

## 4. Implementing Concrete Checks

Follow the pattern below for each resource:

### 4.1 CPU Check

```python
# argus/checks/cpu_check.py
from .base import Check
import psutil

class CPUCheck(Check):
    name = 'cpu'
    categories = ['performance']

    def run(self) -> Dict[str, Any]:
        usage = psutil.cpu_percent(interval=None)
        status = self.evaluate('usage', usage)
        return {
            'name': self.name,
            'status': status,
            'metrics': {'usage_percent': usage},
            'details': f'CPU utilization at {usage:.1f}%'
        }
```

### 4.2 RAM Check

```python
# argus/checks/ram_check.py
from .base import Check
import psutil

class RAMCheck(Check):
    name = 'ram'
    categories = ['resource']

    def run(self) -> Dict[str, Any]:
        mem = psutil.virtual_memory()
        used = mem.used / (1024**2)
        total = mem.total / (1024**2)
        pct = mem.percent
        status = self.evaluate('usage', pct)
        return {
            'name': self.name,
            'status': status,
            'metrics': {'used_mb': used, 'total_mb': total, 'percent': pct},
            'details': f'{used:.0f}MiB / {total:.0f}MiB used'
        }
```

*Repeat analogous patterns for Disk, Network, GPU.*

---

## 5. Configuration Management & Validation

Implement `load_config()` in `argus/config.py` to centralize settings:

```python
import os, json, yaml
from typing import Dict

def load_config(path: str = None) -> Dict:
    defaults = {
        'enabled_checks': ['cpu', 'ram', 'disk', 'network'],
        'thresholds': {},
        'poll_interval': 60,
        'output_format': 'table',
        'log_level': 'INFO'
    }
    cfg_path = path or os.getenv('ARGUS_CONFIG_PATH', 'config/config.yaml')
    if cfg_path.endswith('.json'):
        with open(cfg_path) as f: data = json.load(f)
    else:
        with open(cfg_path) as f: data = yaml.safe_load(f)
    return {**defaults, **data}
```

**Schema Validation**: Use `pydantic` models to enforce types and required fields, raising clear errors on misconfiguration.

---

## 6. Building the CLI with Click

Setup commands, options, and help text in `argus/cli.py`:

```python
import click
from .config import load_config
from .scheduler import Scheduler
from .logger import setup_logging

@click.group()
def cli():
    """Argus Monitor CLI"""
    pass

@cli.command()
@click.option('-c', '--config', help='Path to config file')
@click.option('-i', '--interval', type=int, help='Polling interval (s)')
@click.option('-o', '--output', type=click.Choice(['table','json']), help='Output format')
def status(config, interval, output):
    """Run monitoring checks"""
    cfg = load_config(config)
    if interval: cfg['poll_interval'] = interval
    if output: cfg['output_format'] = output
    setup_logging(cfg['log_level'])
    Scheduler(cfg).run_forever()

if __name__ == '__main__':
    cli()
```

Add subcommands for `checks`, `report`, `version`, and shell `completion` to round out the UX.

---

## 7. Scheduler & Orchestration

Encapsulate job scheduling in `argus/scheduler.py`:

```python
from apscheduler.schedulers.background import BackgroundScheduler
import signal

class Scheduler:
    def __init__(self, config):
        self.config = config
        self.scheduler = BackgroundScheduler()

    def run_all(self):
        from .core import Core
        Core(self.config).execute_checks()

    def run_forever(self):
        interval = self.config['poll_interval']
        self.scheduler.add_job(self.run_all, 'interval', seconds=interval)
        self.scheduler.start()

        def shutdown(signum, frame):
            self.scheduler.shutdown(wait=False)
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

        # Block until scheduler is stopped
        self.scheduler._event.wait()
```

**Backoff & Retries**: Incorporate retry logic in `run_all()` or at individual check levels.

---

## 8. Core Execution & Aggregation

In `argus/core.py`, dynamically load checks and gather results:

```python
import importlib, pkgutil, socket, time

class Core:
    def __init__(self, config):
        self.config = config

    def _discover_checks(self):
        import argus.checks as package
        for _, name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f'argus.checks.{name}')
            for attr in dir(module):
                cls = getattr(module, attr)
                if isinstance(cls, type) and issubclass(cls, package.base.Check) and cls is not package.base.Check:
                    yield cls(self.config)

    def execute_checks(self):
        results = []
        timestamp = time.time()
        host = socket.gethostname()
        for check in self._discover_checks():
            try:
                res = check.run()
                res.update({'timestamp': timestamp, 'host': host})
                results.append(res)
            except Exception as e:
                results.append({'name': check.name, 'status': 'UNKNOWN', 'metrics': {}, 'details': str(e)})
        from .report import Reporter
        Reporter(self.config).send(results)
```

---

## 9. Reporting & Output

Design `argus/report.py` to support multiple output sinks:

```python
import json
from rich.table import Table
from rich.console import Console

class Reporter:
    def __init__(self, config):
        self.cfg = config
        self.console = Console()

    def send(self, results):
        fmt = self.cfg['output_format']
        if fmt == 'json':
            print(json.dumps(results, default=str))
        else:
            table = Table(title='System Metrics')
            table.add_column('Check')
            table.add_column('Status')
            table.add_column('Metric')
            table.add_column('Value')
            table.add_column('Details')
            for r in results:
                for m,v in r['metrics'].items():
                    table.add_row(r['name'], r['status'], m, str(v), r.get('details',''))
            self.console.print(table)
```

Extend `Reporter` to push to databases, files, or alerts via plugin registration.

---

## 10. Logging Best Practices

Centralize logging setup in `argus/logger.py`:

```python
import logging
from rich.logging import RichHandler

def setup_logging(level: str = 'INFO'):
    logging.basicConfig(
        level=level,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    return logging.getLogger('argus')
```

* Use named loggers per module (`logger = logging.getLogger(__name__)`).
* Choose appropriate levels (`DEBUG` for development, `INFO` for production).
* Rotate logs using `logging.handlers.RotatingFileHandler` if needed.

---

## 11. Testing Strategy & Coverage

Ensure reliability with a thorough test suite:

* **Unit Tests**: Test each `Check` class by monkeypatching `psutil` or OS calls.
* **Integration Tests**: Use a temporary SQLite or file-based config to run full `status` command.
* **Fixtures**: Define common configs and mock data in `tests/conftest.py`.
* **Coverage**: Aim for >90% code coverage with `pytest-cov`:

  ```bash
  pytest --cov=argus --cov-report=term-missing
  ```
* **Static Analysis**: Enforce type checking and lint compliance:

  ```bash
  mypy argus
  flake8 argus
  ```

---

## 12. Packaging, Distribution & Release

Prepare for open-source release:

1. **Metadata**: Update `pyproject.toml` or `setup.cfg`:

   ```toml
   [project]
   name = "argus-monitor"
   version = "0.1.0"
   description = "Lightweight system monitoring tool"
   authors = [ {name="Your Name", email="you@example.com"} ]
   dependencies = ["click", "psutil", "rich"]
   ```
2. **Build**:

   ```bash
   python -m build  # Generates dist/argus-monitor-0.1.0*.whl
   ```
3. **Publish**:

   ```bash
   twine upload dist/*
   ```
4. **Release Notes**: Draft release notes or CHANGELOG.md documenting features and breaking changes.

---

## 13. Observability & Metrics Persistence

For long-term analysis and dashboarding:

* **InfluxDB / Prometheus**: Push metrics through HTTP requests or client libraries.
* **SQLite / CSV**: Write metrics locally for ad-hoc querying.
* **Health Endpoints**: Expose a simple HTTP `/metrics` endpoint for scraping.

---

## 14. Security & Compliance

* **Least Privilege**: Only request filesystem or WMI permissions necessary for metrics.
* **Data Sanitization**: Ensure all external inputs (config, env vars) are validated.
* **Secure Transport**: Use HTTPS/TLS for remote webhooks and persistence endpoints.
* **Audit Logging**: Track configuration loads and critical errors for post-incident analysis.

Congratulations! You now have a detailed blueprint to architect, develop, test, and release Argus Monitor as a production-ready open-source project.
