#6주차 실습노트

## 목표 
무적 프레임과 화면 흔들기 기법 적용하기

## AI와의 대화
Q1. 내 게임에서 보스가 등장할때 화면 흔들기 기법을 적용하고 싶어 어떻게 적용해야할까?
    (파일 제시), (화면 흔들기 기법 핵심 구조 제시)

AI 답변: 1단계: shake 변수 추가 (overlay_items 선언 바로 뒤)Add shake state variables to __init__Add shake state variables to __init__Add shake state variables to __init__game.py+6-1완료  
         2단계: trigger_shake / get_shake_offset 메서드 추가 (_calc_spawn_points 앞에)Add shake helper methodsAdd shake helper methodsAdd shake helper methodsgame.py+15-1완료  
         3단계: _render에서 오프셋 적용Apply shake offset in _renderApply shake offset in _renderApply shake offset in _rendergame.py+5-3완료  
         4단계: 몬스터/총알/보스도 오프셋 반영 — _render의 tag_raise 부분과 Monster/Boss의 sync 위치를 찾아 오프셋을 넘깁니다.실제로는 tkinter에서 모든 아이템 개별 이동보다 캔버스 자체를 이동하는 게 훨씬 깔끔합니다. canvas.move("all", dx, dy) 패턴을 사용하겠습니다.Revamp _render to use canvas.move("all") for shake - cleaner approachRevamp _render to use canvas.move("all") for shake - cleaner approachRevamp _render to use canvas.move("all") for shake - cleaner approachgame.py+14-5완료  
         5단계: 보스 등장 시 흔들기 트리거Trigger shake on boss spawnTrigger shake on boss spawn6단계: 플레이어가 보스 총알에 맞을 때도 흔들기 — 보스 총알 충돌 처리 부분 찾기


Q2. 내 게임에 이미 무적 프레임 기능이 넣어져 있는데 이 두 코드의 차이가 뭐야? 
     (내 게임 파일 무적프레임 코드 제시), (PPT속 무적 프레임 코드 제시)

AI 답변: 핵심 차이 정리
슬라이드 방식내 게임 방식무적 지속 측정프레임 카운터 (timer -= 1)실제 시간 (time.time())FPS 영향FPS가 낮으면 무적 시간이 길어짐FPS와 무관하게 항상 정확히 2초깜빡임 속도timer // 4 % 2 → 4프레임 단위remaining * 10 % 2 → 초당 10회 고정상태 변수invincible = True/Falseinvincible_until 시각 하나로 처리
요약하면, 내 게임이 더 정교한 방식이에요. 슬라이드의 방식은 FPS가 흔들리면 무적 시간도 같이 흔들리지만, 내 게임은 time.time()으로 실제 시계를 쓰기 때문에 어떤 환경에서도 정확히 2초가 보장됩니다.

Q3. 내 게임에 너가 만든 화면 흔들기 효과와 PPT자료속 핵심코드 이 두 코드의 차이가 뭐야?
    (내 게임 파일 내 화면 흔들기 코드 제시), (PPT속 화면 흔들기 코드 제시)

AI 답변: 핵심 차이 정리
슬라이드 방식내 게임 방식변수 수shake_amount 1개duration + intensity 2개흔들림 감쇠매 프레임 세기가 줄어듦 (자연스럽게 약해짐)세기 고정, 지속 프레임만 줄어듦연속 피격 처리새 값으로 덮어씀max()로 더 긴 쪽을 유지느낌점점 잦아드는 진동일정 세기로 흔들리다 뚝 끊김
요약하면, 슬라이드 방식은 amount가 세기이자 타이머를 겸하므로 흔들림이 자연스럽게 약해지는 반면, 내 게임은 duration과 intensity를 분리해서 세기는 일정하게 유지하되 연속 피격 시 max()로 흔들기가 씹히지 않도록 처리한 게 더 세련된 부분이에요.
