## 2026-10-02 — Home page hero figure: agents row and claim band

- Done: in the hero architecture figure (`html/index.html`, `html/styles/styles.css`), the "Agents" label, the three agent-name chips and "+ hundreds more" now sit on one row. The chips shrink with the figure width (container-query units on `.cc-agents`, 11.5px down to 10px). The "Validated / Bounded / Observable / Model-neutral" list moved out of `.cc-agents` to be a direct child of the server node, under its own divider, so that the claim is visually separate from the facts.
- Phones (viewport under 500px): the row cannot fit, so the label and chips flow as two rows: "Agents leave_balance fx_rates" then "product_recalls + hundreds more". A `padding-right: max(0px, 100% - 330px)` on `.cc-agents` keeps "+ hundreds more" from being left alone on a row at 452–499px.
- Checked with headless Chrome screenshots at 1440, 1001, 500, 460, 390 and 360px. Headless Chrome does not exit after `--screenshot` on this page and cannot go below a 500px window; run it in the background, stop it once the image exists, and use an iframe page for phone widths.
- State: not committed, not uploaded.
- Open: between 1001px and about 1150px the "Validated…" list wraps "Model-neutral" to a second row (it did before this change).
