import hashlib
from typing import Optional
from discord.ext import commands
from discord.app_commands import Choice
from discord import app_commands, Attachment, Embed, Interaction


class Hash(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client

    @app_commands.command(name="hash", description="Generate a hash using various hash functions")
    @app_commands.describe(function="hash function", text="the text you want to generate a hash of", file="the file you want to generate a hash of")
    @app_commands.choices(
        function=[
            Choice(name="md5", value=1),
            Choice(name="sha1", value=2),
            Choice(name="sha3", value=3),
            Choice(name="sha256", value=4),
            Choice(name="sha384", value=5),
            Choice(name="sha512", value=6),
        ]
    )
    async def generate_hash(self, interaction: Interaction, function: Choice[int], text: Optional[str] = None, file: Optional[Attachment] = None):
        global data_2
        global hash_result2  
        if text and file:
            data = text.encode("utf-8")
            data_2 = await file.read()
        elif text and not file:
            data = text.encode("utf-8")
            data_2 = None
            hash_result2 = None
        elif file and not text:
            data = await file.read()
            data_2 = None
            hash_result2 = None
        else:
            embed = Embed(description="> ❌  **provide either text or a file to hash**", color=0x0C0C0D)
            await interaction.response.send_message(embed=embed)
            return

        if function.name == "md5":
            if data_2 is None:  
                hash_result = hashlib.md5(data).hexdigest()
            else:
                hash_result = hashlib.md5(data).hexdigest()
                hash_result2 = hashlib.md5(data_2).hexdigest() 
        elif function.name == "sha1":
            if data_2 is None:
                hash_result = hashlib.sha1(data).hexdigest()
            else:
                hash_result = hashlib.sha1(data).hexdigest()
                hash_result2 = hashlib.sha1(data_2).hexdigest()
        elif function.name == "sha3":
            if data_2 is None:
                hash_result = hashlib.sha3_256(data).hexdigest()
            else:
                hash_result = hashlib.sha3_256(data).hexdigest()
                hash_result2 = hashlib.sha3_256(data_2).hexdigest()
        elif function.name == "sha256":
            if data_2 is None:
                hash_result = hashlib.sha256(data).hexdigest()
            else:
                hash_result = hashlib.sha256(data).hexdigest()
                hash_result2 = hashlib.sha256(data_2).hexdigest()
        elif function.name == "sha384":
            if data_2 is None:
                hash_result = hashlib.sha384(data).hexdigest()
            else:
                hash_result = hashlib.sha384(data).hexdigest()
                hash_result2 = hashlib.sha384(data_2).hexdigest()
        elif function.name == "sha512":
            if data_2 is None:
                hash_result = hashlib.sha512(data).hexdigest()
            else:
                hash_result = hashlib.sha512(data).hexdigest()
                hash_result2 = hashlib.sha512(data_2).hexdigest()

        if hash_result2 is None:
            await interaction.response.send_message(hash_result)
        else:
            await interaction.response.send_message(f"**text hash:** ```{hash_result}```\n**{file.filename} hash:** ```{hash_result2}```")

    @app_commands.command(name="checksum", description="Determine if a given checksum matches the hash of a file")
    @app_commands.describe(function="hash function", file="the file you want to check", checksum="the checksum you want to check")
    @app_commands.choices(
        function=[
            Choice(name="md5", value=1),
            Choice(name="sha1", value=2),
            Choice(name="sha3", value=3),
            Choice(name="sha256", value=4),
            Choice(name="sha384", value=5),
            Choice(name="sha512", value=6),
        ]
    )

    async def checksum(self, interaction: Interaction, function: Choice[int], file: Attachment, checksum: str):

        data = await file.read()

        if function.name == "md5":
            hash_result = hashlib.md5(data).hexdigest()
        elif function.name == "sha1":
            hash_result = hashlib.sha1(data).hexdigest()
        elif function.name == "sha3":
            hash_result = hashlib.sha3_256(data).hexdigest()
        elif function.name == "sha256":
            hash_result = hashlib.sha256(data).hexdigest()
        elif function.name == "sha384":
            hash_result = hashlib.sha384(data).hexdigest()
        elif function.name == "sha512":
            hash_result = hashlib.sha512(data).hexdigest()

        if hash_result == checksum:
            embed = Embed(description="> ✅  **the checksum matches the hash of the file**", color=0x0C0C0D)
            await interaction.response.send_message(embed=embed)
        else:
            embed = Embed(description="> ❌  **the checksum does not match the hash of the file**", color=0x0C0C0D)
            embed.add_field(name="actual file checksum", value=f"`{hash_result}`")
            embed.add_field(name="incorrect file checksum", value=f"`{checksum}`")
            await interaction.response.send_message(embed=embed)

async def setup(client: commands.Bot) -> None:
    await client.add_cog(Hash(client))
