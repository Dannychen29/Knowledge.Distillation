---
name: rma-accuity-risk-rating
description: 在 RMA risk-rating template 中安全填寫經 Bankers Almanac (Accuity) 確認的身分、排名、上市與長期信用評等欄位。適用於名冊提供銀行名稱與 BIC 時；不得執行 CDD、EDD、PEP 或 AML 提交作業。
---

# RMA Accuity Risk Rating

僅使用 BIC 相符實體頁面上可見的 Bankers Almanac 欄位。BIC 為主要識別鍵；僅在 BIC 無結果時使用 Bank Name，且只能採用唯一且無衝突的匹配結果。保留主管審核與來源可追溯性。

## Template 安全映射

映射前先檢查提供的 template 之標籤、合併範圍、公式與驗證規則。不得僅因儲存格與所需值相鄰，便將標籤當作目標儲存格。

- 就目前的 RMA template 而言，`風險表!B3:B8` 為標籤，絕不可編輯。將 Bank Name 寫入 `C3`、BIC 寫入 `C5`，並將 office type 寫入 `C6`。
- `C4` 是 template 的 Country 公式，必須保持原樣。驗證其由 BIC 推得的國家是否與 Bankers Almanac 的 Country/Region 結果一致；不得以靜態資料覆寫。
- 依 BIC 搜尋結果的 office classification 決定 `C6`：`Bank · Registered Office, Head Office`（或任何同時表明 Registered Office 與 Head Office 的 BA 顯示）一律映射為 `Headquarter`；`Bank Branch` 映射為 `Branch`。不可因頁面未使用單獨的 "Office Type" 欄名而略過此值。於 mapping 保留 BA 顯示的原始 office classification；只有 BA 頁面沒有 office classification 時，才將 `C6` 留白。
- 可用的 BA rating 欄位為 `D12` Accuity World Rank、`D14` publicly traded，以及 `D19:D21` 的 S&P、Moody's 與 Fitch long-term ratings。不得推論數值：每個缺失欄位均映射為 `unavailable`，並保留其目標儲存格空白。

## 建置與驗證

此 Skill 的唯一核准 workbook writer 為 `openpyxl`；這是 RMA template workflow 對通用 spreadsheet authoring 預設的明確覆寫。**不得**因 `@oai/artifact-tool` 或 `load_workspace_dependencies` 未提供而將本 Skill 的 `.xlsx` 建置判定為 blocker。

寫入前閱讀 [references/workbook-build-contract.md](references/workbook-build-contract.md)，並執行：

```powershell
python -c "import openpyxl; print(openpyxl.__version__)"
```

若 import 失敗，才回報 workbook writer blocker；不要改用未驗證的 writer。使用 [scripts/build_rma_risk_rating.py](scripts/build_rma_risk_rating.py) 建置，或只在該 script 無法覆蓋的 template 差異下對其做最小修改。

為每家機構建立一個 package directory，其中包含所有 artifact：

- `filled-risk-rating.xlsx`
- `field-mapping.json`
- `field-mapping.xlsx`
- `workbook-schema.json`
- `build-record.json`

不得在該機構 directory 外建立額外的平面副本。映射必須包含 BIC 結果證據、來源欄位、目標儲存格、狀態與人工審核控制。只有 `confirmed` 映射可以變更 workbook。

交付前確認：已確認的目標均為允許寫入的右側輸入儲存格；左側標籤與 `C4` 公式未變更；BA 的 country 與 office type 和 BIC 結果一致；且 ZIP 完整性、worksheets、公式與 data validations 均已保留。

## 範圍限制

不得填寫 AML questionnaires、PEP/adverse-news、CDD/EDD 或 parent details，亦不得提交至 AML department。unit supervisor 仍為審核者。
