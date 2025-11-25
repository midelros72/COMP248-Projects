# Setup Guide - Health Research Agentic System

## ⚠️ Important: API Key Required

This system requires an **OpenAI API key** to function. Follow these steps to set it up:

### Step 1: Get Your OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Sign up or log in to your OpenAI account
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (it starts with `sk-`)

**Note**: You'll need to add credits to your OpenAI account. The `gpt-4o-mini` model is very affordable (~$0.15 per million tokens).

### Step 2: Configure Your Environment

1. **Copy the example environment file:**
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit `.env` file** and replace the placeholder with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here-do-not-share
   OPENAI_MODEL=gpt-4o-mini
   ```

3. **Keep your API key private!** Never commit the `.env` file to Git.

### Step 3: Initialize ChromaDB

The system uses ChromaDB for document storage. If you get database errors:

```powershell
# Delete corrupted database
Remove-Item -Recurse -Force "kb\chroma_store\*"

# Reload data (if you have health documents)
python kb\load_data.py
```

### Step 4: Run the Application

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start Streamlit
streamlit run ui.py
```

## 🔧 Troubleshooting

### Error: "Incorrect API key provided"
- **Problem**: The `.env` file still has the placeholder `YOUR OPEN API KEY`
- **Solution**: Replace it with your actual OpenAI API key from Step 1

### Error: "range start index 10 out of range"
- **Problem**: ChromaDB database is corrupted
- **Solution**: Delete `kb\chroma_store\*` and reinitialize (Step 3)

### Error: "No module named 'chromadb'"
- **Problem**: Dependencies not installed in virtual environment
- **Solution**: 
  ```powershell
  pip install -r requirements.txt
  ```

### Fallback Mode
If the CrewAI agents fail, the system automatically falls back to a simpler Python-only mode. This still requires:
- Valid OpenAI API key (for future LLM integration)
- Working ChromaDB database (for document retrieval)

## 📊 Testing Without API Key

For **demonstration purposes only**, you can run the test suite which uses mock data:

```powershell
python test_system.py
```

This validates the architecture without making real API calls.

## 💰 Cost Estimation

Using `gpt-4o-mini`:
- **Input**: $0.15 per 1M tokens
- **Output**: $0.60 per 1M tokens

Typical query costs **less than $0.01** per health question.

## 🎓 For Academic Use

If this is for a class project and you don't have an API key:
1. Run `test_system.py` to demonstrate the architecture
2. Show the code structure and design documents
3. Use the fallback mode which doesn't require LLM calls (but needs ChromaDB populated)
4. Consider using a free tier API key (OpenAI provides $5 free credit for new accounts)

## 🆘 Getting Help

If you're still having issues:
1. Check that `.env` file exists and has your real API key
2. Verify virtual environment is activated (you should see `(venv)` in terminal)
3. Ensure ChromaDB directory exists: `kb\chroma_store\`
4. Review terminal output for specific error messages
