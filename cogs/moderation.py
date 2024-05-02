import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands, Embed, Interaction

class Moderation(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    @app_commands.command(name="nuke", description="delete all messages in the channel")
    @app_commands.describe(channel="the channel to nuke")
    @app_commands.default_permissions(manage_channels=True)
    async def nuke(self, interaction: Interaction, channel: Optional[discord.TextChannel]=None, reason: Optional[str]=None):

        if not channel:
            channel = interaction.channel

        if not reason:
            reason = f"no reason provided, channel was nuked by {interaction.user}"

        cloned_channel = await channel.clone(reason=reason)
        await channel.delete(reason=reason)

        embed = Embed(description=f"> ✅ nuked {cloned_channel.mention} | *{reason}*", color=0x0C0C0D)
        await cloned_channel.send(interaction.user.mention, embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Moderation(client))
