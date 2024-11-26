from classes import classes
from fastapi import FastAPI
import numpy as np
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util


# App/API object
app = FastAPI()

# Sentence transformer used for conversions
model_checkpoint = 'sentence-transformers/paraphrase-distilroberta-base-v1'
model = SentenceTransformer(model_checkpoint)

# Predefined messages and their embeddings
classes_text = np.array(classes)
classes_embeddings = model.encode(classes_text, convert_to_numpy=True)
assert classes_embeddings.shape[0] == len(classes)  # Safety check


# Function to compare the embedding of the human chat/text message with the embeddings of the
# predefined messages
def convert(sentence_embedding: np.array, class_embeddings: np.array, top_n=5) -> np.array:
    similarities = np.array(util.cos_sim(
        sentence_embedding, class_embeddings)).reshape(-1,)
    top_n_indices = np.argsort(similarities)[::-1][0:top_n]

    return top_n_indices


# Class to represent requests sent to the convert_message endpoint
class MessageConversionRequest(BaseModel):
    text: str
    n_preds: int


# Root endpoint (can be used to make sure the app is running)
@app.get('/')
def read_root():
    return {'message': 'chat converter is running'}


# Endpoint for converting human chat/text messages into predfined messages
@app.post('/convert/')
async def convert_message(request: MessageConversionRequest):
    text, n_preds = request.text, request.n_preds
    text_embedding = model.encode(text, convert_to_numpy=True)
    indices = convert(text_embedding, classes_embeddings, top_n=n_preds)
    predicted_classes = list(classes_text[indices])

    return {'predictions': predicted_classes}
