import os
# from os.path import exists
import discord
from discord.ext import commands
from io import BytesIO
from jokeapi import Jokes
import time
from random import randint
import json
import base64
import os

import bot.src.consts as consts
import bot.src.util as util
import bot.src.opensea as opensea
import bot.src.kong as kong_util



KONG_ASSET_OPENSEA_URL = "https://opensea.io/assets/ethereum/0xef0182dc0574cd5874494a120750fd222fdb909a/"

ASSETS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
KONGS_PATH = os.path.join(ASSETS_PATH, "kongs")
META_PATH = os.path.join(ASSETS_PATH, "meta.json")
META = json.loads(open(META_PATH).read())


def initialize_bot():
    bot = commands.Bot(command_prefix="$", case_insensitive=True)
    register_commands(bot)
    bot.run(consts.DISCORD_TOKEN)


async def send_image_binary(ctx, img):
    with BytesIO() as image_binary:
        img.save(image_binary, "PNG")
        image_binary.seek(0)
        await ctx.channel.send(file=discord.File(fp=image_binary, filename="tacpeo.png"))    


# Include chat commands within this function to ensure they are registered on startup
def register_commands(bot):

    @bot.command(help="Sweep those thin floors! fr fr", brief="Sweep those thin floors! fr fr")
    async def sweep(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "sweep.gif")))

    @bot.command(help="On your head!", brief="On your head!")
    async def oyh(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "oyh.gif")))

    @bot.command(help="Let's focking go!", brief="Let's focking go!")
    async def lfg(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "lfg.gif")))

    @bot.command(help="Looking for group!", brief="Looking for group!")
    async def lookingforgroup(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "lfg.gif")))

    @bot.command(help="Good Morning!", brief="Good Morning!")
    async def gm(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "gm.gif")))

    @bot.command(help="Good Night!", brief="Good Night!")
    async def gn(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "gn.gif")))

    @bot.command(help="There is no ceiling!", brief="There is no ceiling!")
    async def ceiling(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "ceiling.gif")))

    @bot.command(help="I am Kong!", brief="I am Kong!")
    async def iamkong(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "iamkong.gif")))

    @bot.command(help="Yes.", brief="Yes.")
    async def yes(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "yes.png")))

    @bot.command(help="Ready to Rumble.", brief="Ready to Rumble.")
    async def rumble(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "rumble.gif")))

    @bot.command(help="We are Kong.", brief="We are Kong.")
    async def wearekong(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "wearekong.gif")))

    @bot.command(help="Alpha alert.", brief="Alpha alert.")
    async def alpha(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "alpha.gif")))

    @bot.command(help="Tacpeo.", brief="Tacpeo.")
    async def tacpeo(ctx, *_args):
        await ctx.channel.send(file=discord.File(os.path.join(consts.MEMES_PATH, "tacpeo.gif")))

    @bot.command(
        help="$praise <team member name>",
        brief="Give thanks to the RKL team members.",
    )
    async def praise(ctx, *args):
        name = str(args[0]).lower()
        if name not in consts.STAFF:
            name = "team"
        await ctx.channel.send(
            file=discord.File(os.path.join(consts.STAFF_PATH, consts.STAFF[name]))
        )

    @bot.command(
        help="$image <kong token id> [hd]",
        brief="Get the image of a Rumble Kong by token id.",
    )
    async def image(ctx, *args):
        image_string = "image_url"
        if len(args) > 1 and str(args[1]).lower() == "hd":
            image_string = "image_original_url"

        params = {"token_ids": args[0], "collection_slug": "rumble-kong-league"}
        kong_url = opensea.fetch_opensea_asset(consts.OPENSEA_ASSETS_URL, params)[
            "assets"
        ][0][image_string]
        await ctx.channel.send(str(kong_url))

    @bot.command(
        help=("$jersey <kong token id> <team jersey name>"),
        brief="Rep team's jersey on your Kong.",
    )
    async def jersey(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        jersey_kong = kong_util.apply_drip(kong, str(args[1]).lower(), True)
        await send_image_binary(ctx, jersey_kong)

    @bot.command(
        help=("$jersey <kong token id> <drip name>"),
        brief="Add some drip to your Kong.",
    )
    async def drip(ctx, *args):
        kong = kong_util.draw_naked_kong(int(args[0]))
        dripped_kong = kong_util.apply_drip(kong, str(args[1]).lower(), False)
        await send_image_binary(ctx, dripped_kong)

    @bot.command(
        help=("$rank <kong token id>"),
        brief="Gives you (i) visual, (ii) boost and (iii) total rank of your kong."
    )
    async def rank(ctx, *args):

        kong_token_id = int(args[0])
        image_name = f"{kong_token_id}.jpg"
        kong_image_path = os.path.join(KONGS_PATH, image_name)
        kong_image = ""
        with open(kong_image_path, "rb") as image_file:
            kong_image = base64.b64encode(image_file.read())

        discord_message = discord.Embed(
            title=f"Kong #{kong_token_id} Rarity Card",
            # description=f"Price: {data.price_eth()} {data.payment_symbol}, (${data.price_usd():.2f})",
            url=f"{KONG_ASSET_OPENSEA_URL}{kong_token_id}",
            color=0x00ff00
        )

        img_file = discord.File(kong_image_path, filename=image_name)
        discord_message.set_thumbnail(url=f"attachment://{image_name}")
        # discord_message.add_field(
        #     name="Boost Total", value=data.boosts["cumulative"], inline=True
        # )
        # discord_message.add_field(
        #     name="Boost Total Rank", value=
        # )

        # discord_message.add_field(name="Defense", value=data.boosts["defense"], inline=True)
        # discord_message.add_field(name="Finish", value=data.boosts["finish"], inline=True)
        # discord_message.add_field(
        #     name="Shooting", value=data.boosts["shooting"], inline=True
        # )
        # discord_message.add_field(name="Vision", value=data.boosts["vision"], inline=True)
        # discord_message.add_field(
        #     name="Seller",
        #     value=f"[{data.seller}](https://opensea.io/{data.seller_address})",
        #     inline=False,
        # )
        # discord_message.add_field(
        #     name="Buyer",
        #     value=f"[{data.buyer}](https://opensea.io/{data.buyer_address})",
        #     inline=True,
        # )

        await ctx.channel.send(file=img_file, embed=discord_message)

    # @bot.command(help="Tells you a joke.", brief="Funny jokes left and right.")
    # async def joke(ctx, *args):
    #     j = await Jokes()
    #     joke = await j.get_joke(blacklist=["racist", "religious", "political", "sexist", "nsfw",  "explicit"])
    #     if joke["type"] == "single": # Print the joke
    #         await ctx.channel.send(str(joke["joke"]))
    #     else:
    #         await ctx.channel.send(str(joke["setup"]))
    #         time.sleep(3)
    #         await ctx.channel.send(str(joke["delivery"]))

    # TODO:
    # == !Floor ============================================================================
    # @bot.command(
    #     help="Get statistics about the floor price of RKL collections.",
    #     brief="collection (string):",
    # )
    # async def floor(ctx, *args):
    #     collection = args[0]

    #     filter = ""
    #     if len(args) > 1:
    #         filter = args[1].title()
    #     if collection == "sneakers":
    #         filter = "Sneakers"

    #     listings = util.read_json(
    #         os.path.join(consts.CACHE_PATH, collection, "-asset-cache.json")
    #     )["assets"]
    #     embed = opensea.construct_floor_stats_embed(collection, listings, filter)
    #     await ctx.channel.send(embed=embed)
