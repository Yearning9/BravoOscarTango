import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from discord.ext.commands import MissingRequiredArgument


class Mod(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} message(s)', delete_after=10)
        print(f'{ctx.message.author} has used clear')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, *, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            try:
                muted = await ctx.guild.create_role(name="Muted", reason="Tried to mute someone but role wasn't found, so I created it")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted, send_messages=False)
            except discord.Forbidden:
                return await ctx.send("I don't have the permission to create a role to mute someone, please create a role named 'Muted' or give me the permission to do so")
            await user.add_roles(muted)
            await ctx.send(f"Muted {user.mention}. Reason for mute: {reason}")
        else:
            await user.add_roles(role)
            await ctx.send(f"Muted {user.mention}. Reason for mute: {reason}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name='Muted'))
        await ctx.send(f'{user.mention} has been unmuted')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        await user.ban(reason=reason)
        await ctx.send(f'Banned {user.mention}. Reason for ban: {reason}')
        print(f'{ctx.message.author} has used ban')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        await user.kick(reason=reason)
        await ctx.send(f'Kicked {user.mention}. Reason for kick: {reason}')
        print(f'{ctx.message.author} has used kick')

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the Manage Messages permission")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the Manage Messages permission")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the Manage Messages permission")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the Ban Members permission")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send('You need to specify a user to ban')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have the Kick Members permission")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send('You need to specify a user to kick')


def setup(client):
    client.add_cog(Mod(client))
