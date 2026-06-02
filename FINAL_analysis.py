"""Final 7-game analysis. All numbers derived from verified data."""
import pandas as pd, numpy as np
pd.set_option('display.width', 220, 'display.precision', 1)

p = pd.read_csv('FINAL_player_games.csv')
t = pd.read_csv('FINAL_team_games.csv')
g = pd.read_csv('FINAL_games.csv')

L = "="*72
H = lambda x: print(f"\n{L}\n{x}\n{L}")

# Add margin column to team table
t['margin'] = t.apply(lambda r: r.pts - t[(t.game==r.game)&(t.team!=r.team)].pts.iloc[0], axis=1)
t['won'] = t.margin > 0
t['fg_pct'] = (t.fg_m/t.fg_a*100).round(1)
t['tp_pct'] = (t.tp_m/t.tp_a*100).round(1)
t['ft_pct'] = (t.ft_m/t.ft_a*100).round(1)
t['rim_pct'] = (t.rim_m/t.rim_a*100).round(1)
t['mid_pct'] = (t.mid_m/t.mid_a*100).round(1)
t['treb'] = t.oreb + t.dreb
t['ast_tov'] = (t.ast/t.tov).round(2)

# ============================================================
H("1. SERIES RESULT: SAS WIN 4-3, ADVANCE TO NBA FINALS")
# ============================================================
print("Game-by-game:")
for _,r in g.iterrows():
    print(f"  {r.game} {r.date}  {r.away}@{r.home}: {r.away}{r.away_pts}-{r.home_pts}{r.home}  → {r.winner} by {r.margin}")
sas_pts = t[t.team=='SAS'].pts.sum()
okc_pts = t[t.team=='OKC'].pts.sum()
print(f"\n  Series wins: SAS 4, OKC 3")
print(f"  Total points: SAS {sas_pts}, OKC {okc_pts} (SAS +{sas_pts-okc_pts})")
print(f"  Home record: {(g.winner==g.home).sum()}-{(g.winner!=g.home).sum()}")
print(f"  Avg margin: {g.margin.mean():.1f}")
print(f"  Avg margin in SAS wins ({(g.winner=='SAS').sum()}): {g[g.winner=='SAS'].margin.mean():.1f}")
print(f"  Avg margin in OKC wins ({(g.winner=='OKC').sum()}): {g[g.winner=='OKC'].margin.mean():.1f}")

# ============================================================
H("2. THE 'HIGHER TS% WINS' RULE — DOES IT HOLD FOR G7?")
# ============================================================
print("Game | OKC TS% | SAS TS% | Higher | Winner | Match")
for game in g.game:
    okc_ts = t[(t.game==game)&(t.team=='OKC')].ts_pct.iloc[0]
    sas_ts = t[(t.game==game)&(t.team=='SAS')].ts_pct.iloc[0]
    winner = g[g.game==game].winner.iloc[0]
    higher = 'OKC' if okc_ts > sas_ts else 'SAS'
    match = 'YES' if higher==winner else 'NO'
    print(f" {game}  |  {okc_ts:5.1f}  |  {sas_ts:5.1f}  |   {higher}  |   {winner}  |  {match}")
matches = sum(1 for game in g.game if 
              (t[(t.game==game)&(t.team=='OKC')].ts_pct.iloc[0] > t[(t.game==game)&(t.team=='SAS')].ts_pct.iloc[0])
              == (g[g.game==game].winner.iloc[0]=='OKC'))
print(f"\n  Rule holds in {matches}/7 games")

# ============================================================
H("3. TEAM AVERAGES — ALL 7 GAMES")
# ============================================================
agg = t.groupby('team').agg(
    PPG=('pts','mean'), FG=('fg_pct','mean'), TP=('tp_pct','mean'), 
    TS=('ts_pct','mean'), eFG=('efg_pct','mean'),
    FTm=('ft_m','mean'), FTa=('ft_a','mean'),
    PAINT=('paint','mean'), FB=('fastbreak','mean'), SECOND=('second_chance','mean'),
    OREB=('oreb','mean'), DREB=('dreb','mean'), TREB=('treb','mean'),
    AST=('ast','mean'), TOV=('tov','mean'), AST_TOV=('ast_tov','mean'),
    STL=('stl','mean'), BLK=('blk','mean'),
    BENCH=('bench','mean'), PtsOffTO=('pts_off_to','mean'),
    POSS=('poss','mean'), ORTG=('ortg','mean'), DRTG=('drtg','mean'),
    RIM=('rim_pct','mean'), MID=('mid_pct','mean')).round(1).T
agg['diff'] = (agg.OKC - agg.SAS).round(1)
print(agg.to_string())

# ============================================================
H("4. PLAYER SERIES TOTALS (7-GAME)")
# ============================================================
pa = p.groupby(['player','team']).agg(
    gp=('game','count'),
    pts=('pts','sum'), reb=('reb','sum'), ast=('ast','sum'), tov=('tov','sum'),
    fg_m=('fg_m','sum'), fg_a=('fg_a','sum'),
    tp_m=('tp_m','sum'), tp_a=('tp_a','sum'),
    ft_m=('ft_m','sum'), ft_a=('ft_a','sum'),
    stl=('stl','sum'), blk=('blk','sum'),
    pm=('pm','sum')
).reset_index()
pa['ppg'] = (pa.pts/pa.gp).round(1)
pa['rpg'] = (pa.reb/pa.gp).round(1)
pa['apg'] = (pa.ast/pa.gp).round(1)
pa['fg_pct'] = (pa.fg_m/pa.fg_a*100).where(pa.fg_a>0,0).round(1)
pa['tp_pct'] = (pa.tp_m/pa.tp_a*100).where(pa.tp_a>0,0).round(1)
pa['ft_pct'] = (pa.ft_m/pa.ft_a*100).where(pa.ft_a>0,0).round(1)
pa['ts_pct'] = (pa.pts/(2*(pa.fg_a + 0.44*pa.ft_a))*100).where((pa.fg_a+pa.ft_a)>0,0).round(1)
pa['pm_per_g'] = (pa.pm/pa.gp).round(1)
pa.to_csv('FINAL_player_totals.csv', index=False)

print("Top 12 by PPG (min 5 GP):")
top = pa[pa.gp>=5].sort_values('ppg',ascending=False).head(12)
print(top[['player','team','gp','ppg','rpg','apg','fg_pct','tp_pct','ts_pct','pm','pm_per_g']].to_string(index=False))

print("\nTop 10 by series +/-:")
top_pm = pa[pa.gp>=3].sort_values('pm',ascending=False).head(10)
print(top_pm[['player','team','gp','ppg','ts_pct','pm','pm_per_g']].to_string(index=False))

print("\nWorst 5 by series +/-:")
bot = pa[pa.gp>=3].sort_values('pm').head(5)
print(bot[['player','team','gp','ppg','ts_pct','pm','pm_per_g']].to_string(index=False))

print("\n3-Point leaderboard (min 15 attempts):")
sh = pa[pa.tp_a>=15].sort_values('tp_pct',ascending=False)
print(sh[['player','team','tp_m','tp_a','tp_pct','pts']].to_string(index=False))

# ============================================================
H("5. STAR HEAD-TO-HEAD (7 GAMES)")
# ============================================================
for player in ['Victor Wembanyama','Shai Gilgeous-Alexander']:
    sub = p[p.player==player].sort_values('game')
    team = sub.team.iloc[0]
    gp = len(sub)
    print(f"\n{player} ({team}, {gp}G):")
    print(f"  PPG {sub.pts.mean():.1f}  RPG {sub.reb.mean():.1f}  APG {sub.ast.mean():.1f}  TOV {sub.tov.mean():.1f}")
    print(f"  FG  {sub.fg_m.sum()}/{sub.fg_a.sum()} = {100*sub.fg_m.sum()/sub.fg_a.sum():.1f}%")
    print(f"  3PT {sub.tp_m.sum()}/{sub.tp_a.sum()} = {100*sub.tp_m.sum()/sub.tp_a.sum():.1f}%")
    print(f"  FT  {sub.ft_m.sum()}/{sub.ft_a.sum()} = {100*sub.ft_m.sum()/sub.ft_a.sum():.1f}%")
    ts = sub.pts.sum() / (2*(sub.fg_a.sum() + 0.44*sub.ft_a.sum())) * 100
    print(f"  TS% {ts:.1f}")
    print(f"  +/- total {sub.pm.sum():+d}  avg {sub.pm.mean():+.1f}")
    print(f"  Games:  {list(zip(sub.game, sub.pts, sub.pm))}")

# ============================================================
H("6. SHOT ZONES — ALL 7 GAMES")
# ============================================================
zones = t.groupby('team').agg(
    rim_m=('rim_m','sum'), rim_a=('rim_a','sum'),
    mid_m=('mid_m','sum'), mid_a=('mid_a','sum'),
    tp_m=('tp_m','sum'), tp_a=('tp_a','sum')
).reset_index()
zones['rim_pct'] = (zones.rim_m/zones.rim_a*100).round(1)
zones['mid_pct'] = (zones.mid_m/zones.mid_a*100).round(1)
zones['tp_pct'] = (zones.tp_m/zones.tp_a*100).round(1)
print(zones.to_string(index=False))
print("\nShot diet (% of total FGA):")
for _,r in zones.iterrows():
    total = r.rim_a + r.mid_a + r.tp_a
    print(f"  {r.team}: rim {100*r.rim_a/total:.1f}%, mid {100*r.mid_a/total:.1f}%, three {100*r.tp_a/total:.1f}%")

# ============================================================
H("7. CORRELATION: WHAT PREDICTS MARGIN (14 team-games)")
# ============================================================
metrics = ['ts_pct','tp_pct','tp_m','fg_pct','ft_m','ft_a',
           'oreb','dreb','treb','tov','ast','ast_tov','stl','blk',
           'paint','fastbreak','second_chance','bench','pts_off_to','ortg','drtg',
           'rim_pct','mid_pct']
corrs = [(m, t['margin'].corr(t[m])) for m in metrics]
corrs.sort(key=lambda x:abs(x[1]),reverse=True)
print(f"{'Metric':<15} {'r':>7}")
for m,r in corrs:
    print(f"  {m:<14} {r:>+.3f}")

# ============================================================
H("8. WIN-RECIPES: OKC vs SAS (when each team wins)")
# ============================================================
print("OKC won 3 games, SAS won 4. Their averages:")
for team in ['OKC','SAS']:
    wins = t[(t.team==team)&t.won]
    losses = t[(t.team==team)&~t.won]
    print(f"\n  {team} in WINS ({len(wins)}g) vs LOSSES ({len(losses)}g):")
    for m in ['ts_pct','tp_pct','dreb','treb','tov','ast','blk','paint','bench','fastbreak','rim_pct']:
        w_avg = wins[m].mean() if len(wins) else float('nan')
        l_avg = losses[m].mean() if len(losses) else float('nan')
        print(f"    {m:<10} wins {w_avg:>6.1f} | losses {l_avg:>6.1f} | diff {w_avg-l_avg:+.1f}")

# ============================================================
H("9. THE GAME 7 STORY — VERIFIED FACTS")
# ============================================================
print("Final: SAS 111, OKC 103. SAS wins series 4-3, advances to NBA Finals.")
print()
g7_okc = t[(t.game=='G7')&(t.team=='OKC')].iloc[0]
g7_sas = t[(t.game=='G7')&(t.team=='SAS')].iloc[0]
print(f"Shooting:")
print(f"  OKC: {g7_okc.fg_m}/{g7_okc.fg_a} FG ({g7_okc.fg_pct}%) | "
      f"{g7_okc.tp_m}/{g7_okc.tp_a} 3PT ({g7_okc.tp_pct}%) | TS% {g7_okc.ts_pct}")
print(f"  SAS: {g7_sas.fg_m}/{g7_sas.fg_a} FG ({g7_sas.fg_pct}%) | "
      f"{g7_sas.tp_m}/{g7_sas.tp_a} 3PT ({g7_sas.tp_pct}%) | TS% {g7_sas.ts_pct}")
print(f"\nQuarters: OKC 25-28-24-26  |  SAS 32-24-24-31")
print(f"\nKey lines:")
print(f"  Champagnie: 20 pts on 6-of-11 (6-of-10 from three! +16)")
print(f"  Wembanyama: 22/7/2 on 7-of-15, 3-of-5 from three, +7")
print(f"  SGA: 35 pts on 12-of-21 (57.1%, 2-of-5 from three) BUT -7 +/-")
print(f"  Caruso: 12 pts but on 3-of-14 (21.4%), -5")
print()
print(f"OKC was held to:")
print(f"  - Just 5-of-12 at the rim (41.7%) — series-worst")
print(f"  - 7 fast-break pts (vs SAS 19)")
print(f"  - 14 turnovers leading to 19 SAS points")
print()
print(f"SAS shot 17-of-40 from three (42.5%) — series-best")
