from dataclasses import dataclass


@dataclass
class Action:
    id: str
    name: str


ACTIONS = [
    Action(id="action-1", name="Action 1"),
    Action(id="action-2", name="Action 2"),
    Action(id="action-3", name="Action 3"),
]


def get_all_actions() -> list[Action]:
    return ACTIONS


def get_action_by_id(id: str) -> Action | None:
    for action in ACTIONS:
        if id == action.id:
            return action
    return None
