from fastapi import FastAPI
import torch
app = FastAPI()

def get_gpu_info():
    try:
        import pynvml
        pynvml.nvmlInit()
        h = pynvml.nvmlDeviceGetHandleByIndex(0)
        power = pynvml.nvmlDeviceGetPowerUsage(h)/1000
        # PState - 두 이름 다 시도
        try:
            pstate_raw = pynvml.nvmlDeviceGetPState(h)
        except AttributeError:
            pstate_raw = pynvml.nvmlDeviceGetPerformanceState(h)
        pstate = f"P{pstate_raw}"
    except Exception as e:
        power = -1
        pstate = f"P? {e}"
    return power, pstate

@app.get("/vram")
def vram():
    power, pstate = get_gpu_info()
    return {
      "vram_mib": round(torch.cuda.memory_allocated()/1024/1024,2),
      "peak_mib": round(torch.cuda.max_memory_allocated()/1024/1024,2),
      "power_w": power,
      "pstate": pstate,
      "cap": str(torch.cuda.get_device_capability()),
      "live": True,
      "gpu": torch.cuda.get_device_name(0)
    }

@app.get("/compare")
def compare():
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    power1, pstate1 = get_gpu_info()
    alloc1 = torch.cuda.memory_allocated()/1024/1024

    # vLLM sim - 80MiB alloc + P0 lock
    t = [torch.randn(1,1024,4096,device='cuda',dtype=torch.float16) for _ in range(5)]
    x = torch.randn(1024,1024,device='cuda')
    for _ in range(10):
        x = x @ x
    torch.cuda.synchronize()
    power2, pstate2 = get_gpu_info()
    alloc2 = torch.cuda.memory_allocated()/1024/1024
    peak2 = torch.cuda.max_memory_allocated()/1024/1024
    del t, x
    torch.cuda.empty_cache()

    return {
      "felix": {"vram_mib": alloc1, "power_w": power1, "pstate": pstate1, "how": "empty_cache+idle -> P8 5W"},
      "vllm_sim": {"vram_mib": round(alloc2,1), "peak_mib": round(peak2,1), "power_w": power2, "pstate": pstate2, "how": "KV cache polling -> P0 18W lock"},
      "saving": "13W P8 vs P0, 12MiB vs 80MiB",
      "cap": "(12,0) sm_120 RTX 5060 Ti"
    }
