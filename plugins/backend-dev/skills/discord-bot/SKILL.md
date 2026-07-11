---
name: discord-bot
description: Comprehensive workflow for Discord bot development with discord.py and interactions.py, focusing on cog architecture, slash commands, and event handling.
---

# Discord Bot Development Skill

This skill provides procedural guidance for developing feature-rich Discord bots with Python.

## Core Frameworks
- **discord.py**: Most established, feature-complete.
- **disnake/nextcord/py-cord**: Popular forks with additional slash command support.

## Design Pattern: Cog Architecture
Organize bot functionality into "Cogs" (classes) for better modularity:
```python
import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Ping the bot")
    async def ping(self, inter: discord.ApplicationCommandInteraction):
        await inter.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")

def setup(bot: commands.Bot):
    bot.add_cog(Utility(bot))
```

## Security & Best Practices
- **Token Safety**: Never hardcode tokens. Use `.env` files and `python-dotenv`.
- **Intents**: Explicitly define required `Intents` (e.g., `members`, `message_content`).
- **Error Handling**: Use `on_command_error` listeners to catch common issues.
- **Logging**: Set up structured logging to track bot events and errors.

## Application Commands (Slash Commands)
Prefer slash commands over prefix commands for better user experience:
- Use `app_commands` or framework-specific decorators.
- Manage synchronization with `bot.tree.sync()`.

## Essential Resources
- [Discord Developer Portal](https://discord.com/developers/applications)
- [discord.py Documentation](https://discordpy.readthedocs.io/)
