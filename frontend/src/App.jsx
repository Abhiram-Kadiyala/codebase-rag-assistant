import { useState } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

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
        throw new Error(data.detail || "Failed to analyze repository");
      }

      setRepoInfo(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingRepo(false);
    }
  }

  async function askQuestion() {
    if (!question.trim()) return;

    setLoadingAnswer(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Failed to answer question");
      }

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoadingAnswer(false);
    }
  }

  return (
    <div className="app">
      <div className="hero">
        <div className="badge">AI CODE INTELLIGENCE</div>

        <h1>Codebase RAG Assistant</h1>

        <p>
          Understand unfamiliar repositories instantly using semantic code
          search and AI-powered answers.
        </p>
      </div>

      <div className="container">
        <section className="card">
          <h2>Analyze Repository</h2>

          <div className="inputRow">
            <input
              type="text"
              placeholder="https://github.com/user/repository.git"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
            />

            <button
              onClick={analyzeRepository}
              disabled={loadingRepo}
            >
              {loadingRepo ? "Analyzing..." : "Analyze"}
            </button>
          </div>

          {repoInfo && (
            <div className="repoStats">
              <div className="stat">
                <span>Files</span>
                <strong>{repoInfo.total_files}</strong>
              </div>

              <div className="stat">
                <span>Code Chunks</span>
                <strong>{repoInfo.total_chunks}</strong>
              </div>

              <div className="stat">
                <span>Languages</span>
                <strong>
                  {Object.keys(repoInfo.languages || {}).length}
                </strong>
              </div>
            </div>
          )}
        </section>

        {repoInfo && (
          <section className="card">
            <h2>Ask About This Codebase</h2>

            <div className="inputRow">
              <input
                type="text"
                placeholder="Where is authentication handled?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    askQuestion();
                  }
                }}
              />

              <button
                onClick={askQuestion}
                disabled={loadingAnswer}
              >
                {loadingAnswer ? "Thinking..." : "Ask"}
              </button>
            </div>
          </section>
        )}

        {error && (
          <div className="errorBox">
            {error}
          </div>
        )}

        {answer && (
          <section className="card">
            <h2>AI Answer</h2>

            <div className="answerBox">
              <ReactMarkdown>{answer}</ReactMarkdown>
            </div>
          </section>
        )}

        {sources.length > 0 && (
          <section className="card">
            <h2>Retrieved Sources</h2>

            <div className="sources">
              {sources.map((source, index) => (
                <details key={index} className="sourceCard">
                  <summary>
                    <div>
                      <strong>{source.name}</strong>
                      <span>{source.file}</span>
                    </div>

                    <div className="score">
                      {Math.round(source.similarity * 100)}%
                    </div>
                  </summary>

                  <div className="sourceMeta">
                    Lines {source.start_line}–{source.end_line}
                  </div>

                  <pre>
                    <code>{source.code}</code>
                  </pre>
                </details>
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

export default App;