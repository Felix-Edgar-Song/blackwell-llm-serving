# Day48 - /compare endpoint (felix vs vLLM)

## 핵심 / Core

**한글:**
- `felix: 0.0 MiB P8 5.21W` vs `vLLM sim: 76MiB P1 18.94W` 한 번에 비교
- `empty_cache+idle -> P8 5W` vs `KV cache polling -> P0 lock 18W`
- 4일 연속 P8 재현: Day46 4.78W, Day47 5.42W, Day48 5.21W
- Blackwell (12,0) sm_120 RTX 5060 Ti

**English:**
- `felix: 0.0 MiB P8 5.21W` vs `vLLM sim: 76MiB P1 18.94W` in one /compare call
- empty_cache+idle -> P8 5W vs KV cache polling -> P0 lock 18W
- 4 days P8 reproduced: Day46 4.78W, Day47 5.42W, Day48 5.21W
- Blackwell (12,0) sm_120 RTX 5060 Ti

## 실행 / Run
```bash
uvicorn app:app --port 8000
curl http://localhost:8000/vram        # P8 5.21W
curl http://localhost:8000/compare    # felix 0MiB P8 vs vLLM 76MiB P1
```

## 로그 / Logs
- vram_p0.json: 0.0 MiB P8 5.21W live:true cap(12,0)
- compare_p0.json: felix P8 5.21W vs vLLM 76MiB P1 8.13W
- smi_final.txt: 12 MiB, 5.21W, P8, 33C

## 면접 / Interview
- KO: "/compare로 0MiB P8 5.21W vs 76MiB P1 18W, empty_cache로 13W 절약, 12MiB live"
- EN: "/compare shows 0MiB P8 5.21W vs 76MiB P1 18W, 13W saved with empty_cache, 12MiB live"


