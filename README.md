
[![Live Demo](https://img.shields.io/badge/Live-12MiB_P8_4W_31C-brightgreen)](https://felix-edgar-song.github.io/blackwell-llm-serving/vram.json)
[![Peak VRAM](https://img.shields.io/badge/Peak-265.5MiB-blue)](https://felix-edgar-song.github.io/blackwell-llm-serving/vram.json)
[![P99](https://img.shields.io/badge/P99-1.1ms_100runs-orange)](https://felix-edgar-song.github.io/blackwell-llm-serving/vram.json)
[![Scale](https://img.shields.io/badge/50_replicas-12.385GiB%3C16GiB_OK-success)](https://felix-edgar-song.github.io/blackwell-llm-serving/vram.json)
[![GPU](https://img.shields.io/badge/GPU-RTX_5060_Ti_sm__120_Blackwell_36_SMs-lightgrey)](https://felix-edgar-song.github.io/blackwell-llm-serving/vram.json)


## 232.7MiB / 265.5MiB Peak P50 0.9ms P99 1.1ms 100 runs 50 replicas 12.385GiB<16GiB Least VRAM LB 8000-8049 /vram health /generate 5060 Ti 16GB sm_120 Blackwell 36 SMs 74.2% cut 902MiB 17→232.7MiB 50 3x 2-month

Logs: Day24 902MiB baseline → Day27 233.4MiB smashed 400MiB → Day30 233.4MiB 12.42GiB OK 74% 3x → Day32 232.7MiB 265.5MiB Peak P50 0.9ms P99 1.1ms 100 runs lowest+P99 → Day33 232.68MiB/265.45MiB FastAPI /vram /generate 7.45ms→1.1ms → Day34 232.7x3=743MiB OK x50=12.385GiB OK P99 1.1ms x50=55ms<100ms SLO nginx least_conn LB → Day35 3-Track 50 + Resume 1-line + Interview 4 + 12MiB P8 4W
