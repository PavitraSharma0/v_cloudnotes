import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
        return JsonResponse({'error': 'Invalid request'}, status=400)

    data = json.loads(request.body)
    user_message = data.get('message', '').strip()

    if not user_message:
        return JsonResponse({'reply': 'Please ask something 😊'})

    # Save USER message
    AIMessage.objects.create(
        user=request.user,
        sender='user',
        content=user_message
    )

    # ⚠️ TEMP AI RESPONSE (we will replace with real AI later)
    ai_reply = generate_ai_reply(user_message)

    # Save AI message
    AIMessage.objects.create(
        user=request.user,
        sender='ai',
        content=ai_reply
    )

    return JsonResponse({'reply': ai_reply})


def generate_ai_reply(message: str) -> str:
    """
    TEMPORARY logic.
    This will be replaced by OpenAI / Gemini / local LLM.
    """

    message = message.lower()

    if 'photosynthesis' in message:
        return (
            "Photosynthesis is how plants make food using sunlight 🌱.\n\n"
            "They take in carbon dioxide from air and water from roots, "
            "use sunlight as energy, and produce glucose (food) and oxygen."
        )

    if 'math' in message:
        return (
            "Sure! Please share the full math problem 🧮 "
            "and I’ll solve it step by step."
        )

    if 'essay' in message:
        return (
            "A strong essay introduction needs:\n"
            "1️⃣ A hook\n"
            "2️⃣ Background context\n"
            "3️⃣ A clear thesis statement\n\n"
            "Want help writing one?"
        )

    return (
        "I’m here to help with your studies 📚\n\n"
        "Please explain your question in more detail "
        "so I can give you the best answer."
    )