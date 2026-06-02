# 2026 NBA Western Conference Finals — Analytical Breakdown

A long-form data analysis of the 2026 NBA Western Conference Finals between the Oklahoma City Thunder and San Antonio Spurs. San Antonio won the series 4–3 and advanced to the NBA Finals.

**Live version:** [yourusername.github.io/wcf-analysis](https://yourusername.github.io/wcf-analysis)

## What's in here

A 7-game statistical breakdown covering team-level efficiency, player impact rankings, shot-zone analysis, win-recipe comparisons, and a Game 7 deep dive. Built end-to-end:

- **Data pipeline** — Python + pandas, fetching and reconciling official box-score data
- **Analysis** — descriptive stats, correlation analysis, win-loss profile comparisons
- **Presentation** — hand-coded long-form HTML with custom editorial design, Chart.js visualizations

## Findings highlights

- Victor Wembanyama finished the series at +62 plus-minus on 27.3 PPG / 62.0% TS — the only star combining elite volume and efficiency
- Shai Gilgeous-Alexander finished -35 on 40.9% shooting and 28.6% from three (8-of-28)
- The two teams won in structurally different ways: OKC depended on offensive efficiency, SAS on defense and rebounding
- The team with the higher true-shooting percentage won 6 of 7 games
- Both teams shot exactly 34.1% from three for the series

## Data quality

Every player-game observation was logged individually from official box-score data and reconciled to official team totals. All 14 team-game point totals match official scores exactly. The analysis went through three rounds of error correction — a small SGA three-point line discrepancy was caught on review, fixed, and the corrected version is what's published.

## Structure

```
├── index.html              The published blog
├── data/
│   ├── player_games.csv    153 player-game rows
│   ├── player_totals.csv   Series totals per player
│   ├── team_games.csv      14 team-game rows
│   └── games.csv           7-game schedule and results
└── scripts/
    ├── build.py            Dataset construction with reconciliation checks
    └── analyze.py          Aggregations, correlations, win-recipe analysis
```

## Limitations (honest version)

This is box-score-level analysis. It does not use possession-level play-by-play data, player tracking, lineup splits, or opponent-adjusted impact metrics. Conclusions are descriptive across a 7-game sample, not predictive. For what real NBA analytics shops do, see RAPM, EPM, and Synergy data — none of which are reflected here.

## Stack

Python 3, pandas, Chart.js, hand-coded HTML/CSS. Fonts: Fraunces and JetBrains Mono via Google Fonts.

## License

MIT — feel free to adapt the structure for your own analyses.
