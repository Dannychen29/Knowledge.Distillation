# RMA workbook build contract

## Approved writer

Use `openpyxl` for this RMA template. This contract is specific to
`rma-accuity-risk-rating`; do not apply it to unrelated spreadsheet work.

Before authoring, verify that `python -c "import openpyxl"` succeeds. If it
does not, stop and report that the approved writer is unavailable.

## Inputs

- A template workbook with a visible `風險表` sheet.
- A BIC-matched Bankers Almanac result.
- A per-bank output directory that does not contain another institution's
  completed package.

## Allowed workbook changes

Only write the following cells when their source status is `confirmed`:

| Field | Cell | Source |
|---|---|---|
| Bank name | `C3` | supplied roster |
| BIC | `C5` | supplied roster |
| Office type | `C6` | BIC-matched BA result |
| World rank | `D12` | BIC-matched BA result |
| Publicly traded | `D14` | BA stock symbol/exchange |
| S&P long-term | `D19` | BA credit ratings |
| Moody's long-term | `D20` | BA credit ratings |
| Fitch long-term | `D21` | BA credit ratings |

For `C6`, normalize the BIC-matched BA office classification as follows:

| BA visible classification | Workbook value |
|---|---|
| `Bank · Registered Office, Head Office` (or a result that states both Registered Office and Head Office) | `Headquarter` |
| `Bank Branch` | `Branch` |

Record the displayed BA classification in the mapping source field. Do not
leave `C6` blank merely because the portal labels it as a Bank classification
rather than an Office Type field.

Never edit `B3:B8` labels or `C4`, which must remain the template formula.
Leave a missing BA value blank in the workbook and record it as `unavailable`
in the mapping. Do not populate AML, PEP, adverse-news, CDD/EDD, parent, or
final-risk fields.

## Required package contents

Create exactly these artifacts inside the per-bank output directory:

- `filled-risk-rating.xlsx`
- `field-mapping.json`
- `field-mapping.xlsx`
- `workbook-schema.json`
- `build-record.json`

Do not create a flat duplicate outside that directory.

## Required checks

Before returning the package, verify all of the following:

1. The output ZIP passes an integrity check.
2. All original worksheet names remain present.
3. The formula count and data-validation count match the template.
4. `C4` still contains the template formula and `B3:B8` values are unchanged.
5. Each confirmed mapping round-trips to the intended target cell.
6. The mapping records BA ID, BIC, source field, target cell, status, and
   `manual review required`.
