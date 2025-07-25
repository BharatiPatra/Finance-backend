from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from app.agent.finance_agent.agent import get_root_agent
from google.genai import types


session_service = InMemorySessionService()

APP_NAME = "FinanceAgent"


async def get_session_service(user_id: str, session_id: str):
    """
    Returns the session service for the given user and session ID.
    """
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    if not session:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
    return session


async def get_runner(user_id: str, session_id: str):
    """
    Returns the runner for the given user and session ID.
    """
    # Initialize the session service if it doesn't exist
    await get_session_service(user_id, session_id)
    return Runner(
        agent=get_root_agent(), app_name=APP_NAME, session_service=session_service
    )


async def run_agent(user_id: str, session_id: str, input_text: str):
    """
    Runs the agent with the given input text and returns the response.
    """
    content = types.Content(role="user", parts=[types.Part(text=input_text)])
    runner = await get_runner(user_id, session_id)

    events = runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    )
    async for ev in events:
        pass

    final_session = await session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    return final_session.state
