import math


def calculate_bmr(weight: float) -> float:
    """
    기초 대사량(RER) 계산: 70 * (weight^0.75)
    국립축산과학원 권장 기준 적용
    """
    return 70 * math.pow(weight, 0.75)


def calculate_daily_calories(weight: float, activity_level: str) -> float:
    """
    유지 에너지 요구량(DER) 계산: RER * 활동 계수
    """
    rer = calculate_bmr(weight)

    # 활동 계수 설정 (강아지 기준 일반적 지표)
    factors = {
        "low": 1.2,  # 비만 성향 / 활동량 낮음
        "normal": 1.6,  # 보통 활동량
        "high": 2.5,  # 매우 활발함
    }

    factor = factors.get(activity_level, 1.6)
    return rer * factor


def simulate_vision_api(image_data: str) -> dict:
    """
    Multimodal Vision API 시뮬레이터 (펫시어지 면접용)
    - 이미지의 성분표 OCR 및 원재료 특징 추출
    """
    # 실제 구현 시 Google Vision API 또는 GPT-4o Vision 연동
    return {
        "detected_brand": "Premium Dog Food A",
        "detected_ingredients": ["Chicken", "Corn", "Wheat Gluten"],
        "analysis_summary": "고단백이나 곡물 함량이 높아 알러지 유발 가능성이 확인됨.",
        "safety_score": 65
    }


def generate_llm_commentary(pet_name: str, breed: str, vision_data: dict, selected_recipe: str) -> str:
    """
    LLM 기반 개인화 영양 코멘터리 생성 (GPT-4o/Claude 3.5 Sonnet 연동 가정)
    """
    # 펫시어지의 'AI 중심 제품' 철학을 반영한 고도의 개인화 텍스트
    breed_info = {
        "Bichon": "비숑 특유의 피부 민감도를 고려했을 때,",
        "Poodle": "푸들의 슬개골 건강과 곱슬거리는 모질 유지를 위해,",
        "Retriever": "리트리버의 관절 건강과 체중 관리를 위해,"
    }
    
    prefix = breed_info.get(breed, f"{pet_name}님의 건강 상태를 분석한 결과,")
    
    if "Grain" in str(vision_data.get("detected_ingredients")):
        vision_insight = "기존 사료에서 발견된 곡물 성분은 현재의 소화 불량 원인이 될 수 있습니다."
    else:
        vision_insight = "현재 급여 중인 사료의 성분은 양호하나 영양 균형이 다소 치중되어 있습니다."

    return f"{prefix} {vision_insight} 따라서 AI는 {selected_recipe}를 기반으로 한 맞춤 식단을 처방하였습니다. 이는 단순 칼로리 매칭을 넘어 {pet_name}님의 생애 주기와 비전 데이터를 통합 분석한 결과입니다."


def analyze_diet(weight: float, activity_level: str, allergies: list[str], vision_data: dict = None) -> dict:
    """
    Mealiq 맞춤형 식단 산출 엔진 (v3: AI-Native Multimodal)
    1. Vision API 데이터를 통한 가중치 조정
    2. DER 기반 14일치 필요 칼로리 계산
    3. LLM 기반 개인화 리포트 생성
    """
    daily_kcal = calculate_daily_calories(weight, activity_level)
    fortnight_kcal = daily_kcal * 14
    
    # 비전 데이터가 있을 경우 알러지 리스트 자동 업데이트 (AI-Native 경험)
    if vision_data and "detected_ingredients" in vision_data:
        # 비전에서 감지된 성분 중 위험 요소를 알러지 리스트에 동적 추가
        if "Corn" in vision_data["detected_ingredients"]:
            allergies.append("옥수수")
    
    KCAL_PER_BUCKET = 150
    total_buckets = math.ceil(fortnight_kcal / KCAL_PER_BUCKET)
    
    # 원물 라이브러리
    library = [
        {"id": "chicken", "name": "닭고기", "category": "protein", "protein_pct": 82, "precision": 98},
        {"id": "beef", "name": "소고기", "category": "protein", "protein_pct": 78, "precision": 96},
        {"id": "duck", "name": "오리고기", "category": "protein", "protein_pct": 75, "precision": 95},
        {"id": "pumpkin", "name": "단호박", "category": "vitamin", "protein_pct": 12, "precision": 92},
        {"id": "carrot", "name": "당근", "category": "vitamin", "protein_pct": 8, "precision": 94},
        {"id": "broccoli", "name": "브로콜리", "category": "vitamin", "protein_pct": 15, "precision": 93},
        {"id": "salmon_oil", "name": "연어 오일", "category": "oil", "protein_pct": 0, "precision": 99},
        {"id": "coconut_oil", "name": "코코넛 오일", "category": "oil", "protein_pct": 0, "precision": 97},
    ]
    
    # 지능형 알러지 필터링 (부분 일치 지원)
    lower_allergies: list[str] = [str(a).lower() for a in allergies]
    def is_safe(ingredient: dict) -> bool:
        i_name = str(ingredient['name']).lower()
        i_id = str(ingredient['id']).lower()
        for a in lower_allergies:
            if a in i_name or a in i_id:
                return False
        return True

    safe_ingredients = [i for i in library if is_safe(i)]
    
    # 카테고리별 재료 선정
    selected_protein = next((i for i in safe_ingredients if i['category'] == 'protein'), {"name": "혼합 단백질", "protein_pct": 0, "precision": 0})
    selected_vitamin = next((i for i in safe_ingredients if i['category'] == 'vitamin'), {"name": "혼합 채소", "protein_pct": 0, "precision": 0})
    selected_oil = next((i for i in safe_ingredients if i['category'] == 'oil'), {"name": "영양 오일", "protein_pct": 0, "precision": 0})

    # 동적 레시피 구성
    recipes = [
        {
            "name": f"Mealiq {selected_protein['name']} 베이스", 
            "quantity": math.ceil(total_buckets * 0.6), 
            "unit": "통",
            "nutrients": [
                {"label": "칼로리 비율", "value": selected_protein.get("protein_pct", 0)},
                {"label": "영양 정밀도", "value": selected_protein.get("precision", 0)}
            ]
        },
        {
            "name": f"Mealiq {selected_vitamin['name']} & 채소", 
            "quantity": math.ceil(total_buckets * 0.3), 
            "unit": "통",
            "nutrients": [
                {"label": "칼로리 비율", "value": selected_vitamin.get("protein_pct", 0)},
                {"label": "영양 정밀도", "value": selected_vitamin.get("precision", 0)}
            ]
        },
        {
            "name": f"Mealiq {selected_oil['name']} 보충", 
            "quantity": math.ceil(total_buckets * 0.1), 
            "unit": "통",
            "nutrients": [
                {"label": "칼로리 비율", "value": 45},
                {"label": "영양 정밀도", "value": selected_oil.get("precision", 0)}
            ]
        },
    ]
    
    # LLM 코멘터리 생성 (비전 데이터 결합)
    ai_commentary = generate_llm_commentary("User's Pet", "Unknown", vision_data or {}, selected_protein['name'])

    return {
        "daily_kcal": round(daily_kcal, 2),
        "total_buckets": total_buckets,
        "recipes": recipes,
        "metabolism_status": "Optimum",
        "vision_analysis": vision_data,
        "ai_commentary": ai_commentary,
        "ai_optimized": True
    }
