import discord, gnupg
from discord.ext import commands
from discord.ui import Modal, TextInput
from discord import app_commands, Embed, Interaction


class ContactModal(Modal, title="send an encrypted message to Ibn Aleem"):

    def __init__(self) -> None:
        self.encrypt_text = ""
        self.recipient_fingerprint = ""
    message = TextInput(
        style=discord.TextStyle.long,
        label="message",
        required=True,
        placeholder="Your message to Ibn Aleem"
    )

    fingerprint = TextInput(
        style=discord.TextStyle.short,
        label="your PGP fingerprint (optional)",
        required=False,
        placeholder="Ibn Aleem will not respond to your message without a PGP fingerprint. He will encrypt all communications to that fingerprint."
    )

    async def on_submit(self, interaction: Interaction):

        await interaction.response.defer(ephemeral=True)

        if self.fingerprint is not None:
            self.recipient_fingerprint = self.fingerprint

        self.encrypted_text = self.encrypt_text(message=self.message)
        embed = Embed(description=f"> ✅ your encrypted message to Ibn Aleem was successfully sent", color=0x0C0C0D)
        await interaction.followup.send(embed=embed, ephemeral=True)

    def encrypt_text(self, message: str) -> str:
        gpg = gnupg.GPG()
        result = gpg.encrypt(message, recipients="20247EC023F2769E66181C0F581B4A2A862BBADE")

        if result.ok:
            return str(result)
        else:
            print(f"Encryption failed: {result.status}")
            return "Encryption failed."


class Contact(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    @app_commands.command(name="contact-owner", description="contact my owner with a message")
    async def contact_owner(self, interaction: Interaction):
        
        contact_modal = ContactModal()
        await interaction.response.send_modal(ContactModal())
        embed = Embed(description=f"> {contact_modal.encrypted_text}", color=0x0C0C0D)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.add_field(name="fingerprint", value=contact_modal.recipient_fingerprint if contact_modal.recipient_fingerprint is not None else "no fingerprint provided")
        owner = self.client.fetch_user(1110526906106904626)
        await owner.send(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Contact(client))