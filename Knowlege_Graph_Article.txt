from flask import Flask, render_template, request, jsonify
import random, re, math, os
from collections import Counter, defaultdict
import nltk
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def setup_nltk():
    try:
        if os.environ.get('VERCEL'):
            nltk.data.path.append("/tmp/nltk_data")
        pkgs = ['punkt', 'stopwords', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng', 'maxent_ne_chunker', 'words']
        for pkg in pkgs:
            try:
                nltk.data.find(pkg)
            except:
                nltk.download(pkg, quiet=True)
    except:
        pass

setup_nltk()

app = Flask(__name__)
DATA_FILE = "sherlock_holmes.txt"

def load_models(filename):
    if not os.path.exists(filename):
        return [], [], {}
    with open(filename, encoding='utf-8') as f:
        text = f.read()
    tokens = re.findall(r"\b[\w']+\b", text.lower())
    bigrams = defaultdict(Counter)
    for i in range(len(tokens) - 1):
        bigrams[tokens[i]][tokens[i + 1]] += 1
    return tokens, list(set(tokens)), bigrams

tokens, vocab, bigram_map = load_models(DATA_FILE)


def load_word2vec(filename):
    if not os.path.exists(filename):
        return None
    try:
        return Word2Vec.load(filename)
    except Exception:
        return None

w2v_model = load_word2vec('w2v.model')


def next_word(context, method):
    if method == "word2vec" and w2v_model is not None:
        valid_context = [w for w in context[-3:] if w in w2v_model.wv]
        if valid_context:
            try:
                candidates = w2v_model.wv.most_similar(positive=valid_context, topn=15)
                if candidates:
                    words, sims = zip(*candidates)
                    chosen = random.choices(words, weights=[max(sim, 0.01) for sim in sims], k=1)[0]
                    score = next(sim for w, sim in candidates if w == chosen)
                    return chosen, float(score)
            except KeyError:
                pass

    last_word = context[-1]
    if method == "random" or last_word not in bigram_map:
        return random.choice(vocab), 0.0

    candidates = bigram_map[last_word]
    total = sum(candidates.values())
    words, weights = zip(*[(w, c / total) for w, c in candidates.items()])
    chosen = random.choices(words, weights=weights, k=1)[0]
    return chosen, math.log(candidates[chosen] / total)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not vocab:
        return jsonify({"error": "No data loaded."}), 500
    data = request.json
    prompt_words = data.get("prompt", "the").lower().split() or ["the"]
    method = data.get("method", "likelihood")
    length = int(data.get("length", 20))
    result = list(prompt_words)
    score = 0
    for _ in range(length):
        w, lh = next_word(result, method)
        result.append(w)
        score += lh
    return jsonify({"output": " ".join(result), "score": round(float(score), 2), "method": method})

@app.route('/kg', methods=['POST'])
def get_kg():
    data = request.json
    text = data.get("article", "")
    if not text:
        return jsonify({"nodes": [], "edges": []})

    try:
        tokens_raw = word_tokenize(text)
        tagged = nltk.pos_tag(tokens_raw)
    except:
        words = re.findall(r"\b[\w']+\b", text)
        tagged = [(w, 'NNP' if w[0].isupper() else 'NN') for w in words]

    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = {"the", "and", "this", "that", "with", "from", "said"}

    extended_stops = {
        "said", "added", "think", "thing",
        "extraordinary", "according", "possible", "already",
        "within"
    }
    stop_words.update(extended_stops)

    weighted_counts = Counter()
    term_labels = {}

    for w, tag in tagged:
        wl = w.lower()
        if wl in stop_words or len(wl) < 3:
            continue

        if tag in ('NNP', 'NNPS'):
            weighted_counts[wl] += 3
            term_labels.setdefault(wl, w)
        elif tag in ('NN', 'NNS') and len(wl) > 4:
            weighted_counts[wl] += 1
            term_labels.setdefault(wl, wl)

    top_terms = [w for w, c in weighted_counts.most_common(20)]

    nodes = []
    for term in top_terms:
        nodes.append({
            "id": term,
            "label": term_labels.get(term, term),
            "size": int(weighted_counts[term]) * 2 + 15
        })

    sentences = [
        re.findall(r"\b[\w']+\b", line.lower())
        for line in text.split('.') if len(line) > 5
    ]

    edges = []
    seen_edges = set()

    for i, w1 in enumerate(top_terms):
        for w2 in top_terms[i + 1:]:
            wl1, wl2 = w1.lower(), w2.lower()
            co_occurrence = sum(
                0.5 for s in sentences if wl1 in s and wl2 in s
            )
            if co_occurrence > 0:
                edge_id = tuple(sorted((w1, w2)))
                if edge_id not in seen_edges:
                    edges.append({"from": w1, "to": w2, "value": float(co_occurrence)})
                    seen_edges.add(edge_id)

    return jsonify({"nodes": nodes, "edges": edges})

if __name__ == '__main__':
    app.run(debug=True)