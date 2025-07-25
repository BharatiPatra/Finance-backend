import time
from google.adk.events import Event, EventActions


def create_event(delta: dict, author: str = "system") -> Event:

    actions_with_update = EventActions(state_delta=delta)
    return Event(
        invocation_id="inv_login_update",
        author=author,
        actions=actions_with_update,
        timestamp=time.time(),
        # content might be None or represent the action taken
    )
