<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Text Sampling & Knowledge Graph</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  
  <style>
    :root {
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #10b981;
      --bg: #030712;
      --card-bg: rgba(17, 24, 39, 0.7);
      --border: rgba(255, 255, 255, 0.1);
      --text: #f9fafb;
      --text-muted: #9ca3af;
      --glass: rgba(255, 255, 255, 0.03);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Outfit', sans-serif;
      background: var(--bg);
      background-image: 
        radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(16, 185, 129, 0.1) 0%, transparent 40%);
      color: var(--text);
      min-height: 100vh;
      overflow-x: hidden;
      display: flex;
      flex-direction: column;
    }

    header {
      padding: 2rem;
      text-align: center;
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      margin-bottom: 2rem;
    }

    header h1 {
      font-size: 2.5rem;
      font-weight: 700;
      letter-spacing: -0.05em;
      background: linear-gradient(to right, #818cf8, #34d399);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    header p { color: var(--text-muted); margin-top: 0.5rem; font-weight: 300; }

    main {
      flex: 1;
      max-width: 1200px;
      margin: 0 auto;
      width: 95%;
      padding-bottom: 4rem;
    }

    .tabs {
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin-bottom: 2rem;
    }

    .tab-btn {
      background: var(--glass);
      border: 1px solid var(--border);
      color: var(--text-muted);
      padding: 0.75rem 1.5rem;
      border-radius: 9999px;
      cursor: pointer;
      font-family: inherit;
      font-weight: 600;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .tab-btn.active {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
    }

    .content-section { display: none; animation: fadeIn 0.5s ease-out; }

    .content-section.active {
      display: grid;
      grid-template-columns: 1fr 1.5fr;
      gap: 2rem;
    }

    @media (max-width: 900px) {
      .content-section.active { grid-template-columns: 1fr; }
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: 24px;
      padding: 2rem;
      height: fit-content;
    }

    .controls-card { display: flex; flex-direction: column; gap: 1.5rem; }

    h2 { font-size: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }

    .form-group { display: flex; flex-direction: column; gap: 0.5rem; }

    label { font-size: 0.875rem; color: var(--text-muted); font-weight: 500; }

    input, select, textarea {
      background: rgba(0, 0, 0, 0.3);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 0.875rem;
      color: var(--text);
      font-family: inherit;
      font-size: 1rem;
      transition: all 0.2s;
    }

    textarea { resize: vertical; min-height: 150px; }

    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--primary), var(--primary-hover));
      color: white;
      border: none;
      padding: 1rem;
      border-radius: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
      transition: all 0.2s;
      margin-top: 0.5rem;
    }

    .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4); }
    .btn-primary:active { transform: translateY(0); }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    .result-card { display: flex; flex-direction: column; gap: 1rem; }

    .output-box {
      background: rgba(0, 0, 0, 0.5);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 1.5rem;
      min-height: 300px;
      font-family: 'JetBrains Mono', monospace;
      line-height: 1.8;
      font-size: 1rem;
      position: relative;
      white-space: pre-wrap;
    }

    .meta-tags { display: flex; gap: 0.75rem; flex-wrap: wrap; }

    .tag {
      background: var(--glass);
      border: 1px solid var(--border);
      padding: 0.4rem 0.8rem;
      border-radius: 8px;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
    }

    .tag.highlight { color: var(--accent); border-color: rgba(16, 185, 129, 0.3); }

    #kg-container {
      width: 100%;
      height: 600px;
      border-radius: 16px;
      background: rgba(0, 0, 0, 0.4);
      margin-top: 1rem;
    }

    .loader {
      display: inline-block;
      width: 20px;
      height: 20px;
      border: 3px solid rgba(255,255,255,.3);
      border-radius: 50%;
      border-top-color: #fff;
      animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin { to { transform: rotate(360deg); } }

    footer {
      text-align: center;
      padding: 2rem;
      color: var(--text-muted);
      font-size: 0.875rem;
      border-top: 1px solid var(--border);
    }

    select option { background: #1f2937; color: var(--text); }
  </style>
</head>
<body>

  <header>
    <h1>Text Sampling & Knowledge Graph</h1>
    <p>Advanced Text Generation & Semantic Knowledge Mapping</p>
  </header>

  <main>
    <div class="tabs">
      <button class="tab-btn active" onclick="switchTab('gen', event)">✦ Text Generator</button>
      <button class="tab-btn" onclick="switchTab('kg', event)">⬡ Knowledge Graph</button>
    </div>

    <!-- Generation Section -->
    <div id="section-gen" class="content-section active">
      <div class="card controls-card">
        <h2><span style="color: var(--primary)">⚡</span> Generation Tuning</h2>

        <div class="form-group">
          <label for="prompt">Starting Context (Seed)</label>
          <input type="text" id="prompt" placeholder="e.g. In the midst of the battlefield...">
        </div>

        <div class="form-group">
          <label for="method">Sampling Methodology</label>
          <select id="method">
            <option value="likelihood">Statistical Likelihood (Bigram)</option>
            <option value="word2vec">Vector Semantic (Word2Vec)</option>
            <option value="random">Creative Random</option>
          </select>
        </div>

        <div class="form-group">
          <label for="length">Output Length tokens: <span id="length-val" style="color: var(--primary)">50</span></label>
          <input type="range" id="length" min="10" max="500" value="50" oninput="document.getElementById('length-val').innerText = this.value">
        </div>

        <button id="gen-btn" class="btn-primary" onclick="generateText()">
          Generate Sequence
        </button>
      </div>

      <div class="card result-card">
        <h2><span style="color: var(--accent)">📑</span> Predicted Output</h2>
        <div class="output-box" id="output-text">Your generated text will appear here with the chosen semantic coherence...</div>
        <div class="meta-tags" id="meta-tags">
          <div class="tag">Ready</div>
          <div class="tag" id="meta-method">None</div>
          <div class="tag highlight" id="meta-score">Score: 0.00</div>
        </div>
      </div>
    </div>

    <!-- Knowledge Graph Section -->
    <div id="section-kg" class="content-section">
      <div class="card controls-card">
        <h2><span style="color: var(--primary)">🔍</span> Semantic Analysis</h2>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1rem;">
          Paste any article or text. Key terms are extracted via POS tagging and connected by sentence co-occurrence.
        </p>

        <div class="form-group">
          <label for="article">Input Article / Text</label>
          <textarea id="article" placeholder="Paste your article here to build the knowledge graph..."></textarea>
        </div>

        <button id="kg-btn" class="btn-primary" onclick="buildKG()">
          Extract Knowledge Graph
        </button>
      </div>

      <div class="card result-card">
        <h2><span style="color: var(--accent)">🌐</span> Knowledge Graph Explorer</h2>
        <div id="kg-container"></div>
        <p style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
          * Nodes = key terms (sized by frequency). Edges = terms that co-occur in the same sentence.
        </p>
      </div>
    </div>
  </main>

  <footer>
    Built with Python, NLTK, and Flask
  </footer>

  <script>
    let network = null;

    function switchTab(tab, event) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));

      event.target.classList.add('active');
      document.getElementById('section-' + tab).classList.add('active');

      if (tab === 'kg' && network) {
        setTimeout(() => network.fit(), 200);
      }
    }

    async function generateText() {
      const btn = document.getElementById('gen-btn');
      const out = document.getElementById('output-text');
      const method = document.getElementById('method').value;

      btn.disabled = true;
      btn.innerHTML = '<span class="loader"></span> Sampling...';
      out.style.opacity = '0.5';

      try {
        const response = await fetch('/generate', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            prompt: document.getElementById('prompt').value,
            method: method,
            length: parseInt(document.getElementById('length').value)
          })
        });

        const data = await response.json();
        if (data.error) throw new Error(data.error);

        out.innerText = data.output;
        document.getElementById('meta-method').innerText = data.method.toUpperCase();
        document.getElementById('meta-score').innerText = `Score: ${data.score}`;
      } catch (err) {
        out.innerText = 'Error: ' + err.message;
      } finally {
        btn.disabled = false;
        btn.innerText = 'Generate Sequence';
        out.style.opacity = '1';
      }
    }

    async function buildKG() {
      const btn = document.getElementById('kg-btn');
      const text = document.getElementById('article').value;

      if (!text.trim()) return alert("Please provide some text to analyze.");

      btn.disabled = true;
      btn.innerHTML = '<span class="loader"></span> Building Graph...';

      try {
        const response = await fetch('/kg', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ article: text })
        });

        const data = await response.json();

        if (!data.nodes.length) {
          alert("No key terms found. Try a longer article.");
          return;
        }

        const container = document.getElementById('kg-container');

        if (network) {
          network.destroy();
          network = null;
        }

        const nodes = new vis.DataSet(data.nodes.map(n => ({
          ...n,
          color: {
            background: '#0f172a',
            border: '#6366f1',
            highlight: { background: '#6366f1', border: '#fff' },
            hover: { background: '#4f46e5', border: '#818cf8' }
          },
          font: { color: '#f3f4f6', size: 16, face: 'Outfit', strokeWidth: 3, strokeColor: '#030712' },
          shape: 'dot',
          borderWidth: 2,
          borderWidthSelected: 4
        })));

        const edges = new vis.DataSet(data.edges.map(e => ({
          ...e,
          color: {
            color: 'rgba(99, 102, 241, 0.4)',
            highlight: '#10b981',
            hover: '#34d399'
          },
          width: 2,
          smooth: false,
          hoverWidth: 3,
          selectionWidth: 3
        })));

        const options = {
          layout: { improvedLayout: true },
          nodes: { scaling: { min: 15, max: 40 } },
          physics: {
            enabled: true,
            stabilization: {
              enabled: true,
              iterations: 1000,
              updateInterval: 25,
              onlyDynamicEdges: false
            },
            barnesHut: {
              gravitationalConstant: -20000,
              centralGravity: 0.6,
              springLength: 180,
              avoidOverlap: 1
            }
          },
          interaction: {
            hover: true,
            tooltipDelay: 100,
            zoomView: true,
            dragNodes: true
          }
        };

        network = new vis.Network(container, { nodes, edges }, options);

        network.once("stabilizationIterationsDone", function () {
          network.setOptions({ physics: { enabled: false } });
        });

        network.on("stabilized", function () {
          network.setOptions({ physics: { enabled: false } });
        });

      } catch (err) {
        alert('Error building Knowledge Graph: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerText = 'Extract Knowledge Graph';
      }
    }
  </script>
</body>
</html>