import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [question, setQuestion] = useState("");
  const [repoInfo, setRepoInfo] = useState(null);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loadingRepo, setLoadingRepo] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [error, setError] = useState("");

  const suggestedQuestions = [
    "Where is authentication handled?",
    "How is error handling implemented?",
    "Where are API requests made?",
    "How is SSL certificate verification handled?",
  ];

  async function analyzeRepository() {
    if (!repoUrl.trim()) return;

    setLoadingRepo(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          repo_url: repoUrl,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to analyze repository"
        );
      }

      setRepoInfo(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingRepo(false);
    }
  }

  async function askQuestion(customQuestion = null) {
    const finalQuestion = customQuestion || question;

    if (!finalQuestion.trim()) return;

    setLoadingAnswer(true);
    setError("");
    setQuestion(finalQuestion);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: finalQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to answer question"
        );
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingAnswer(false);
    }
  }

  function getRepoName() {
    if (!repoUrl) return "No repo loaded 👾";

    try {
      const parts = repoUrl
        .replace(".git", "")
        .split("/")
        .filter(Boolean);

      return parts.slice(-2).join("/");
    } catch {
      return repoUrl;
    }
  }

  return (
    <div className="appShell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brandIcon">⚡</div>

          <div>
            <h1>CodeLens AI</h1>
            <span>v2.0 // Gen-Z Edition</span>
          </div>
        </div>

        <div className="sidebarSection">
          <span className="sidebarLabel">TARGET REPO</span>

          <div className="repoMiniCard">
            <div className="statusDot"></div>

            <div>
              <strong>{getRepoName()}</strong>

              <span>
                {repoInfo
                  ? "Indexed & Ready 🚀"
                  : "Waiting for input..."}
              </span>
            </div>
          </div>
        </div>

        {repoInfo && (
          <div className="sidebarSection">
            <span className="sidebarLabel">STATS VIBES</span>

            <div className="sidebarStats">
              <div>
                <span>Files</span>
                <strong>{repoInfo.total_files}</strong>
              </div>

              <div>
                <span>Chunks</span>
                <strong>{repoInfo.total_chunks}</strong>
              </div>

              <div>
                <span>Langs</span>
                <strong>
                  {Object.keys(
                    repoInfo.languages || {}
                  ).length}
                </strong>
              </div>
            </div>
          </div>
        )}
      </aside>

      <main className="mainContent">
        <section className="topHero">
          <div>
            <span className="eyebrow">
              🔥 NEXT-GEN CODEBASE INTELLIGENCE
            </span>

            <h2>
              Crack any code
              <br />
              in seconds flat.
            </h2>

            <p>
              Drop a GitHub repository link, parse through vector intelligence, and extract clean answers backed by exact file line references. No fluff.
            </p>
          </div>
        </section>

        <section className="panel repoPanel">
          <div className="panelHeader">
            <div>
              <span className="stepNumber">01</span>
              <div>
                <h3>Link Repository</h3>
                <p>
                  Paste any public GitHub repository URL below.
                </p>
              </div>
            </div>
          </div>

          <div className="repoInputRow">
            <div className="inputWrapper">
              <span className="inputIcon">🔗</span>

              <input
                type="text"
                placeholder="https://github.com/user/repository.git"
                value={repoUrl}
                onChange={(e) =>
                  setRepoUrl(e.target.value)
                }
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    analyzeRepository();
                  }
                }}
              />
            </div>

            <button
              className="primaryButton"
              onClick={analyzeRepository}
              disabled={loadingRepo}
            >
              {loadingRepo ? (
                <>
                  <span className="spinner"></span>
                  Analyzing...
                </>
              ) : (
                <>Analyze Repo 🚀</>
              )}
            </button>
          </div>

          {repoInfo && (
            <div className="statGrid">
              <div className="statCard">
                <span>Source Files</span>
                <strong>{repoInfo.total_files}</strong>
              </div>

              <div className="statCard">
                <span>Code Chunks</span>
                <strong>{repoInfo.total_chunks}</strong>
              </div>

              <div className="statCard">
                <span>Languages</span>
                <strong>
                  {Object.keys(
                    repoInfo.languages || {}
                  ).length}
                </strong>
              </div>

              <div className="statCard">
                <span>Status</span>
                <strong className="readyText">
                  Online ✨
                </strong>
              </div>
            </div>
          )}
        </section>

        {repoInfo && (
          <section className="panel">
            <div className="panelHeader">
              <div>
                <span className="stepNumber">02</span>

                <div>
                  <h3>Interrogate Codebase</h3>
                  <p>
                    Ask architectural or debugging questions in plain language.
                  </p>
                </div>
              </div>
            </div>

            <div className="questionBox">
              <textarea
                placeholder="Where is authentication handled?"
                value={question}
                onChange={(e) =>
                  setQuestion(e.target.value)
                }
                onKeyDown={(e) => {
                  if (
                    e.key === "Enter" &&
                    !e.shiftKey
                  ) {
                    e.preventDefault();
                    askQuestion();
                  }
                }}
              />

              <button
                className="askButton"
                onClick={() => askQuestion()}
                disabled={loadingAnswer}
              >
                {loadingAnswer ? (
                  <>
                    <span className="spinner"></span>
                    Thinking...
                  </>
                ) : (
                  <>Ask AI 💡</>
                )}
              </button>
            </div>

            <div className="suggestions">
              <span>Quick Prompts:</span>

              <div className="suggestionList">
                {suggestedQuestions.map(
                  (item, index) => (
                    <button
                      key={index}
                      onClick={() =>
                        askQuestion(item)
                      }
                    >
                      {item}
                    </button>
                  )
                )}
              </div>
            </div>
          </section>
        )}

        {error && (
          <div className="errorBox">
            <strong>⚠️ Yikes, something went wrong:</strong>
            <span>{error}</span>
          </div>
        )}

        {answer && (
          <section className="panel answerPanel">
            <div className="panelHeader">
              <div>
                <span className="stepNumber">03</span>

                <div>
                  <h3>AI Response</h3>
                  <p>
                    Synthesized context from loaded codebase chunks.
                  </p>
                </div>
              </div>

              <span className="groundedBadge">
                ✓ Grounded
              </span>
            </div>

            <div className="answerContent">
              <ReactMarkdown>
                {answer}
              </ReactMarkdown>
            </div>
          </section>
        )}

        {sources.length > 0 && (
          <section className="panel">
            <div className="panelHeader">
              <div>
                <span className="stepNumber">04</span>

                <div>
                  <h3>Source Code Matches</h3>
                  <p>
                    Exact code snippets leveraged for this answer.
                  </p>
                </div>
              </div>
            </div>

            <div className="sourceList">
              {sources.map((source, index) => (
                <details
                  key={index}
                  className="sourceCard"
                  open={index === 0}
                >
                  <summary>
                    <div className="sourceMain">
                      <div className="sourceIndex">
                        {String(
                          index + 1
                        ).padStart(2, "0")}
                      </div>

                      <div>
                        <strong>{source.name}</strong>
                        <span>{source.file}</span>
                      </div>
                    </div>

                    <div className="sourceRight">
                      <span className="lineBadge">
                        L{source.start_line}–
                        {source.end_line}
                      </span>

                      <span className="scoreBadge">
                        {Math.round(
                          source.similarity * 100
                        )}
                        % match
                      </span>
                    </div>
                  </summary>

                  <div className="codeHeader">
                    <span>{source.file}</span>
                    <span>
                      {source.type}
                    </span>
                  </div>

                  <pre>
                    <code>{source.code}</code>
                  </pre>
                </details>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default App;