from aiohttp import web
import asyncio


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    welcome_html = f'''
    <div hx-swap-oob="beforeend:#chat">
        <div class="flex justify-start">
            <div class="bg-gray-200 p-2 rounded-lg">
            Hi.
            </div>
        </div>
    </div>
    '''
    await ws.send_str(welcome_html)

    print("WebSocket client connected")
    try:
        async for msg in ws:
            print(f"Received: {msg}")
            if msg.type == web.WSMsgType.TEXT:
                import json
                user_message = json.loads(msg.data).get('message')

                user_message_html = f'''
                <div hx-swap-oob="beforeend:#chat">
                    <div class="flex justify-end">
                        <div class="bg-blue-200 p-2 rounded-lg">{user_message}</div>
                    </div>
                </div>
                '''
                await ws.send_str(user_message_html)

                chatbot_reply = f'You said {user_message}'
                reply_message_html = f'''
                <div hx-swap-oob="beforeend:#chat">
                    <div class="flex justify-start">
                        <div class="bg-gray-200 p-2 rounded-lg">{chatbot_reply}</div>
                    </div>
                </div>
                '''
                await ws.send_str(reply_message_html)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"WebSocket connection closed with exception: {ws.exception()}")
    except asyncio.CancelledError:
        print("WebSocket client disconnected")
    return ws

async def index(request):
    return web.FileResponse("index.html")

def main():
    app = web.Application()

    app.router.add_get("/", index)
    app.router.add_get("/ws", websocket_handler)

    port = 5000
    print(f"Server running at http://localhost:{port}")
    print(f"WebSocket endpoint available at ws://localhost:{port}/ws")
    web.run_app(app, port=port)

if __name__ == "__main__":
    main()
