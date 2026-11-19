from dungeon_duel.core.models import Actor, GameState, OutcomeType, Position, TileType
from dungeon_duel.core.rules import calculate_damage, get_hero_current_attack
from dungeon_duel.ai.bfs import get_tactical_distance, bfs_path, hero_objective_path

TERMINAL_HERO_WIN = 100000.0
TERMINAL_MONSTER_WIN = -100000.0
TERMINAL_DRAW = 0.0


def is_terminal_score(score: float) -> bool:
    """True for scores of a decided game (100000 minus actions taken, so a fixed +-50 window fails after turn 50)."""
    return abs(score) != float("inf") and abs(score) > TERMINAL_HERO_WIN / 2


def evaluate_hero_perspective(state: GameState) -> float:
    if state.outcome is not None:
        if state.outcome.outcome == OutcomeType.HERO_WIN:
            return TERMINAL_HERO_WIN - state.actions_taken
        elif state.outcome.outcome == OutcomeType.MONSTER_WIN:
            return TERMINAL_MONSTER_WIN + state.actions_taken
        else:
            return TERMINAL_DRAW

    hp_delta = (state.hero.hp - state.monster.hp) * 1.5
    weapon_score = 25.0 if state.inventory.has_weapon else 0.0
    potion_score = state.inventory.potions * 12.0
    key_score = state.inventory.keys * 8.0
    treasure_score = 60.0 if state.inventory.has_treasure else 0.0

    hero_atk = get_hero_current_attack(state.inventory.has_weapon, state.hero.base_attack)
    hero_dmg = calculate_damage(hero_atk, state.monster.defense)
    monster_dmg = calculate_damage(state.monster.base_attack, state.hero.defense)

    turns_to_kill_monster = (state.monster.hp + hero_dmg - 1) // hero_dmg
    turns_to_kill_hero = (state.hero.hp + monster_dmg - 1) // monster_dmg

    # Whoever moves next strikes first, so the hero must be strictly faster on the monster's turn.
    if state.active_actor == Actor.HERO:
        is_winning = turns_to_kill_monster <= turns_to_kill_hero
    else:
        is_winning = turns_to_kill_monster < turns_to_kill_hero
    tactical_dist = get_tactical_distance(state)
    dist = min(tactical_dist, 10.0) if tactical_dist != float("inf") else 10.0

    if is_winning:
        combat_score = (10.0 - dist) * 3.0
    else:
        combat_score = dist * 3.0

    exit_score = 0.0
    goal_score = 0.0
    if state.inventory.has_treasure:
        for y in range(state.height):
            for x in range(state.width):
                if state.tiles[y][x] == TileType.EXIT:
                    dist_exit, _, _ = bfs_path(
                        state.tiles,
                        state.hero.pos,
                        Position(x, y),
                        state.width,
                        state.height,
                        blocked={(state.monster.pos.x, state.monster.pos.y)},
                        allow_goal_blocked=False,
                    )
                    if dist_exit != float("inf"):
                        exit_score = max(0.0, 15.0 - dist_exit) * 5.0
                    break
    else:
        goal_dist, _ = hero_objective_path(state)
        if goal_dist != float("inf"):
            goal_score = max(0.0, 15.0 - goal_dist) * 2.0

    return (
        hp_delta
        + weapon_score
        + potion_score
        + key_score
        + treasure_score
        + combat_score
        + exit_score
        + goal_score
    )
