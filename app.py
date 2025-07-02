
from flask import Flask, jsonify, render_template
import random
import json

app = Flask(__name__)

# 점수 및 상태 초기화
state = {
    "score": 0,
    "prev_score": 0
}

# 점수 기반 성장 단계 계산 함수
def calculate_stage(score):
    if score <= 0:
        return 1
    elif score <= 10:
        return 2
    elif score <= 20:
        return 3
    elif score <= 30:
        return 4
    elif score <= 40:
        return 5
    elif score <= 50:
        return 6
    elif score <= 60:
        return 7
    elif score <= 80:
        return 8
    elif score <= 90:
        return 9
    elif score <= 99:
        return 10
    else:
        return 11

# 멘트 불러오기
with open("data/messages.json", encoding="utf-8") as f:
    MESSAGES = json.load(f)

# 점수 증가
def increase_score(amount):
    state["prev_score"] = state["score"]
    state["score"] += amount
    if state["score"] > 100:
        state["score"] = 100

# 점수 감소
def decrease_score(amount):
    state["prev_score"] = state["score"]
    state["score"] -= amount
    if state["score"] < 0:
        state["score"] = 0

# 홈 라우트 (프론트 페이지)
@app.route("/")
def home():
    return render_template("index.html")

# 현재 성장 단계와 점수
@app.route("/get_growth")
def get_growth():
    stage = calculate_stage(state["score"])
    if stage == 11:
        # 죽었을 때 초기화
        state["score"] = 0
        state["prev_score"] = 0
        return jsonify({
            "stage": 1,
            "score": 0,
            "message": "새 씨앗을 입양하셔야 합니다"
        })
    return jsonify({
        "stage": stage,
        "score": state["score"]
    })

# 물 주기 (점수 증가 + 멘트)
@app.route("/get_water")
def get_water():
    increase_score(5)
    return jsonify({
        "message": random.choice(MESSAGES["water"])
    })

# 햇빛 주기 (점수 증가 + 멘트)
@app.route("/get_sunlight")
def get_sunlight():
    increase_score(5)
    return jsonify({
        "message": random.choice(MESSAGES["sunlight"])
    })

# 기분 멘트 (감소 시엔 나쁜 멘트만)
@app.route("/get_mood")
def get_mood():
    stage = calculate_stage(state["score"])
    if state["score"] < state["prev_score"]:
        # 점수 감소 → 기분 나쁨 필터
        filtered = [m for m in MESSAGES["mood"] if "윤라고동" in m or "시련" in m or "빛 부족" in m or "없었으면" in m or "삐침" in m]
        msg = random.choice(filtered) if filtered else random.choice(MESSAGES["mood"])
    else:
        msg = random.choice(MESSAGES["mood"])
    return jsonify({
        "message": msg,
        "stage": stage,
        "score": state["score"]
    })

# 서버 실행
if __name__ == "__main__":
    app.run(debug=True, port=5001)
