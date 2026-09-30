# 本次實作驗證紀錄

日期：2026-09-30。環境：Windows、Python 3.13.15；核心依賴 PyYAML 6.0.3、jsonschema 4.26.0。範圍：重建的知識工作流程、資料契約與本機工具。沒有導入真實部門或 RMA 內容。

## 已執行

| 檢查 | 結果 | 能證明什麼 |
| --- | --- | --- |
| unittest discover，17 tests | 全部通過 | 來源/依賴/確認/快照/追溯契約的正反例 |
| skill-creator quick_validate，10 Skills | 全部通過 | frontmatter、命名及 Skill 基本格式 |
| check-repo | 通過 | 六核心＋四媒體 Skill、schema 格式、指令及 docs 的相對 reference |
| Python compileall | 通過 | 新程式及保留的 Python 檔可解析 |
| recording_control.ps1 parser | 通過 | 修改後 PowerShell 語法可解析 |
| synthetic build_demo | 成功產生 release、手冊與 Skill | source/model/release/solution 格式能銜接 |
| 手冊及 Skill 原始文字檢視 | 已檢視 | 中文內容、details、來源及 SYNTHETIC 標記被保存 |
| git diff --check | 通過 | 受追蹤變更無空白錯誤 |

Windows 的 skill-creator 檢查器預設使用系統編碼，第一次檢查遇到 cp950 解碼失敗；使用 Python `-X utf8` 後十個 Skill 全數通過。reference link 檢查也發現並修正了三個新 Skill 的相對路徑。

## 自動測試涵蓋

1. 合法 release 與多層依賴 closure。
2. 遺失 evidence 及重複 ID。
3. unknown detail 必須有 open gap。
4. 知識改變使 participant confirmation 過期。
5. 核心知識缺少案例。
6. 非核心未知知識仍阻止依賴它的產品。
7. 專家歸屬未納入 target。
8. 複製來源不能當兩個獨立來源。
9. optional 缺口產生 limited-scope。
10. 遺失依賴與案例範圍不符。
11. 發布、手冊及拒絕覆蓋／變更偵測。
12. solution 映射及缺少 artifact。
13. execution 產品不能以合成紀錄通過。
14. init 建立未確認草稿，拒絕不安全 slug。
15. 重複 YAML key 不會靜默覆蓋。
16. schema 與 Skill references。
17. 另一個案例 pass 不能掩蓋目前版本的 fail。

## 尚未驗證及限制

- 合成示範的 participant/scenario/test records 是明示的假資料；未執行另一個 Agent 的行為評估，不能當成 Skill 答案品質的證明。
- 尚未進行真實專家訪談、真實部門知識驗證或未見案例泛化測試。
- 沒有實際啟動畫面/麥克風錄製、下載語音模型、轉錄或分析影片。媒體工具這次只改呼叫關係與路徑，做語法檢查；其平台相容性留待需要時測試。
- schema/引用檢查不會判定來源語意是否正確，也不會證明 review 紀錄真實。Codex 和參與者仍需核對原始來源。
- hash snapshot 可偵測意外修改，但沒有簽章、存取控制或併發寫入保護；MVP 預期單一 Codex 工作流程寫入同一 library。
- Skill 的生成是 Codex 依契約進行的產品化工作；沒有一個全自動語意 compiler。

重現命令與合成來源見 [README](../README.md) 和 [合成示範](../examples/synthetic/README.md)。
