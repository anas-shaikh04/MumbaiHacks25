# Veritas Guardian - Frontend Setup Guide

## 🎯 Overview

The React frontend has been updated to include a comprehensive verification page inspired by the Streamlit UI, with all the multi-agent verification system functionality.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── VerificationPage.tsx      # NEW - Full multi-agent verification UI
│   │   ├── VerificationPage.module.css # Styling for verification page
│   │   ├── FileUploadPage.tsx        # Simple file upload detection
│   │   ├── MessageCheckPage.tsx      # Message verification
│   │   ├── QuizPage.tsx             # Fake news IQ quiz
│   │   └── ...
│   ├── components/
│   │   ├── Header.tsx               # Updated with new navigation
│   │   ├── Body.tsx                 # Simple text/URL detection
│   │   └── Loading.tsx
│   ├── services/
│   │   ├── api.ts                   # Axios instance
│   │   └── verifyNews.ts            # API calls
│   └── App.tsx                      # Updated routes
├── package.json
└── vite.config.ts
```

## 🆕 New Features

### Veritas Guardian Page (`/verify`)

The main verification page includes:

1. **Multiple Input Methods**
   - Text input with metadata (views, likes, shares, comments)
   - URL verification
   - Image upload with preview
   - Video upload with preview
   - PDF document upload

2. **Comprehensive Results Display**
   - Summary metrics (total claims, true/false/neutral counts, risk level)
   - Individual claim cards with:
     - Verdict (True/False/Neutral)
     - Confidence percentage
     - Multilingual explanations
     - Virality scores
     - Risk level badges
     - Evidence sources (collapsible)
     - PDF receipt download
     - Human review flags

3. **Visual Enhancements**
   - Animated transitions with Framer Motion
   - Color-coded verdicts
   - Risk badges (low/medium/high/critical)
   - Responsive design
   - Sticky sidebar with agent info

4. **Settings Panel**
   - Toggle evidence display
   - Toggle agent workflow
   - About section with agent descriptions

## 🚀 Installation & Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Backend URL

The frontend is configured to connect to `http://localhost:8000`. If your backend runs on a different port, update the API calls in `VerificationPage.tsx`.

### 3. Run Development Server

```bash
npm run dev
```

The frontend will start on `http://localhost:5173` (or another available port).

### 4. Build for Production

```bash
npm run build
```

Built files will be in the `dist/` directory.

## 🔗 API Integration

### Backend Endpoints Used

- `POST /api/verify/text` - Verify text content
- `POST /api/verify/url` - Verify URL content
- `POST /api/verify/image` - Verify image
- `POST /api/verify/video` - Verify video
- `POST /api/verify/pdf` - Verify PDF
- `GET /api/job/{job_id}/status` - Poll job status
- `GET /api/download/{claim_id}` - Download PDF receipt

### Job Polling

The frontend polls the backend every 2 seconds to check job status until completion or timeout (60 attempts = 2 minutes).

## 📱 Routes

- `/` - Simple text/URL detector (Body component)
- `/verify` - **Full Veritas Guardian verification system** (NEW)
- `/messages` - Message verification
- `/file` - File upload verification
- `/quiz` - Fake news IQ quiz

## 🎨 Styling

The verification page uses CSS Modules for scoped styling:
- `VerificationPage.module.css` - Main page styles
- Responsive design with mobile-first approach
- Color scheme matches the Streamlit UI
- Animations with Framer Motion

## 🔧 Configuration

### TypeScript

The project uses TypeScript with strict type checking. Types are defined in:
- `src/Types/types.ts` - Shared types

### Vite Configuration

- Path aliases configured in `vite.config.ts`:
  - `@components` → `src/components`
  - `@pages` → `src/pages`
  - `@services` → `src/services`
  - `@Types` → `src/Types`

## 🧪 Testing the Full System

### 1. Start Backend

```bash
cd ..  # Go to project root
python backend.py
```

Backend should be running on `http://localhost:8000`

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

Frontend should be running on `http://localhost:5173`

### 3. Test Verification

1. Navigate to `http://localhost:5173/verify`
2. Try any input method (text, URL, image, video, PDF)
3. Click verify and wait for results
4. Results will show:
   - Summary metrics
   - Individual claims with verdicts
   - Evidence sources
   - Risk assessment
   - PDF download options

## 🔄 Comparison: Streamlit vs React

| Feature | Streamlit (app.py) | React (VerificationPage) |
|---------|-------------------|--------------------------|
| Input Types | Tabs | Tabs |
| Text Input | ✅ | ✅ |
| URL Input | ✅ | ✅ |
| Image Upload | ✅ | ✅ with preview |
| Video Upload | ✅ | ✅ with preview |
| PDF Upload | ✅ | ✅ with file info |
| Metadata | Views, Likes, etc | ✅ Same |
| Results Display | Streamlit cards | Custom React cards |
| Evidence | Expander | Collapsible details |
| PDF Download | ✅ | ✅ |
| Agent Workflow | Optional | Optional |
| Risk Badges | ✅ | ✅ |
| Animations | Basic | Framer Motion |
| Responsive | ✅ | ✅ Enhanced |

## 📝 Key Differences

1. **Asynchronous Processing**: React uses job polling while Streamlit processes synchronously
2. **User Experience**: React provides smoother animations and transitions
3. **File Previews**: React shows image/video previews before verification
4. **Navigation**: React has client-side routing, Streamlit uses tabs
5. **Styling**: React uses CSS Modules, Streamlit uses custom CSS with unsafe_allow_html

## 🐛 Troubleshooting

### CORS Issues
If you see CORS errors, ensure the backend has proper CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### TypeScript Errors
Run `npm install` to ensure all dependencies are installed, including type definitions.

### Backend Connection
Check that the backend is running and accessible at `http://localhost:8000`

## 🚀 Deployment

### Frontend
- Build: `npm run build`
- Deploy `dist/` folder to any static hosting (Vercel, Netlify, etc.)

### Backend
- Ensure backend is running on a publicly accessible URL
- Update API URLs in frontend before building

## 📄 License

Same as the main Veritas Guardian project.
