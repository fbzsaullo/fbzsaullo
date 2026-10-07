"""Gera os SVGs do README (banner e cards) em versão clara e escura.

Uso: python tools/build_assets.py
"""
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
WORDMARK = Path.home() / "myaitoolkit-logo" / "final" / "myaitoolkit-wordmark.svg"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", faint="#21262d", dot="#30363d", a1="#7c8ff0", a2="#9b6fd0"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", faint="#eaeef2", dot="#d0d7de", a1="#5a67d8", a2="#764ba2"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, t, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{t['a1']}"/><stop offset="1" stop-color="{t['a2']}"/>
  </linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.4" fill="{t['dot']}"/>
  </pattern>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/>
  </linearGradient>
  <mask id="fadeMask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
  <clipPath id="card"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="{t['bg']}"/>
{body}
  <rect x="0" y="0" width="{w}" height="3" fill="url(#accent)"/>
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="none" stroke="{t['border']}" stroke-width="1.2"/>
</svg>
"""


def lines(x, y, text, size, color, width_chars, leading=1.45, weight=400):
    out = []
    for i, ln in enumerate(textwrap.wrap(text, width_chars)):
        out.append(f'  <text x="{x}" y="{y + i * size * leading:.1f}" font-family="{SANS}" font-size="{size}" '
                   f'font-weight="{weight}" fill="{color}">{esc(ln)}</text>')
    return "\n".join(out)


def pills(x, y, labels, t, size=16):
    out, cx, ph = [], x, round(size * 2.15)
    for label in labels:
        w = len(label) * size * 0.62 + 28
        out.append(f'  <rect x="{cx:.1f}" y="{y}" width="{w:.1f}" height="{ph}" rx="{ph / 2}" '
                   f'fill="{t["panel"]}" stroke="{t["border"]}"/>')
        out.append(f'  <text x="{cx + w / 2:.1f}" y="{y + ph / 2 + size * 0.36:.1f}" text-anchor="middle" '
                   f'font-family="{MONO}" font-size="{size}" fill="{t["muted"]}">{esc(label)}</text>')
        cx += w + 10
    return "\n".join(out)


def eyebrow(x, y, text, t):
    return (f'  <rect x="{x}" y="{y - 12}" width="10" height="10" fill="url(#accent)"/>\n'
            f'  <text x="{x + 22}" y="{y - 1}" font-family="{MONO}" font-size="16" letter-spacing="2.4" '
            f'fill="{t["muted"]}">{esc(text)}</text>')


# ---------------------------------------------------------------- banner
def header(t):
    w, h = 1200, 300
    # janela de código abstrata à direita
    wx, wy, ww, wh = 790, 58, 350, 190
    code = [  # (indentação, largura, cor)
        (0, 120, "accent"), (0, 0, None), (1, 90, "muted"), (1, 170, "faint"), (2, 140, "accent"),
        (2, 100, "faint"), (1, 60, "muted"), (0, 40, "accent"),
    ]
    bars = []
    for i, (ind, bw, c) in enumerate(code):
        if not bw:
            continue
        fill = {"accent": "url(#accent)", "muted": t["border"], "faint": t["faint"]}[c]
        bars.append(f'  <rect x="{wx + 28 + ind * 22}" y="{wy + 52 + i * 16}" width="{bw}" height="7" rx="3.5" fill="{fill}"/>')
    body = f"""  <rect x="560" y="0" width="640" height="{h}" fill="url(#dots)" mask="url(#fadeMask)"/>
{eyebrow(64, 92, "FULL-STACK DEVELOPER", t)}
  <text x="62" y="162" font-family="{SANS}" font-size="66" font-weight="700" letter-spacing="-1.5" fill="{t['text']}">Fabrízio Saullo</text>
  <text x="64" y="208" font-family="{SANS}" font-size="25" fill="{t['muted']}">Sistemas web, apps desktop e automações com IA.</text>
  <text x="64" y="254" font-family="{MONO}" font-size="18" fill="{t['muted']}">São Paulo, Brasil  ·  <tspan fill="{t['text']}">fbz.dev</tspan></text>
  <rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  <circle cx="{wx + 22}" cy="{wy + 20}" r="5" fill="{t['border']}"/>
  <circle cx="{wx + 40}" cy="{wy + 20}" r="5" fill="{t['border']}"/>
  <circle cx="{wx + 58}" cy="{wy + 20}" r="5" fill="{t['border']}"/>
  <line x1="{wx}" y1="{wy + 38}" x2="{wx + ww}" y2="{wy + 38}" stroke="{t['border']}"/>
{chr(10).join(bars)}
  <rect x="{wx + 28 + 40 + 8}" y="{wy + 52 + 7 * 16}" width="2" height="9" fill="{t['text']}"/>"""
    return svg(w, h, body, t, "Fabrízio Saullo — Full-stack developer")


# ---------------------------------------------------------------- MyAiToolKit
def wordmark(color):
    raw = WORDMARK.read_text(encoding="utf-8")
    paths = re.findall(r"<path[^>]*/>", raw)
    return f'<g fill="{color}">' + "".join(paths) + "</g>"


def card_myaitoolkit(t):
    w, h = 1200, 300
    scale = 42 / 136.2
    steps = ["Arquitetura", "PRD", "Plano", "Execução", "Review"]
    px, py, pw, ph = 700, 64, 456, 172
    gap = (pw - 64) / (len(steps) - 1)
    nodes = []
    for i, s in enumerate(steps):
        cx = px + 32 + i * gap
        filled = i < 3
        nodes.append(f'  <rect x="{cx - 8:.1f}" y="{py + 80}" width="16" height="16" '
                     f'fill="{t["text"] if filled else t["panel"]}" stroke="{t["text"]}" stroke-width="2.2"/>')
        nodes.append(f'  <text x="{cx:.1f}" y="{py + 130}" text-anchor="middle" font-family="{MONO}" '
                     f'font-size="14.5" fill="{t["text"] if filled else t["muted"]}">{esc(s)}</text>')
        if i < len(steps) - 1:
            nodes.append(f'  <line x1="{cx + 14:.1f}" y1="{py + 88}" x2="{cx + gap - 14:.1f}" y2="{py + 88}" '
                         f'stroke="{t["border"]}" stroke-width="2.2" stroke-dasharray="{"0" if i < 2 else "5 5"}"/>')
    body = f"""{eyebrow(48, 64, "PROJETO EM DESTAQUE", t)}
  <g transform="translate(48 {88 - 73.2 * scale:.2f}) scale({scale:.4f})">{wordmark(t['text'])}</g>
{lines(48, 168, "Kit open source de skills para assistentes de IA de programação, guiado por Spec-Driven Development.", 21, t['muted'], 60)}
{pills(48, 234, ["Claude Code", "Codex", "SDD", "MIT"], t)}
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="{t['panel']}" stroke="{t['border']}"/>
  <text x="{px + 28}" y="{py + 40}" font-family="{MONO}" font-size="16" fill="{t['muted']}"><tspan fill="{t['text']}">/sdd-start</tspan>  →  pipeline</text>
{chr(10).join(nodes)}"""
    return svg(w, h, body, t, "MyAiToolKit — kit open source de skills para IA baseado em Spec-Driven Development")


# ---------------------------------------------------------------- cards menores
def card_small(t, tag, title, desc, tags, aria):
    w, h = 590, 300
    body = f"""  <rect x="300" y="0" width="290" height="{h}" fill="url(#dots)" mask="url(#fadeMask)"/>
{eyebrow(40, 64, tag, t)}
  <text x="38" y="122" font-family="{SANS}" font-size="40" font-weight="700" letter-spacing="-0.8" fill="{t['text']}">{esc(title)}</text>
{lines(40, 168, desc, 21, t['muted'], 44)}
{pills(40, 234, tags, t)}"""
    return svg(w, h, body, t, aria)


def main():
    OUT.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        files = {
            "header": header(t),
            "myaitoolkit": card_myaitoolkit(t),
            "stratify": card_small(
                t, "IA · GAMES", "Stratify",
                "Coach de desempenho em jogos com IA, com análise de partida e orientação por voz.",
                ["Rails", "Python", "Redis", "Tauri"],
                "Stratify — coach de desempenho em jogos com IA"),
            "structrabuilds": card_small(
                t, "MINECRAFT · PLUGIN", "StructraBuilds",
                "Plugin Paper que transforma construções em itens, com preview e anti-dupe transacional.",
                ["Java 21", "Paper", "PostgreSQL"],
                "StructraBuilds — plugin Paper que transforma construções em itens"),
        }
        for key, content in files.items():
            (OUT / f"{key}-{name}.svg").write_text(content, encoding="utf-8")
    print("ok:", sorted(p.name for p in OUT.glob("*.svg")))


if __name__ == "__main__":
    main()
