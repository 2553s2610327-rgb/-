<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>원망의 벽 - 자리바꾸기 리뷰</title>
    <style>
        /* 기본 배경 및 폰트 설정 (공포 컨셉) */
        body {
            background-color: #070000;
            background-image: radial-gradient(circle, #2b0000 0%, #000000 80%);
            color: #8b0000;
            font-family: '궁서', 'Gungsuh', serif;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* 화면 상단에서 피가 흐르는 효과 */
        .blood-drip-container {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 150px;
            display: flex;
            justify-content: space-around;
            z-index: -1;
        }

        .drop {
            width: 15px;
            background-color: #8b0000;
            border-radius: 0 0 10px 10px;
            animation: drip random(3s) infinite ease-in;
        }

        /* 피 흘러내리는 애니메이션 */
        @keyframes drip {
            0% { height: 10px; opacity: 1; }
            80% { opacity: 1; }
            100% { height: 150px; opacity: 0; }
        }

        /* 메인 컨테이너 */
        .container {
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: rgba(0, 0, 0, 0.7);
            border: 1px solid #4a0000;
            box-shadow: 0 0 20px #4a0000;
        }

        /* 으스스하게 깜빡이는 제목 */
        h1 {
            text-align: center;
            color: #ff0000;
            font-size: 3em;
            text-shadow: 2px 2px 5px #ff0000;
            animation: flicker 2s infinite alternate;
        }

        @keyframes flicker {
            0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
                text-shadow: 2px 2px 10px #ff0000, 0 0 20px #ff0000;
                opacity: 1;
            }
            20%, 24%, 55% {
                text-shadow: none;
                opacity: 0.3;
            }
        }

        p.desc {
            text-align: center;
            color: #a04040;
            font-size: 1.2em;
            margin-bottom: 40px;
            letter-spacing: 2px;
        }

        /* 폼(입력창) 디자인 */
        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-size: 1.2em;
            color: #ff3333;
        }

        input[type="text"], textarea {
            width: 100%;
            padding: 10px;
            background-color: #110000;
            border: 1px solid #8b0000;
            color: #ff6666;
            font-family: '궁서', 'Gungsuh', serif;
            box-sizing: border-box;
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #ff0000;
            box-shadow: 0 0 10px #ff0000;
        }

        textarea {
            resize: vertical;
            height: 150px;
        }

        /* 제출 버튼 */
        button {
            width: 100%;
            padding: 15px;
            background-color: #4a0000;
            color: #ffffff;
            font-family: '궁서', 'Gungsuh', serif;
            font-size: 1.5em;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
            text-shadow: 1px 1px 2px #000;
        }

        button:hover {
            background-color: #ff0000;
            box-shadow: 0 0 15px #ff0000;
            color: #000;
            text-shadow: none;
        }

        /* 리뷰(불만) 목록 디자인 */
        .review-list {
            margin-top: 50px;
        }

        .review-item {
            background-color: #0a0000;
            border-left: 5px solid #8b0000;
            padding: 15px;
            margin-bottom: 15px;
            position: relative;
        }

        .review-item::before {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="40" fill="rgba(139,0,0,0.05)"/></svg>') no-repeat right top;
            pointer-events: none;
        }

        .review-item h3 {
            margin: 0 0 10px 0;
            color: #ff4444;
        }

        .review-item p {
            margin: 0;
            line-height: 1.5;
            color: #cccccc;
        }
    </style>
</head>
<body>

    <!-- 피가 흐르는 효과를 위한 빈 div들 -->
    <div class="blood-drip-container">
        <div class="drop" style="animation-duration: 2s; height: 80px;"></div>
        <div class="drop" style="animation-duration: 3s; height: 120px;"></div>
        <div class="drop" style="animation-duration: 1.5s; height: 60px;"></div>
        <div class="drop" style="animation-duration: 4s; height: 140px;"></div>
        <div class="drop" style="animation-duration: 2.5s; height: 90px;"></div>
    </div>

    <div class="container">
        <h1>원망의 벽</h1>
        <p class="desc">...자리 배정의 저주를 이곳에 토해내십시오...</p>

        <!-- 불만 작성 폼 -->
        <div class="form-group">
            <label for="name">희생자 이름</label>
            <input type="text" id="name" placeholder="당신의 이름을 남기세요...">
        </div>
        <div class="form-group">
            <label for="curse">불만 및 저주 (개선점)</label>
            <textarea id="curse" placeholder="이 지옥 같은 시스템에 대해 말해보십시오... 무엇이 바뀌어야 합니까?"></textarea>
        </div>
        <button type="button">피로 물든 글 남기기</button>

        <!-- 기존 리뷰 목록 -->
        <div class="review-list">
            <h2 style="color: #660000; border-bottom: 1px solid #4a0000; padding-bottom: 10px;">기록된 저주들</h2>
            
            <div class="review-item">
                <h3>알고리즘은 악마다</h3>
                <p>왜 맨날 내 앞에는 키가 190인 녀석이 앉는 건가? 칠판이 보이지 않는다... 당장 랜덤 로직을 뜯어고쳐라...</p>
            </div>

            <div class="review-item">
                <h3>숨이 막힙니다</h3>
                <p>히터 바로 밑 자리에 3번 연속 배정되었습니다. 내 피부가 말라 비틀어지길 바라는 건가요? 자리 제외 기능 당장 만드세요.</p>
            </div>

            <div class="review-item">
                <h3>저주받은 4번 자리</h3>
                <p>그 자리에 앉은 사람들은 모두 시름시름 앓았습니다... 그 자리는 영구 결번으로 처리해주십시오...</p>
            </div>
        </div>
    </div>

</body>
</html>
