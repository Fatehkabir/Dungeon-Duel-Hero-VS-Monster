import argparse
import sys
from dungeon_duel.core.models import Difficulty
from dungeon_duel.core.maps import get_preset_state
from dungeon_duel.core.rules import apply_action
from dungeon_duel.ai.controller import choose_action, with_retreat_memory


def run_headless_match(map_name="balanced_crypt", hero_diff="medium", monster_diff="medium", seed=42):
    print(f"=== DUNGEON DUEL: HEADLESS MATCH ===")
    print(f"Map: {map_name} | Hero AI: {hero_diff.upper()} | Monster AI: {monster_diff.upper()} | Seed: {seed}")
    
    state = get_preset_state(map_name)
    h_diff = Difficulty(hero_diff)
    m_diff = Difficulty(monster_diff)
    
    while state.outcome is None:
        action, telemetry = choose_action(
            state, hero_difficulty=h_diff, monster_difficulty=m_diff, thinking_deadline_ms=100, seed=seed
        )
        actor = state.active_actor
        state, desc = apply_action(state, action)
        with_retreat_memory(state, actor, telemetry)
        print(f"[{state.actions_taken:03d}] {desc} | {telemetry['explanation']}")
    
    print("\n=== MATCH COMPLETE ===")
    print(f"Outcome: {state.outcome.outcome.value}")
    print(f"Winner: {state.outcome.winner.value if state.outcome.winner else 'None (Draw)'}")
    print(f"Reason: {state.outcome.reason}")
    print(f"Total Turns: {state.actions_taken}")
    return state.outcome


def main():
    parser = argparse.ArgumentParser(description="Dungeon Duel: Hero AI vs Monster AI")
    parser.add_argument("--headless", action="store_true", help="Run in headless simulation mode")
    parser.add_argument("--map", default="balanced_crypt", choices=["balanced_crypt", "corridor_interception", "resource_rich"])
    parser.add_argument("--hero-ai", default="medium", choices=["easy", "medium", "hard"])
    parser.add_argument("--monster-ai", default="medium", choices=["easy", "medium", "hard"])
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.headless:
        run_headless_match(args.map, args.hero_ai, args.monster_ai, args.seed)
    else:
        # Check if pygame-ce is present for graphical window; if not or no display, run headless
        try:
            import pygame
            # Test video driver
            pygame.init()
            print("Pygame initialized. For full interactive visual dashboard, use the web interface on port 3000.")
            run_headless_match(args.map, args.hero_ai, args.monster_ai, args.seed)
        except Exception as e:
            print(f"Graphical display not available ({e}). Running in headless mode:")
            run_headless_match(args.map, args.hero_ai, args.monster_ai, args.seed)


if __name__ == "__main__":
    main()
