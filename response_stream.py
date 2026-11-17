import os
from gpt4all import GPT4All

model_name = "Llama-3.2-3B-Instruct-Q4_K_M.gguf"
model_initial_prompt = "Você é um assistente útil, educado e direto. Responda sempre em português."
max_response_size = 512

current_folder = os.path.dirname(os.path.abspath(__file__))

stderr_fd = os.dup(2)
devnull = os.open(os.devnull, os.O_WRONLY)
os.dup2(devnull, 2)

try:
    model = GPT4All(
        model_name=model_name,
        model_path=current_folder,
        allow_download=False,
        device="cpu"
    )
finally:
    os.dup2(stderr_fd, 2)
    os.close(devnull)
    os.close(stderr_fd)

formated = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{model_initial_prompt}<|eot_id|>"
template_chat = "<|start_header_id|>user<|end_header_id|>\n\n{0}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"

def generate_response_stream(message: str):
    with model.chat_session(system_prompt=formated, prompt_template=template_chat):
        for token in model.generate(message, max_tokens=max_response_size, streaming=True):
            if token == "<|eot_id|>": continue
            yield token