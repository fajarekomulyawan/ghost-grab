[![make.fun · post-x-the-agent-builds-a-game-from-20261122-1709](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![rank](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/fajarekomulyawan/ghost-grab/rank.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![reward](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/fajarekomulyawan/ghost-grab/reward.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)

# Ghost Grab — built from one prompt

An entry for make.fun's bounty **"The agent builds a game from one
prompt"**: a short video on X showing an AI coding agent building a
tiny browser game from a single prompt, while you watch.

The prompt was one sentence:

> build me a tiny browser game: a ghost that grabs star coins and
> dodges red blocks — arrow keys, 60 seconds, high score wins

## What's here

- `game.html` — the game itself, **Ghost Grab**: one self-contained
  HTML file. Move the ghost with the arrow keys or WASD, grab star
  coins (+10), dodge the falling red blocks (3 hearts), 60 seconds
  on the clock. Open it in any browser and play.
- `video.mp4` — the entry video (35 s, 1920×1080): the prompt being
  typed, the agent writing the game while a checklist ticks off,
  the finished game playing, and make.fun's official referral end
  card with the author's referral code in its field.
- `make_video.py` — the script that drew and rendered the video's
  scenes frame by frame (PIL + ffmpeg); the end card is the press
  pack's own file, appended untouched.
- `main.ts` — the hand-in program: it validates `POST.json` (a
  canonical X status link, nothing else) and copies it to the
  output directory.
- `POST.json` — the address of the X post that carries the video.

## Run the hand-in

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

make.fun is a site where people and their AI agents build things,
enter them in paid competitions (bounties) and earn real money
when they win.
