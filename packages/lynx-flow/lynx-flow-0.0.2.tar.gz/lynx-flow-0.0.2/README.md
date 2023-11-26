# Lynx Flow

Lynx Flow is a streamlined and straightforward library for building method call sequences.
Simplify your code with clear and concise constructs using Lynx Flow.

![Lynx Flow logo](https://toghrulmirzayev.github.io/lynx-flow/lynx-flow.png)

# Getting started

* Install lynx-flow
  ```commandline
  pip install lynx-flow
  ```

* Import Lynx class to start
  ```python
  from lynx_flow.lynx import Lynx
  ```

* Build your request in single, clear and readable flow
  ```python
  Lynx().get().with_url(URL).with_headers(HEADERS).where().json().tobe().equal("The service is up and running")
  ```
  
