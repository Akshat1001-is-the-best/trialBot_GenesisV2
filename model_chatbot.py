import spacy

nlp = spacy.load("en_core_web_sm")

def is_question(text: str) -> bool:
    doc = nlp(text.strip())
    
    if text.endswith("?"):
        return True
    
    question_words = {"who", "what", "where", "when", "why", "how", "is", "do", "does", "can"}
    first_token = doc[0].text.lower()
    if first_token in question_words:
        return True
    
    if len(doc) > 1 and doc[0].pos_ == "AUX" and doc[1].pos_ == "PRON":
        return True

def is_greeting(text: str) -> bool:
    doc = nlp(text.lower().strip())
    
    # Common greeting tokens
    greeting_words = {
        "hi", "hello", "hey", "greetings", 
        "good morning", "good afternoon", "good evening",
        "howdy", "what's up", "yo"
    }
    
    # Check for greeting patterns
    patterns = [
        any(token.text in greeting_words for token in doc),

        (len(doc) >= 2 and doc[0].text in greeting_words 
         and doc[1].is_punct is False),

        (any(t.text in {"how", "how's"} for t in doc[:3]) 
         and any(t.lemma_ in {"be", "do"} for t in doc)),

        doc[0].text in {"welcome", "nice"} and len(doc) > 1
    ]
    
    return any(patterns)

def is_goodbye(text: str) -> bool:
    doc = nlp(text.lower().strip())
    
    # Common goodbye tokens
    goodbye_words = {
        "bye", "goodbye", "farewell", "see you", "see ya",
        "later", "take care", "good night", "cya", "adios", "stop"
    }
    
    # Check for patterns
    patterns = [
        any(token.text in goodbye_words for token in doc),
        
        (doc[0].text == "have" and len(doc) > 2 and 
         doc[2].text in {"nice", "good", "great"}),

        (doc[0].text == "see" and len(doc) > 1 and doc[1].text in {"you", "ya"}),
        
        (any(t.text in {"off", "leaving"} for t in doc) and 
         any(t.text in {"now", "today"} for t in doc[-2:]))
    ]
    
    return any(patterns)

def classify_intent(text):
    doc = nlp(text)
    if is_greeting(text):
        return "greeting"
    elif is_goodbye(text):
        return "goodbye"
    elif is_question(text):
        return "question"
    return "unknown"

intent_responses = {
    "greeting": "Hi there!",
    "goodbye": "goodbye",
    "question": "question",
    "unknown": "Could you rephrase that?"
}

def respond(user_input):
    intent = classify_intent(user_input)
    return intent_responses[intent]