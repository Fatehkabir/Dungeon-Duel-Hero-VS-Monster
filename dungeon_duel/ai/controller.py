from typing import Dict, Any, Optional, Tuple
from dungeon_duel.core.models import GameState, Action, ActionType, Actor, Difficulty
from dungeon_duel.core.actions import DIRECTIONS
from dungeon_duel.core.rules import apply_action, decisive_actions
from dungeon_duel.ai.bfs import bfs_path, get_tactical_distance, hero_objective_path
from dungeon_duel.ai.evaluation import is_terminal_score
from dungeon_duel.ai.retreat import (
    SAFE_HEAL_HP_FRACTION,
    avoids_unwinnable_duel,
    retreat_action,
    should_retreat,
)
from dungeon_duel.ai.minimax import minimax_search
from dungeon_duel.ai.mcts import mcts_search


def _move_dest(state: GameState, action: Action) -> Optional[Tuple[int, int]]:
    if action.type not in DIRECTIONS:
        return None
    pos = (state.hero if state.active_actor == Actor.HERO else state.monster).pos
    d = DIRECTIONS[action.type]
    return pos.x + d.x, pos.y + d.y


def _avoid_reverse(state: GameState, action: Action, actions: list) -> Action:
    """Swap a move straight back onto the cell just left (the usual two-step loop) for another move."""
    back = state.last_pos.get(state.active_actor)
    dest = _move_dest(state, action)
    if back is None or dest is None or dest != (back.x, back.y):
        return action
    alternatives = [a for a in actions if _move_dest(state, a) != (back.x, back.y)]
    return next((a for a in alternatives if a.type in DIRECTIONS), alternatives[0] if alternatives else action)


def _strategic_action(state: GameState) -> Action:
    actions = decisive_actions(state)
    adjacent = state.hero.pos.is_adjacent(state.monster.pos)
    if state.active_actor == Actor.HERO:
        # Heal while it is safe: out of melee, hurt enough that a full +30 is not wasted.
        if (
            not adjacent
            and state.hero.hp <= state.hero.max_hp * SAFE_HEAL_HP_FRACTION
            and state.hero.hp <= state.hero.max_hp - 30
        ):
            potion = next((action for action in actions if action.type == ActionType.USE_POTION), None)
            if potion:
                return potion
        attack = next((action for action in actions if action.type == ActionType.ATTACK), None)
        if attack:
            return attack
        for kind in (ActionType.PICK_UP, ActionType.OPEN_DOOR):
            found = next((action for action in actions if action.type == kind), None)
            if found:
                return found
        _, step = hero_objective_path(state)
        if step:
            move = next((action for action in actions if action.type == step), None)
            if move:
                return _avoid_reverse(state, move, actions)
        _, _, chase = bfs_path(
            state.tiles,
            state.hero.pos,
            state.monster.pos,
            state.width,
            state.height,
            blocked={(state.monster.pos.x, state.monster.pos.y)},
            allow_goal_blocked=True,
        )
        if chase:
            move = next((action for action in actions if action.type == chase), None)
            if move:
                return _avoid_reverse(state, move, actions)
    else:
        attack = next((action for action in actions if action.type == ActionType.ATTACK), None)
        if attack:
            return attack
        _, _, step = bfs_path(
            state.tiles,
            state.monster.pos,
            state.hero.pos,
            state.width,
            state.height,
            blocked={(state.hero.pos.x, state.hero.pos.y)},
            allow_goal_blocked=True,
        )
        if step:
            move = next((action for action in actions if action.type == step), None)
            if move:
                return _avoid_reverse(state, move, actions)
    return actions[0]


def with_retreat_memory(state: GameState, actor: Actor, telemetry: Dict[str, Any]) -> GameState:
    """Record whether `actor` was retreating so the next decision can apply hysteresis.

    Call on the state returned by apply_action, with the telemetry that produced the action.
    """
    state.retreating[actor] = telemetry.get("mode") == "RETREAT"
    return state


def _plan_action(state: GameState) -> Tuple[Action, str, str]:
    """Decide what the agent wants to do: break contact when hurt, otherwise follow its objective."""
    actor = state.active_actor
    agent = state.hero if actor == Actor.HERO else state.monster
    actions = decisive_actions(state)
    if should_retreat(state):
        hp = f"{agent.hp}/{agent.max_hp} HP"
        why = "Unarmed and outmatched" if avoids_unwinnable_duel(state) else f"Losing the fight at {hp}"
        flee = retreat_action(state, actions)
        if flee:
            what = {
                ActionType.USE_POTION: "drinking a potion",
                ActionType.PICK_UP: "grabbing an item underfoot",
                ActionType.OPEN_DOOR: "opening a door",
                ActionType.WAIT: "holding position out of reach to recover",
            }.get(flee.type, f"breaking contact with {flee.type.value}")
            return flee, "RETREAT", f"{why}: {what}."
        fight = _strategic_action(state)
        return fight, "RETREAT", f"{why} and cornered: fighting back with {fight.type.value}."
    action = _strategic_action(state)
    reason = "Striking." if action.type == ActionType.ATTACK else (
        f"Pressing the {'objective' if actor == Actor.HERO else 'pursuit'} with {action.type.value}."
    )
    return action, "ADVANCE", reason


def _forced(actor: Actor, score: float, win: bool) -> bool:
    """Is `score` (hero perspective) a forced win (win=True) or forced loss (win=False) for `actor`?"""
    if not is_terminal_score(score):
        return False
    hero_good = score > 0
    return hero_good == win if actor == Actor.HERO else hero_good != win


def choose_action(
    state: GameState,
    hero_difficulty: Difficulty = Difficulty.MEDIUM,
    monster_difficulty: Difficulty = Difficulty.MEDIUM,
    thinking_deadline_ms: float = 250.0,
    seed: int = 42,
) -> Tuple[Action, Dict[str, Any]]:
    actor = state.active_actor
    diff = hero_difficulty if actor == Actor.HERO else monster_difficulty

    dist = get_tactical_distance(state)

    if dist <= 3:
        # Minimax alpha-beta
        depth_map = {Difficulty.EASY: 2, Difficulty.MEDIUM: 4, Difficulty.HARD: 6}
        depth = depth_map.get(diff, 4)
        minimax_action, score, comp_depth, nodes, cuts = minimax_search(
            state, depth, deadline_ms=thinking_deadline_ms
        )
        action, mode, reason = _plan_action(state)
        overrode = False
        # Lookahead only overrides the plan when it is certain: it sees a forced win, or the plan walks
        # into a forced loss that another move avoids. Deeper search (harder difficulty) sees more.
        if comp_depth >= 1 and action != minimax_action:
            if _forced(actor, score, True):
                action, overrode = minimax_action, True
            elif comp_depth >= 2:
                after, _ = apply_action(state, action)
                if not after.outcome or after.outcome.winner != actor:
                    plan_score = minimax_search(after, comp_depth - 1, deadline_ms=thinking_deadline_ms)[1]
                    if _forced(actor, plan_score, False) and not _forced(actor, score, False):
                        action, overrode = minimax_action, True
        telemetry = {
            "algorithm": "MINIMAX",
            "distance": dist,
            "depth_completed": comp_depth,
            "depth_requested": depth,
            "nodes": nodes,
            "cutoffs": cuts,
            "score": score,
            "mode": mode,
            "search_overrode": overrode,
            "explanation": (
                f"Opponent within tactical distance ({dist} tiles). "
                f"{'Minimax found a forced line.' if overrode else reason} Minimax depth {comp_depth}."
            ),
        }
        return action, telemetry
    else:
        # MCTS
        iter_map = {Difficulty.EASY: 100, Difficulty.MEDIUM: 500, Difficulty.HARD: 2000}
        iters = iter_map.get(diff, 500)
        action, comp_iters, avg_steps, visits = mcts_search(
            state,
            iters,
            deadline_ms=thinking_deadline_ms,
            seed=seed + state.actions_taken,
        )
        action, mode, reason = _plan_action(state)
        telemetry = {
            "algorithm": "MCTS",
            "distance": dist,
            "iterations_completed": comp_iters,
            "iterations_requested": iters,
            "avg_rollout_steps": avg_steps,
            "action_visits": {k.value: v for k, v in visits.items()},
            "mode": mode,
            "explanation": f"Opponent at distance {dist}. {reason} ({comp_iters} MCTS rollouts, advisory at this range).",
        }
        return action, telemetry
