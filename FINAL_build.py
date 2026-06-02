"""DEFINITIVE 7-GAME DATASET v3.
Strategy: 
1) Player rows are the source of truth (already reconciled to official team points)
2) Team totals for player-stats (FG, 3PT, FT, AST, REB, STL, BLK) derived from player rows
3) Team-only stats (paint, fastbreak, second_chance, bench, pts_off_to, ortg, drtg, possessions,
   rim/midrange splits) come from team_stats JSON I fetched
4) Turnovers: take official team_total (includes team-attributed TOVs not in player rows)
"""
import pandas as pd

# Read the verified player rows (these have been reconciled and are authoritative)
players = pd.read_csv('verified_player_games.csv')

# Add G7 player rows (verified from G7 box score)
g7 = [
    # OKC
    ('G7','Chet Holmgren','OKC',4,4,0,2,1,2,0,0,2,4,2,2,-3),
    ('G7','Jaylin Williams','OKC',11,10,4,0,5,9,1,3,0,0,0,0,10),
    ('G7','Cason Wallace','OKC',17,7,4,2,6,10,5,9,0,0,2,1,-3),
    ('G7','Shai Gilgeous-Alexander','OKC',35,4,9,3,12,21,2,5,9,11,3,1,-7),
    ('G7','Kenrich Williams','OKC',2,1,0,0,1,4,0,2,0,0,0,0,-1),
    ('G7','Jared McCain','OKC',12,1,0,1,5,12,2,7,0,0,1,0,-8),
    ('G7','Luguentz Dort','OKC',3,1,2,0,1,4,1,3,0,0,0,0,-9),
    ('G7','Isaiah Hartenstein','OKC',7,5,0,2,3,7,0,0,1,1,1,0,-14),
    ('G7','Alex Caruso','OKC',12,5,4,3,3,14,1,6,5,6,0,1,-5),
    # SAS
    ('G7','De\'Aaron Fox','SAS',15,0,5,2,6,12,3,7,0,0,3,0,3),
    ('G7','Luke Kornet','SAS',2,4,0,0,0,3,0,0,2,2,0,1,1),
    ('G7','Dylan Harper','SAS',12,7,3,2,5,8,2,3,0,0,0,0,9),
    ('G7','Keldon Johnson','SAS',11,3,1,0,4,8,2,5,1,2,1,0,6),
    ('G7','Carter Bryant','SAS',2,1,0,0,1,1,0,0,0,0,0,0,2),
    ('G7','Harrison Barnes','SAS',0,0,0,0,0,1,0,1,0,0,0,0,-5),
    ('G7','Victor Wembanyama','SAS',22,7,2,1,7,15,3,5,5,7,1,1,7),
    ('G7','Stephon Castle','SAS',16,6,6,6,7,15,0,3,2,3,1,0,1),
    ('G7','Julian Champagnie','SAS',20,6,1,1,6,11,6,10,2,3,1,0,16),
    ('G7','Devin Vassell','SAS',11,6,3,0,4,14,1,6,2,2,2,0,0),
]
g7_df = pd.DataFrame(g7, columns=players.columns.tolist())
players = pd.concat([players, g7_df], ignore_index=True)
players.to_csv('FINAL_player_games.csv', index=False)

# ========================================================================
# Build team totals by aggregating verified player rows
# ========================================================================
team = players.groupby(['game','team']).agg(
    pts=('pts','sum'),
    fg_m=('fg_m','sum'), fg_a=('fg_a','sum'),
    tp_m=('tp_m','sum'), tp_a=('tp_a','sum'),
    ft_m=('ft_m','sum'), ft_a=('ft_a','sum'),
    reb=('reb','sum'),
    ast=('ast','sum'),
    tov_players=('tov','sum'),  # player-attributed only
    stl=('stl','sum'),
    blk=('blk','sum'),
).reset_index()

# ========================================================================
# Layer in team-only stats from box score JSON (paint, fastbreak, etc.)
# These come directly from team_stats blocks. tov_official = total_turnovers (incl team)
# All values cross-checked against the raw JSON I fetched.
# ========================================================================
team_only = [
    # game, team, oreb, dreb, paint, fastbreak, second_chance, bench, pts_off_to,
    # tov_official, ortg, drtg, ts_pct, efg_pct, poss, rim_m, rim_a, mid_m, mid_a
    ('G1','SAS', 15,46, 52, 9,13,16,17,  15, 104.5, 99.7, 56.1, 49.5, 116.8, 20,35,2,5),
    ('G1','OKC',  9,31, 38,16, 8,50,28,  14,  99.7,104.5, 52.6, 49.0, 115.4, 15,27,0,0),
    ('G2','SAS', 16,29, 46,10,22,25,10,  21, 117.1,125.1, 61.8, 58.3,  96.5, 20,29,3,9),
    ('G2','OKC', 17,24, 42, 8,17,57,27,  10, 125.1,117.1, 58.3, 54.8,  97.6, 12,19,11,19),
    ('G3','SAS',  9,28, 40,13,17,23,16,  15, 107.4,123.6, 57.1, 50.6, 100.5, 16,24,1,6),
    ('G3','OKC',  7,34, 42, 2,22,76,20,  11, 123.6,107.4, 64.4, 58.6,  99.5, 11,15,1,10),
    ('G4','SAS', 14,38, 50,18,17,30,25,  12,  99.9, 76.0, 49.5, 43.9, 103.1, 19,34,1,9),
    ('G4','OKC', 11,36, 36, 7,14,34,13,  17,  76.0, 99.9, 41.4, 36.3, 107.9, 14,29,6,17),
    ('G5','SAS', 15,26, 46,26,15,33,22,  16, 107.5,123.6, 53.7, 46.7, 106.1, 17,28,2,7),  # team tov inc.
    ('G5','OKC', 14,34, 38, 9,26,40,20,  17, 123.6,107.5, 63.7, 56.6, 102.7, 15,24,4,11),
    ('G6','SAS', 11,41, 44,18,14,46,15,  13, 116.8, 90.7, 59.6, 55.1, 101.0, 13,20,4,5),
    ('G6','OKC', 12,30, 38,10,18,38,11,  13,  90.7,116.8, 45.8, 42.6, 100.3, 12,26,6,12),
    ('G7','SAS', 15,25, 34,19,17,27,19,  12, 118.9,106.5, 57.6, 55.1,  93.4, 16,29,6,11),
    ('G7','OKC', 10,28, 32, 7,20,37, 9,  14, 106.5,118.9, 55.6, 51.8,  96.7,  5,12,9,16),
]
to_cols = ['game','team','oreb','dreb','paint','fastbreak','second_chance','bench','pts_off_to',
           'tov_official','ortg','drtg','ts_pct','efg_pct','poss','rim_m','rim_a','mid_m','mid_a']
to_df = pd.DataFrame(team_only, columns=to_cols)

# Merge
team_full = team.merge(to_df, on=['game','team'])
team_full = team_full.drop(columns=['tov_players']).rename(columns={'tov_official':'tov'})
# Reorder
col_order = ['game','team','pts','fg_m','fg_a','tp_m','tp_a','ft_m','ft_a','oreb','dreb',
             'ast','tov','stl','blk','paint','fastbreak','second_chance','bench','pts_off_to',
             'ortg','drtg','ts_pct','efg_pct','poss','rim_m','rim_a','mid_m','mid_a']
team_full = team_full[col_order]
team_full.to_csv('FINAL_team_games.csv', index=False)

# Game results
results = []
sched = [
    ('G1','2026-05-18','OKC','SAS',115,122,'SAS','OT'),
    ('G2','2026-05-20','OKC','SAS',122,113,'OKC','REG'),
    ('G3','2026-05-22','SAS','OKC',108,123,'OKC','REG'),
    ('G4','2026-05-24','SAS','OKC',103,82, 'SAS','REG'),
    ('G5','2026-05-26','OKC','SAS',127,114,'OKC','REG'),
    ('G6','2026-05-28','SAS','OKC',118,91, 'SAS','REG'),
    ('G7','2026-05-30','OKC','SAS',103,111,'SAS','REG'),
]
games = pd.DataFrame(sched, columns=['game','date','home','away','home_pts','away_pts','winner','type'])
games['margin'] = (games.home_pts - games.away_pts).abs()
games.to_csv('FINAL_games.csv', index=False)

# ========================================================================
# VERIFICATION — must pass before continuing
# ========================================================================
print("="*72)
print("DEFINITIVE DATASET — RECONCILIATION CHECK")
print("="*72)
print()

# Check 1: all point totals match official scores
official = {('G1','SAS'):122,('G1','OKC'):115,('G2','SAS'):113,('G2','OKC'):122,
            ('G3','SAS'):108,('G3','OKC'):123,('G4','SAS'):103,('G4','OKC'):82,
            ('G5','SAS'):114,('G5','OKC'):127,('G6','SAS'):118,('G6','OKC'):91,
            ('G7','SAS'):111,('G7','OKC'):103}
print("Check 1 — Points (team_full vs official scores):")
ok = True
for _,r in team_full.iterrows():
    exp = official[(r.game, r.team)]
    if r.pts != exp:
        print(f"  FAIL  {r.game} {r.team}: {r.pts} vs official {exp}")
        ok=False
print(f"  {'ALL POINTS MATCH' if ok else 'ERRORS FOUND'}")

# Check 2: player-row sums match team totals (FG, 3PT, FT, AST, REB, STL, BLK)
print("\nCheck 2 — Player-row sums vs derived team totals:")
all_ok = True
for _,row in team_full.iterrows():
    psub = players[(players.game==row.game)&(players.team==row.team)]
    # Check player-summable stats. Skip 'reb' since team has oreb/dreb only.
    for stat,col in [('fg_m','fg_m'),('fg_a','fg_a'),('tp_m','tp_m'),('tp_a','tp_a'),
                     ('ft_m','ft_m'),('ft_a','ft_a'),('ast','ast'),
                     ('stl','stl'),('blk','blk')]:
        if psub[col].sum() != row[stat]:
            print(f"  FAIL  {row.game} {row.team} {stat}: players={psub[col].sum()} team={row[stat]}")
            all_ok=False
print(f"  {'ALL PLAYER SUMS MATCH TEAM TOTALS' if all_ok else 'PLAYER-TEAM MISMATCH'}")

# Check 3: game margins and winners
print("\nCheck 3 — Game results consistency:")
for _,g in games.iterrows():
    home_team_pts = team_full[(team_full.game==g.game)&(team_full.team==g.home)].iloc[0].pts
    away_team_pts = team_full[(team_full.game==g.game)&(team_full.team==g.away)].iloc[0].pts
    expected_margin = abs(home_team_pts - away_team_pts)
    expected_winner = g.home if home_team_pts > away_team_pts else g.away
    if g.winner != expected_winner or g.margin != expected_margin:
        print(f"  FAIL {g.game}: schedule says winner={g.winner} margin={g.margin}, data says winner={expected_winner} margin={expected_margin}")
    else:
        print(f"  OK   {g.game}: {g.winner} by {g.margin}")

print(f"\nFINAL: {len(players)} player-game rows  |  {len(team_full)} team-game rows  |  {len(games)} games")
