from __future__ import annotations

import argparse
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from chat import run_model_tool_loop, safe_slug, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)


INDEX_HTML = r"""<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SmartCharging Agent UI</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --ink: #18212f;
      --muted: #667085;
      --line: #d8dde6;
      --accent: #0f766e;
      --accent-soft: #d8f3ee;
      --warn: #9a3412;
      --code: #111827;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Arial, sans-serif;
      background: var(--bg);
      color: var(--ink);
    }
    header {
      display: flex;
      gap: 16px;
      align-items: center;
      justify-content: space-between;
      padding: 14px 20px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      position: sticky;
      top: 0;
      z-index: 2;
    }
    h1 { font-size: 18px; margin: 0; font-weight: 700; }
    .meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 12px; color: var(--muted); }
    .pill { border: 1px solid var(--line); border-radius: 999px; padding: 4px 9px; background: #fbfcfd; }
    main {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 420px;
      gap: 16px;
      padding: 16px;
      max-width: 1440px;
      margin: 0 auto;
    }
    .panel {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      min-width: 0;
    }
    #chat { display: flex; flex-direction: column; min-height: calc(100vh - 98px); }
    #messages { flex: 1; overflow: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
    .message { max-width: 86%; padding: 10px 12px; border-radius: 8px; line-height: 1.45; white-space: pre-wrap; }
    .user { align-self: flex-end; background: #e8eefc; }
    .assistant { align-self: flex-start; background: #edf7f5; }
    .error { align-self: flex-start; background: #fff1e8; color: var(--warn); }
    form { display: flex; gap: 10px; padding: 12px; border-top: 1px solid var(--line); }
    textarea {
      flex: 1;
      resize: vertical;
      min-height: 48px;
      max-height: 160px;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      font: inherit;
    }
    button {
      border: 0;
      border-radius: 8px;
      padding: 0 16px;
      background: var(--accent);
      color: white;
      font-weight: 700;
      cursor: pointer;
      min-width: 92px;
    }
    button:disabled { opacity: .55; cursor: wait; }
    aside { padding: 12px; max-height: calc(100vh - 98px); overflow: auto; }
    h2 { font-size: 14px; margin: 4px 0 10px; }
    details {
      border: 1px solid var(--line);
      border-radius: 8px;
      margin-bottom: 10px;
      background: #fbfcfd;
    }
    summary { cursor: pointer; padding: 9px 10px; font-weight: 650; }
    pre {
      margin: 0;
      padding: 10px;
      overflow: auto;
      border-top: 1px solid var(--line);
      color: var(--code);
      font-size: 12px;
      line-height: 1.35;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .empty { color: var(--muted); font-size: 13px; padding: 8px 2px; }
    @media (max-width: 980px) {
      main { grid-template-columns: 1fr; }
      #chat { min-height: 62vh; }
      aside { max-height: none; }
      .message { max-width: 94%; }
    }
  </style>
</head>
<body>
  <header>
    <h1>SmartCharging Agent</h1>
    <div class="meta" id="meta"></div>
  </header>
  <main>
    <section id="chat" class="panel">
      <div id="messages"></div>
      <form id="form">
        <textarea id="input" placeholder="Nhập yêu cầu sạc, kiểm tra trạm, đặt/hủy reservation..."></textarea>
        <button id="send" type="submit">Send</button>
      </form>
    </section>
    <aside class="panel">
      <h2>Tool trace</h2>
      <div id="trace" class="empty">Chưa có tool call.</div>
    </aside>
  </main>
  <script>
    const messages = [];
    const meta = document.querySelector("#meta");
    const list = document.querySelector("#messages");
    const form = document.querySelector("#form");
    const input = document.querySelector("#input");
    const send = document.querySelector("#send");
    const trace = document.querySelector("#trace");

    function addMessage(role, text) {
      const el = document.createElement("div");
      el.className = `message ${role}`;
      el.textContent = text || "";
      list.appendChild(el);
      list.scrollTop = list.scrollHeight;
    }

    function renderTrace(rounds) {
      trace.className = "";
      trace.innerHTML = "";
      let count = 0;
      for (const round of rounds || []) {
        const calls = round.tool_calls || [];
        const results = round.tool_results || [];
        calls.forEach((call, index) => {
          count += 1;
          const details = document.createElement("details");
          details.open = true;
          const summary = document.createElement("summary");
          summary.textContent = `${count}. ${call.name}`;
          const pre = document.createElement("pre");
          pre.textContent = JSON.stringify({
            round: round.round,
            input_args: call.args,
            result: results[index] || null
          }, null, 2);
          details.appendChild(summary);
          details.appendChild(pre);
          trace.appendChild(details);
        });
      }
      if (!count) {
        trace.className = "empty";
        trace.textContent = "Lượt này không gọi tool.";
      }
    }

    async function loadConfig() {
      const res = await fetch("/api/config");
      const cfg = await res.json();
      meta.innerHTML = "";
      ["provider", "model", "version", "artifact_version", "transcript"].forEach((key) => {
        const span = document.createElement("span");
        span.className = "pill";
        span.textContent = `${key}: ${cfg[key] || ""}`;
        meta.appendChild(span);
      });
    }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      input.value = "";
      send.disabled = true;
      addMessage("user", text);
      messages.push({role: "user", content: text});
      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({messages})
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Request failed");
        addMessage("assistant", data.assistant_text);
        messages.push({role: "assistant", content: data.assistant_text});
        renderTrace(data.rounds);
      } catch (err) {
        addMessage("error", String(err.message || err));
      } finally {
        send.disabled = false;
        input.focus();
      }
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
      }
    });

    loadConfig();
  </script>
</body>
</html>
"""


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class SmartChargingUIServer:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.system_prompt = args.system_prompt.read_text(encoding="utf-8")
        self.tool_declarations = load_tool_declarations(args.tools)
        self.openai_tools = to_openai_tools(self.tool_declarations)
        self.provider = make_provider(args.provider)
        self.selected_model = args.model or getattr(self.provider, "default_model", None)
        self.artifact_version = build_artifact_version(args.version, args.system_prompt, args.tools)
        timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
        transcript_id = "_".join([safe_slug(args.version), safe_slug(args.provider), "ui", timestamp])
        self.transcript_path = args.transcripts_dir / f"{transcript_id}.transcript.json"
        self.transcript: dict[str, Any] = {
            "transcript_id": transcript_id,
            **artifact_version_dict(self.artifact_version),
            "provider": args.provider,
            "model": self.selected_model,
            "system_prompt": str(args.system_prompt),
            "tools": str(args.tools),
            "ui": "http.server",
            "history_window": args.history_window,
            "max_tool_rounds": args.max_tool_rounds,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        }

    def config(self) -> dict[str, Any]:
        return {
            "provider": self.args.provider,
            "model": self.selected_model,
            "version": self.args.version,
            "artifact_version": self.artifact_version.artifact_version,
            "transcript": str(self.transcript_path),
        }

    def chat(self, payload: dict[str, Any]) -> dict[str, Any]:
        browser_messages = payload.get("messages", [])
        if not isinstance(browser_messages, list) or not browser_messages:
            raise ValueError("messages must be a non-empty list")
        latest = browser_messages[-1]
        if latest.get("role") != "user" or not str(latest.get("content", "")).strip():
            raise ValueError("latest message must be a non-empty user message")

        history = [
            {"role": item.get("role", ""), "content": str(item.get("content", ""))}
            for item in browser_messages[:-1]
            if item.get("role") in {"user", "assistant"}
        ]
        messages = [
            {"role": "system", "content": self.system_prompt},
            *trim_history(history, self.args.history_window),
            {"role": "user", "content": str(latest["content"])},
        ]
        result = run_model_tool_loop(
            provider=self.provider,
            messages=messages,
            tools=self.openai_tools,
            model=self.args.model,
            max_tool_rounds=self.args.max_tool_rounds,
        )
        turn_record = {
            "turn_index": len(self.transcript["turns"]) + 1,
            "started_at": now_iso(),
            "user": str(latest["content"]),
            **result,
            "ended_at": now_iso(),
        }
        self.transcript["turns"].append(turn_record)
        write_transcript(self.transcript_path, self.transcript)
        return result | {"transcript": str(self.transcript_path)}


def make_handler(app: SmartChargingUIServer):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format: str, *args: Any) -> None:
            print(f"[ui] {self.address_string()} - {format % args}")

        def write_json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False, indent=2, default=str).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:
            if self.path == "/" or self.path.startswith("/?"):
                body = INDEX_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if self.path == "/api/config":
                self.write_json(200, app.config())
                return
            self.write_json(404, {"error": "not_found"})

        def do_POST(self) -> None:
            if self.path != "/api/chat":
                self.write_json(404, {"error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
                self.write_json(200, app.chat(payload))
            except Exception as exc:
                self.write_json(500, {"error": f"{type(exc).__name__}: {str(exc)}"})

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description="SmartCharging web UI with visible tool traces.")
    parser.add_argument("--provider", choices=["openrouter", "openai", "anthropic", "gemini", "ollama"], required=True)
    parser.add_argument("--model", default=None)
    parser.add_argument("--version", required=True)
    parser.add_argument("--system-prompt", type=Path, default=ARTIFACTS_DIR / "system_prompt.md")
    parser.add_argument("--tools", type=Path, default=ARTIFACTS_DIR / "tools.yaml")
    parser.add_argument("--transcripts-dir", type=Path, default=ROOT / "transcripts")
    parser.add_argument("--history-window", type=int, default=5)
    parser.add_argument("--max-tool-rounds", type=int, default=4)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7860)
    args = parser.parse_args()

    app = SmartChargingUIServer(args)
    server = ThreadingHTTPServer((args.host, args.port), make_handler(app))
    url = f"http://{args.host}:{args.port}"
    print(f"SmartCharging UI: {url}")
    print(f"artifact_version={app.artifact_version.artifact_version}")
    print(f"transcript={app.transcript_path}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
