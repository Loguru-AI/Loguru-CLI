# Loguru CLI

<p align="center">
  <img src="https://raw.githubusercontent.com/Loguru-AI/Loguru-CLI/main/loguru.png" width="200" alt="">
</p>

An interactive commandline interface that brings intelligence to your logs.

<p align="center">
    <a href="https://pypi.org/project/loguru-cli/">
        <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/loguru-cli?style=for-the-badge&label=Latest%20Version&color=green&link=https%3A%2F%2Fpypi.org%2Fproject%2Floguru-cli%2F">
    </a>
    <a href="https://pypi.org/project/loguru-cli/">
        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/Loguru-CLI?style=for-the-badge">
    </a>
</p>

### What is it?

**Loguru-CLI** (read as "Log Guru" 📋🧘) is a Python package that brings intelligence to your logs. It is designed to be a
universal tool for log
aggregation and analysis, with seamless integrations with any LLM (Large Language Model), whether self-hosted or
cloud-based.

### Features

- Leverage LLMs to gain insights from your logs.
- Easily integrate with any LLM (self-hosted or cloud-service offerings).
- Easily hook up any log sources to gain insights on your logs. Perform refined/advanced queries supported by the
  logging platform/tool (by applying capabilities such as function-calling (tooling) of LLM) and gain insights on the
  results.
- Save and replay history.
- Scan and rebuild index from your logs.

> [!NOTE]
> Currently supports filesystem-based logs only, with plans to extend support to more log sources soon.

### Roadmap

#### Log sources

| Log Source | Availability |
|------------|--------------|
| Log files  | ✔️           |
| ELK Stack  |              |
| Graylog    |              |

#### LLM Integrations

| LLM Integration | Availability |
|-----------------|--------------|
| Ollama          | ✔️           |
| OpenAI          |              |
| Amazon Bedrock  |              |

### Getting Started

```shell
pip install loguru-cli
```

> [!NOTE]  
> Install one of these based on your environment - `faiss-gpu==1.7.2` or `faiss-cpu==1.8.0.post1`

#### Show config

```shell
loguru show-config
```

#### Scan and rebuild index from log files

```shell
loguru scan
```

#### Run app

```shell
loguru run
```

#### Example Interactions

```text
>>> List all the errors

1. The error message indicates that there is a problem connecting to the PostgreSQL database at localhost on port 5432. Specifically, it says "Connection refused". This means that either the hostname or port number is incorrect, or the postmaster (the process that manages the PostgreSQL server) is not accepting TCP/IP connections.
2. The stack trace shows that the problem is occurring in the HikariCP connection pool, which is being used to manage connections to the database. Specifically, it says "Exception during pool initialization". This suggests that there may be a problem with the configuration of the connection pool or the database connection settings.
3. It is also possible that there is a firewall or network issue preventing the connection from being established. For example, if there is a firewall on the server running PostgreSQL, it may be blocking incoming connections on port 5432.
```

#### Sample Config

```json
{
  "num_chunks_to_return": 100,
  "ollama": {
    "hosts": [
      "http://localhost:11434/"
    ],
    "llm_name": "mistral",
    "embedding_model_name": "all-MiniLM-L6-v2",
    "options": {
      "temperature": 0.1
    }
  },
  "data_sources": [
    {
      "type": "filesystem",
      "ds_params": {
        "recursion_depth": 2,
        "file_size_limit": "100MB",
        "scan_locations": [
          {
            "location": "/path/to/log-dir",
            "pattern": "(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}[+-]\\d{2}:\\d{2})"
          },
          {
            "location": "/path/to/another-log-dir",
            "pattern": "(\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\.\\d{3}[+-]\\d{2}:\\d{2})"
          }
        ]
      }
    }
  ]
}
```

### Development

#### Install the libs

```shell
make libs
```

#### Setup as a local dev installation

```shell
make dev-install
```

#### Build wheel

```shell
make wheel
```

### Contributing

Contributions are most welcome! Whether it's reporting a bug, proposing an enhancement, or helping with code - any sort
of contribution is much appreciated.

### License

This project is licensed under the MIT License - see
the [LICENSE](https://github.com/Loguru-AI/Loguru-CLI/blob/main/LICENSE) file for details.
