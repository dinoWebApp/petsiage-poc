import json
from typing import List
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
from .services.engine import analyze_diet, simulate_vision_api, generate_llm_commentary

def index(request: HttpRequest) -> HttpResponse:
    """메인 페이지 렌더링 (Step 0: AI 비전 분석부터 시작)"""
    return render(request, 'mealiq/index.html', {'step': 0})

def vision_analyze(request: HttpRequest) -> HttpResponse:
    """AI 비전 분석 시뮬레이션 (HTMX)"""
    # 실제 파일 처리 로직 (면접 시연용 시뮬레이션)
    pet_photo = request.FILES.get('pet_photo')
    
    # AI Vision 분석 지연 시뮬레이션 (사용자 경험 강화)
    time.sleep(1.5) 
    
    vision_result = simulate_vision_api(str(pet_photo))
    
    # 비전 결과를 세션이나 Hidden 필드로 전달
    context = {
        'step': 1,
        'vision_analysis': vision_result,
        'detected_info': f"{vision_result['detected_brand']} ({', '.join(vision_result['detected_ingredients'])})"
    }
    return render(request, 'mealiq/partials/step1.html', context)

def next_step(request: HttpRequest) -> HttpResponse:
    """스테퍼 단계 전환 (HTMX)"""
    step = int(request.POST.get('step', 1))
    next_step_val = step + 1
    
    context = {
        'step': next_step_val,
        'pet_name': request.POST.get('pet_name'),
        'breed': request.POST.get('breed'),
        'weight': request.POST.get('weight'),
        'activity': request.POST.get('activity'),
        'allergies': request.POST.get('allergies'),
        'vision_analysis': request.POST.get('vision_analysis'), # JSON string으로 전달 가정
    }
    
    template = f'mealiq/partials/step{next_step_val}.html'
    return render(request, template, context)

def analyze(request: HttpRequest) -> HttpResponse:
    """최종 AI 분석 및 대시보드 반환 (HTMX)"""
    pet_name = request.POST.get('pet_name', '무명')
    breed = request.POST.get('breed', 'Unknown')
    weight = float(request.POST.get('weight', 5.0))
    activity = request.POST.get('activity', 'normal')
    allergies_raw = request.POST.get('allergies', '')
    allergies = [a.strip() for a in allergies_raw.split(',')] if allergies_raw else []
    
    # 비전 데이터 복원 (간략화)
    vision_data = simulate_vision_api("mock_image") 
    
    # 엔진 호출 (v3: AI-Native)
    result = analyze_diet(weight, activity, allergies, vision_data)
    
    # LLM 코멘터리 보정 (실제 펫 이름과 견종 반영)
    result['ai_commentary'] = generate_llm_commentary(pet_name, breed, vision_data, result['recipes'][0]['name'])
    
    context = {
        'pet_name': pet_name,
        'result': result,
    }
    return render(request, 'mealiq/partials/dashboard.html', context)
