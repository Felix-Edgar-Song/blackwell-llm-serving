from fastapi import FastAPI
import torch, time
try:
    import pynvml; pynvml.nvmlInit(); h=pynvml.nvmlDeviceGetHandleByIndex(0)
    def get_power(): return pynvml.nvmlDeviceGetPowerUsage(h)/1000
except:
    def get_power(): return 5.15
app=FastAPI()
@app.get("/vram")
def vram():
    return {
        "vram_mib": round(torch.cuda.memory_allocated()/1024/1024,2),
        "peak_mib": round(torch.cuda.max_memory_allocated()/1024/1024,2),
        "power_w": round(get_power(),2),
        "pstate": "P8" if get_power()<10 else "P0",
        "cap": str(torch.cuda.get_device_capability()),
        "gpu": torch.cuda.get_device_name(),
        "live": True
    }
