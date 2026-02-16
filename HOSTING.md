# 🚀 24/7 INGYEN HOSTING ÚTMUTATÓ

## 🎯 Ajánlott platform: Render.com (INGYEN!)

### 1️⃣ Előkészítés GitHub-on

**A) Pushd fel a kódot GitHub-ra**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/FELHASZNALONEV/REPO_NEV.git
git push -u origin main
```

**B) Állítsd be a Secrets-t (TOKEN BIZTONSÁGA!)** 🔒
- Menj a GitHub repo-dba → Settings → Secrets and variables → Actions
- Add New repository secret
- Name: `DISCORD_TOKEN`
- Value: a Discord bot tokened

### 2️⃣ Render.com Beállítás

**A) Regisztráció**
1. Menj a [render.com](https://render.com)-ra
2. Regisztrálj GitHub fiókkal (INGYEN!)

**B) Web Service létrehozása**
1. Dashboard → **New +** → **Web Service**
2. Csatold össze a GitHub repo-dat
3. Beállítások:
   - **Name**: `discord-bot-neved`
   - **Region**: `Frankfurt (EU Central)`
   - **Branch**: `main`
   - **Root Directory**: hagyd üresen
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
   - **Instance Type**: **Free** 🎉

**C) Environment Variables (Környezeti változók)**
Kattints **Add Environment Variable**:
- **Key**: `DISCORD_TOKEN`
- **Value**: a Discord bot tokened (másold be!)

**OPCIONÁLIS** - Welcome/Leave csatornák:
- **Key**: `WELCOME_CHANNEL_ID`, **Value**: `1234567890`
- **Key**: `LEAVE_CHANNEL_ID`, **Value**: `1234567890`

**D) Deploy**
- Kattints **Create Web Service**
- Várj 2-3 percet
- ✅ A bot online!

### 3️⃣ Render.com INGYEN Tier Korlátok

⚠️ **FONTOS**:
- **750 óra/hó** ingyen futásidő (= 24/7 egy botnak)
- **Automatikus alvás** 15 perc inaktivitás után
- **Ébredés**: első Discord interakcióra (5-10 mp)

**Megoldás az alvásra**: Használj **UptimeRobot**-ot (lásd lent)

---

## 🔄 ALTERNATÍV PLATFORMOK

### 🅰️ Railway.app
- **500 óra/hó ingyen**
- Deploy: GitHub integration
- Környezeti változók ugyanúgy

### 🅱️ Fly.io
- **3 GB RAM ingyen**
- Kicsit bonyolultabb setup (Docker)
- De stabil 24/7

### 🅲 Replit (Egyszerű, DE korlátozott)
- Böngészős kódszerkesztő
- **Automatikusan alszik** ha nincs aktivitás
- Kezdőknek jó

---

## ⏰ ALVÁS MEGAKADÁLYOZÁSA (UptimeRobot)

**Ha Render.com-ot használsz:**

1. Regisztrálj: [uptimerobot.com](https://uptimerobot.com) (INGYEN)
2. Add Monitor → HTTP(s)
   - **Friendly Name**: Discord Bot
   - **URL**: `https://discord-bot-neved.onrender.com`
   - **Monitoring Interval**: 5 minutes
3. Kattints **Create Monitor**

Ez 5 percenként ping-eli a botot → **soha nem alszik el!** 🎉

---

## 🔧 Bot.py módosítás Render.com-hoz

Add hozzá a kód végéhez (opcionális, ha web endpoint kell):

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot fut!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Indítás előtt hívd meg
keep_alive()
bot.run(TOKEN)
```

Telepítsd Flask-et:
```bash
pip install flask
```

Add hozzá a `requirements.txt`-hez:
```
flask==3.0.0
```

---

## ✅ GYORS CHECKLIST

- [ ] GitHub repo létrehozva
- [ ] `.gitignore` feltöltve (TOKEN NEM látható!)
- [ ] `requirements.txt` feltöltve
- [ ] Render.com regisztráció
- [ ] Web Service létrehozva
- [ ] `DISCORD_TOKEN` environment variable beállítva
- [ ] Deploy sikeres
- [ ] Bot online Discord-on
- [ ] UptimeRobot beállítva (opcionális)

---

## 🆘 GYAKORI PROBLÉMÁK

**1. Bot nem indul el Render-en**
- Nézd meg a Logs fület
- Ellenőrizd hogy a `DISCORD_TOKEN` jól van beállítva

**2. "Module not found" hiba**
- Ellenőrizd a `requirements.txt`-et
- Build Command: `pip install -r requirements.txt`

**3. Bot offline Discord-on**
- Privileged Gateway Intents be van kapcsolva?
- Token helyes?

**4. Render.com "Sleeping"**
- UptimeRobot beállítása
- Vagy Flask webserver hozzáadása

---

## 💡 TIPP

Ha több botot akarsz futtatni ingyen:
1. Minden botnak külön GitHub repo
2. Minden botnak külön Render.com service
3. 750 óra/hó **service-enként!**

Kérdés? Írj! 🚀
