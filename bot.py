import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.tree.sync()
    print(f"✅ Bot logged in as {client.user}")

# /join_project COMMAND
@client.tree.command(name="join_project", description="研究員とプロジェクト名のロールを付与します")
@app_commands.describe(user="対象ユーザー", project="プロジェクト名")
async def join_project(interaction: discord.Interaction, user: discord.Member, project: str):
    guild = interaction.guild

    async def get_or_create_role(name):
        role = discord.utils.get(guild.roles, name=name)
        if role is None:
            print(f"🛠 ロール『{name}』が存在しないため作成します")
            role = await guild.create_role(name=name)
            print(f"✅ 作成されたロール: {role.name}, ID: {role.id}")
        else:
            print(f"📌 既存のロール: {role.name}, ID: {role.id}")
        return role
    
    researcher_role = await get_or_create_role("研究員")
    project_role = await get_or_create_role(project)

    await user.add_roles(researcher_role, project_role)
    await interaction.response.send_message(f"{user.mention} にロール『研究員』と『{project}』を付与しました。", ephemeral=True)

# /set_leader COMMAND
@client.tree.command(name="set_leader", description="研究主任ロールを付与します")
@app_commands.describe(user="リーダーにしたいユーザー", project="担当プロジェクト名")
async def set_leader(interaction: discord.Interaction, user: discord.Member, project: str):
    guild = interaction.guild
    print(f"🛠 set_leader called with user={user}, project={project}")

    # Create leader role
    leader_role = discord.utils.get(guild.roles, name="研究主任")
    if not leader_role:
        print("🎩 '研究主任' ロールが存在しないので作成します")
        leader_role = await guild.create_role(name="研究主任")
    else:
        print("✅ '研究主任' ロールは既に存在します")
    
    # Get Project Role
    project_role = discord.utils.get(guild.roles, name=project)
    if not project_role:
        print(f"⚠ プロジェクト『{project}』ロールが見つかりません")
        await interaction.response.send_message(f"⚠ プロジェクト『{project}』のロールが存在しません。先に `/join_project` を実行してください。", ephemeral=True)
        return
    else:
        print(f"✅ プロジェクトロール『{project}』を見つけました")
    
    await user.add_roles(leader_role, project_role)
    print(f"🏅 {user} に『研究主任』と『{project}』ロールを付与しました")
    await interaction.response.send_message(f"{user.mention} をプロジェクト『{project}』の研究主任に任命しました。", ephemeral=True)

client.run(TOKEN)