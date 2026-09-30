# 完全虛構的流程示範

[source.md](source.md) 是虛構卡片判讀訪談：只有 blue 得到 accept，缺值/其他值 stop。它用來示範來源、知識 ID、確認版本、產品追溯的連結，不代表真實業務。

這個測試腳本同時產生知識版本與選用 Skill，以涵蓋兩種資料契約；真實蒸餾可在 Knowledge Release 完成後結案。先看 `draft/handbook.md`，再看 `knowledge/synthetic/toy/releases/toy-v1/` 的發布快照；`solution/` 是額外的產品契約示範。這些輸出留在指定的示範目錄，不會直接加入 repo 根目錄的正式 `knowledge/` 或 `solutions/`。

請 Codex 執行：

```powershell
.venv/Scripts/python.exe examples/synthetic/build_demo.py --out runs/synthetic-demo
```

輸出目錄必須尚不存在；重跑請換新目錄。打開輸出下的 draft/handbook.md、knowledge/synthetic/toy/releases/toy-v1/coverage.md，以及 solution/artifact/toy-advisor/SKILL.md。

build_demo.py 會產生標記 SYNTHETIC 的模型、假參與者確認、假案例紀錄、手冊、release 和範例 Skill。它的 purpose 是檢查契約接受合法 fixture；**沒有執行訪談、呼叫模型或測量 Skill 的實際決策品質**。不要把 sign_fixture 函式用於真實知識確認。

tests 另外會破壞這些資料，確認遺失證據、過期確認、衝突等情形被拒絕。真正實證要使用未見過的案例、真實參與者及實際產品行為，留待後續試點。
