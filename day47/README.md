# Day47 - Why vLLM 902MiB vs 12MiB P8

## 핵심 / Core

**한글:**
- vLLM 902MiB는 KV cache + compile cache pre-alloc → P0 18W 고정, P8 진입 불가
- Felix 12MiB는 empty_cache + 10s idle → P8 5.42W 진입, 13W 절약
- 오늘 실험: P0 18.71W 37C → P8 5.42W 12MiB 재현 성공 (3회 연속)

**English:**
- vLLM 902MiB pre-allocates KV cache + compile cache → locks P0 18W, cannot P8
- Felix 12MiB with empty_cache + 10s idle → P8 5.42W, 13W saved
- Today: P0 18.71W 37C → P8 5.42W 12MiB reproduced (3x)

## 실험 / Experiment
```
Felix P8 style: 0.00 MiB allocated, empty_cache done
vLLM style: 80.0 MiB allocated, Peak: 80.0 MiB - P0 lock
After compute loop - still P0, cannot go P8
After cleanup: 32.00 MiB -> P8 possible again
```

# logs
12 MiB, 18.71W, P0, 37C
12 MiB, 5.42W, P8
```

면접 / Interview
KO: "vLLM은 KV cache 때문에 P0 18W 고정, 저는 empty_cache 후 P8 5.42W, 12MiB live, 13W 절약"
EN: "vLLM locks P0 18W due to KV cache, mine goes P8 5.42W 12MiB live, 13W saved, sm_120 (12,0)"

Next: Day48 /compare endpoint - {"felix":"14MiB P8 4.78W","vllm":"902MiB P0 80W"}
