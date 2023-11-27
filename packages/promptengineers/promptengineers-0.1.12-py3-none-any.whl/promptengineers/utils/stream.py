"""Stream Utils"""
from typing import Awaitable
import asyncio
import ujson
import openai

from fastapi.responses import StreamingResponse

from promptengineers.utils import logger


async def wrap_done(fn_name: Awaitable, event: asyncio.Event):
    """Wrap an awaitable with a event to signal when it's done or an exception is raised."""
    try:
        await fn_name
    except asyncio.CancelledError:
        pass
    except openai.APIError as error:
        print(f"Caught API error: {error}")
    finally:
        # Signal the aiter to stop.
        event.set()

def token_stream(token: str = None, action_type: str = None):
    """ Use server-sent-events to stream the response"""
    if not token and not action_type:
        data = {
            'sender': 'assistant',
            'message': "",
            'type': 'end'
        }
        logger.debug('[utils.stream.token_stream] End: %s', str(data))
    elif action_type == 'tool':
        data = {
            'sender': 'assistant',
            'message': token,
            'type': 'tool'
        }
        logger.debug('[utils.stream.token_stream] Action: %s', str(data))
    elif action_type == 'log':
        data = {
            'sender': 'assistant',
            'message': token,
            'type': 'log'
        }
        logger.debug('[utils.stream.token_stream] Log: %s', str(data))
    else:
        data = {
            'sender': 'assistant',
            'message': token,
            'type': 'stream'
        }
        logger.debug('[utils.stream.token_stream] Token: %s', str(data))
    return f"data: {ujson.dumps(data)}\n\n"

async def handle_streaming_response(stream, stream_type):
    return StreamingResponse(
        stream,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": stream_type,
        },
    )