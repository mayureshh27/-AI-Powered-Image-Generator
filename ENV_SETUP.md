# AI Image Generator - Environment Setup

## Quick Start

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` and add your Groq API key:**
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

3. **Get your Groq API key:**
   - Go to https://console.groq.com
   - Sign up (free)
   - Create an API key
   - Copy and paste it into `.env`

4. **Run the application:**
   ```bash
   source venv/Scripts/activate
   streamlit run app_article.py
   ```

## Important Notes

- **Never commit `.env`** - It contains your API key
- `.env.example` is safe to commit (template only)
- The `.env` file is already in `.gitignore`

## For Submission

When submitting your code, make sure to:
1. **Do NOT include your `.env` file**
2. Include `.env.example` instead
3. In your Word document, mention that users need to create `.env` with their own API key
