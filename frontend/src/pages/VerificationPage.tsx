import { useState, useRef } from "react";
import { motion } from "framer-motion";
import styles from "./VerificationPage.module.css";
import Loading from "@components/Loading";
import FNDB from "../assets/FNDbackground.png";

interface VerificationResult {
  summary: {
    total_claims: number;
    true_count: number;
    false_count: number;
    neutral_count: number;
    highest_risk: string;
  };
  language_support: string;
  language_name: string;
  primary_language: string;
  visual_forensics?: {
    suspicion_level: string;
  };
  results: Array<{
    claim_id: string;
    claim: string;
    user_label: string;
    confidence: number;
    short_explain_local: string;
    short_explain_en: string;
    virality_score: number;
    combined_risk_level: string;
    evidence?: Array<{
      source_type: string;
      title: string;
      credibility_score: number;
      url: string;
    }>;
    receipt_pdf_path?: string;
    needs_human_review?: boolean;
  }>;
}

const VerificationPage = () => {
  const [textInput, setTextInput] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [showEvidence, setShowEvidence] = useState(true);
  const [showWorkflow, setShowWorkflow] = useState(false);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleVerifyText = async () => {
    if (!textInput.trim()) {
      alert("Please enter some text to verify");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/verify/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: textInput,
        }),
      });

      const data = await response.json();
      // Poll for job status
      await pollJobStatus(data.job_id);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to verify text");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyUrl = async (url: string) => {
    if (!url.trim()) {
      alert("Please enter a URL");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("url", url);

      const response = await fetch("http://localhost:8000/api/verify/url", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      await pollJobStatus(data.job_id);
    } catch (error) {
      console.error("Error:", error);
      alert("Failed to verify URL");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyFile = async (type: "image" | "video" | "pdf") => {
    if (!file) {
      alert("Please upload a file");
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`http://localhost:8000/api/verify/${type}`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      await pollJobStatus(data.job_id);
    } catch (error) {
      console.error("Error:", error);
      alert(`Failed to verify ${type}`);
    } finally {
      setLoading(false);
    }
  };

  const handleVerify = async () => {
    // Determine what to verify based on input
    if (textInput.trim()) {
      // Check if it's a URL
      if (textInput.trim().match(/^https?:\/\//)) {
        await handleVerifyUrl(textInput.trim());
      } else {
        await handleVerifyText();
      }
    } else if (file) {
      // Determine file type
      if (file.type.startsWith("image/")) {
        await handleVerifyFile("image");
      } else if (file.type.startsWith("video/")) {
        await handleVerifyFile("video");
      } else if (file.type === "application/pdf") {
        await handleVerifyFile("pdf");
      }
    } else {
      alert("Please enter text/URL or upload a file");
    }
  };

  const pollJobStatus = async (jobId: string) => {
    const maxAttempts = 60;
    let attempts = 0;

    const poll = async () => {
      try {
        const response = await fetch(
          `http://localhost:8000/api/job/${jobId}/status`
        );
        const data = await response.json();

        if (data.status === "completed") {
          setResult(data.result);
          return true;
        } else if (data.status === "failed") {
          alert("Verification failed: " + data.error);
          return true;
        } else if (attempts >= maxAttempts) {
          alert("Verification timed out");
          return true;
        }

        attempts++;
        await new Promise((resolve) => setTimeout(resolve, 2000));
        return poll();
      } catch (error) {
        console.error("Polling error:", error);
        return true;
      }
    };

    await poll();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
  };

  const clearResults = () => {
    setResult(null);
    setTextInput("");
    setUrlInput("");
    setFile(null);
  };

  const getRiskColor = (risk: string) => {
    const colors = {
      low: "#28a745",
      medium: "#ffc107",
      high: "#fd7e14",
      critical: "#dc3545",
    };
    return colors[risk as keyof typeof colors] || "#6c757d";
  };

  const getRiskEmoji = (risk: string) => {
    const emojis = {
      low: "🟢",
      medium: "🟡",
      high: "🟠",
      critical: "🔴",
    };
    return emojis[risk as keyof typeof emojis] || "⚪";
  };

  return (
    <div className={styles.pageWrap}>
      <img src={FNDB} alt="background" className={styles.pageBg} />

      <div className={styles.container}>
        {/* Main Title */}
        <motion.div
          className={styles.pageHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className={styles.mainTitle}>VERITAS GUARDIAN</h1>
          <p className={styles.subtitle}>
            Multi-Agent Misinformation Verification System
          </p>
        </motion.div>

        {/* Settings Bar */}
        <div className={styles.settingsBar}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={showWorkflow}
              onChange={(e) => setShowWorkflow(e.target.checked)}
            />
            <span>Show Agent Workflow</span>
          </label>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={showEvidence}
              onChange={(e) => setShowEvidence(e.target.checked)}
            />
            <span>Show All Evidence</span>
          </label>
        </div>

        {/* Main Content */}
        <div className={styles.mainContent}>
          {/* Input Section */}
          <div className={styles.inputContainer}>
            <h2 className={styles.sectionTitle}>Enter Content to Verify</h2>
            <p className={styles.sectionDesc}>
              Paste text, URL, or upload an image/video/document for analysis
            </p>

            {/* Text/URL Input */}
            <div className={styles.textInputArea}>
              <label className={styles.inputLabel}>Text or URL</label>
              <textarea
                className={styles.textarea}
                placeholder="Paste any text, WhatsApp message, tweet, article URL, or YouTube link..."
                value={textInput}
                onChange={(e) => setTextInput(e.target.value)}
                rows={6}
              />
            </div>

            {/* File Upload Area */}
            <div className={styles.fileUploadArea}>
              <label className={styles.inputLabel}>Upload File</label>
              <div
                className={`${styles.dropzone} ${
                  file ? styles.hasFile : ""
                }`}
                onDragOver={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.add(styles.dragover);
                }}
                onDragLeave={(e) => {
                  e.currentTarget.classList.remove(styles.dragover);
                }}
                onDrop={(e) => {
                  e.preventDefault();
                  e.currentTarget.classList.remove(styles.dragover);
                  const droppedFile = e.dataTransfer.files[0];
                  if (droppedFile) {
                    setFile(droppedFile);
                  }
                }}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/*,video/*,.pdf"
                  onChange={handleFileChange}
                  style={{ display: "none" }}
                />
                {!file ? (
                  <>
                    <div className={styles.uploadIcon}>
                      <svg
                        width="48"
                        height="48"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="17 8 12 3 7 8" />
                        <line x1="12" y1="3" x2="12" y2="15" />
                      </svg>
                    </div>
                    <p className={styles.dropzoneText}>
                      <strong>Click to upload</strong> or drag and drop
                    </p>
                    <p className={styles.dropzoneHint}>
                      Images, Videos, or PDF documents
                    </p>
                  </>
                ) : (
                  <div className={styles.filePreviewContainer}>
                    {file.type.startsWith("image/") && (
                      <img
                        src={URL.createObjectURL(file)}
                        alt="Preview"
                        className={styles.imagePreview}
                      />
                    )}
                    {file.type.startsWith("video/") && (
                      <video
                        src={URL.createObjectURL(file)}
                        controls
                        className={styles.videoPreview}
                      />
                    )}
                    {file.type === "application/pdf" && (
                      <div className={styles.pdfInfo}>
                        <div className={styles.pdfIcon}>📄</div>
                        <div className={styles.pdfDetails}>
                          <div className={styles.pdfName}>{file.name}</div>
                          <div className={styles.pdfSize}>
                            {Math.round(file.size / 1024)} KB
                          </div>
                        </div>
                      </div>
                    )}
                    <button
                      className={styles.removeFileBtn}
                      onClick={(e) => {
                        e.stopPropagation();
                        setFile(null);
                      }}
                    >
                      Remove
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Verify Button */}
            <button
              className={styles.verifyBtn}
              onClick={handleVerify}
              disabled={loading || (!textInput && !file)}
            >
              {loading ? <Loading /> : "Verify Content"}
            </button>
          </div>

          {/* Results Section */}
          {result && (
            <motion.div
              className={styles.results}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <h2 className={styles.resultsTitle}>Verification Results</h2>

              {/* Summary Metrics */}
              <div className={styles.summaryMetrics}>
                <div className={styles.metric}>
                  <div className={styles.metricValue}>
                    {result.summary.total_claims}
                  </div>
                  <div className={styles.metricLabel}>Total Claims</div>
                </div>
                <div className={styles.metric}>
                  <div className={styles.metricValue} style={{ color: "#28a745" }}>
                    {result.summary.true_count}
                  </div>
                  <div className={styles.metricLabel}>True</div>
                </div>
                <div className={styles.metric}>
                  <div className={styles.metricValue} style={{ color: "#dc3545" }}>
                    {result.summary.false_count}
                  </div>
                  <div className={styles.metricLabel}>False</div>
                </div>
                <div className={styles.metric}>
                  <div className={styles.metricValue} style={{ color: "#ffc107" }}>
                    {result.summary.neutral_count}
                  </div>
                  <div className={styles.metricLabel}>Neutral</div>
                </div>
                <div className={styles.metric}>
                  <div
                    className={styles.metricValue}
                    style={{ color: getRiskColor(result.summary.highest_risk) }}
                  >
                    {result.summary.highest_risk.toUpperCase()}
                  </div>
                  <div className={styles.metricLabel}>Risk Level</div>
                </div>
              </div>

              {/* Language Info */}
              {result.language_support === "partial" && (
                <div className={styles.infoBox}>
                  Detected {result.language_name}. Explanation shown in
                  English due to limited local-language support.
                </div>
              )}

              {/* Visual Forensics Warning */}
              {result.visual_forensics?.suspicion_level &&
                ["medium", "high"].includes(
                  result.visual_forensics.suspicion_level
                ) && (
                  <div className={styles.warningBox}>
                    Visual Forensics:{" "}
                    {result.visual_forensics.suspicion_level.toUpperCase()}{" "}
                    suspicion of image manipulation detected
                  </div>
                )}

              {/* Individual Claims */}
              {result.results.map((claim, idx) => (
                <div key={claim.claim_id} className={styles.claimCard}>
                  <h3 className={styles.claimTitle}>Claim #{idx + 1}</h3>

                  <div
                    className={`${styles.verdictBox} ${
                      styles[`verdict-${claim.user_label.toLowerCase()}`]
                    }`}
                  >
                    <div className={styles.verdictContent}>
                      <div className={styles.claimText}>{claim.claim}</div>
                      <div className={styles.verdictInfo}>
                        <div>
                          <strong>Verdict:</strong> {claim.user_label}
                        </div>
                        <div>
                          <strong>Confidence:</strong> {claim.confidence}%
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className={styles.explanation}>
                    <h4>Explanation:</h4>
                    {result.primary_language !== "en" &&
                      result.language_support === "full" && (
                        <div className={styles.localExplanation}>
                          <strong>{result.language_name}:</strong>{" "}
                          {claim.short_explain_local}
                        </div>
                      )}
                    <div className={styles.englishExplanation}>
                      {claim.short_explain_en}
                    </div>
                  </div>

                  <div className={styles.metricsRow}>
                    <div className={styles.metricBox}>
                      <div className={styles.metricLabel}>Virality Score</div>
                      <div className={styles.metricValue}>
                        {claim.virality_score}/100
                      </div>
                    </div>
                    <div className={styles.metricBox}>
                      <div className={styles.metricLabel}>Risk Level</div>
                      <div
                        className={styles.riskBadge}
                        style={{
                          backgroundColor: getRiskColor(
                            claim.combined_risk_level
                          ),
                        }}
                      >
                        {claim.combined_risk_level.toUpperCase()}
                      </div>
                    </div>
                  </div>

                  {/* Evidence */}
                  {showEvidence && claim.evidence && claim.evidence.length > 0 && (
                    <div className={styles.evidenceSection}>
                      <h4>Top 5 Credible Sources</h4>
                      <div className={styles.evidenceList}>
                        {claim.evidence.slice(0, 5).map((ev, evIdx) => (
                          <div key={evIdx} className={styles.evidenceItem}>
                            <div className={styles.evidenceHeader}>
                              <span className={styles.evidenceNumber}>{evIdx + 1}</span>
                              <span className={styles.sourceName}>
                                {ev.source_name || ev.domain || 'Unknown Source'}
                              </span>
                              <span className={styles.evidenceType}>{ev.source_type.toUpperCase()}</span>
                              <span className={styles.evidenceCredibility}>
                                {ev.credibility_score}/100
                              </span>
                            </div>
                            <div className={styles.evidenceTitle}>{ev.title}</div>
                            <a
                              href={ev.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className={styles.evidenceLink}
                            >
                              {ev.url}
                            </a>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* PDF Download */}
                  {claim.receipt_pdf_path && (
                    <a
                      href={`http://localhost:8000/api/download/${claim.claim_id}`}
                      download
                      className={styles.downloadBtn}
                    >
                      Download Verification Receipt (PDF)
                    </a>
                  )}

                  {claim.needs_human_review && (
                    <div className={styles.warningBox}>
                      This claim requires human review due to sensitivity or
                      low confidence.
                    </div>
                  )}
                </div>
              ))}

              <button className={styles.clearBtn} onClick={clearResults}>
                Clear Results
              </button>
            </motion.div>
          )}
        </div>

        {/* Footer */}
        <footer className={styles.footer}>
          <div className={styles.footerContent}>
            <h3>About Veritas Guardian</h3>
            <p>
              <strong>Veritas Guardian</strong> uses 6 AI agents to verify any content:
            </p>
            <div className={styles.agentGrid}>
              <div className={styles.agentItem}>
                <strong>Ingestion</strong>
                <span>Extract text from any media</span>
              </div>
              <div className={styles.agentItem}>
                <strong>Claims</strong>
                <span>Detect language & extract facts</span>
              </div>
              <div className={styles.agentItem}>
                <strong>Evidence</strong>
                <span>Search reliable sources</span>
              </div>
              <div className={styles.agentItem}>
                <strong>Verification</strong>
                <span>AI-powered fact-checking</span>
              </div>
              <div className={styles.agentItem}>
                <strong>Virality</strong>
                <span>Assess spread & risk</span>
              </div>
              <div className={styles.agentItem}>
                <strong>Synthesis</strong>
                <span>Generate reports</span>
              </div>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default VerificationPage;
