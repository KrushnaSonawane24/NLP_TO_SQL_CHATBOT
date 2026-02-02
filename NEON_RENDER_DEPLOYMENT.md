# 🚀 Complete Deployment Guide - Neon + Render

## **Complete Step-by-Step Deployment for NL2SQL Chatbot**

---

## 📋 **Part 1: Neon Database Setup (Free Forever)**

### **Step 1.1: Create Neon Account**

1. Open browser and go to: **https://neon.tech**
2. Click **"Sign Up"** button (top right)
3. Choose **"Continue with GitHub"** (easiest option)
4. Authorize Neon to access your GitHub
5. You'll be logged in - **No credit card required!** ✅

---

### **Step 1.2: Create New Project**

1. You'll see Dashboard
2. Click **"Create a project"** (big green button)
3. Fill in details:
   - **Project name:** `nl2sql-database` (or any name you like)
   - **PostgreSQL version:** 16 (default is fine)
   - **Region:** Select closest to you
     - US East (Ohio) - for USA
     - Europe (Frankfurt) - for Europe
     - Asia Pacific (Singapore) - for Asia
4. Click **"Create project"**
5. Wait 10-15 seconds - database will be ready!

---

### **Step 1.3: Get Connection String**

1. After project is created, you'll see **"Connection Details"** page
2. Look for **"Connection string"** section
3. You'll see a dropdown - select **"Parameters"** or **"Connection string"**
4. Copy the connection string - it looks like:
   ```
   postgresql://neondb_owner:AbCd123XyZ@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
5. **SAVE THIS!** You'll need it in multiple places

**Format breakdown:**
```
postgresql://[user]:[password]@[host]/[database]?sslmode=require
              ^^^^   ^^^^^^^^    ^^^^
              user   password    hostname
```

---

### **Step 1.4: Load Sample Data into Neon**

1. **Open** `setup_database.py` in your code editor

2. **Find** line 18 (the `DB_CONFIG` section)

3. **Replace** with Neon connection details:
   ```python
   DB_CONFIG = {
       'host': 'ep-cool-name-123456.us-east-2.aws.neon.tech',  # From Neon URL
       'port': 5432,
       'user': 'neondb_owner',        # From Neon URL
       'password': 'AbCd123XyZ',      # From Neon URL
       'database': 'neondb'            # From Neon URL
   }
   ```

4. **Parse your connection string:**
   - If URL is: `postgresql://USER:PASS@HOST/DB?sslmode=require`
   - Extract: `USER`, `PASS`, `HOST`, `DB`

5. **Run the setup script:**
   ```bash
   python setup_database.py
   ```

6. **Expected output:**
   ```
   ============================================================
   🚀 PostgreSQL Database Setup
   ============================================================

   📦 Step 1: Creating database...
   ℹ️  Database 'neondb' already exists.

   🔌 Step 2: Connecting to database...
   ✅ Connected to 'neondb'

   📋 Step 3: Creating tables...
   ✅ Customers table created!
   ✅ Orders table created!

   👥 Step 4: Generating customer data...
   ✅ Generated 200 customers

   💾 Step 5: Inserting customers...
   ✅ Inserted 200 customers!

   📦 Step 6: Generating order data...
   ✅ Generated 200 orders

   💾 Step 7: Inserting orders...
   ✅ Inserted 200 orders!

   ✅ Step 8: Verifying data...
      Customers: 200
      Orders: 200

   ============================================================
   🎉 Database setup completed successfully!
   ============================================================
   ```

7. **If you get errors:**
   - Check your internet connection
   - Verify the connection details are correct
   - Make sure Faker is installed: `pip install Faker`

---

## 📋 **Part 2: Render Deployment**

### **Step 2.1: Create Render Account**

1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render
5. You're logged in! (Free tier - no credit card needed)

---

### **Step 2.2: Connect GitHub Repository**

1. In Render dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. You'll see "Create a new Web Service" page
4. Click **"Connect account"** next to GitHub (if not connected)
5. Authorize Render to access your repos
6. Find and select: **`nl2sql-postgres-chatbot`**
7. Click **"Connect"**

---

### **Step 2.3: Configure Web Service**

Now fill in the deployment form:

#### **Basic Settings:**

| Field | Value | Notes |
|-------|-------|-------|
| **Name** | `nl2sql-chatbot` | Your app URL will be: nl2sql-chatbot.onrender.com |
| **Region** | Oregon (US West) | Or closest to your Neon region |
| **Branch** | `main` | Default branch |
| **Root Directory** | *(leave blank)* | We're deploying from root |
| **Runtime** | `Python 3` | Auto-detected |

#### **Build & Deploy:**

| Field | Value |
|-------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app_langchain.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true` |

#### **Instance Type:**
- Select: **Free** (shows "$0/month")

---

### **Step 2.4: Add Environment Variables**

**IMPORTANT:** Click **"Advanced"** button to expand more options

You'll see **"Environment Variables"** section. Add these **one by one**:

#### **Click "Add Environment Variable" for each:**

**1. DATABASE_URL**
```
Key: DATABASE_URL
Value: postgresql://neondb_owner:AbCd123XyZ@ep-cool-name-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```
*(Use YOUR full Neon connection string)*

**2. PROVIDER**
```
Key: PROVIDER
Value: gemini
```
*(or `groq` if using Groq)*

**3. GEMINI_API_KEY**
```
Key: GEMINI_API_KEY
Value: AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXX
```
*(Your actual Gemini API key from Google AI Studio)*

**4. MODEL**
```
Key: MODEL
Value: gemini-1.5-flash
```

**5. MAX_SQL_STATEMENTS**
```
Key: MAX_SQL_STATEMENTS
Value: 4
```

**6. STATEMENT_TIMEOUT_MS**
```
Key: STATEMENT_TIMEOUT_MS
Value: 8000
```

**7. MAX_ROWS**
```
Key: MAX_ROWS
Value: 200
```

**8. MEMORY_USER_TURNS**
```
Key: MEMORY_USER_TURNS
Value: 10
```

---

### **Step 2.5: Deploy!**

1. Scroll to bottom
2. Click **"Create Web Service"** (big button)
3. Render will start building your app
4. You'll see **"Build Logs"** - watch them scroll
5. Build takes **5-8 minutes**

**Build Process:**
```
Cloning repository...
Installing Python...
Running: pip install -r requirements.txt
Installing dependencies... (this takes longest)
Build successful!
Starting application...
Streamlit app running on port 10000
Deploy successful!
```

6. Once you see **"Deploy successful"**, your app is LIVE! ✅

---

### **Step 2.6: Access Your App**

1. At the top of Render dashboard, you'll see your app URL:
   ```
   https://nl2sql-chatbot.onrender.com
   ```
2. Click it to open your app
3. **First load takes 20-30 seconds** (cold start)
4. You should see your chatbot interface!

---

## 🧪 **Part 3: Test Your Deployment**

### **Test Queries:**

Try these in your deployed app:

1. **Simple query:**
   ```
   Show me all customers
   ```
   Expected: Table with 200 customers

2. **Aggregation:**
   ```
   How many orders do we have?
   ```
   Expected: "200 orders"

3. **Join query:**
   ```
   Show top 10 customers by total sales
   ```
   Expected: Table with customer names and sales

4. **Filter:**
   ```
   Show married customers
   ```
   Expected: Filtered customer list

---

## 🐛 **Troubleshooting**

### **Problem: Build Failed**

**Error:** `ERROR: Could not find a version that satisfies...`

**Fix:**
1. Check `requirements.txt` - all packages should have versions
2. Make sure Python version is compatible (3.11+)

---

### **Problem: Database Connection Error**

**Error:** `could not connect to server` or `connection refused`

**Fix:**
1. Go to Render → Your Service → Environment
2. Double-check `DATABASE_URL` matches EXACTLY your Neon URL
3. Make sure you copied the FULL URL including `?sslmode=require`

---

### **Problem: App Shows Error Page**

**Error:** `ModuleNotFoundError` or import errors

**Fix:**
1. Check Render logs (click "Logs" tab)
2. Missing package? Add to `requirements.txt`
3. Redeploy: click "Manual Deploy" → "Deploy latest commit"

---

### **Problem: App Works But No Data**

**Error:** Queries return empty results

**Fix:**
1. Your Neon database is empty!
2. Run `setup_database.py` locally with Neon credentials
3. Verify data:
   ```bash
   psql "YOUR_NEON_URL"
   SELECT COUNT(*) FROM customers;
   ```

---

### **Problem: API Key Error**

**Error:** `API key not configured` or LLM errors

**Fix:**
1. Render → Environment → Check `GEMINI_API_KEY`
2. Make sure no extra spaces
3. Regenerate key from Google AI Studio if needed

---

## ⚡ **Important Notes**

### **Free Tier Limitations:**

**Render Free:**
- ✅ Perfect for demos and testing
- ⚠️ Sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep = ~30 seconds to wake up
- ✅ 750 hours/month (enough for multiple projects)

**Neon Free:**
- ✅ 0.5 GB storage (plenty for this project)
- ✅ Unlimited compute hours
- ✅ 1 project
- ✅ Perfect for learning/demos

### **Keeping App Awake (Optional):**

Use a free service like UptimeRobot:
1. Go to: https://uptimerobot.com
2. Add monitor for your Render URL
3. Ping every 5 minutes
4. App stays awake!

---

## 📝 **Quick Reference**

### **Your URLs:**

```
Neon Database: https://console.neon.tech
Render Dashboard: https://dashboard.render.com
Your Live App: https://nl2sql-chatbot.onrender.com
```

### **Connection String Format:**

```
postgresql://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require
```

---

## ✅ **Final Checklist**

Before you say "deployment successful":

- [ ] Neon project created
- [ ] Connection string saved
- [ ] `setup_database.py` run successfully against Neon
- [ ] 200 customers and 200 orders in Neon database
- [ ] Render web service created
- [ ] All 8 environment variables added in Render
- [ ] Build completed successfully (green checkmark)
- [ ] App accessible via Render URL
- [ ] Test query works (e.g., "show all customers")
- [ ] SQL generates correctly
- [ ] Results display properly

---

## 🎉 **Success!**

Your NL2SQL chatbot is now live on the internet! 🌐

**Share your app:** Just send the Render URL to anyone!

**Deployment time:** ~15 minutes total
- Neon setup: 5 min
- Render deployment: 10 min

---

**Need help?** Check logs in Render dashboard or Neon console.

Happy deploying! 🚀
