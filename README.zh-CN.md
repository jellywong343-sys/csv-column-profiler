# CSV 瀛楁鍒嗘瀽宸ュ叿

[English](README.md)

鍒嗘瀽 CSV 鍚勫瓧娈电殑鏁版嵁绫诲瀷銆佺┖鍊笺€佸敮涓€鍊笺€佹暟鍊艰寖鍥村拰楂橀鍊笺€?
## 涓昏鍔熻兘

- 鎺ㄦ柇鏁存暟銆佹暟鍊笺€佸竷灏斻€佹棩鏈熴€佹枃鏈€佹贩鍚堟垨绌哄瓧娈点€?- 缁熻绌哄€肩巼鍜屽敮涓€鍊兼瘮渚嬨€?- 璁＄畻鏁板€煎瓧娈电殑鏈€灏忓€笺€佹渶澶у€煎拰骞冲潎鍊笺€?- 鏄剧ず楂橀鍊煎拰鏂囨湰闀垮害鑼冨洿銆?- 鏀寔瀵煎嚭 JSON 鎶ュ憡銆?- 鍙鍙栨暟鎹紝涓嶄慨鏀规簮鏂囦欢銆?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/csv-column-profiler.git
cd csv-column-profiler
python -m pip install -e .
```

## 浣跨敤

```bash
csv-profile examples/people.csv
csv-profile data.csv --top 10 --json profile.json
csv-profile legacy.csv --encoding gb18030
```

绫诲瀷鎺ㄦ柇鍙槸瀹炵敤鎽樿锛屼笉绛夊悓浜庢寮忕殑鏁版嵁绾︽潫銆備慨鏀圭敓浜ф暟鎹墠璇蜂汉宸ユ鏌ョ粨鏋溿€?
## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT


