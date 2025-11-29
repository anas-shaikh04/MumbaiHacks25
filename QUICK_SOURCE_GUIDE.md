# Quick Reference: Source & Explanation Improvements

## ✨ What Changed?

### Sources Display
- **Now shows official names**: "BBC News", "Reuters", "The Hindu", etc. instead of just URLs
- **Top 5 most credible sources** per claim (was showing 6, with less clear info)
- **Prominent credibility scores** in green badges
- **Clear visual hierarchy**: Number → Source Name → Type → Score

### Explanations
- **Simple language** - No jargon, easy to understand
- **2-3 sentences max** - Quick to read
- **Includes TRUE facts** when claim is false/misleading
- **Clear reasoning** based on evidence

---

## 🎨 Visual Changes

### Evidence Card Layout:
```
┌───────────────────────────────────────────────────────────┐
│ Top 5 Credible Sources                                    │
├───────────────────────────────────────────────────────────┤
│ [1] BBC News          [NEWS]         [95/100]            │
│ Article Title Here About The Topic                       │
│ https://bbc.com/news/article-url                         │
├───────────────────────────────────────────────────────────┤
│ [2] Reuters           [NEWS]         [90/100]            │
│ Another Article Title                                     │
│ https://reuters.com/article                              │
└───────────────────────────────────────────────────────────┘
```

### Explanation Example:

**For FALSE claim: "5G towers cause COVID-19"**

**Old style:**
> The claim contradicts scientific consensus and lacks peer-reviewed evidence.

**New style:**
> This claim is false. According to WHO and CDC, 5G networks do not spread COVID-19. The virus spreads through respiratory droplets when an infected person coughs or sneezes, not through radio waves.

---

## 🏆 Recognized Sources (40+)

### Major News
- BBC News, Reuters, Associated Press, NPR
- The Hindu, Indian Express, The Guardian
- CNN, New York Times, NDTV, Livemint

### Fact-Checkers  
- Alt News, BOOM Live, Vishvas News
- FactCheck.org, Snopes, AFP Fact Check

### Official/Government
- WHO, CDC, Ministry of Health & Family Welfare
- PIB, Election Commission of India

### Auto-formatted
- Any other domain automatically formatted (e.g., "example.com" → "Example")

---

## 🚀 Testing It

1. **Enter any claim or upload content**
2. **Toggle "Show Evidence Sources"** 
3. **Look for:**
   - Official source names in bold
   - Green credibility badges
   - Simple, clear explanation
   - If false/misleading: TRUE facts included

---

## 📝 For Developers

### Backend Files Changed:
- `agents/agent3_evidence.py` - Added `_get_source_name()`, returns top 5
- `agents/agent4_verification.py` - New LLM prompt, simpler explanations
- `agents/agent6_synthesis.py` - PDF shows source names

### Frontend Files Changed:
- `frontend/src/pages/VerificationPage.tsx` - Display source names
- `frontend/src/pages/VerificationPage.module.css` - New `.sourceName` style
- `frontend/src/Types/types.ts` - Added `EvidenceSource` type

### API Response Structure:
```json
{
  "evidence": [
    {
      "url": "https://bbc.com/news/article",
      "title": "Article Title",
      "snippet": "Article content...",
      "source_type": "news",
      "credibility_score": 95,
      "domain": "bbc.com",
      "source_name": "BBC News"
    }
  ],
  "short_explain_en": "Simple 2-3 sentence explanation with true facts if claim is false"
}
```

---

## ⚙️ Configuration

To add more source mappings, edit `agents/agent3_evidence.py`:

```python
def _get_source_name(self, domain: str) -> str:
    source_map = {
        "yourdomain.com": "Your Official Name",
        # Add more mappings here
    }
```

---

That's it! Sources are now clearer and explanations are easier to understand. 🎉
