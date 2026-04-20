# Text Sampling & Knowledge Graph Explorer

A comprehensive web application for advanced text generation and semantic analysis. This project integrates traditional statistical models (Bigram) with modern neural embeddings (Word2Vec) to provide multiple text sampling strategies, alongside an interactive knowledge graph for visualizing semantic relationships in any input text.

## 📖 Overview

The Text Sampling & Knowledge Graph Explorer is designed for researchers, developers, and enthusiasts interested in natural language processing (NLP) techniques. It offers a user-friendly interface to experiment with different text generation methods and analyze textual content through knowledge graphs.

The application uses *War and Peace* by Leo Tolstoy as the default training corpus, but can be adapted to other texts. It supports real-time text generation with scoring metrics and dynamic knowledge graph construction from user-provided articles.

## ✨ Features

### Text Generation Module
- **Multiple Sampling Methods**:
  - **Likelihood (Bigram)**: Uses statistical bigram probabilities to predict the next word based on immediate context. This method provides coherent, statistically likely continuations.
  - **Vector Semantic (Word2Vec)**: Leverages pre-trained word embeddings to find semantically similar words. It considers the last few words in context for more nuanced, conceptually related predictions.
  - **Random**: Pure random sampling from the vocabulary for creative, unpredictable outputs.
- **Customizable Parameters**:
  - Starting prompt (seed text)
  - Output length (10-500 tokens)
  - Real-time score display (log-likelihood for bigram, similarity score for Word2Vec)
- **Fallback Mechanisms**: If a method fails (e.g., word not in model), it gracefully falls back to bigram or random sampling.

### Knowledge Graph Module
- **NLP-Powered Extraction**:
  - Uses NLTK for tokenization and part-of-speech (POS) tagging.
  - Extracts key terms: Proper Nouns (NNP/NNPS) and significant Common Nouns (NN/NNS) based on frequency and length.
  - Filters out stopwords and low-frequency terms.
- **Graph Construction**:
  - Nodes represent key terms, sized by weighted frequency.
  - Edges connect terms that co-occur in the same sentence, with edge weights based on co-occurrence count.
- **Interactive Visualization**:
  - Built with Vis.js for smooth, stabilized network graphs.
  - Features hover tooltips, zoom, drag, and physics stabilization.
  - Prevents duplicate nodes and stabilizes layout after rendering.

### User Interface
- **Modern Design**: Dark mode with glassmorphism effects using CSS.
- **Responsive Layout**: Adapts to different screen sizes.
- **Tabbed Interface**: Separate sections for text generation and knowledge graph.
- **Real-time Feedback**: Loading indicators, error handling, and dynamic updates.

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/LokheshNK/Text-Sampling.git
   cd Text-Sampling
   ```

2. **Create a Virtual Environment** (Recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   This installs:
   - Flask: Web framework
   - Gensim: For Word2Vec model handling
   - NLTK: Natural language processing toolkit
   - Scikit-learn: Machine learning utilities
   - SciPy: Scientific computing

4. **Download Training Data**:
   ```bash
   python download_data.py
   ```
   This script downloads *War and Peace* from Project Gutenberg and saves it as `war_and_peace.txt`.

5. **Train Models** (Automatic on first run):
   - Bigram model: Built from word pairs in the corpus.
   - Word2Vec model: Trained and saved as `w2v.model` (may take 10-20 seconds on first startup).

### Starting the Application
```bash
python app.py
```
The app will run on `http://localhost:5000` by default.

> **Note**: On the first run, NLTK will download required packages (punkt, stopwords, etc.). Ensure internet connectivity.

## 📋 Usage

### Text Generation
1. Navigate to the "Text Generator" tab.
2. Enter a starting prompt (e.g., "In the midst of the battlefield").
3. Select a sampling method:
   - Likelihood (Bigram) for coherent, statistical text.
   - Vector Semantic (Word2Vec) for creative, semantic continuations.
   - Random for unpredictable outputs.
4. Adjust the output length (10-500 tokens).
5. Click "Generate Sequence" to produce text.
6. View the output, method used, and score.

### Knowledge Graph
1. Switch to the "Knowledge Graph" tab.
2. Paste an article or text into the input field.
3. Click "Extract Knowledge Graph".
4. Explore the interactive graph:
   - Nodes: Key terms (hover for labels).
   - Edges: Connections based on co-occurrence.
   - Use mouse to zoom, pan, and select nodes.

## 🔧 API Endpoints

The Flask backend exposes the following endpoints:

### GET /
- **Description**: Serves the main web interface.
- **Response**: HTML page (`templates/index.html`).

### POST /generate
- **Description**: Generates text based on provided parameters.
- **Request Body** (JSON):
  ```json
  {
    "prompt": "starting text",
    "method": "likelihood" | "word2vec" | "random",
    "length": 50
  }
  ```
- **Response** (JSON):
  ```json
  {
    "output": "generated text...",
    "score": 1.23,
    "method": "likelihood"
  }
  ```
- **Error Response**: `{"error": "message"}` with status 500.

### POST /kg
- **Description**: Builds a knowledge graph from input text.
- **Request Body** (JSON):
  ```json
  {
    "article": "text to analyze..."
  }
  ```
- **Response** (JSON):
  ```json
  {
    "nodes": [{"id": "term", "label": "Term", "size": 20}],
    "edges": [{"from": "term1", "to": "term2", "value": 0.5}]
  }
  ```

## 📁 Project Structure

```
Text-Sampling/
├── app.py                    # Main Flask application with model loading and API routes
├── download_data.py          # Script to download training corpus from Project Gutenberg
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── vercel.json               # Deployment configuration for Vercel
├── w2v.model                 # Pre-trained Word2Vec model (generated on first run)
├── war_and_peace.txt         # Training corpus (downloaded via download_data.py)
├── templates/
│   └── index.html            # Frontend interface with tabs and visualizations
└── __pycache__/              # Python bytecode cache (auto-generated)
```

## 🛠️ Technology Stack

- **Backend**:
  - Flask: Lightweight web framework for Python.
  - Gensim: Library for topic modeling and word embeddings (Word2Vec).
  - NLTK: Toolkit for natural language processing (tokenization, POS tagging, stopwords).
- **Frontend**:
  - HTML5/CSS3: Structure and styling with glassmorphism effects.
  - JavaScript (Vanilla): DOM manipulation and API calls.
  - Vis.js: Network visualization library for knowledge graphs.
- **Data Processing**:
  - Regular Expressions: For token extraction.
  - Collections (Counter, defaultdict): For frequency counting and bigram storage.
- **Deployment**:
  - Vercel: For serverless deployment (optional).

## 🔍 How It Works

### Model Training
- **Bigram Model**: Counts word pairs from the corpus to build transition probabilities.
- **Word2Vec Model**: Uses Gensim to train embeddings on tokenized sentences, capturing semantic relationships.

### Text Generation
- For each step, the `next_word()` function selects the next token based on the chosen method.
- Context-aware: Word2Vec uses recent words; Bigram uses the immediate predecessor.

### Knowledge Graph
- Text is tokenized and POS-tagged.
- Terms are filtered and weighted.
- Co-occurrence is calculated per sentence.
- Graph is rendered with physics stabilization.

## 🐛 Troubleshooting

- **Model Loading Errors**: Ensure `w2v.model` and `war_and_peace.txt` exist. Re-run `download_data.py` if needed.
- **NLTK Download Issues**: Check internet connection; NLTK packages are downloaded automatically.
- **Graph Not Stabilizing**: Refresh the page; physics should disable after stabilization.
- **Generation Errors**: Check console for details; ensure valid prompt and parameters.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch.
3. Make changes and test thoroughly.
4. Submit a pull request with a clear description.

## 📄 License

This project is licensed under the MIT License. It uses public domain literature from Project Gutenberg for training data.

---

**Built for the Advanced AI Package Development Course** | Developed by Lokhesh NK