Rock–Paper–Scissors–Plus (AI Referee)

>>Overview

This project is a minimal AI referee for a short game of Rock–Paper–Scissors–Plus.
The referee enforces the rules, tracks game state across rounds, and clearly reports outcomes. The focus is on correctness and clean agent design rather than UI or polish.

>>State & Game Logic

Game state is stored in a persistent in-memory dictionary that tracks rounds, scores, and bomb usage for both players.
State is kept outside the prompt so the game behaves consistently across turns.
All rule enforcement and state updates happen inside tool functions, not in the agent or main loop.

>>Agent & ADK Usage

The game follows a Google ADK-style agent architecture.
A single referee agent orchestrates the game
Explicit tools handle move validation, round resolution, and state updates
The agent itself contains no game logic
Since Google ADK is not publicly runnable in lightweight environments, I implemented a minimal ADK-style abstraction to demonstrate correct agent and tool usage in a runnable setup.

>>Tradeoffs

The game runs in a simple CLI loop for clarity
ADK primitives are simulated due to runtime availability
Outputs are kept simple and human-readable

>>Future Improvements

With more time, this could be migrated to native ADK primitives, use structured outputs, and include a smarter bot strategy.