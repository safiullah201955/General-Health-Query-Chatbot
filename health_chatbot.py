#  IMPORTS

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_core.output_parsers import StrOutputParser
import os
import datetime

# LOAD ENVIRONMENT VARIABLES

load_dotenv()  # Loads .env file to access your Hugging Face API token securely

#  SETUP LLM MODEL & PROMPT

# Configure Hugging Face LLM endpoint

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HuggingFace_Token")
)

# Wrap in LangChain's Chat interface

model = ChatHuggingFace(llm=llm)


# Create a reusable, safe prompt template

prompt = PromptTemplate(
    template=(
        "You are a friendly and knowledgeable medical assistant. "
        "Respond briefly and to the point (2-3 sentences max). "
        "Answer the user's health-related question in a clear, simple, and supportive tone: {query}. "
        "Provide general wellness advice only (e.g., diet, exercise, sleep, stress management, hydration, preventive measures). "
        "Do NOT give medical diagnoses, prescribe treatments, suggest medications, or discuss emergencies. "
        "If asked about specific diseases, medications, or treatments, politely refuse and advise consulting a healthcare professional. "
        "NEVER provide advice that could be harmful or unsafe."
    ),
    input_variables=["query"]
)

# Setup output parser for plain text output

parser = StrOutputParser()


# Build the LangChain sequence: Prompt ➜ Model ➜ OutputParser

chain = RunnableSequence(prompt, model, parser)


# ✅ CHAT HISTORY MANAGEMENT
HISTORY_FILE = "chat_history.txt"


def load_history():
    """Load previous chat history from file (silently)."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = file.read()
        return history  # Loaded but not displayed
    return ""



def save_history(chat_history):
    """Save current chat history to file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(f"\n--- Chat session @ {timestamp} ---\n")
        for entry in chat_history:
            file.write(f"{entry['role']}: {entry['content']}\n")


# ✅ UTILITY FUNCTIONS

def is_greeting(text):
    """Check if user input is a greeting."""
    greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]
    return text.strip().lower() in greetings

# ✅ MAIN CHAT LOOP

def run_chatbot():
    print("🤖 Health Chatbot \n")
    load_history()  # # Load history

    chat_history = [] # Store user & bot messages

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            save_history(chat_history)
            break

        # Save user message
        chat_history.append({"role": "User", "content": user_input})

        try:
            if is_greeting(user_input):
                # Custom greeting response
                reply = "Hi, I’m your medical assistant. How can I help you today?"
            else:
                # Get response from model for non-greetings
                response = chain.invoke({"query": user_input})
                reply = response.strip()

            print(f"Bot: {reply}\n")

            # Save bot response
            chat_history.append({"role": "Bot", "content": reply})

        except Exception as e:
            print(f"⚠️ Error: {e}\n")

# ✅ ENTRY POINT

if __name__ == "__main__":
    run_chatbot()