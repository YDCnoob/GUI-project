import csv
from pathlib import Path


# ==============================
# 장수 CSV 경로
# ==============================

DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "general.csv"
)


# ==============================
# 장수 데이터 로드
# ==============================

def load_officers():
    officers = []

    with DATA_PATH.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            officer = {
                "id": int(row["id"]),
                "name": row["이름"].strip(),
                "faction": row["소속 국가"].strip(),
                "leadership": int(row["통솔"]),
                "war": int(row["무력"]),
                "intelligence": int(row["지력"]),
                "politics": int(row["정치"]),

                # 현재 CSV에는 매력 데이터가 없음
                "charisma": None,
            }

            officers.append(officer)

    return officers


officers = load_officers()


# ==============================
# ID 검색용 딕셔너리
# ==============================

officers_by_id = {
    officer["id"]: officer
    for officer in officers
}


# ==============================
# ID로 장수 찾기
# ==============================

def find_officer_by_id(officer_id):
    return officers_by_id.get(officer_id)


# ==============================
# 이름으로 장수 찾기
# 기존 코드 호환용
# ==============================

def find_officer(name):
    for officer in officers:
        if officer["name"] == name:
            return officer

    return None


# ==============================
# 세력별 장수
# ==============================

def get_officers_by_faction(faction):
    return [
        officer
        for officer in officers
        if officer["faction"] == faction
    ]

# ==============================
# 도시 세력
# 아직 city가 이름 기반이므로 유지
# ==============================

def get_city_faction(city):
    governor_name = city["governor"]

    if not governor_name:
        return None

    governor = find_officer(governor_name)

    if governor is None:
        return None

    return governor["faction"]


# ==============================
# 장수 세력
# 기존 이름 기반 함수
# ==============================

def get_faction(name):
    officer = find_officer(name)

    if officer is None:
        return None

    return officer["faction"]


# ==============================
# 임명 가능한 통치자
# 아직 city가 이름 기반이므로 유지
# ==============================

def get_available_governors(
    cities,
    faction,
):

    used_governors = [
        city["governor"]
        for city in cities
        if city["governor"]
    ]

    return [
        officer
        for officer in officers
        if officer["faction"] == faction
        and officer["name"] not in used_governors
    ]