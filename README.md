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
- Markdown-based pretty-printing of LLM responses in your console

> [!NOTE]
> Currently supports filesystem-based logs only, with plans to extend support to more log sources soon.

### Roadmap

#### Log sources

| Log Source | Availability |
|------------|--------------|
| Log files  | ✅️           |
| ELK Stack  |              |
| Graylog    |              |

#### LLM Integrations

| LLM Integration | Availability | Additional Info                                                      |
|-----------------|--------------|----------------------------------------------------------------------|
| Ollama          | ✅️           |                                                                      |
| Gemini          | ✅️           | Generate API Key from [here](https://aistudio.google.com/app/apikey) |
| OpenAI          |              |                                                                      |
| Amazon Bedrock  |              |                                                                      |

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

This takes some time to scan your logs.

```text
Using config: /Users/macuser/.loguru/config.json
Scanning log locations to rebuild index. Please be patient. This may take a while.
Scanning directory: /Users/macuser/logs/auth...
Processing /Users/macuser/logs/auth/auth-service.log...
Creating new vector store with logs of /Users/macuser/logs/auth/auth-service.log...
Scanning directory: /Users/macuser/logs/customer-details...
Processing /Users/macuser/logs/customer-details/customer-details-service.log...
Updating vector store with logs of /Users/macuser/logs/customer-details/customer-details-service.log...
Scanning complete.
```

#### Run app

```shell
loguru run
```

#### Sample Interactions

```text
>>> List all the errors

1. The error message indicates that there is a problem connecting to the PostgreSQL database at localhost on port 5432. Specifically, it says "Connection refused". This means that either the hostname or port number is incorrect, or the postmaster (the process that manages the PostgreSQL server) is not accepting TCP/IP connections.
2. The stack trace shows that the problem is occurring in the HikariCP connection pool, which is being used to manage connections to the database. Specifically, it says "Exception during pool initialization". This suggests that there may be a problem with the configuration of the connection pool or the database connection settings.
3. It is also possible that there is a firewall or network issue preventing the connection from being established. For example, if there is a firewall on the server running PostgreSQL, it may be blocking incoming connections on port 5432.
```

```text
>>> What are the services used and what states are they in?

1. auth-service, which ran on 10/01/2024 and failed to start.
2. customer-details-service, which ran on 14/01/2024 and also failed to start.
```

```text
>>> Give me a summary of the top errors as a table with the first column as timestamp, second column as component/service name and the third column as the short error summary.
  
  ────────────────  ──────────────────────────  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Timestamp         Component/Service Name      Error Summary
  10/01/2024 11:05  auth-service                Connection to localhost:5432 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
  14/01/2024 12:06  customer-details-service    Connection to localhost:5432 refused. Check that the hostname and port are correct and that the postmaster is accepting TCP/IP connections.
  14/01/2024 12:09  customer-details-service    java.lang.NoClassDefFoundError: org/springframework/core/type/classreading/ClassFormatException
  ────────────────  ──────────────────────────  ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

#### Sample Config

```json
{
  "service": "gemini",
  "gemini": {
    "api_key": "your-api-key",
    "llm_name": "gemini-1.5-flash"
  },
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
  "num_chunks_to_return": 100,
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

### Roadmap

- [ ] Auto log pattern identification and parsing
- [ ] Support for non-filesystem based vector stores
- [ ] Ignore `/history`, `/bye` while storing the commands in command history
- [ ] Handle keyboard interrupt during the token-generation phase
- [ ] Support for streaming the responses to console
- [ ] Support for switching between raw mode and tools mode (function-calling). Maybe by enabling custom `set` command.
  For example: `set raw true` and `set raw false` to toggle between the modes.

### Contributing

Contributions are most welcome! Whether it's reporting a bug, proposing an enhancement, or helping with code - any sort
of contribution is much appreciated.

### Credits

- [MDV](https://github.com/axiros/terminal_markdown_viewer): Amazing package to pretty-print Markdown text in
  console.[^1]
- [Loghub](https://github.com/logpai/loghub): A beautiful collection of freely accessible logs. [^2]

[^1]: MDV Python pacakge on PyPi: https://pypi.org/project/mdv/

[^2]: Jieming Zhu, Shilin He, Pinjia He, Jinyang Liu, Michael R.
Lyu. [Loghub: A Large Collection of System Log Datasets for AI-driven Log Analytics](https://arxiv.org/abs/2008.06448).
IEEE International Symposium on Software Reliability Engineering (ISSRE), 2023.

### License

This project is licensed under the MIT License - see
the [LICENSE](https://github.com/Loguru-AI/Loguru-CLI/blob/main/LICENSE) file for details.
