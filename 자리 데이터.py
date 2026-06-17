import streamlit as st
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>자리 이동 시스템</title>
  <style>
    body { font-family: sans-serif; }
    .seat { margin: 5px; padding: 10px; border: 1px solid #333; display: inline-block; cursor: pointer; }
    #history { margin-top: 20px; padding: 10px; border: 2px solid #aaa; }
  </style>
</head>
<body>

<h2>학생 자리 배치</h2>

<button onclick="shuffleSeats()">자리 섞기</button>

<div id="seats"></div>

<h3>학생 이전 자리 기록</h3>
<div id="history">학생을 클릭하세요</div>

<script>
const students = ["민수", "지훈", "서연", "유진", "하늘"];

// 현재 자리
let currentSeats = {};

// 이전 자리 기록
let seatHistory = {};

// 초기화
students.forEach(name => {
  seatHistory[name] = [];
});

// 자리 섞기
function shuffleSeats() {
  const shuffled = [...students].sort(() => Math.random() - 0.5);

  shuffled.forEach((student, index) => {
    const newSeat = index + 1;

    // 이전 자리 기록 저장
    if (currentSeats[student]) {
      seatHistory[student].push(currentSeats[student]);
    }

    currentSeats[student] = newSeat;
  });

  renderSeats();
}

// 화면 표시
function renderSeats() {
  const container = document.getElementById("seats");
  container.innerHTML = "";

  Object.keys(currentSeats).forEach(name => {
    const div = document.createElement("div");
    div.className = "seat";
    div.innerText = `${name} → ${currentSeats[name]}번`;

    div.onclick = () => showHistory(name);

    container.appendChild(div);
  });
}

// 이전 자리 보기
function showHistory(name) {
  const historyDiv = document.getElementById("history");

  const history = seatHistory[name];

  historyDiv.innerHTML = `
    <b>${name}</b>의 이전 자리:<br>
    ${history.length === 0 ? "기록 없음" : history.join(", ")}
  `;
}

// 최초 실행
shuffleSeats();
</script>

</body>
</html>
