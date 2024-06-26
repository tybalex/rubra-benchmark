# Rubra Benchmark

## Quickstart

### Prerequisites

1.
To start a server to test Rubra models:
* [rubra-vllm](https://github.com/rubra-ai/vllm?tab=readme-ov-file#quickstart)
* [tools.cpp](https://github.com/rubra-ai/tools.cpp?tab=readme-ov-file#toolscpp-quickstart)


To test base models with LocalAI:
```
docker compose up
```
This will start a server 

by default 5 models will get downloaded. For more details or add more models, check out the `models` dir and add yaml config file.

2. install gptscript: `curl https://get.gptscript.ai/install.sh | sh`
3. install python dependancies: 
```
pip install -r requirements.txt
```


### Run test

rubra-vllm:
```
bash test_rubra.sh --port 8000 --model sanjay920/Llama-3-8b-function-calling-alpha-v1
```

tools.cpp:
```
bash test_rubra.sh --port 1234 --model Llama-3-8b-function-calling-alpha-v1.gguf
```

localai:
```
bash test_rubra.sh --port 8080  --model Meta-Llama-3-8B-Instruct
```