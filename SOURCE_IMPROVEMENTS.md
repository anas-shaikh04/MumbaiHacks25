# Source Display & Explanation Improvements

## Summary of Changes

I've improved how credible sources are displayed and made explanations clearer and easier to understand.

---

## 🎯 What's New

### 1. **Top 5 Credible Sources with Official Names**

**Before:**
- Sources shown with just URLs
- Hard to identify which organization/website
- Generic display

**After:**
- **Shows official source names** (e.g., "BBC News", "Reuters", "Indian Express")
- **Top 5 most credible sources** for each claim (prioritized by credibility score)
- **Domain names mapped to friendly names** (e.g., "thehindu.com" → "The Hindu")
- **Credibility score prominently displayed** with green badge

**Source Name Mapping Includes:**
- **News Organizations:** BBC News, Reuters, The Hindu, Indian Express, The Guardian, CNN, NDTV, etc.
- **Fact-Checkers:** Alt News, BOOM Live, FactCheck.org, Snopes, AFP Fact Check, Vishvas News
- **Government Sources:** WHO, CDC, Ministry of Health & Family Welfare, PIB, Election Commission of India
- **Generic domains:** Automatically formatted as title case (e.g., "example.com" → "Example")

---

### 2. **Simpler, Easier-to-Understand Explanations**

**Before:**
- Technical language
- Complex reasoning
- Only explained why claim is true/false

**After:**
- **Simple, everyday language** (no jargon)
- **Maximum 2-3 sentences** for quick understanding
- **When claim is FALSE or MISLEADING, explanation includes what the TRUE facts are**
- Clear reasoning based on evidence

**Example:**

**Before (complex):**
```
The claim lacks corroboration from authoritative epidemiological sources and 
contradicts established scientific consensus per WHO guidelines.
```

**After (simple):**
```
This claim is false. According to WHO and CDC, 5G networks do not spread COVID-19. 
The true facts are that COVID-19 spreads through respiratory droplets when an 
infected person coughs or sneezes, not through radio waves.
```

---

### 3. **Enhanced UI Display**

**Source Display Now Shows:**
1. **Number badge** (1-5) in green circle
2. **Official source name** in bold (e.g., "BBC News")
3. **Source type badge** (FACTCHECK, NEWS, GOVT, etc.) in blue
4. **Credibility score** in green badge (e.g., "95/100")
5. **Article title**
6. **Clickable URL**

**Visual Hierarchy:**
```
┌─────────────────────────────────────────────┐
│ [1] BBC News [NEWS] [95/100]               │
│ Article Title Here                          │
│ https://bbc.com/news/article               │
└─────────────────────────────────────────────┘
```

---

## 📊 Technical Changes

### Backend Changes:

**1. agents/agent3_evidence.py:**
- Added `_get_source_name()` method to map 40+ domains to official names
- Enhanced evidence items with `domain` and `source_name` fields
- Returns top 5 sources (changed from 6)

**2. agents/agent4_verification.py:**
- Updated LLM prompt to generate simple, clear explanations
- Instructions to include TRUE facts when claim is false/misleading
- Improved evidence formatting to show source names prominently
- Changed from "rationale" to "explanation" (supports both for compatibility)

**3. agents/agent6_synthesis.py:**
- PDF receipts now show top 5 sources with source names
- Better formatting: "BBC News [NEWS] - Credibility: 95/100"

### Frontend Changes:

**1. VerificationPage.tsx:**
- Updated evidence section header to "Top 5 Credible Sources"
- Displays `source_name` prominently
- Shows domain as fallback if source_name not available

**2. VerificationPage.module.css:**
- New `.sourceName` style: bold, larger font (1rem)
- Credibility score now green badge (was gray)
- Better visual hierarchy in evidence cards

---

## 🔍 How It Works

### Source Name Resolution:

```
URL → Extract Domain → Check Mapping → Display Name

Example Flow:
https://www.thehindu.com/news/article → thehindu.com → "The Hindu"
https://www.bbc.co.uk/news/world → bbc.co.uk → "BBC News"
https://altnews.in/fact-check → altnews.in → "Alt News"
```

### Explanation Generation:

The LLM is now prompted to:
1. Use **simple language** (no jargon)
2. Keep it **concise** (2-3 sentences max)
3. **Include true facts** when claim is false/misleading
4. **Explain WHY** based on evidence

**Prompt Template:**
```
For the explanation:
- Use simple, easy-to-understand language (avoid technical jargon)
- Keep it concise (2-3 sentences maximum)
- If the claim is FALSE or MISLEADING, include what the TRUE facts are
- Explain WHY the claim is true/false/misleading based on evidence
```

---

## 📋 Supported Source Mappings

### News Organizations (85-100 credibility):
- BBC News, Reuters, Associated Press, NPR
- The Hindu, Indian Express, The Guardian
- New York Times, Washington Post, CNN
- NDTV, Livemint, The Quint

### Fact-Checkers (95-100 credibility):
- Alt News, BOOM Live, Vishvas News
- FactCheck.org, Snopes, AFP Fact Check

### Government & Health (100 credibility):
- World Health Organization (WHO)
- CDC, NIH
- Ministry of Health & Family Welfare
- Press Information Bureau (PIB)
- Election Commission of India

### Generic Domains:
- Automatically formatted as title case
- Example: "example.org" → "Example Org"

---

## ✅ User Benefits

1. **Easier to trust results** - See recognizable source names at a glance
2. **Faster understanding** - Simple explanations in plain language
3. **Better context** - Know the TRUE facts when claim is false
4. **Professional appearance** - Clean, organized source display
5. **Top credibility** - Only see the 5 most reliable sources

---

## 🧪 Testing

To test the improvements:

1. **Try a false claim:**
   ```
   "5G towers cause COVID-19"
   ```
   - Check that explanation includes TRUE facts about COVID spread
   - Verify top 5 sources show WHO, CDC, fact-checkers with official names

2. **Try a news URL:**
   ```
   Any article from BBC, Reuters, The Hindu, etc.
   ```
   - Check that source name displays correctly (e.g., "BBC News")

3. **Check PDF receipt:**
   - Verify top 5 sources listed with names and credibility scores

---

## 🔮 Future Enhancements

1. **More source mappings** - Add regional news sources (Bengali, Tamil, etc.)
2. **Source logos** - Display official logos next to source names
3. **Source bias indicators** - Show left/right/center political leaning
4. **Interactive source explorer** - Click to see full article context
5. **Multi-language explanations** - Generate simple explanations in Hindi/Marathi too

---

## 📞 Support

If sources aren't displaying correctly:
1. Check backend logs for evidence retrieval
2. Verify `source_name` field in API response
3. Ensure frontend receives evidence array
4. Check CSS styles are applied correctly

For adding new source mappings, edit `agents/agent3_evidence.py` → `_get_source_name()` method.
