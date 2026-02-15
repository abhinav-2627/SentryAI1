from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

TOXIC_LABELS = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]

def is_toxic(text: str, threshold=0.7):
    result = classifier(text)[0]  # single dict

    label = result["label"].lower()
    score = result["score"]

    if label in TOXIC_LABELS and score >= threshold:
        return True, label, score

    return False, None, score
