# 🩺 Health Chatbot
A simple, safe **Health & Wellness Chatbot** powered by LangChain and a Hugging Face LLM.

# ✅ Objective

The goal of this project is to build an **interactive command-line chatbot** that:

- Provides **general wellness advice** (diet, sleep, exercise, stress management, hydration, etc.)
 
- **Politely refuses** to answer questions requiring medical diagnoses, prescriptions, or emergency advice
  
- Maintains a **friendly, supportive tone** with clear, concise responses (2–3 sentences)
- 
- Stores **chat history** for each session with timestamps

 # 📂 Dataset Used

No external dataset is used.

- The chatbot uses a **custom prompt template** to guide the LLM’s responses.
  
- The model generates text on the fly based on the user’s queries and the prompt’s instructions.

# Models Applied

- **LLM:** [Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) via the **Hugging Face Hub**
  
- **Framework:** [LangChain](https://python.langchain.com) for prompt chaining and output parsing

# 🔑 Key Results & Findings

- The chatbot can handle **greetings** and general wellness questions conversationally.
  
- When asked about **diagnoses or treatments**, it **politely declines** and advises consulting a healthcare professional.
  
- Sessions are automatically **saved to a `.txt` file**, creating an audit trail for each chat.
  
- Easy to run locally via the terminal — no web server required (but can be extended to FastAPI).

- 
