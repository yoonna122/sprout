
let score = 0;
let stage = 1;
let moodTimer;

const scoreDisplay = document.getElementById("score-display");
const speechBubble = document.getElementById("speech-bubble");
const plantImg = document.getElementById("plant-img");
const waterBtn = document.getElementById("water-btn");
const sunlightBtn = document.getElementById("sunlight-btn");

function updateScoreDisplay(newScore) {
  scoreDisplay.textContent = `점수: ${newScore}`;
}

function updatePlantImage(stage) {
  plantImg.src = `/static/images/plant_${stage}_stage.png`;
}

function updateSpeechBubble(msg) {
  speechBubble.textContent = msg;
}

function setMoodMessage() {
  fetch("/get_mood")
    .then(res => res.json())
    .then(data => {
      updateSpeechBubble(data.message);
      updatePlantImage(data.stage);
      updateScoreDisplay(data.score);
    });
}

function setTemporaryMessage(endpoint) {
  fetch(endpoint)
    .then(res => res.json())
    .then(data => {
      updateSpeechBubble(data.message);
      clearTimeout(moodTimer);
      moodTimer = setTimeout(setMoodMessage, 30000);
    });
}

function refreshGrowth() {
  fetch("/get_growth")
    .then(res => res.json())
    .then(data => {
      updatePlantImage(data.stage);
      updateScoreDisplay(data.score);
      if (data.message) {
        updateSpeechBubble(data.message);
      }
    });
}

waterBtn.addEventListener("click", () => {
  setTemporaryMessage("/get_water");
  refreshGrowth();
});

sunlightBtn.addEventListener("click", () => {
  setTemporaryMessage("/get_sunlight");
  refreshGrowth();
});

// 초기 로딩 시
refreshGrowth();
setMoodMessage();
moodTimer = setInterval(setMoodMessage, 1800000); // 30분마다 기분 업데이트
