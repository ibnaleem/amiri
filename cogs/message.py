import ollama, os
from icecream import ic
from discord import Message, DMChannel
from discord.ext import commands


class MessageCog(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        super().__init__()
        self.client = client
        self.chat_log = []

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:

        if message.author.id == self.client.user.id:
            return

        if isinstance(message.channel, DMChannel):
            print("Message received: initiated typing...")
            await message.channel.typing()

            if message.attachments:
                for attachment in message.attachments:
                    print("Checking if attachment is image...")
                    if os.path.splitext(attachment.filename)[1] in [
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".gif",
                    ]:  
                        print("Attachment is an image! Attempting to save...")
                        await attachment.save(attachment.filename)
                        print("Saved attachment!")
                        print("Generating response...")
                        response = ollama.generate(
                            model="llava",
                            prompt=message.content,
                            images=[attachment.filename],
                            stream=False,
                        )

                        print("Sending response...")
                        await message.channel.send(response["response"])
                        print("Response sent!\nDeleting saved image...")
                        os.remove(attachment.filename)
                        print("Image deleted!")

            else:
                num = 1
                while num != 0:
                    print("Appending message to chat_log array...")
                    self.chat_log.append({"role": "user", "content": message.content})
                    print("Generating response...")
                    chat_call = ollama.chat(model="llama3", messages=self.chat_log)
                    response = chat_call["message"]["content"]
                    print("Appending response to chat_log array...")
                    self.chat_log.append({"role": "assistant", "content": response})
                    print("Sending response...")
                    await message.channel.send(response)
                    print("Response sent!")
                    num -= 1
                    if num == 0:
                        break
        else:
            pass


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MessageCog(client))
