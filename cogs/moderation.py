import discord
from typing import Optional
from discord.ext import commands
from discord import app_commands, Embed, Interaction

class Moderation(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    @app_commands.command(name="nuke", description="nuke a channel")
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

    @app_commands.command(name="purge", description="delete messages in the channel")
    @app_commands.describe(amount="the amount of messages to delete", channel="the channel to delete messages from", reason="the reason for the purge", member="the member to delete messages from", bots="whether to delete messages from bots")
    @app_commands.default_permissions(manage_messages=True)
    async def purge(self, interaction: Interaction, amount: Optional[int]=None, channel: Optional[discord.TextChannel]=None, reason: Optional[str]=None, member: Optional[discord.Member]=None, bots: Optional[bool]=None):

        await interaction.response.defer()

        if not amount:
            amount = 10

        if not channel:
            channel = interaction.channel

        if not reason:
            reason = f"no reason provided, messages were purged by {interaction.user}"

        if member and bots:
            embed = Embed(description=f"> ❌ you can't delete messages from both a member and bots", color=0x0C0C0D)
            await interaction.followup.send(embed=embed)

        elif member:
            embed = Embed(description=f"> ✅ purged {amount} messages from {member.mention} in {channel.mention}| *{reason}*", color=0x0C0C0D)
            await channel.purge(limit=amount, check=lambda m: m.author == member, reason=reason)
            await interaction.followup.send(embed=embed)

        elif bots:
            embed = Embed(description=f"> ✅ purged {amount} messages from bots in {channel.mention} | *{reason}*", color=0x0C0C0D)
            await channel.purge(limit=amount, check=lambda m: m.author.bot, reason=reason)
            await interaction.followup.send(embed=embed)

        else:
            await channel.purge(limit=amount, reason=reason)
            embed = Embed(description=f"> ✅ purged {amount} messages in {channel.mention} | *{reason}*", color=0x0C0C0D)
            await interaction.followup.send(embed=embed)

    @app_commands.command(name="kick", description="kick a member")
    @app_commands.describe(member="the member to kick", reason="the reason for the kick")
    async def kick(self, interaction: Interaction, member: discord.Member, reason: Optional[str]=None):
        if not reason:
            reason = f"no reason provided, member was kicked by {interaction.user}"

        embed = Embed(description=f"> ✅ kicked {member.mention} | *{reason}*", color=0x0C0C0D)
        await member.kick(reason=reason)
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Moderation(client))
