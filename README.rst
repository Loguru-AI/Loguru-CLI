Loguru CLI
==========

.. image:: https://raw.githubusercontent.com/Loguru-AI/Loguru-CLI/main/images/loguru-small.png
 :align: center

.. epigraph:: An interactive commandline interface that brings intelligence to your logs.



*********************
What is it?
*********************

**Loguru-CLI** (read as "Log Guru" 📋🧘) is a Python package that brings intelligence to your logs. It is designed to be a universal tool for log aggregation and analysis, with seamless integrations with any LLM (Large Language Model), whether self-hosted or cloud-based.

For more details, check out our GitHub repository: https://github.com/Loguru-AI/Loguru-CLI

*********************
Features
*********************

* Leverage LLMs to gain insights from your logs.
* Easily integrate with any LLM (self-hosted or cloud-service offerings).
* Easily hook up any log sources to gain insights on your logs. Perform refined/advanced queries supported by the
  logging platform/tool (by applying capabilities such as function-calling (tooling) of LLM) and gain insights on the
  results.
* Save and replay history.
* Scan and rebuild index from your logs.

.. tip:: Currently supports filesystem-based logs only, with plans to extend support to more log sources soon.

*********************
Getting Started
*********************

Install Loguru::

  pip install loguru-cli

Show config::

  loguru show-config

Scan and rebuild index from log files::

  loguru scan

Run app::

  loguru run

Example Interaction:

.. code-block:: javascript

   >>> List all the errors
   1. The error message indicates that there is a problem connecting to the PostgreSQL database at localhost on port 5432. Specifically, it says "Connection refused". This means that either the hostname or port number is incorrect, or the postmaster (the process that manages the PostgreSQL server) is not accepting TCP/IP connections.
   2. The stack trace shows that the problem is occurring in the HikariCP connection pool, which is being used to manage connections to the database. Specifically, it says "Exception during pool initialization". This suggests that there may be a problem with the configuration of the connection pool or the database connection settings.
   3. It is also possible that there is a firewall or network issue preventing the connection from being established. For example, if there is a firewall on the server running PostgreSQL, it may be blocking incoming connections on port 5432.

