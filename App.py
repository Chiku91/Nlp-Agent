import spacy
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from fer import FER
from rake_nltk import Rake
from typing import List, Dict
from sklearn.neighbors import NearestNeighbors

# ----------------------------- AGENT 1: INPUT AGENT -----------------------------
def input_agent(text: str) -> str:
    return text.strip()

# ----------------------------- AGENT 2: NLP AGENT -----------------------------
nlp = spacy.load("en_core_web_sm")

def extract_key_phrases(text: str) -> List[str]:
    rake = Rake()
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:5]

def extract_triples(text: str) -> List[tuple]:
    doc = nlp(text)
    triples = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ == "ROOT":
                subject = [w.text for w in token.lefts if w.dep_ in ("nsubj", "nsubjpass")]
                obj = [w.text for w in token.rights if w.dep_ in ("dobj", "attr")]
                if subject and obj:
                    triples.append((subject[0], token.text, obj[0]))
    return triples

def nlp_agent(text: str) -> Dict:
    key_terms = extract_key_phrases(text)
    triples = extract_triples(text)
    topic_type = "process" if "how" in text.lower() else "theory"
    return {
        "key_terms": key_terms,
        "triples": triples,
        "topic_type": topic_type
    }

# ----------------------------- AGENT 3: VISUAL GENERATOR AGENT -----------------------------
def generate_diagram(key_terms: List[str]):
    G = nx.DiGraph()
    for i in range(len(key_terms)):
        G.add_node(key_terms[i])
        if i > 0:
            G.add_edge(key_terms[i - 1], key_terms[i])
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, font_size=10)
    plt.title("Concept Map")
    plt.savefig("concept_map.png")
    plt.show()

# ----------------------------- AGENT 4: DIALOGUE MEMORY AGENT -----------------------------
dialogue_memory = []
memory_embeddings = []

def store_dialogue(text: str):
    doc = nlp(text)
    vec = doc.vector
    dialogue_memory.append(text)
    memory_embeddings.append(vec)

def retrieve_similar_query(current_text: str):
    if not memory_embeddings:
        return None
    model = NearestNeighbors(n_neighbors=1, metric="cosine").fit(memory_embeddings)
    current_vec = nlp(current_text).vector.reshape(1, -1)
    dist, ind = model.kneighbors(current_vec)
    if dist[0][0] < 0.2:
        return dialogue_memory[ind[0][0]]
    return None

# ----------------------------- AGENT 5: ENGAGEMENT MONITOR AGENT -----------------------------
def monitor_engagement() -> float:
    detector = FER(mtcnn=True)
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    result = detector.detect_emotions(frame)
    if result:
        emotion = detector.top_emotion(frame)[0]
        if emotion in ['happy', 'surprise']: return 0.8
        elif emotion in ['neutral']: return 0.5
        else: return 0.2
    return 0.5

# ----------------------------- AGENT 6: ADAPTIVE TEACHING AGENT -----------------------------
def adaptive_teaching(response: str, engagement_score: float):
    if engagement_score < 0.4:
        return response + "\n(Simplified with visual aid)"
    elif engagement_score > 0.7:
        return response + "\n(Advanced explanation with more depth)"
    else:
        return response

# ----------------------------- MAIN SYSTEM FLOW -----------------------------
def teaching_assistant_pipeline(user_text: str):
    # Input Agent
    input_text = input_agent(user_text)

    # NLP Agent
    parsed = nlp_agent(input_text)
    print("\n🔍 NLP Agent Output:", parsed)

    # Visual Generator
    generate_diagram(parsed['key_terms'])

    # Dialogue Memory
    store_dialogue(input_text)
    similar = retrieve_similar_query(input_text)
    if similar:
        print(f"\n🧠 You've asked something similar before: {similar}")

    # Engagement Monitor
    engagement_score = monitor_engagement()
    print(f"\n📊 Engagement Score: {engagement_score}")

    # Adaptive Teaching
    response = "Here's your explanation based on the input."
    final = adaptive_teaching(response, engagement_score)
    print("\n🤖 Final Response:\n", final)

# ----------------------------- RUN -----------------------------
if __name__ == "__main__":
    query = input("Enter your question: ")
    teaching_assistant_pipeline(query)
