# 🤖 Magyar Discord Bot

Teljes funkcionalitású Discord moderációs bot magyar nyelven.

## ✨ Funkciók

- **Moderáció**: mute, unmute, ban, kick
- **Figyelmeztetés rendszer**: warn, warnings (privát üzenetekkel)
- **Üzenet küldés**: /say (formázással), /embed
- **Ticket rendszer**: automatikus ticket létrehozás rangokkal
- **Welcome/Leave üzenetek**: embed formátumban
- **Üzenetekre reagálás**: automatikus reakciók kulcsszavakra

## 📋 Telepítés

1. **Clone-ozd a repo-t:**
```bash
git clone https://github.com/FELHASZNALONEV/REPO_NEV.git
cd REPO_NEV
```

2. **Telepítsd a csomagokat:**
```bash
pip install -r requirements.txt
```

3. **Állítsd be a tokent:**
```bash
cp .env.example .env
nano .env
```
Írd be a Discord bot tokenedet!

4. **Futtasd a botot:**
```bash
python bot.py
```

## 🔧 Discord Bot Beállítása

1. Menj a [Discord Developer Portal](https://discord.com/developers/applications)-ra
2. Hozz létre új alkalmazást
3. Bot fülön add hozzá a botot
4. **Privileged Gateway Intents** - kapcsold be:
   - MESSAGE CONTENT INTENT ✅
   - SERVER MEMBERS INTENT ✅
   - PRESENCE INTENT ✅
5. Másold ki a tokent és tedd a `.env` fájlba

## 🎮 Parancsok

### Moderáció
- `/mute @felhasználó [perc] [ok]` - Felhasználó némítása
- `/unmute @felhasználó` - Némítás feloldása
- `/ban @felhasználó [ok]` - Felhasználó kitiltása
- `/kick @felhasználó [ok]` - Felhasználó kirúgása

### Figyelmeztetések
- `/warn @felhasználó [ok]` - Figyelmeztetés kiadása (privát üzenettel)
- `/warnings @felhasználó` - Figyelmeztetések megtekintése

### Üzenetek
- `/say [üzenet]` - Bot üzenet küldése (formázással)
- `/embed [cím] [leírás] [szín]` - Embed üzenet

### Ticket rendszer
- `/ticket_setup [kategória] [support_rang]` - Ticket rendszer beállítása

## 🚀 24/7 Hosting (INGYEN)

Lásd a [HOSTING.md](HOSTING.md) fájlt!

## 📝 Licensz

MIT License
