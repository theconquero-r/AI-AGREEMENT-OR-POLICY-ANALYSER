# llm.py

from pyexpat.errors import messages
from urllib import response

from prompt_toolkit import prompt

from ollama import Client
import os


class LLM:
    def __init__(self, model="gpt-oss:120b"):
        self.client = Client(
            host="https://ollama.com",
            headers={
                "Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY")
            }
        )
        self.model = model

    def _generate(self, prompt):
        messages = [{"role": "user", "content": prompt}]
        response = ""

        for part in self.client.chat(self.model, messages=messages, stream=True):
            content = part.get("message", {}).get("content", "")
            response += content

        return response.strip()

    def generate_answer(self, query, chunks):
        """
        RAG: Answer user query using retrieved chunks
        """

        context = "\n\n".join([
            f"[{c['type'].upper()}]\n{c['text']}"
            for c in chunks
        ])

        prompt = f"""
You are a legal AI assistant.

Context:
{context}

Question:
{query}

Rules:
- Answer using ONLY the context
- Give a complete sentence answer
- Explain clearly in 1-2 sentences
- Do NOT give one-word answers
- If not found, say "Not mentioned in the agreement"

Answer:
"""
        return self._generate(prompt)

    def generate_summary(self, chunks):
        """
        Generate agreement summary
        """

        context = "\n\n".join([c["text"] for c in chunks])

        prompt = f"""
You are a legal AI assistant.

Summarize the following agreement in EXACTLY 2-3 bullet points.

Rules:
- Use simple English
- Each point must be a complete sentence
- Do NOT assume missing information
- If something is mentioned, use it exactly
- Do not contradict the context
- Do NOT add extra text before or after
- Output ONLY bullet points starting with "-"

Agreement:
{context}

Summary:
"""

        return self._generate(prompt)