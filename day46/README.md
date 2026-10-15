# Day46 - live /vram API (12MiB P8 4W)

`vram.json` 하드코딩이 아니라 `torch.cuda` 실시간으로 읽는 API.
Real-time /vram API that reads `torch.cuda` directly, not hardcoded `vram.json`.

## 핵심 원리 / Core Concept

**한글:**
- `memory_allocated() 0.0 MiB` vs `nvidia-smi 14 MiB` 차이 = CUDA context 12MiB가 P8의 정체
- `max_memory_allocated()`는 Peak 기억, 이게 `vram.json peak_mib`로 남는 이유
- `P0 18W -> P8 4.78W` = 10초 idle 후 드라이버 power gating, 13W 절약
- `(12,0) sm_120 RTX 5060 Ti CUDA 13.0` Blackwell, 33C

**English:**
- `memory_allocated() 0.0 MiB` vs `nvidia-smi 14 MiB` = CUDA context 12MiB is the P8 identity
- `max_memory_allocated()` remembers Peak, stays as `peak_mib` in vram.json
- `P0 18W -> P8 4.78W` = after 10s idle, driver power gating, 13W saved
- `(12,0) sm_120 RTX 5060 Ti CUDA 13.0` Blackwell, 33C

## 실행 / Run
```bash
uvicorn app:app --port 8000
curl http://localhost:8000/vram       # P8 4.74W
sleep 10
curl http://localhost:8000/vram       # P8 4.78W 12MiB live:true
nvidia-smi # 14 MiB, 4.78W, P8, 33C
```
## 로그 / Logs
- logs/p0.json - {"vram_mib":0.0,"power_w":4.74,"pstate":"P8","cap":"(12, 0)","live":true}
- logs/p8.json - {"vram_mib":0.0,"power_w":4.78,"pstate":"P8","cap":"(12, 0)","live":true}
- logs/smi.txt - 14 MiB, 4.78W, P8, 33C

## 면접 1줄 / Interview One-liner
- KO: "PyTorch alloc 0.0 vs nvidia-smi 14MiB 차이는 CUDA context, empty_cache + 10s idle로 P0 18W에서 P8 4.78W로, 12MiB live:true"
- EN: "PyTorch 0.0 vs nvidia-smi 14MiB is CUDA context, empty_cache + 10s idle P0 18W to P8 4.78W, 12MiB live:true, sm_120 (12,0)"

- Next: Day47 vLLM 902MiB why
