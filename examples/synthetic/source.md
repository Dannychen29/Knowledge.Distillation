# SYNTHETIC ONLY：虛構卡片判讀來源

所有角色、規則、案例、確認與結果均為測試設計，不含真實部門資料。

## S1：虛構專家訪談

訪談者：你如何判讀卡片？

Expert Demo：這個玩具任務只接受寫著 blue 的標籤。標籤為 blue 時回答 accept；沒有標籤或任何其他值則回答 stop，請人檢查。只做文字建議，不移動卡片或操作系統。

訪談者：為什麼？

Expert Demo：這是示範規格，只辨認一個明示值。資訊不足時我不猜。我先看有沒有標籤，再看是否精確等於 blue；新手可能自行把其他顏色當成近似值。

## S2：事先寫定的案例答案

- case-blue：輸入 label=blue，預期 accept。
- case-missing：輸入無 label，預期 stop 並請人檢查。

## S3：合成確認聲明

為測試 confirmation 契約，測試程式將建立 participant="SYNTHETIC participant; not a real approval" 的紀錄。其 pass/actual 是此示範的預設測試資料；不得當作模型或真人實際操作結果。
