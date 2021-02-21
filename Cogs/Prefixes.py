from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from discord.ext import commands

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class PrefixDatabase(db.Model):
    __tablename__ = 'prefixes'
    id = db.Column(db.Integer, primary_key=True)
    id_guild = db.Column(db.Text)
    prefix = db.Column(db.Text, default='.')

    def __init__(self, id_guild, prefix):
        self.id_guild = id_guild
        self.prefix = prefix



class Prefixes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['changeprefix'])
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str):
        if len(prefix) > 3:
            return await ctx.reply('Please use a prefix of max 3 characters', mention_author=False)
        elif db.session.query(PrefixDatabase).filter(PrefixDatabase.id_guild == str(ctx.guild.id)).count() != 0:
            guild_db = db.session.query(PrefixDatabase).filter_by(id_guild=str(ctx.guild.id)).first()
            guild_db.prefix = prefix
            db.session.commit()
            print(f'Guild {ctx.guild.id} changed prefix to {prefix}')
            return await ctx.reply(f'Prefix set to {prefix}', mention_author=False)
        else:
            data = PrefixDatabase(str(ctx.guild.id), prefix)
            db.session.add(data)
            db.session.commit()
            print(f"Couldn't find guild {ctx.guild.id} in database when changing prefix to {prefix} so i added it")
            return await ctx.reply(f'Prefix set to {prefix}', mention_author=False)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send('You have to be a server admin to change the prefix')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You have to specify a new prefix')


def setup(client):
    client.add_cog(Prefixes(client))


if __name__ == '__main__':
    app.run()
