#!/usr/bin/env node
// Converts SURVEY_PROCESS_v3.md to a print-ready PDF using Chrome headless
// Usage: node build_pdf.js

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const mdFile = path.join(__dirname, 'SURVEY_PROCESS_v3.md');
const htmlFile = path.join(__dirname, 'SURVEY_PROCESS_v3.html');
const pdfFile = path.join(__dirname, 'SURVEY_PROCESS_v3.pdf');

// Simple markdown-to-HTML conversion (covers what we need)
function mdToHtml(md) {
  let html = md;

  // Escape HTML entities in code blocks first, then process
  const codeBlocks = [];
  html = html.replace(/```([^`]*?)```/gs, (match, code) => {
    codeBlocks.push(code);
    return `%%CODEBLOCK_${codeBlocks.length - 1}%%`;
  });

  // Inline code
  const inlineCodes = [];
  html = html.replace(/`([^`]+?)`/g, (match, code) => {
    inlineCodes.push(code);
    return `%%INLINECODE_${inlineCodes.length - 1}%%`;
  });

  // Headers
  html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
  html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
  html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');

  // Horizontal rules
  html = html.replace(/^---+$/gm, '<hr>');

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Tables
  html = html.replace(/^(\|.+\|)\n(\|[-| :]+\|)\n((?:\|.+\|\n?)*)/gm, (match, header, sep, body) => {
    const headers = header.split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
    const rows = body.trim().split('\n').map(row => {
      const cells = row.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('\n');
    return `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
  });

  // Checklist items
  html = html.replace(/^- \[ \] (.+)$/gm, '<div class="checklist"><span class="checkbox">☐</span> $1</div>');
  html = html.replace(/^- \[x\] (.+)$/gm, '<div class="checklist"><span class="checkbox">☑</span> $1</div>');

  // Unordered lists
  html = html.replace(/^(\s*)- (.+)$/gm, (match, indent, content) => {
    return `${indent}<li>${content}</li>`;
  });

  // Ordered lists
  html = html.replace(/^\d+\.\s+(.+)$/gm, '<li class="ordered">$1</li>');

  // Wrap consecutive <li> in <ul> or <ol>
  html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>');
  html = html.replace(/((?:<li class="ordered">.*<\/li>\n?)+)/g, (match) => {
    return '<ol>' + match.replace(/ class="ordered"/g, '') + '</ol>';
  });

  // Paragraphs - wrap text lines that aren't already in block-level elements
  // Only skip lines starting with block elements (h, div, table, ul, ol, pre, hr, thead, tbody, tr, li)
  // Lines starting with inline elements (<strong>, <em>, <a>, <code>) DO need <p> wrapping
  const blockTags = /^<(h[1-6]|div|table|thead|tbody|tr|th|td|ul|ol|li|pre|hr|p|!)/;
  html = html.split('\n').map(line => {
    const trimmed = line.trim();
    if (!trimmed) return line;  // blank line
    if (trimmed.startsWith('%%')) return line;  // placeholder
    if (blockTags.test(trimmed)) return line;  // already block-level
    // Wrap non-block content in <p>
    return `<p>${line}</p>`;
  }).join('\n');

  // Restore code blocks
  codeBlocks.forEach((code, i) => {
    const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    html = html.replace(`%%CODEBLOCK_${i}%%`, `<pre><code>${escaped}</code></pre>`);
  });

  inlineCodes.forEach((code, i) => {
    const escaped = code.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    html = html.replace(`%%INLINECODE_${i}%%`, `<code>${escaped}</code>`);
  });

  return html;
}

const md = fs.readFileSync(mdFile, 'utf8');
const body = mdToHtml(md);

const htmlDoc = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>River Survey Procedure v3 — OpenRiverCam</title>
<style>
  @page {
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {
      content: counter(page);
      font-size: 9pt;
      color: #666;
    }
  }

  * { box-sizing: border-box; }

  body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1a1a1a;
    max-width: 100%;
  }

  h1 {
    font-size: 20pt;
    margin-top: 0.8em;
    margin-bottom: 0.3em;
    color: #1a3a5c;
    border-bottom: 2px solid #1a3a5c;
    padding-bottom: 4pt;
    page-break-after: avoid;
  }

  h2 {
    font-size: 15pt;
    margin-top: 1em;
    margin-bottom: 0.3em;
    color: #2a5a8c;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3pt;
    page-break-after: avoid;
  }

  h3 {
    font-size: 12pt;
    margin-top: 0.8em;
    margin-bottom: 0.2em;
    color: #333;
    page-break-after: avoid;
  }

  h4 {
    font-size: 11pt;
    margin-top: 0.6em;
    margin-bottom: 0.2em;
    color: #444;
    page-break-after: avoid;
  }

  p {
    margin: 0.4em 0;
    orphans: 3;
    widows: 3;
  }

  a {
    color: #2a5a8c;
    text-decoration: none;
  }

  hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 1em 0;
  }

  table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.5em 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }

  th, td {
    border: 1px solid #bbb;
    padding: 4pt 8pt;
    text-align: left;
    vertical-align: top;
  }

  th {
    background: #e8eef4;
    font-weight: 600;
    color: #1a3a5c;
  }

  tr:nth-child(even) {
    background: #f8f9fa;
  }

  ul, ol {
    margin: 0.3em 0;
    padding-left: 1.8em;
  }

  li {
    margin: 0.15em 0;
  }

  .checklist {
    margin: 0.2em 0;
    padding-left: 0.2em;
  }

  .checkbox {
    font-size: 12pt;
    margin-right: 0.3em;
    vertical-align: middle;
  }

  code {
    font-family: "SF Mono", "Menlo", "Monaco", "Consolas", monospace;
    font-size: 9pt;
    background: #f0f2f5;
    padding: 1pt 4pt;
    border-radius: 3pt;
  }

  pre {
    background: #f0f2f5;
    border: 1px solid #ddd;
    border-radius: 4pt;
    padding: 8pt 12pt;
    font-size: 8.5pt;
    line-height: 1.4;
    overflow-x: auto;
    page-break-inside: avoid;
    white-space: pre-wrap;
    word-wrap: break-word;
  }

  pre code {
    background: none;
    padding: 0;
    font-size: inherit;
  }

  strong {
    font-weight: 600;
  }

  /* Print-specific */
  @media print {
    body { font-size: 10pt; }
    a { color: #1a3a5c; }
    h1 { page-break-before: always; }
    h1:first-of-type { page-break-before: avoid; }
    .no-break { page-break-inside: avoid; }
  }
</style>
</head>
<body>
${body}
</body>
</html>`;

fs.writeFileSync(htmlFile, htmlDoc);
console.log(`HTML written to ${htmlFile}`);

// Generate PDF with Chrome headless
try {
  execSync(
    `google-chrome --headless --disable-gpu --no-sandbox --print-to-pdf="${pdfFile}" --no-pdf-header-footer "${htmlFile}"`,
    { stdio: 'inherit', timeout: 30000 }
  );
  console.log(`PDF written to ${pdfFile}`);
} catch (err) {
  // Try alternative flag names
  try {
    execSync(
      `google-chrome --headless=new --disable-gpu --no-sandbox --print-to-pdf="${pdfFile}" --no-pdf-header-footer "file://${htmlFile}"`,
      { stdio: 'inherit', timeout: 30000 }
    );
    console.log(`PDF written to ${pdfFile}`);
  } catch (err2) {
    console.error('Chrome PDF generation failed:', err2.message);
    console.log(`HTML file is available at ${htmlFile} — open in a browser and print to PDF.`);
    process.exit(1);
  }
}

// Clean up HTML
// fs.unlinkSync(htmlFile);  // keep for debugging
