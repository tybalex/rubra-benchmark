from utils import get_oai_response, run_completion
from functools import partial
import json
from tqdm import tqdm
import os
import argparse




parser = argparse.ArgumentParser(description="benchmark")
parser.add_argument('--verbose', action='store_true', help="Increase output verbosity")
parser.add_argument('--models', required=True,  help="Specify the models name to test, if multiple models, use comma to separate, such as 'model1,model2'")
parser.add_argument('--port', required=True,  help="Specify the port of the model api")


# Parse the arguments
args = parser.parse_args()
models = args.models.split(",")
verbose = args.verbose
port = args.port

local_api_key = "sk-"
local_base_url = f"http://localhost:{port}/v1/"
get_model_response = partial(get_oai_response, api_key=local_api_key, base_url=local_base_url)
print(f"Pointing to local URL: {local_base_url}\n")

with open('questions.json', 'r') as file:
    data = json.load(file)
    questions = [d["user_query"] for d in data['queries']]
directory = "output"
if not os.path.exists(directory):
    os.makedirs(directory)
    
for model in models:
    print(f"working on model : {model}")
    qa_pair = []
    for i, q in enumerate(tqdm(questions)):
        msgs = run_completion(get_model_response, q, model=model)
        qa_pair.append({"index":i ,"question": q, "messages": msgs})

    if not os.path.exists(os.path.join(directory, model)):
        os.makedirs(os.path.join(directory, model))
    with open(os.path.join(directory, model, "benchmark_output.json"), 'w') as fout:
        json.dump(qa_pair, fout, indent=4)

