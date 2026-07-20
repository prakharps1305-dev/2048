# 2048 + Expectimax Bot

A terminal implementation of 2048 with an AI that plays it. Written in Python, no dependencies.

## Run it

```bash
python game.py    # play yourself (w/a/s/d)
python bot.py     # watch the bot play a game
python gui.py     # play in a window, or watch the bot (requires tkinter)
```

To reproduce the benchmark, call `benchmark(100)` instead of `run_bot()` at the bottom of
`bot.py` — it runs 100 silent games and prints stats (takes a few minutes).

## Result

Reaches the 2048 tile in **43% of games** (n=300, depth 4). Best tile seen: 4096.
Three independent 100-game runs: 39%, 47%, 43%.

Most losses stall at 1024, where large tiles fragment across the board and stop being mergeable.

## How it works

**Game engine.** The board is a 4×4 list of ints, with `0` for empty. Only one merge function
exists — `slide_left(row)` — which compresses out the zeros, merges adjacent equal pairs
(each tile merging at most once per move), then pads back to length 4. The other three
directions reuse it: right is left on a reversed row, and up/down transpose the board so
columns become rows.

**Search.** The bot uses expectimax over the game tree, alternating two node types:
- *Max nodes* — the bot's turn. It picks the move with the highest value.
- *Chance nodes* — the tile spawn. Nothing is chosen, so the value is the
  probability-weighted average over every possible spawn (each empty cell × 90% a 2,
  10% a 4).

At depth 0 it stops and evaluates the board with a heuristic.

**Heuristic.** A positional weight matrix that increases toward one corner, so the score is
the dot product of tiles and weights. This pushes large tiles into a corner and keeps values
sloping toward it, which is what makes cascade merges possible. Empty cells are added with a
separate weight to discourage crowding.

## Notes on AI assistance

## Notes on AI assistance

The game engine — board representation, merge logic, direction transforms, spawn, game-over
detection, and the game loop — was written by hand. The expectimax search function was
implemented with AI assistance. The heuristic design and the benchmarking were my own.

`gui.py` was written entirely by Claude Code from a spec I wrote. I did not write any of it.

## Possible improvements

- Memoize board evaluations so deeper search becomes practical (depth 5 is currently too slow
  — the branching factor is roughly 120× per full layer)
- Prune very low-probability spawn branches
- Add an explicit monotonicity term to reduce the 1024 fragmentation failure mode