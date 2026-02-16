import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Környezeti változók betöltése
load_dotenv()

# Intents beállítása
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Adatok tárolása (warnings, tickets)
if not os.path.exists('data'):
    os.makedirs('data')

def load_data(filename):
    try:
        with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(filename, data):
    with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

warnings = load_data('warnings')
ticket_settings = load_data('ticket_settings')

# ============= MODERÁCIÓS PARANCSOK =============

@bot.tree.command(name="mute", description="Némítsd el a felhasználót")
@app_commands.describe(tag="A felhasználó akit némítani szeretnél", ido="Idő percben", ok="Indok")
@app_commands.checks.has_permissions(moderate_members=True)
async def mute(interaction: discord.Interaction, tag: discord.Member, ido: int, ok: str = "Nincs megadva"):
    await tag.timeout(discord.utils.utcnow() + discord.timedelta(minutes=ido), reason=ok)
    
    embed = discord.Embed(
        title="🔇 Felhasználó némítva",
        color=discord.Color.orange(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Felhasználó", value=tag.mention, inline=True)
    embed.add_field(name="Moderátor", value=interaction.user.mention, inline=True)
    embed.add_field(name="Időtartam", value=f"{ido} perc", inline=True)
    embed.add_field(name="Indok", value=ok, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unmute", description="Szüntesd meg a némítást")
@app_commands.describe(tag="A felhasználó akit feloldanál")
@app_commands.checks.has_permissions(moderate_members=True)
async def unmute(interaction: discord.Interaction, tag: discord.Member):
    await tag.timeout(None)
    await interaction.response.send_message(f"✅ {tag.mention} némítása feloldva!")

@bot.tree.command(name="ban", description="Tiltsd ki a felhasználót")
@app_commands.describe(tag="A felhasználó akit kitiltanál", ok="Indok")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, tag: discord.Member, ok: str = "Nincs megadva"):
    embed = discord.Embed(
        title="🔨 Ki lettél tiltva",
        description=f"Ki lettél tiltva a(z) **{interaction.guild.name}** szerverről.",
        color=discord.Color.red(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Indok", value=ok, inline=False)
    embed.add_field(name="Moderátor", value=interaction.user.name, inline=False)
    
    try:
        await tag.send(embed=embed)
    except:
        pass
    
    await interaction.guild.ban(tag, reason=ok)
    await interaction.response.send_message(f"✅ {tag.mention} ki lett tiltva! Indok: {ok}")

@bot.tree.command(name="kick", description="Rúgd ki a felhasználót")
@app_commands.describe(tag="A felhasználó akit kirúgnál", ok="Indok")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, tag: discord.Member, ok: str = "Nincs megadva"):
    embed = discord.Embed(
        title="👢 Ki lettél rúgva",
        description=f"Ki lettél rúgva a(z) **{interaction.guild.name}** szerverről.",
        color=discord.Color.orange(),
        timestamp=datetime.now()
    )
    embed.add_field(name="Indok", value=ok, inline=False)
    embed.add_field(name="Moderátor", value=interaction.user.name, inline=False)
    
    try:
        await tag.send(embed=embed)
    except:
        pass
    
    await interaction.guild.kick(tag, reason=ok)
    await interaction.response.send_message(f"✅ {tag.mention} ki lett rúgva! Indok: {ok}")

# ============= WARNING RENDSZER =============

@bot.tree.command(name="warn", description="Figyelmeztesd a felhasználót")
@app_commands.describe(tag="A felhasználó", ok="Figyelmeztetés oka")
@app_commands.checks.has_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, tag: discord.Member, ok: str):
    guild_id = str(interaction.guild.id)
    user_id = str(tag.id)
    
    if guild_id not in warnings:
        warnings[guild_id] = {}
    if user_id not in warnings[guild_id]:
        warnings[guild_id][user_id] = []
    
    warning_data = {
        "ok": ok,
        "moderator": interaction.user.name,
        "datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    warnings[guild_id][user_id].append(warning_data)
    save_data('warnings', warnings)
    
    warn_count = len(warnings[guild_id][user_id])
    
    # Privát üzenet a usernek
    dm_embed = discord.Embed(
        title="⚠️ Figyelmeztetés",
        description=f"Figyelmeztetést kaptál a(z) **{interaction.guild.name}** szerveren!",
        color=discord.Color.yellow(),
        timestamp=datetime.now()
    )
    dm_embed.add_field(name="Indok", value=ok, inline=False)
    dm_embed.add_field(name="Moderátor", value=interaction.user.name, inline=True)
    dm_embed.add_field(name="Összes figyelmeztetésed", value=str(warn_count), inline=True)
    
    try:
        await tag.send(embed=dm_embed)
        dm_sent = "✅ Privát üzenet elküldve"
    except:
        dm_sent = "❌ Nem sikerült privát üzenetet küldeni"
    
    # Válasz embed
    response_embed = discord.Embed(
        title="⚠️ Figyelmeztetés kiadva",
        color=discord.Color.yellow(),
        timestamp=datetime.now()
    )
    response_embed.add_field(name="Felhasználó", value=tag.mention, inline=True)
    response_embed.add_field(name="Moderátor", value=interaction.user.mention, inline=True)
    response_embed.add_field(name="Indok", value=ok, inline=False)
    response_embed.add_field(name="Összes figyelmeztetés", value=str(warn_count), inline=True)
    response_embed.set_footer(text=dm_sent)
    
    await interaction.response.send_message(embed=response_embed)

@bot.tree.command(name="warnings", description="Nézd meg a felhasználó figyelmeztetéseit")
@app_commands.describe(tag="A felhasználó")
async def warnings_check(interaction: discord.Interaction, tag: discord.Member):
    guild_id = str(interaction.guild.id)
    user_id = str(tag.id)
    
    if guild_id not in warnings or user_id not in warnings[guild_id]:
        await interaction.response.send_message(f"{tag.mention} még nem kapott figyelmeztetést!")
        return
    
    user_warnings = warnings[guild_id][user_id]
    
    embed = discord.Embed(
        title=f"⚠️ {tag.name} figyelmeztetései",
        color=discord.Color.yellow(),
        timestamp=datetime.now()
    )
    
    for i, warn in enumerate(user_warnings, 1):
        embed.add_field(
            name=f"#{i} - {warn['datum']}",
            value=f"**Indok:** {warn['ok']}\n**Moderátor:** {warn['moderator']}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# ============= ÜZENET KÜLDÉS /SAY =============

@bot.tree.command(name="say", description="Küldjön a bot egy üzenetet")
@app_commands.describe(uzenet="Az üzenet amit küldeni szeretnél")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, uzenet: str):
    await interaction.response.send_message("✅ Üzenet elküldve!", ephemeral=True)
    await interaction.channel.send(uzenet)

@bot.tree.command(name="embed", description="Küldj embed üzenetet")
@app_commands.describe(
    cim="Az embed címe",
    leiras="Az embed leírása",
    szin="Szín hex kódban (pl: ff0000)"
)
@app_commands.checks.has_permissions(manage_messages=True)
async def send_embed(interaction: discord.Interaction, cim: str, leiras: str, szin: str = "3498db"):
    try:
        color = discord.Color(int(szin, 16))
    except:
        color = discord.Color.blue()
    
    embed = discord.Embed(
        title=cim,
        description=leiras,
        color=color,
        timestamp=datetime.now()
    )
    embed.set_footer(text=f"Készítette: {interaction.user.name}", icon_url=interaction.user.avatar.url if interaction.user.avatar else None)
    
    await interaction.response.send_message("✅ Embed elküldve!", ephemeral=True)
    await interaction.channel.send(embed=embed)

# ============= TICKET RENDSZER =============

@bot.tree.command(name="ticket_setup", description="Állítsd be a ticket rendszert")
@app_commands.describe(
    kategoria="A kategória ahol a ticketek létrejönnek",
    support_rang="A rang aki hozzáfér a ticketekhez"
)
@app_commands.checks.has_permissions(administrator=True)
async def ticket_setup(interaction: discord.Interaction, kategoria: discord.CategoryChannel, support_rang: discord.Role):
    guild_id = str(interaction.guild.id)
    
    ticket_settings[guild_id] = {
        "kategoria_id": kategoria.id,
        "support_rang_id": support_rang.id
    }
    save_data('ticket_settings', ticket_settings)
    
    embed = discord.Embed(
        title="🎫 Ticket Rendszer",
        description="Kattints a gombra hogy ticket-et nyiss!",
        color=discord.Color.blue()
    )
    
    view = TicketButton()
    await interaction.response.send_message("✅ Ticket rendszer beállítva!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=view)

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎫 Ticket Nyitása", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild_id = str(interaction.guild.id)
        
        if guild_id not in ticket_settings:
            await interaction.response.send_message("❌ A ticket rendszer nincs beállítva!", ephemeral=True)
            return
        
        kategoria = interaction.guild.get_channel(ticket_settings[guild_id]["kategoria_id"])
        support_rang = interaction.guild.get_role(ticket_settings[guild_id]["support_rang_id"])
        
        # Ticket csatorna létrehozása
        ticket_channel = await kategoria.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            topic=f"Ticket {interaction.user.id}",
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                support_rang: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }
        )
        
        embed = discord.Embed(
            title="🎫 Ticket megnyitva",
            description=f"Üdv {interaction.user.mention}!\n\nA support csapat hamarosan segít neked.\nÍrd le a problémádat!",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        
        close_view = CloseTicketButton()
        await ticket_channel.send(f"{interaction.user.mention} {support_rang.mention}", embed=embed, view=close_view)
        await interaction.response.send_message(f"✅ Ticketed létrehozva: {ticket_channel.mention}", ephemeral=True)

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🔒 Ticket Bezárása", style=discord.ButtonStyle.red, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🔒 Ticket bezárva",
            description=f"Ticket bezárva {interaction.user.mention} által.",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        await interaction.response.send_message(embed=embed)
        await interaction.channel.delete(reason=f"Ticket bezárva {interaction.user.name} által")

# ============= WELCOME/LEAVE ÜZENETEK =============

# Környezeti változókból betöltés
WELCOME_CHANNEL_ID = os.getenv('WELCOME_CHANNEL_ID')
LEAVE_CHANNEL_ID = os.getenv('LEAVE_CHANNEL_ID')

# Ha van beállítva, akkor int-re konvertálás
if WELCOME_CHANNEL_ID:
    WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID)
if LEAVE_CHANNEL_ID:
    LEAVE_CHANNEL_ID = int(LEAVE_CHANNEL_ID)

@bot.event
async def on_member_join(member):
    if WELCOME_CHANNEL_ID:
        channel = bot.get_channel(WELCOME_CHANNEL_ID)
        embed = discord.Embed(
            title="👋 Üdvözlünk!",
            description=f"Üdv a szerveren, {member.mention}!\n\nMost már **{member.guild.member_count}** tagunk van!",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    if LEAVE_CHANNEL_ID:
        channel = bot.get_channel(LEAVE_CHANNEL_ID)
        embed = discord.Embed(
            title="👋 Viszlát!",
            description=f"**{member.name}** elhagyta a szervert.\n\nMost már csak **{member.guild.member_count}** tagunk van.",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await channel.send(embed=embed)

# ============= ÜZENETEKRE REAGÁLÁS =============

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # Reakciók bizonyos kulcsszavakra
    content_lower = message.content.lower()
    
    if "szia" in content_lower or "hello" in content_lower or "helló" in content_lower:
        await message.add_reaction("👋")
    
    if "köszönöm" in content_lower or "köszi" in content_lower or "thx" in content_lower:
        await message.add_reaction("❤️")
    
    await bot.process_commands(message)

# ============= BOT INDÍTÁS =============

@bot.event
async def on_ready():
    print(f'✅ {bot.user} bejelentkezett!')
    print(f'🔧 Szerverek: {len(bot.guilds)}')
    
    # Slash commandok szinkronizálása
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} parancs szinkronizálva!")
    except Exception as e:
        print(f"❌ Hiba a szinkronizálásban: {e}")
    
    # Ticket gombok újratöltése
    bot.add_view(TicketButton())
    bot.add_view(CloseTicketButton())

# Token környezeti változóból
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    print("❌ HIBA: DISCORD_TOKEN nincs beállítva!")
    print("Hozz létre egy .env fájlt és add hozzá: DISCORD_TOKEN=ide_a_tokened")
    exit(1)

bot.run(TOKEN)
