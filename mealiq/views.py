import json
from typing import List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .services.engine import analyze_diet

def index(request: HttpRequest) -> HttpResponse:
    """메인 페이지 렌더링 (Step 1 포함)"""
    return render(request, 'mealiq/index.html', {'step': 1})

def next_step(request: HttpRequest) -> HttpResponse:
    """스테퍼 단계 전환 (HTMX)"""
    step = int(request.POST.get('step', 1))
    next_step_val = step + 1
    
    # 이전 단계 데이터 수집
    context = {
        'step': next_step_val,
        'pet_name': request.POST.get('pet_name'),
        'breed': request.POST.get('breed'),
        'weight': request.POST.get('weight'),
        'activity': request.POST.get('activity'),
        'allergies': request.POST.get('allergies'),
    }
    
    template = f'mealiq/partials/step{next_step_val}.html'
    return render(request, template, context)

def analyze(request: HttpRequest) -> HttpResponse:
    """최종 분석 및 대시보드 반환 (HTMX)"""
    pet_name = request.POST.get('pet_name', '무명')
    weight = float(request.POST.get('weight', 5.0))
    activity = request.POST.get('activity', 'normal')
    allergies_raw = request.POST.get('allergies', '')
    allergies = [a.strip() for a in allergies_raw.split(',')] if allergies_raw else []
    
    # 엔진 호출
    result = analyze_diet(weight, activity, allergies)
    
    context = {
        'pet_name': pet_name,
        'result': result,
    }
    return render(request, 'mealiq/partials/dashboard.html', context)
