import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response) if not is_private else await message.author.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTEyOTA0Njk4NzgyODg5NTkxNw.G22web.1KA6VCZZmjMJpDQ3B7399OgB9RdKl3_N_esULA'
    intens = discord.Intents.default()
    intens.message_content = True
    client = discord.Client(intents = intens)


    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username}: {user_message} ({channel})')
        
        if user_message[0] == '!':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=False)

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)

    client.run(TOKEN)