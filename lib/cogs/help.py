import asyncio
import discord
from discord import Colour, Embed
from discord.ext import commands
from discord.utils import get


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self,ctx):
        cur_page = 1
        pages = 6
        contents = [
            f"""
            Shows information about the server and on the installation of the modpack.
        
            Syntax: 
            `!beta`
        
            Help Page 1/{pages}""",
            f"""
            Shows the rules. Read them carefully, because ***by playing on the server you automatically agree to them.*** 
                
            Syntax: 
            `!rules`
        
            Help Page 2/{pages}""",
            f"""
            Shows information on how to debug the modpack and ask for support in *#modpack-support*.
                
            Syntax: 
            `!debug`
        
            Help Page 3/{pages}""",
            f"""
            Shows information on how to claim land ingame.

            Syntax: 
            `!claiming`

            Help Page 4/{pages}""",
            f"""
            Make a suggestion in `#suggestions`. The bot will start asking you questions, that you just have to answer.

            Syntax: 
            `!suggest`

            Help Page 5/{pages}"""
        ]
        titles = [
            "Public Beta / Modpack",
            "Rules",
            "Debugging / Modpack Support",
            "Claiming Land"
        ]
        embed = Embed(
            title=titles[cur_page-1],
            colour=Colour(0x71368a),
            description=contents[cur_page-1]
        )
        message = await ctx.send(embed=embed)

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=120, check=check)
                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    embed = Embed(
                        title=titles[cur_page - 1],
                        colour=Colour(0x71368a),
                        description=contents[cur_page - 1]
                    )
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    embed = Embed(
                        title=titles[cur_page - 1],
                        colour=Colour(0x71368a),
                        description=contents[cur_page - 1]
                    )
                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)
                else:
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

def setup(bot):
    bot.add_cog(HelpCog(bot))