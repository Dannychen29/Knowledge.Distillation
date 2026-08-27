# BU 知識萃取工作流技能集

這個專案提供一套以 Codex 為核心、可重複使用的商業單位（BU）知識萃取技能。其目標是把訪談、文件、畫面操作與影音證據，轉換為可追溯、可確認且可用來建置解決方案的規格與工作成果。

## 技能位置與結構

請從專案根目錄執行工作；唯一的技能目錄為 `.agents/skills/`。

```text
.agents/
  skills/
    bu-knowledge-workflow/           # 工作流入口與共用契約
    conduct-bu-interview/            # 第一階段：需求訪談與證據缺口辨識
    distill-bu-knowledge/            # 第二階段：知識萃取與確認
    build-bu-solution/               # 第三階段：選擇並建置適切解決方案
    validate-and-improve-solution/   # 第四階段：驗證、回饋與修正
    record-bu-walkthrough/           # 選用：授權的螢幕與麥克風操作錄製
    prepare-audio-evidence/          # 選用：音訊證據整理
    extract-video-evidence/          # 選用：長影片的重點證據萃取
    analyze-video-evidence/          # 選用：分析附時間碼的影片證據
```

## 主要工作流

新案件或續辦案件請由 `$bu-knowledge-workflow` 開始。它會依需求引導各階段，並在每個關卡保留狀態、輸出與後續行動。

```text
bu-knowledge-workflow
  -> conduct-bu-interview
  -> distill-bu-knowledge
  -> build-bu-solution
  -> validate-and-improve-solution
```

影音與畫面相關技能依證據類型按需使用，不會自行推進主要工作流。

## 使用原則

- 僅使用已授權的訪談、文件、影音與畫面證據。
- 保留來源、時間碼、確認狀態與尚待釐清事項；不以推測補足缺漏。
- 通用技能不保存個案事實；個案資料與產出應留在各自的 `runs/` 工作目錄。
- 建置解決方案前，先取得參與者對萃取知識的確認。
- 涉及螢幕錄製或麥克風時，必須先取得明確同意。

## 驗證技能結構

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .agents/skills/bu-knowledge-workflow/scripts/validate-agent-structure.ps1
```
