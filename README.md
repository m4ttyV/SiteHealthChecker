# Site Health Checker

Python CLI application for monitoring website availability and response time.

The application reads a list of websites from a YAML configuration file, performs HTTP health checks concurrently, stores results in SQLite and generates aggregated monitoring statistics.

## Features

- HTTP availability monitoring
- Response-time measurement
- HTTP status code tracking
- Concurrent website checks using `ThreadPoolExecutor`
- SQLite history storage
- Aggregated availability statistics
- JSON statistics export
- File-based logging
- Continuous monitoring mode
- YAML-based configuration
- Configurable list of monitored websites

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Requests | HTTP health checks |
| SQLite | Monitoring history |
| PyYAML | Configuration |
| ThreadPoolExecutor | Concurrent checks |
| JSON | Statistics export |

## How It Works

```text
config.yaml
    │
    ▼
List of websites
    │
    ▼
ThreadPoolExecutor
    │
    ├── HTTP request
    ├── HTTP status
    └── Response time
    │
    ▼
SQLite database
    │
    ├── History
    └── Aggregated statistics
            │
            ▼
        stats.json
```
