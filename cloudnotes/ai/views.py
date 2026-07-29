import json
import os
import urllib.request
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import AIMessage


@login_required
def assistant(request):
    messages = AIMessage.objects.filter(user=request.user)
    return render(request, 'ai/assistant.html', {
        'messages': messages
    })


@login_required
def ai_ask(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse({'reply': 'Please ask something 😊'})

    try:
        # Save USER message
        AIMessage.objects.create(
            user=request.user,
            sender='user',
            content=user_message
        )

        # Generate AI reply
        ai_reply = generate_ai_reply(user_message)

        # Save AI message
        AIMessage.objects.create(
            user=request.user,
            sender='ai',
            content=ai_reply
        )

        return JsonResponse({'reply': ai_reply})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def generate_ai_reply(message: str) -> str:
    """
    Generate AI Study response using Gemini API if key exists,
    otherwise fallback to an intelligent study assistant engine.
    """
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = json.dumps({
                "contents": [{"parts": [{"text": f"You are a helpful AI Study Assistant for students. Answer clearly and concisely:\n\n{message}"}]}]
            }).encode("utf-8")
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                reply = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return reply.strip()
        except Exception:
            pass

    msg_lower = message.lower()

    if 'photosynthesis' in msg_lower:
        return (
            "Photosynthesis is how plants make food using sunlight 🌱.\n\n"
            "Key Steps:\n"
            "1. Plants absorb Sunlight using chlorophyll in leaves.\n"
            "2. Water is drawn up from roots.\n"
            "3. Carbon Dioxide is taken in from the air.\n"
            "4. Result: Glucose (sugar for plant growth) + Oxygen released into air! 🍃"
        )

    if 'math' in msg_lower or 'calcul' in msg_lower or 'solve' in msg_lower:
        return (
            "I can help solve math & quantitative problems! 🧮\n\n"
            "Please type out your math equation or question clearly, and I will break down the solution step-by-step for you."
        )

    if 'essay' in msg_lower or 'write' in msg_lower or 'paragraph' in msg_lower:
        return (
            "Here is the structure for a stellar essay: ✍️\n\n"
            "1️⃣ Introduction: Hook the reader, provide brief context, end with a thesis.\n"
            "2️⃣ Body Paragraphs: Focus on one topic per paragraph with evidence/examples.\n"
            "3️⃣ Conclusion: Rephrase thesis and summarize main points without adding new data.\n\n"
            "Share your topic if you'd like outline suggestions!"
        )

    if 'python' in msg_lower or 'code' in msg_lower or 'program' in msg_lower:
        return (
            "Programming Help 💻:\n\n"
            "I can assist with Python, JavaScript, HTML/CSS, Django, and algorithms.\n"
            "Paste your code snippet or describe the problem/bug you're encountering!"
        )

    if 'war' in msg_lower or 'history' in msg_lower:
        return (
            "History Study Notes 🏛️:\n\n"
            "World War I (1914–1918) was triggered by the assassination of Archduke Franz Ferdinand.\n"
            "Key factors included Militarism, Alliances, Imperialism, and Nationalism (MAIN)."
        )

    return (
        f"I'm your AI Study Assistant! 📚\n\n"
        f"Regarding your query: '{message}'\n\n"
        f"I can help explain concepts, solve practice questions, or organize notes. "
        f"Feel free to clarify your topic (e.g. Science, Math, History, Coding)!"
    )