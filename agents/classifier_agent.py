import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from openai import OpenAI
from config import OPENROUTER_API_KEY
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClassifierAgent:
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
            self.model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            logger.info("Loaded pre-trained BERT sentiment model.")
        except Exception as e:
            logger.warning(f"Failed to load local model: {e}. Using OpenRouter fallback.")
            self.model = None
            try:
                self.client = OpenAI(
                    api_key=OPENROUTER_API_KEY,
                    base_url="https://openrouter.ai/api/v1"
                )
                logger.info("Initialized OpenRouter client.")
            except Exception as e:
                logger.error(f"Failed to initialize OpenRouter client: {e}")
                self.client = None

    def classify_intent(self, text):
        try:
            if self.model:
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                with torch.no_grad():
                    outputs = self.model(**inputs)
                logits = outputs.logits
                predicted_class = torch.argmax(logits, dim=1).item()
                # Map sentiment scores (0-4) to intents
                intent_map = {
                    0: "Complaint",  # Very negative
                    1: "Complaint",  # Negative
                    2: "Other",      # Neutral
                    3: "Invoice",    # Positive
                    4: "RFQ"         # Very positive
                }
                return intent_map.get(predicted_class, "Other")
            elif self.client:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Classify the intent of the following text as RFQ, Invoice, Complaint, or Other."},
                        {"role": "user", "content": text}
                    ],
                    max_tokens=50
                )
                intent = response.choices[0].message.content.strip()
                if intent not in ["RFQ", "Invoice", "Complaint", "Other"]:
                    intent = "Other"
                return intent
            else:
                raise Exception("No model or client available for classification.")
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return "Other"