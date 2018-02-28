import discord, scrython, BotUtils, asyncio
from discord.ext import commands

bot = commands.Bot(description='FetchBot', command_prefix="?")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def mtg(name):
    getCard = str(name)

    await asyncio.sleep(0.05)
    card = scrython.cards.Named(fuzzy=getCard)

    if card.type_line() == 'Creature':
        PT = "({}/{})".format(card.power(), card.toughness())
    else:
        PT = ""

    if card.cmc() == 0:
        mana_cost = ""
    else:
        mana_cost = card.mana_cost()

    string = """
    {cardname} {mana_cost}
    {type_line} {set_code} {rarity}
    {oracle_text}{power_toughness}
    """.format(
        cardname=card.name(),
        mana_cost=mana_cost,
        type_line=card.type_line(),
        set_code=card.set_code().upper(),
        rarity=card.rarity(),
        oracle_text=card.oracle_text(),
        power_toughness=PT
    )

    await self.bot.say(string)

bot.run(BotUtils.AUTH_TOKEN)
