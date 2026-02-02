# Render Deployment Guide - NL2SQL LangChain Chatbot

## 🚀 Deploy to Render - Step by Step

### **Prerequisites:**

1. ✅ GitHub account with code pushed
2. ✅ Render account (free) - https://render.com
3. ✅ Cloud PostgreSQL database (see options below)
4. ✅ Gemini or Groq API key

---

## **Step 1: Setup Cloud Database (REQUIRED)**

Your local PostgreSQL won't work on Render. Use a cloud database:

### **Option A: Neon (Recommended - Free Forever)**

1. Go to: **https://neon.tech**
2. Click "Sign up" (use GitHub)
3. Create new project:
   - Name: `nl2sql-db`
   - Region: Choose closest to you
4. Copy connection string:
   ```
   postgresql://user:password@ep-xxx-xxx.neon.tech/neondb?sslmode=require
   ```
5. **Load your data:**
   ```bash
   # Edit setup_database.py and change DB_CONFIG to Neon URL
   python setup_database.py
   ```

### **Option B: Supabase (Free)**

1. Go to: **https://supabase.com**
2. New project → Copy "Connection pooling" URL
3. Use Transaction mode

### **Option C: ElephantSQL (Free 20MB)**

1. Go to: **https://elephantsql.com**
2. Create "Tiny Turtle" free instance
3. Copy URL

---

## **Step 2: Deploy on Render**

### **2.1: Create Web Service**

1. Go to: **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository:
   - Click "Connect account" if needed
   - Select: `KrushnaSonawane24/nl2sql-postgres-chatbot`

### **2.2: Configure Service**

Fill in the form:

**Basic Settings:**
- **Name:** `nl2sql-langchain` (or any name)
- **Region:** Oregon (US West) or closest to you
- **Branch:** `main`
- **Root Directory:** Leave blank (or `.`)
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command:**
  ```bash
  streamlit run app_langchain.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true
  ```

**Instance Type:**
- Select: **Free** ($0/month)

### **2.3: Add Environment Variables**

Click **"Advanced"** → **"Add Environment Variable"**

Add these variables:

| Key | Value | Example |
|-----|-------|---------|
| `DATABASE_URL` | Your cloud DB URL | `postgresql://user:pass@ep-xxx.neon.tech/db` |
| `PROVIDER` | `gemini` or `groq` | `gemini` |
| `GEMINI_API_KEY` | Your Gemini API key | `AIzaSy...` |
| `MODEL` | Model name | `gemini-1.5-flash` |
| `MAX_SQL_STATEMENTS` | `4` | `4` |
| `STATEMENT_TIMEOUT_MS` | `8000` | `8000` |
| `MAX_ROWS` | `200` | `200` |
| `MEMORY_USER_TURNS` | `10` | `10` |

**If using Groq:**
| Key | Value |
|-----|-------|
| `PROVIDER` | `groq` |
| `GROQ_API_KEY` | Your Groq key |
| `MODEL` | `llama-3.3-70b-versatile` |

---

## **Step 3: Deploy!**

1. Click **"Create Web Service"** at bottom
2. Wait 5-10 minutes for build
3. Watch logs for any errors
4. Once deployed, you'll get a URL: `https://nl2sql-langchain.onrender.com`

---

## **Step 4: Test Your Deployment**

1. Open the Render URL
2. Try a query: "Show me all customers"
3. Check if SQL generates and executes

---

## 🐛 **Troubleshooting**

### **Build Failed:**
- Check `requirements.txt` has all dependencies
- Check Python version is 3.11+

### **Database Connection Error:**
- Verify `DATABASE_URL` in environment variables
- Make sure cloud database is running
- Check if database has tables (run `setup_database.py` against cloud DB)

### **LLM API Error:**
- Verify API key is correct
- Check provider name matches (`gemini` or `groq`)
- Ensure you have API credits

### **App Crashes:**
- Check Render logs for errors
- Verify all environment variables are set
- Make sure `Procfile` exists

---

## 📊 **Load Data to Cloud Database**

After creating cloud database, load sample data:

1. **Edit `setup_database.py`:**
   ```python
   DB_CONFIG = {
       'host': 'ep-xxx-xxx.neon.tech',  # From Neon URL
       'port': 5432,
       'user': 'your_user',
       'password': 'your_password',
       'database': 'neondb'
   }
   ```

2. **Run setup:**
   ```bash
   python setup_database.py
   ```

3. **Verify:**
   ```bash
   psql "your_cloud_database_url"
   SELECT COUNT(*) FROM customers;
   SELECT COUNT(*) FROM orders;
   ```

---

## 🚀 **Free Tier Limits**

**Render Free:**
- Spins down after 15 min inactivity
- First request after sleep takes ~30 seconds
- 750 hours/month (enough for demo)

**Neon Free:**
- 0.5 GB storage
- Unlimited compute hours
- Perfect for demo/testing

---

## 🎯 **Production Upgrades (Optional)**

For 24/7 uptime without sleep:
- Render: $7/month (Starter plan)
- Neon: Free tier is enough
- Or use Railway, Fly.io (also have free tiers)

---

## ✅ **Success Checklist**

- [ ] Cloud database created (Neon/Supabase)
- [ ] Sample data loaded (customers, orders)
- [ ] Render web service created
- [ ] Environment variables added
- [ ] Build successful
- [ ] App accessible via Render URL
- [ ] Test queries working

---

**Your app will be live at:** `https://your-app-name.onrender.com`

Deployment time: ~10 minutes 🚀
