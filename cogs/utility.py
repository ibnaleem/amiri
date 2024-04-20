from discord.ext import commands
from discord import app_commands, Embed, Interaction

class Utility(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    @app_commands.command(name="members", description="Displays the amount of members in the guild")
    async def members(self, interaction: Interaction):

        embed = Embed(color=0x0C0C0D)
        embed.set_author(name=f"{len(interaction.guild.members)} members", icon_url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"requested by {interaction.user.name}", icon_url=f"{interaction.user.avatar}")

        await interaction.response.send_message(embed=embed)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Utility(client))