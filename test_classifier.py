from agents.classifier_agent import ClassifierAgent

classifier = ClassifierAgent()
text = "Please provide a quote for 100 units of Product X."
intent = classifier.classify_intent(text)
print(f"Intent: {intent}")
