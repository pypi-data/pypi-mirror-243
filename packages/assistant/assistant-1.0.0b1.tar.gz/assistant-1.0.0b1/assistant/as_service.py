"""LLM genaration and embedding service."""

import os
import torch
import subprocess

G = 1000

print("Checking for CUDA GPU...", end="")

def get_gpu_info():
    """Get GPU info."""
    try:
        output = subprocess.check_output(
            "nvidia-smi --query-gpu=memory.total,memory.used --format=csv,nounits,noheader",
            shell=True,
        )
        _gpu_memory = output.decode("utf-8").strip().split("\n")
        _gpu_memory = [
            int(mem) for gpu_mem in _gpu_memory for mem in gpu_mem.split(", ")
        ]
        gpu_memory = dict(zip(range(len(_gpu_memory)), _gpu_memory))
    except subprocess.CalledProcessError:
        gpu_memory = None
    return gpu_memory  # in MB

def get_gpu_memory():
    """Get GPU memory."""
    gpu_memory = get_gpu_info()
    if gpu_memory is None:
        return None
    return int(gpu_memory[0]) - int(gpu_memory[1])  # in MB

# assert we have at least 1 GPU w/ at least 12 Gb of VRAM and a compute score of 6.0 or above.

def get_gpu_count():
    """Get GPU count."""
    gpu_memory = get_gpu_info()
    if gpu_memory is None:
        return None
    return torch.cuda.device_count()

def get_gpu_memory_usage():
    """Get GPU memory usage."""
    gpu_memory = get_gpu_info()
    if gpu_memory is None:
        return None
    return gpu_memory[1] # in MB

def check_cuda_gpu():
    """Check CUDA GPU and return active GPU ID."""
    
    gpu_count = get_gpu_count()

    assert gpu_count is not None, "No CUDA GPUs available!"
    assert gpu_count >= 1, "No CUDA GPUs available!"

    print(f"\nFound {gpu_count} CUDA GPU{'s' if gpu_count > 1 else ''} available.")

    gpu_mem = get_gpu_memory()

    assert gpu_mem is not None, "No CUDA GPUs available!"
    assert gpu_mem >= 12*G, f"Not enough memory available on GPU! (12 Gb required but only {gpu_mem/G} Gb available.)"

    def get_gpu_id():
        """Get GPU id."""
        # if we have more than 2 GPU, we can use all GPUS (most likely a server)
        # but if we only have 2, use the second one as the first is probably being used by the display
        if not gpu_count:
            return None
        if gpu_count > 2:
            gpu_memory = get_gpu_info()
            if not gpu_memory:
                return None
            max_mem_id = ",".join(range(gpu_count - 1, 0))
            return max_mem_id
        elif gpu_count == 2:
            return str(1)
        else:
            return str(gpu_count - 1)

    gpu_id = get_gpu_id()

    assert gpu_id and gpu_id != str(0), f"No CUDA GPUs available! ({gpu_id=})"

    print(f"Trying to use GPU#{gpu_id}.")

    def get_gpu_compute_score(gid: int):
        """Get GPU compute score by ID."""
        gpu_compute_score = torch.cuda.get_device_capability()
        return gpu_compute_score

    _ids = []
    for gid in gpu_id.split(","):
        c_score = get_gpu_compute_score(int(gid))

        if c_score >= (6, 0):
            _ids.append(gid)
    
    assert _ids, f"No CUDA GPUs available! ({_ids=})"
    
    r = ",".join(_ids)
    return r

gpu = check_cuda_gpu()

print(f"Using GPU(s)#{gpu}.")

# Make sure docker is installed and configured for gpu passthrough
print("Checking for Docker GPU support...", end="")

def get_nvctr():
    """Get NVCTR."""
    nvctr = subprocess.check_output(
        "nvidia-container-cli --load-kmods info",
        shell=True,
    )
    runtime_dict = {}
    for line in nvctr.decode("utf-8").strip().split("\n"):
        lsplt = line.split(":")
        if ":" in line and len(lsplt) == 2:
            k, v = lsplt
            runtime_dict[k.strip()] = v.strip()
    return runtime_dict

def get_docker():
    docker_bin = subprocess.check_output(
        "which docker",
        shell=True,
    )
    return docker_bin.decode("utf-8").strip()


def check_nvidia_container_toolkit():
    """Check GPU in docker container."""
    
    docker_bin = get_docker()
    assert docker_bin
    
    docker_gpu_runtime = get_nvctr()
    assert docker_gpu_runtime

check_nvidia_container_toolkit()
print("Done.")

print("Starting Assistant as a service...")

# model_id = "wasertech/assistant-llama2-7b-merge-bf16"
# model_id = "wasertech/assistant-llama2-7b-chat-fp16"
# model_id = "TheBloke/Llama-2-7b-chat-fp16"
# model_id = "Photolens/llama-2-7b-langchain-chat"
# model_id = "wasertech/assistant-llama2-chat-rlhf-awq"
# model_id = "mistralai/Mistral-7B-Instruct-v0.1"
# tokenizer_id = "mistralai/Mistral-7B-Instruct-v0.1"

model_id = "ehartford/dolphin-2.2.1-mistral-7b"
tokenizer_id = "ehartford/dolphin-2.2.1-mistral-7b"

mount_from = "~/.cache/huggingface/"

# VLLM
mount_to = "/root/.cache/huggingface/"
port = 5085
# --env N_GPUS="{gp}" \
# --env DTYPE="half" \
# --env QUANT="awq" \
# --env GPU_MEM="0.35" \

s = f"""docker run \
-it \
-p {port}:{port} \
--gpus=all \
--privileged \
--shm-size=8g \
--ulimit memlock=-1 \
--ulimit stack=67108864 \
--mount type=bind,src=`echo {mount_from}`,dst={mount_to} \
--env MODEL_ID="{model_id}" \
--env TOKENIZER_ID="{tokenizer_id}" \
--env PORT="{port}" \
--env DTYPE="half" \
--env CUDA_VISIBLE_DEVICES="{gpu}" \
wasertech/vllm-inference-api:latest
"""

if __name__ == "__main__":
    print("Launching container...")
    os.system(s)

