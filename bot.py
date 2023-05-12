import discord
import interactions
import openai
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed

#
# DEFINE VARIABLES #
#

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')
OPENAI_KEY = os.getenv('OPENAI_KEY')
WEBHOOK = os.getenv('WEBHOOK')

intents = discord.Intents.default()
client = discord.Client(intents=intents)

bot = interactions.Client(token=TOKEN)
openai.api_key = OPENAI_KEY

# DEFINING FUNCTIONS #

async def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
 
async def source_send():
    embed_first = DiscordEmbed(
        title='**GitHub**',
        description='Thanks for taking an interest in **DiscordGPT**!\nBelow is the official GitHub for the project!',
        color='58b9ff'
    )
    embed_second = DiscordEmbed(
        title='GitHub',
        url='https://github.com/byestumpy/DiscordGPT',
        color='58b9ff'
    )
    webhook = DiscordWebhook(url=WEBHOOK)
    webhook.add_embed(embed_first)
    webhook.add_embed(embed_second)
    response = webhook.execute()
    
    if response.status_code not in range(200, 300):
        print('Failed to send message to Discord')
    else:
        print('Message sent to Discord')

#
#
# BOT COMMANDS #
#
#

print("Script starting...")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
      
@bot.command(
    name="chat",
    description="Chat with the AI!",
    options=[
        interactions.Option(
            name="message",
            description="Message to send to the AI",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)

async def chat(ctx, message: str):
    await ctx.defer()
    logger.info(f"User {ctx.author.name} sent command: {message}")
    response = await generate_response(message)
    logger.info(f"Bot response: {response}")
    chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
    for chunk in chunks:
        await ctx.send(content=chunk, ephemeral=False)
        
@bot.command(
    name="source",
    description="Bot GitHub",
)
async def source(ctx):
    await ctx.defer()
    await source_send()
   
bot.start()
