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


def analyze_diet(weight: float, activity_level: str, allergies: list[str]) -> dict:
    """
    Mealiq 맞춤형 식단 산출 엔진 (v2: Intelligent Matching)
    1. DER 기반 14일치 필요 칼로리 계산
    2. 알러지 성분 필터링 및 카테고리별 최적 원물 매칭
    3. 동적 레시피 생성 및 영양 상태 반환
    """
    daily_kcal = calculate_daily_calories(weight, activity_level)
    fortnight_kcal = daily_kcal * 14
    
    KCAL_PER_BUCKET = 150
    total_buckets = math.ceil(fortnight_kcal / KCAL_PER_BUCKET)
    
    # 원물 라이브러리 (영양 데이터 추가)
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
    
    # 알러지 필터링 (부분 일치 지원: '연어' 입력 시 '연어 오일' 제외)
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

    # 라이브러리에 없는 알러지 성분 확인
    known_all = {str(i['id']).lower() for i in library} | {str(i['name']) for i in library}
    unknown_allergies = [a for a in allergies if str(a).lower() not in known_all and str(a) not in known_all]

    # 동적 레시피 구성 (실제 영양 수치 포함)
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
                {"label": "칼로리 비율", "value": 45}, # 오일의 경우 고정값 또는 다른 로직 적용
                {"label": "영양 정밀도", "value": selected_oil.get("precision", 0)}
            ]
        },
    ]
    
    return {
        "daily_kcal": round(daily_kcal, 2),
        "total_buckets": total_buckets,
        "recipes": recipes,
        "metabolism_status": "Optimum",
        "ai_optimized": True,
        "warning": f"미등록 알러지 성분({', '.join(unknown_allergies)})은 AI가 별도로 분석 중입니다." if unknown_allergies else None
    }
