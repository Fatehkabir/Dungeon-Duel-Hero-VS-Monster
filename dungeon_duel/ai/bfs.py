from collections import deque
from typing import List, Optional, Tuple, Set
from dungeon_duel.core.models import Position, TileType, ActionType, GameState, ItemType


def bfs_path(
    tiles: List[List[TileType]],
    start: Position,
    goal: Position,
    width: int,
    height: int,
    blocked: Optional[Set[Tuple[int, int]]] = None,
    allow_goal_blocked: bool = True,
) -> Tuple[int, List[Position], Optional[ActionType]]:
    if start == goal:
        return 0, [], None

    blocked_set = blocked or set()

    queue = deque([start])
    visited = { (start.x, start.y) }
    parent = {}

    found = False
    deltas = [
        (0, -1, ActionType.MOVE_UP),
        (0, 1, ActionType.MOVE_DOWN),
        (-1, 0, ActionType.MOVE_LEFT),
        (1, 0, ActionType.MOVE_RIGHT),
    ]

    while queue:
        cur = queue.popleft()
        if cur == goal:
            found = True
            break

        for dx, dy, _ in deltas:
            nx, ny = cur.x + dx, cur.y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    tile = tiles[ny][nx]
                    walkable = tile in (TileType.FLOOR, TileType.DOOR_OPEN, TileType.EXIT)
                    is_dest = (nx == goal.x and ny == goal.y)
                    is_cell_blocked = (nx, ny) in blocked_set and not (allow_goal_blocked and is_dest)

                    if walkable and not is_cell_blocked:
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (cur.x, cur.y)
                        queue.append(Position(nx, ny))

    if not found:
        return float("inf"), [], None

    # Reconstruct path
    path = []
    curr = (goal.x, goal.y)
    start_tuple = (start.x, start.y)

    while curr != start_tuple:
        path.append(Position(curr[0], curr[1]))
        curr = parent[curr]

    path.reverse()
    first_step = path[0]

    action = None
    if first_step.x > start.x:
        action = ActionType.MOVE_RIGHT
    elif first_step.x < start.x:
        action = ActionType.MOVE_LEFT
    elif first_step.y > start.y:
        action = ActionType.MOVE_DOWN
    elif first_step.y < start.y:
        action = ActionType.MOVE_UP

    return len(path), path, action


def get_tactical_distance(state: GameState) -> int:
    h = state.hero.pos
    m = state.monster.pos

    if h.is_adjacent(m):
        return 1

    dist, _, _ = bfs_path(
        state.tiles,
        h,
        m,
        state.width,
        state.height,
        blocked={(m.x, m.y)},
        allow_goal_blocked=True,
    )
    return dist


def distance_map(
    tiles: List[List[TileType]],
    start: Position,
    width: int,
    height: int,
    blocked: Optional[Set[Tuple[int, int]]] = None,
) -> List[List[float]]:
    """BFS distance from `start` to every reachable walkable tile (inf when unreachable)."""
    blocked = blocked or set()
    inf = float("inf")
    dist = [[inf] * width for _ in range(height)]
    dist[start.y][start.x] = 0
    queue = deque([(start.x, start.y)])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and dist[ny][nx] == inf:
                if _walkable_floor(tiles[ny][nx]) and (nx, ny) not in blocked:
                    dist[ny][nx] = dist[y][x] + 1
                    queue.append((nx, ny))
    return dist


# Hero HP fraction at or below which finding a potion outranks weapon, relic and key.
HEAL_FIRST_HP_FRACTION = 0.6


def _walkable_floor(tile: TileType) -> bool:
    return tile in (TileType.FLOOR, TileType.DOOR_OPEN, TileType.EXIT)


def hero_objective_path(state: GameState) -> Tuple[float, Optional[ActionType]]:
    """Distance and next step toward the hero's current objective.

    Priority matches the TypeScript planner: exit once the treasure is carried,
    otherwise a reachable weapon, then treasure, key, locked door, and potion.
    """
    hero = state.hero.pos
    blocked = {(state.monster.pos.x, state.monster.pos.y)}
    width, height = state.width, state.height

    def first_reachable(goals: List[Position]) -> Optional[Tuple[float, Optional[ActionType]]]:
        best: Optional[Tuple[float, Optional[ActionType]]] = None
        for goal in goals:
            dist, _, action = bfs_path(state.tiles, hero, goal, width, height, blocked, False)
            if dist != float("inf") and (best is None or dist < best[0]):
                best = (dist, action)
        return best

    if state.inventory.has_treasure:
        for y in range(height):
            for x in range(width):
                if state.tiles[y][x] == TileType.EXIT:
                    dist, _, action = bfs_path(
                        state.tiles, hero, Position(x, y), width, height, blocked, False
                    )
                    if dist != float("inf"):
                        return dist, action

    # Hurt, with no potion in the pack: a reachable potion comes before weapon, relic and key.
    if state.inventory.potions == 0 and state.hero.hp <= state.hero.max_hp * HEAL_FIRST_HP_FRACTION:
        hurt_potion = first_reachable([it.pos for it in state.items if it.type == ItemType.POTION])
        if hurt_potion:
            return hurt_potion

    if not state.inventory.has_weapon:
        weapon = first_reachable([it.pos for it in state.items if it.type == ItemType.WEAPON])
        if weapon:
            return weapon

    treasure = first_reachable([it.pos for it in state.items if it.type == ItemType.TREASURE])
    if treasure:
        return treasure

    key = first_reachable([it.pos for it in state.items if it.type == ItemType.KEY])
    if key:
        return key

    if state.inventory.keys > 0:
        approaches: List[Position] = []
        for y in range(height):
            for x in range(width):
                if state.tiles[y][x] != TileType.DOOR_LOCKED:
                    continue
                for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    ax, ay = x + dx, y + dy
                    if 0 <= ax < width and 0 <= ay < height and _walkable_floor(state.tiles[ay][ax]):
                        approaches.append(Position(ax, ay))
        door = first_reachable(approaches)
        if door:
            return door

    potion = first_reachable([it.pos for it in state.items if it.type == ItemType.POTION])
    if potion:
        return potion

    return float("inf"), None
