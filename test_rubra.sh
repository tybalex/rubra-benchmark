#!/bin/bash

# Initialize variables
MODEL=""
PORT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    --model)
      MODEL="$2"
      shift # past argument
      shift # past value
      ;;
    --port)
      PORT="$2"
      shift
      shift
      ;;
    *)    # unknown option
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
done

# Check if model and port are set
if [ -z "$MODEL" ] || [ -z "$PORT" ]; then
  echo "Usage: bash test.sh --model <model> --port <port>"
  exit 1
fi

# Export the model
export TEST_MODEL=$MODEL

# Run the Python benchmark
python run_benchmark.py --port $PORT --models "$TEST_MODEL"

# Set environment variables
export GPTSCRIPT_INTERNAL_OPENAI_STREAMING=false
export GPTSCRIPT_PROVIDER_LOCALHOST_API_KEY=token-abc123

# Run gptscript commands with the provided model and port
BASE_URL="http://localhost:${PORT}/v1"
gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/count-lines-of-code.gpt "Find all .py pattern files in the current dir and count the lines of text in each file, add the result and print it"

gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/samples-readme.gpt "Look at each *.gpt file in gptscript_examples/, generate a summary for it. Each entry should include a link to the referenced file. Eventually concat everything together as a readme."

gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/fac.gpt

gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/time.gpt

gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/understand_python_script.gpt

gptscript --disable-cache --default-model "$TEST_MODEL from $BASE_URL" gptscript_examples/describe-code.gpt
