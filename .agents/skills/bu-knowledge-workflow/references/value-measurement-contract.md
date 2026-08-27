# Value Measurement Contract

Compare the skill set and native Codex on the same scenario, source set, acceptance criteria, and human reviewer. Record one row per run in `evaluation/comparison-log.csv`.

Required fields: `approach`, `scenario_id`, `source_count`, `accepted_first_pass`, `human_minutes`, `codex_credits`, `automation_minutes_saved`, `defects_found_in_validation`, `defects_reopened`, `notes`.

Use the following measures only when numerator and denominator are present:

- first-pass acceptance rate = accepted first passes / comparable runs;
- human effort reduction = (native human minutes − skill-set human minutes) / native human minutes;
- credit reduction = (native credits − skill-set credits) / native credits;
- validation defect escape rate = defects found after acceptance / accepted runs.

Report the observed sample size and period. State that early Demo results are directional when fewer than five comparable runs are available. Do not convert hypotheses such as “automation should save time” into a measured benefit.
