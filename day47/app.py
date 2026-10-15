import torch
# vLLM 스타일 vs 네 스타일 비교
print(f"GPU: {torch.cuda.get_device_name()} {torch.cuda.get_device_capability()}")

# 1. 네 방식 - P8 가능
torch.cuda.empty_cache()
alloc = torch.cuda.memory_allocated()/1024/1024
print(f"Felix P8 style: {alloc:.2f} MiB allocated, empty_cache done")

# 2. vLLM 스타일 재현 - 902MiB 흉내
# transformers 없이 torch로 KV cache 느낌
x = torch.randn(1, 1, 4096, 4096, device='cuda', dtype=torch.float16) # ~32MiB
# 여러 레이어 쌓으면 902MiB
tensors = [torch.randn(2, 32, 128, device='cuda', dtype=torch.float16) for _ in range(20)]
alloc2 = torch.cuda.memory_allocated()/1024/1024
peak = torch.cuda.max_memory_allocated()/1024/1024
print(f"vLLM style: {alloc2:.1f} MiB allocated, Peak: {peak:.1f} MiB")
# P0 유지 시뮬레이션 - 계속 compute
for _ in range(10):
    _ = x @ x.T
    torch.cuda.synchronize()
print(f"After compute loop - still P0, cannot go P8")
del tensors, x
torch.cuda.empty_cache()
print(f"After cleanup: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB -> P8 possible again")
