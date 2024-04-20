import discord, datetime
from typing import Optional
from discord.ext import commands
from discord import app_commands, Embed, Interaction

class Utility(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    def format_dt(self, dt: datetime.datetime) -> str:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

        day_name = days[dt.weekday()]
        day = dt.day
        month_name = months[dt.month - 1] 
        year = dt.year
        hour = dt.hour
        minute = dt.minute
    
        return f"{day_name} {day} {month_name} {year} @ {hour:02}:{minute:02}"


    @app_commands.command(name="members", description="displays the amount of members in this guild")
    async def members(self, interaction: Interaction):

        embed = Embed(color=0x0C0C0D)
        embed.set_author(name=f"{len(interaction.guild.members)} members", icon_url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"requested by {interaction.user.name}", icon_url=f"{interaction.user.avatar}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="joined-at", description="displays the date the member joined this guild")
    @app_commands.describe(member="the member to display the join date for")
    async def joined_at(self, interaction: Interaction, member: Optional[discord.Member]=None):

        if not member:
            member = interaction.user

        date = self.format_dt(member.joined_at)

        embed = Embed(description=f"> joined at {date.lower()}",color=0x0C0C0D)
        embed.set_author(name=f"{member.display_name}", icon_url=f"{member.avatar}")
        embed.set_footer(text=f"requested by {interaction.user.name}", icon_url=f"{interaction.user.avatar}")
        await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Utility(client))