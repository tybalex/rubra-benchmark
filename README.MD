# Rubra Benchmark

## Quickstart

### Prerequisites
To start a server to test Rubra models:
* [rubra-vllm](https://github.com/rubra-ai/vllm?tab=readme-ov-file#quickstart)
* [tools.cpp](https://github.com/rubra-ai/tools.cpp?tab=readme-ov-file#toolscpp-quickstart)


To test base models with LocalAI:
```
docker compose up
```
This will start a server 

by default 5 models will get downloaded. For more details or add more models, check out the `models` dir and add yaml config file.

### Run test

tools.cpp:
```
bash test_rubra.sh --port 1234 --model Llama-3-8b-function-calling-alpha-v1.gguf
```

localai:
```
bash test_rubra.sh --port 8080  --model Meta-Llama-3-8B-Instruct
```