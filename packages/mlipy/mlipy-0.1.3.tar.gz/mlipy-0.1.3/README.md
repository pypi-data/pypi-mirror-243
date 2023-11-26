# mlipy

<!--
[![Build][build-image]]()
[![Status][status-image]][pypi-project-url]
[![Stable Version][stable-ver-image]][pypi-project-url]
[![Coverage][coverage-image]]()
[![Python][python-ver-image]][pypi-project-url]
[![License][mit-image]][mit-url]
-->
[![Downloads](https://img.shields.io/pypi/dm/mlipy)](https://pypistats.org/packages/mlipy)
[![Supported Versions](https://img.shields.io/pypi/pyversions/mlipy)](https://pypi.org/project/mlipy)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Pure **Python**-based **Machine Learning Interface** for multiple engines with multi-modal support.

Python HTTP Server/Client (including WebSocket streaming support) for:
- [candle](https://github.com/huggingface/candle)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [LangChain](https://python.langchain.com)


# Prerequisites

## Debian/Ubuntu

```bash
sudo apt update -y
sudo apt install build-essential git curl libssl-dev libffi-dev pkg-config
```


### Rust

1) Using latest system repository:

```bash
sudo apt install rustc cargo
```

2) Install rustup using official instructions:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
rustup default stable
```


### Python

1) Install Python using internal repository:
```bash
sudo apt install python3.11 python3.11-dev python3.11-venv
```

2) Install Python using external repository:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update -y
sudo apt install python3.11 python3.11-dev python3.11-venv
```


## Arch/Manjaro

### Rust

1) Using latest system-wide rust/cargo:
```bash
sudo pacman -Sy base-devel openssl libffi git rust cargo rust-wasm wasm-bindgen
```

2) Using latest rustup:
```bash
sudo pacman -Sy base-devel openssl libffi git rustup
rustup default stable
```


## macOS

```bash
brew update
brew install rustup
rustup default stable
```


# llama.cpp

```bash
cd ~
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make
```


# candle

```bash
cd ~
git clone https://github.com/huggingface/candle.git
cd candle
find candle-examples -type f -exec sed -i 's/println/eprintln/g' {} +
cargo build -r --examples
```


# Run Development Server

Setup virtualenv and install requirements:

```bash
git clone https://github.com/mtasic85/mlipy.git
cd mlipy

python3.11 -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```

Download models:

```bash
# NOTE: login in case you need to accept terms and conditions for some models
# huggingface-cli login

# mistral
huggingface-cli download TheBloke/Mistral-7B-v0.1-GGUF mistral-7b-v0.1.Q4_K_M.gguf
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.1-GGUF mistral-7b-instruct-v0.1.Q4_K_M.gguf
huggingface-cli download TheBloke/zephyr-7B-beta-GGUF zephyr-7b-beta.Q4_K_M.gguf
huggingface-cli download TheBloke/Yarn-Mistral-7B-128k-GGUF yarn-mistral-7b-128k.Q4_K_M.gguf

# llama2
# huggingface-cli download meta-llama/Llama-2-7b-hf
huggingface-cli download TheBloke/Orca-2-7B-GGUF orca-2-7b.Q4_K_M.gguf
huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf
huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf
huggingface-cli download TheBloke/Yarn-Llama-2-7B-128K-GGUF yarn-llama-2-7b-128k.Q4_K_M.gguf

# stable-lm
huggingface-cli download TheBloke/rocket-3B-GGUF rocket-3b.Q4_K_M.gguf

# code mistral-based
huggingface-cli download TheBloke/sqlcoder-7B-GGUF sqlcoder-7b.Q4_K_M.gguf
```

Run server:

```bash
python -B mli/server.py
```


# Run Examples

```bash
python -B examples/sync_demo.py
python -B examples/async_demo.py
python -B examples/langchain_sync_demo.py
python -B examples/langchain_async_demo.py
```


# Run mlipy Server

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -U mlipy
python -B -m mli.server
```
