import random
from typing import Dict


# ADK primitives

class Agent:
    def __init__(self, name: str, tools: list):
        self.name = name
        self.tools = {tool.__name__: tool for tool in tools}

    def call_tool(self, tool_name: str, *args, **kwargs):
        return self.tools[tool_name](*args, **kwargs)


def tool(func):
    """ADK-style tool decorator"""
    func.is_tool = True
    return func

# Game State 

state: Dict = {
    "round": 1,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False
}

VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

WIN_RULES = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}


# Tools 

@tool
def validate_move(move: str, is_user: bool) -> bool:
    move = move.lower().strip()

    if move not in VALID_MOVES:
        return False

    if move == "bomb":
        if is_user and state["user_bomb_used"]:
            return False
        if not is_user and state["bot_bomb_used"]:
            return False

    return True


@tool
def resolve_round(user_move: str, bot_move: str) -> str:
    # Bomb rules
    if user_move == "bomb" and bot_move == "bomb":
        state["user_bomb_used"] = True
        state["bot_bomb_used"] = True
        return "Both used bomb. Round is a draw."

    if user_move == "bomb":
        state["user_score"] += 1
        state["user_bomb_used"] = True
        return "User used bomb and wins the round."

    if bot_move == "bomb":
        state["bot_score"] += 1
        state["bot_bomb_used"] = True
        return "Bot used bomb and wins the round."

    if user_move == bot_move:
        return "Both chose the same move. Round is a draw."

    if WIN_RULES[user_move] == bot_move:
        state["user_score"] += 1
        return "User wins the round."

    state["bot_score"] += 1
    return "Bot wins the round."


@tool
def update_game_state():
    state["round"] += 1


# Referee Agent

referee_agent = Agent(
    name="RPS-Plus-Referee",
    tools=[validate_move, resolve_round, update_game_state]
)

# Game Loop 

def run_game():
    # RULES
    print("Rock–Paper–Scissors–Plus")
    print("Rules:")
    print("- Best of 3 rounds")
    print("- Moves: rock, paper, scissors, bomb")
    print("- Bomb can be used once per game.")
    print("- Invalid input wastes the round")
    print("-" * 40)
   

    while state["round"] <= 3:
        print(f"\nRound {state['round']}")

        user_move = input("Your move: ").lower().strip()

        is_valid = referee_agent.call_tool(
            "validate_move", user_move, is_user=True
        )

        if not is_valid:
            print("Invalid move. Round wasted.")
            referee_agent.call_tool("update_game_state")
            continue

        bot_move = random.choice(VALID_MOVES)
        if bot_move == "bomb" and state["bot_bomb_used"]:
            bot_move = random.choice(["rock", "paper", "scissors"])

        print(f"Bot played: {bot_move}")

        result = referee_agent.call_tool(
            "resolve_round", user_move, bot_move
        )
        print(result)

        print(
            f"Score -> User: {state['user_score']} | "
            f"Bot: {state['bot_score']}"
        )

        referee_agent.call_tool("update_game_state")

    # Final Result
 
    print("\nGame Over")
    print(
        f"Final Score -> User: {state['user_score']} | "
        f"Bot: {state['bot_score']}"
    )

    if state["user_score"] > state["bot_score"]:
        print("User wins the game.")
    elif state["bot_score"] > state["user_score"]:
        print("Bot wins the game.")
    else:
        print("The game is a draw.")



if __name__ == "__main__":
    run_game()
