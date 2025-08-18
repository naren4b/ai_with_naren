"""
langchain-llm-chat.py
---------------------

An interactive, beginner-friendly chatbot using LangChain and Ollama LLMs.

**Features:**
- Chat with a local or remote Ollama LLM (e.g., llama3:latest) using `ChatOllama`.
- Set the model, system prompt, temperature, and Ollama server via environment variables:
    - `OLLAMA_MODEL` (default: llama3:latest)
    - `OLLAMA_SYSTEM_MESSAGE` (default: "I am a Prompt Engineer")
    - `OLLAMA_HOST` (default: http://localhost:11434)
    - `OLLAMA_TEMPERATURE` (default: 0.5)
- Temperature controls the creativity of the model (see comments in code).
- Maintains conversation context and prints a summary table when you type `exit`.

**How to Run:**
1. Start your Ollama server (locally or remotely).
2. Install dependencies: `pip install langchain_ollama`
3. (Optional) Set environment variables to customize your chat:
     ```bash
     export OLLAMA_HOST=http://your-ollama-server:11434
     export OLLAMA_MODEL=llama3:latest
     export OLLAMA_SYSTEM_MESSAGE="I am a Prompt Engineer"
     export OLLAMA_TEMPERATURE=0.5
     ```
4. Run: `python langchain-llm-chat.py`
5. Type your messages. Type `exit` to end and see a summary.

**Customization Tips:**
- Change the system message for different AI personas.
- Adjust temperature for more creative or more focused responses.
- Switch models or servers easily with environment variables.

---
"""

from langchain_ollama import ChatOllama
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os
from textwrap import fill

# Lower Temperature (e.g., 0.2): The model is more likely to choose the most probable next word, leading to more focused and deterministic text. This is useful when accuracy and consistency are crucial, like in factual question answering or code generation.
# Higher Temperature (e.g., 0.8): The model is more likely to select less probable words, resulting in more varied, surprising, and creative text. This is useful for tasks like creative writing or brainstorming.
# Mid-Range Temperature (e.g., 0.5): A balanced approach, offering a mix of coherence and creativity.
TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.5"))
MODEL = os.getenv("OLLAMA_MODEL", "llama3:latest")
HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")


SYSTEM_MESSAGE = os.getenv("OLLAMA_SYSTEM_MESSAGE", "I am a Prompt Engineer")


EXIT_MESSAGE = "\n🐼 \x1b[3mNice Talking with you. bye bye ! \x1b[0m"


def print_on_exit(messages):
    """
    Prints a summary table of the conversation history.
    Args:
        messages (list): List of LangChain message objects (SystemMessage, HumanMessage, AIMessage).
    """
    print("Here is the summary of our conversation:")
    print("\n" + "=" * 115)
    print(f"{'Role':<15}| {'Message':<100}")
    print("=" * 115)

    for message in messages:
        if isinstance(message, SystemMessage):
            role = "SystemMessage"
        elif isinstance(message, HumanMessage):
            role = "HumanMessage"
        elif isinstance(message, AIMessage):
            role = "AIMessage"
        else:
            role = "UnknownMessage"
        wrapped_content = fill(message.content, width=100)
        lines = wrapped_content.split("\n")
        print(f"{role:<15}| {lines[0]:<100}")
        for line in lines[1:]:
            print(f"{'':<15}| {line:<100}")
    print("=" * 115)


if __name__ == "__main__":
    messages = []
    if HOST is not None:
        chat = ChatOllama(model=MODEL, temperature=TEMPERATURE, base_url=HOST)
    messages.append(SystemMessage(content=SYSTEM_MESSAGE))
    print("Welcome to panda chatbot.")
    print("About Me:")
    print(f"\tModel: {MODEL},Temperature: {chat.temperature}")
    print(f"\t{SYSTEM_MESSAGE}")

    while True:
        try:
            human_message = input("🗣️ :")
            messages.append(HumanMessage(content=human_message))
            if human_message.strip().lower() == "exit":
                print_on_exit(messages)
                print(f"{EXIT_MESSAGE}")
                break
        except KeyboardInterrupt:
            print(f"{EXIT_MESSAGE}")
            break
        response = chat.invoke(messages)
        print(f"🐼 : {response.content}", end="\n")
        print("\n")
        messages.append(AIMessage(content=response.content))
