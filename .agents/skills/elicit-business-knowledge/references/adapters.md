# 來源 adapters 與可選 workers

## 文件及流程圖

保留頁碼、段落、表格/儲存格、版本、來源。使用可用的文件/PDF/試算表工具，不要求 PRD。drawio 使用 [extract-drawio-evidence.py](../../bu-knowledge-workflow/scripts/extract-drawio-evidence.py)，先看 --help。XML 以 UTF-8 解析；必要時看圖確認 edge，不把終端亂碼當來源損壞。

## 瀏覽器／觀察

用目前可用且已授權的能力，不綁特定 CLI。記前置狀態、輸入、操作、結果及時間；靜態截圖只能支持狀態。無法存取時保留 stated 口述，另列 observation gap。

## 媒體

- `$prepare-audio-evidence`：轉錄/正規化音訊，保留時間碼及 speaker uncertainty。
- `$extract-video-evidence`：挑高價值片段與畫格。
- `$analyze-video-evidence`：分析選取片段，產生候選主張。
- `$record-bu-walkthrough`：具名缺口及 screen/microphone consent 下錄製。

workers 保持 `.agents/skills/<worker>/` 以利發現。adapter 是本文件路由，不是頂層業務階段。路徑統一 `runs/<id>/evidence/audio/<evidence-id>/`、`video/<evidence-id>/`、`recordings/`。

worker 的 corroborated 不直接映射成 shared 或 scenario-tested。檢查來源獨立性，多份複製文件不算獨立支持。缺工具時記限制，使用既有逐字稿、文件或截圖。
