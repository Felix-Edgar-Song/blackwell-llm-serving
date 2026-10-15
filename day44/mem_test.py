import torch

# 기초 0: 내 GPU 확인 - sm_120이 뭔지
print("=== 내 GPU ===")
print(f"Capability: {torch.cuda.get_device_capability()}")  # (12,0) = sm_120 Blackwell
print(f"CUDA: {torch.version.cuda}")  # cu128이어야 5060 Ti 지원
print(f"Name: {torch.cuda.get_device_name()}")
print()

# 기초 1: 메모리 3형제
print("=== 메모리 3형제 ===")
torch.cuda.reset_peak_memory_stats()  # 측정 시작

print(f"1. 시작: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB")  # 0 MiB

x = torch.randn(1000, 1000, device='cuda', dtype=torch.float16)  # 2MB짜리 텐서
print(f"2. 텐서 1개 후: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB")  # ~2 MiB allocated

y = torch.randn(1000, 1000, device='cuda', dtype=torch.float16)
print(f"3. 텐서 2개 후: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB")  # ~4 MiB
print(f"   Peak는? {torch.cuda.max_memory_allocated()/1024/1024:.2f} MiB")  # Peak = 지금까지 최대

del x, y
print(f"4. del 후: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB")  # 0 아니고 4MiB? 캐시 때문!

torch.cuda.empty_cache()  # 진짜 비우기 - 이게 P8 4W로 가는 열쇠
print(f"5. empty_cache 후: {torch.cuda.memory_allocated()/1024/1024:.2f} MiB")  # 이제 0
print(f"   그래도 Peak는 유지: {torch.cuda.max_memory_allocated()/1024/1024:.2f} MiB")  # 265.5MiB Peak의 원리


