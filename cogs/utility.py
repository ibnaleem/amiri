from icecream import ic
from typing import Optional
from discord.ext import commands
import asyncio, discord, datetime
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

    @app_commands.command(name="member-info", description="displays information about a member")
    @app_commands.describe(member="the member to display the information for")
    async def member_info(self, interaction: Interaction, member: Optional[discord.Member]=None):

        if not member:
            member = interaction.user

        print("Fetching member information...")
        # await interaction.response.defer()

        date = self.format_dt(member.joined_at)
        ic(date)
        roles = [role.mention for role in member.roles]
        ic(roles)
        roles = " ".join(roles)
        ic(roles)
        discord_id = member.id
        ic(discord_id)
        avatar_url = member.avatar
        ic(avatar_url)
        is_bot = bool(member.bot)
        ic(is_bot)
        is_owner = bool(member.guild.owner_id == member.id)
        ic(is_owner)
        status = member.raw_status
        ic(status)
        timed_out_until = member.timed_out_until
        ic(timed_out_until)
        is_on_mobile = member.is_on_mobile()
        ic(is_on_mobile)
        created_at = self.format_dt(member.created_at)
        ic(created_at)
        booster_since = self.format_dt(member.premium_since) if member.premium_since else "hasn't boosted yet"
        ic(booster_since)
        boost_level = member.premium_tier if member.premium_since else "0"
        ic(boost_level)
        permission = [permission for permission, value in member.guild_permissions if value]
        ic(permission)
        permission = " | ".join(permission)
        nickname = member.nick if member.nick else member.display_name
        ic(nickname)
        banner = member.banner if member.banner else None
        ic(banner)

        embed = Embed(description=f"> *{status}*", color=member.colour)
        embed.set_author(name=f"{member.display_name}", icon_url=f"{avatar_url}")
        embed.set_thumbnail(url=f"{avatar_url}")
        embed.add_field(name="nickname", value=f"{nickname}", inline=True)
        embed.add_field(name="id", value=f"{discord_id}", inline=True)
        embed.add_field(name="created at", value=f"{created_at.lower()}", inline=True)
        embed.add_field(name="joined at", value=f"{date.lower()}", inline=True)
        embed.add_field(name="booster since", value=f"{booster_since.lower()}", inline=True)
        embed.add_field(name="boost level", value=f"{boost_level}", inline=True)
        embed.add_field(name="top role", value=f"{member.top_role.mention}", inline=True)
        embed.add_field(name="roles", value=f"{roles}", inline=True)
        embed.add_field(name="is bot", value=f"{is_bot}", inline=True)
        embed.add_field(name="is owner", value=f"{is_owner}", inline=True)
        embed.add_field(name="is on mobile", value=f"{is_on_mobile}", inline=True)
        embed.add_field(name="timed out until", value=f"{timed_out_until}", inline=True)
        embed.add_field(name="permissions", value=f"{permission}", inline=True)

        if banner:
            embed.set_image(url=f"{banner}")

        print("Sending embed...")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="avatar", description="displays the avatar of a member")
    @app_commands.describe(member="the member to display the avatar for")
    async def avatar(self, interaction: Interaction, member: Optional[discord.Member]=None):
        if not member:
            member = interaction.user

        if not member.avatar is None:
            embed = Embed(color=member.colour)
            embed.set_author(name=f"{member.display_name}", icon_url=f"{member.avatar}")
            embed.set_image(url=f"{member.avatar}")
        else:
            embed = Embed(color=member.colour)
            embed.set_author(name=f"{member.display_name}", icon_url=f"{member.default_avatar}")
            embed.set_image(url=f"{member.default_avatar}")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="guild-info", description="displays information about this guild")
    @app_commands.describe(guild_id="optional: guild id to display information for")
    async def guild_info(self, interaction: Interaction, guild_id: Optional[str]=None):

        print("Deferring response...")
        await interaction.response.defer()
        print("Response sucessfully deferred")

        if guild_id:
            print(f"Fetching guild {guild_id} information...")
            try:
                guild_id = int(guild_id)
                guild = self.client.get_guild(guild_id)
                if guild is None:
                    await interaction.followup.send(f"i do not have access to the guild with the id {guild_id}: i must have access to the guild to retreive its information")
                    return
                ic(guild)

            except ValueError:
                await interaction.followup.send("provide a valid guild ID")
                return
            except Exception as e:
                await interaction.followup.send(f"**Error:** {e}")
                return
        else:
            print("'guild_id' was not specified, fetching 'interaction.guild'...")
            guild = interaction.guild
            ic(guild)

        print(f"Fetching guild information...")

        guild_desc = guild.description if guild.description else "no description"
        ic(guild_desc)
        ic(guild.name)
        ic(guild.icon)
        ic(len(guild.members))
        ic(guild.id)
        ic(guild.owner.mention)
        ic(len(guild.channels))
        ic(len(guild.text_channels))
        ic(len(guild.voice_channels))
        ic(len(guild.forums))
        ic(len(guild.roles))
        ic(len(guild.emojis))
        ic(len(guild.threads))
        guild_creation = self.format_dt(guild.created_at)
        ic(guild_creation)
        rules_channel = (guild.rules_channel.mention if guild.rules_channel else "not set")
        ic(rules_channel)
        ic(guild.verification_level)
        ic(guild.afk_timeout)
        afk_channel = guild.afk_channel.mention if guild.afk_channel else "not set"
        ic(afk_channel)
        system_channel = guild.system_channel.mention if guild.system_channel else "not set"
        ic(system_channel)
        ic(guild.premium_subscription_count)
        ic(len(guild.premium_subscribers))
        booster_role = guild.premium_subscriber_role.mention if guild.premium_subscriber_role else "not set"
        ic(booster_role)
        vanity = guild.vanity_url if guild.vanity_url else "not set"
        ic(vanity)
        filesize = guild.filesize_limit
        filesize = round(filesize * 0.000001)
        emoji_limit = guild.emoji_limit
        ic(emoji_limit)

        print("Creating embed...")
        embed = Embed(description=f"> *{guild_desc}*", color=0x0C0C0D)
        ic(embed)
        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
        ic(embed)
        embed.set_thumbnail(url=f"{guild.icon}")
        ic(embed)
        embed.add_field(name="total members", value=f"{len(guild.members)}", inline=True)
        ic(embed)
        embed.add_field(name="rules channel", value=f"{rules_channel}", inline=True)
        ic(embed)
        embed.add_field(name="guild id", value=f"{guild.id}", inline=True)
        ic(embed)
        embed.add_field(name="guild owner", value=f"{guild.owner.mention}", inline=True)
        ic(embed)
        embed.add_field(name="total channels", value=f"{len(guild.channels)}", inline=True)
        ic(embed)
        embed.add_field(name="text channels", value=f"{len(guild.text_channels)}", inline=True)
        ic(embed)
        embed.add_field(name="voice channels", value=f"{len(guild.voice_channels)}", inline=True)
        ic(embed)
        embed.add_field(name="forums", value=f"{len(guild.forums)}", inline=True)
        ic(embed)
        embed.add_field(name="roles", value=f"{len(guild.roles)}", inline=True)
        ic(embed)
        embed.add_field(name="emojis", value=f"{len(guild.emojis)}", inline=True)
        ic(embed)
        embed.add_field(name="threads", value=len(guild.threads), inline=True)
        ic(embed)
        embed.add_field(name="stage channels", value=len(guild.stage_channels))
        ic(embed)
        embed.add_field(name="filesize limit", value=f"{filesize} MB", inline=True)
        ic(embed)
        embed.add_field(name="bitrate limit", value=f"{(guild.bitrate_limit / 1000)} kbps", inline=True)
        ic(embed)
        embed.add_field(name="emoji limit", value=f"{emoji_limit} emojis", inline=True)
        ic(embed)
        embed.add_field(name="created at", value=f"{guild_creation.lower()}", inline=True)
        ic(embed)
        embed.add_field(name="verification level", value=f"{guild.verification_level}", inline=True)
        ic(embed)
        embed.add_field(name="afk timeout", value=f"{guild.afk_timeout} seconds", inline=True)
        ic(embed)
        embed.add_field(name="afk channel", value=f"{afk_channel}", inline=True)
        ic(embed)
        embed.add_field(name="system channel", value=f"{system_channel}", inline=True)
        ic(embed)
        embed.add_field(name="# of boosts", value=f"{guild.premium_subscription_count}", inline=True)
        ic(embed)
        embed.add_field(name="# of boosters", value=f"{len(guild.premium_subscribers)}", inline=True)
        ic(embed)
        embed.add_field(name="booster role", value=booster_role, inline=True)
        ic(embed)
        embed.add_field(name="vanity url", value=f"{vanity}", inline=True)
        ic(embed)
        embed.add_field(name="verification level", value=f"{guild.verification_level}", inline=True)
        ic(embed)
        embed.set_footer(text=f"requested by {interaction.user}", icon_url=interaction.user.avatar)
        ic(embed)

        print("Sending followup webhook...")
        # await interaction.response.send(embed=embed)
        await interaction.followup.send(embed=embed)
        print("Sucessfully sent followup webhook")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Utility(client))
