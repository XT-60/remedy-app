from django.shortcuts import render
import csv

import os
def home(request):
    return render(request, 'index.html')

from django.shortcuts import render
from .search import search_remedies   # ✅ import your semantic search function

def result(request):
    """
    Handle the symptom submitted by the user,
    run semantic search using MongoDB vector search,
    and return the best-matching remedies.
    """

    if request.method == 'POST':
        # ✅ 1. Get the user’s symptom from the form
        user_input = request.POST.get('symptom', '').strip()

        # ✅ 2. Run semantic search (this replaces CSV + if/else logic)
        results = search_remedies(user_input, k=5)

        # ✅ 3. Render the results page with the remedies returned
        return render(request, 'index.html', {
            'results': results,
            'symptom': user_input
        })

    # ✅ If someone opens /result/ directly without POST
    return render(request, 'index.html', {
        'results': [],
        'symptom': ''
    })





# Create your views here.
