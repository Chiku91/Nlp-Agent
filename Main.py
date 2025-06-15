# Virtual AI Teaching Assistant - Full System Code (MVP + Adaptive Response System)

# Requirements:
# pip install spacy textacy faiss-cpu opencv-python deepface matplotlib graphviz


import spacy
import textacy.extract
import faiss
import numpy as np
from deepface import DeepFace
import cv2
import time
import graphviz
from typing import List, Dict

# ----------------------------- AGENT 1: INPUT AGENT -----------------------------
def input_agent(text: str) -> str:
    return text  # Start simple with text only input

# ----------------------------- AGENT 2: NLP AGENT -----------------------------
nlp = spacy.load("en_core_web_sm")

def nlp_agent(text: str) -> Dict:
    doc = nlp(text)
    key_terms = textacy.ke.textrank(doc, topn=5)
    triples = list(textacy.extract.semistructured_statements(doc, cue="is"))
    topic_type = "process" if "how" in text.lower() else "theory"
    return {
        "key_terms": list(key_terms),
        "triples": [(s.text, v.text, o.text) for s, v, o in triples],
        "topic_type": topic_type
    }

# ----------------------------- AGENT 3: VISUAL GENERATOR AGENT -----------------------------
def generate_diagram(key_terms: List[str], topic_type: str):
    dot = graphviz.Digraph(comment='Concept Graph')
    for i, term in enumerate(key_terms):
        dot.node(str(i), term)
        if i > 0:
            dot.edge(str(i - 1), str(i))
    dot.render('concept_graph', view=True, format='png')

# ----------------------------- AGENT 4: DIALOGUE MEMORY AGENT -----------------------------
dialogue_memory = []

def store_dialogue(text: str, embedding: np.ndarray):
    dialogue_memory.append((text, embedding))

def retrieve_similar_query(embedding: np.ndarray):
    if not dialogue_memory:
        return None
    dim = len(embedding)
    index = faiss.IndexFlatL2(dim)
    data = np.array([e for _, e in dialogue_memory]).astype('float32')
    index.add(data)
    D, I = index.search(np.array([embedding]).astype('float32'), 1)
    return dialogue_memory[I[0][0]][0] if D[0][0] < 0.1 else None

# ----------------------------- AGENT 5: ENGAGEMENT MONITOR AGENT -----------------------------
def monitor_engagement() -> float:
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    engagement_score = 0.5  # default medium
    try:
        ret, frame = cap.read()
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        if emotion in ['happy', 'surprise']: engagement_score = 0.8
        elif emotion in ['neutral']: engagement_score = 0.5
        else: engagement_score = 0.2
    except:
        engagement_score = 0.5
    finally:
        cap.release()
        cv2.destroyAllWindows()
    return engagement_score

# ----------------------------- AGENT 6: ADAPTIVE TEACHING AGENT -----------------------------
def adaptive_teaching(response: str, engagement_score: float):
    if engagement_score < 0.4:
        print("\n🧠 You seem disengaged. Here's a simplified explanation with a diagram:")
        return response + "\n(Simplified with visual aid)"
    elif engagement_score > 0.7:
        return response + "\n(Going deeper with more detail...)"
    else:
        return response

# ----------------------------- MAIN SYSTEM FLOW -----------------------------
def teaching_assistant_pipeline(text: str):
    # Step 1: Input Agent
    input_text = input_agent(text)

    # Step 2: NLP Agent
    parsed = nlp_agent(input_text)
    print("\n🔍 NLP Agent Output:", parsed)

    # Step 3: Visual Generation
    generate_diagram(parsed["key_terms"], parsed["topic_type"])

    # Step 4: Dialogue Memory
    embed_vector = np.random.rand(300).astype('float32')  # Placeholder for real embeddings
    store_dialogue(input_text, embed_vector)
    similar = retrieve_similar_query(embed_vector)
    if similar:
        print(f"\n🧠 Previously you asked something similar: '{similar}'")

    # Step 5: Engagement Monitor
    engagement = monitor_engagement()
    print(f"\n📊 Engagement Score: {engagement}")

    # Step 6: Adaptive Teaching
    final_response = adaptive_teaching("Here’s your explanation based on input.", engagement)
    print("\n🤖 Final Teaching Response:\n", final_response)

# ----------------------------- TEST -----------------------------
if __name__ == "__main__":
    user_query = input("Enter your question: ")
    teaching_assistant_pipeline(user_query)
