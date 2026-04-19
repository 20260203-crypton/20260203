"""
Pixel Adventure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
background2.png 타일로 Sprite-0008 배치 재현
흰색 내부 영역(11×11 타일) 밖으로 플레이어 이동 불가

조작: 방향키 또는 WASD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import tkinter as tk

# ── 설정 ──────────────────────────────────────────────────────
SCALE    = 3       # 화면 확대 배율
TILE     = 16      # 타일 원본 크기 (px)

# Sprite-0008 구조: 13×13 타일 (테두리 1타일, 내부 11×11 흰색)
MAP_TILES_X = 13
MAP_TILES_Y = 13
BORDER_TILES = 1   # 테두리 두께 (타일 단위)

PLAYER_W = 16
PLAYER_H = 16
SPEED    = 1
FPS      = 60
TRANS    = "#010101"

# ── 총알 설정 ─────────────────────────────────────────────────
BULLET_SPEED    = 4          # 총알 속도 (픽셀/프레임, SCALE 적용 전)
BULLET_COOLDOWN = 0.5        # 연사 쿨다운 (초)
import math, time

# ── background 타일 픽셀 데이터 ───────────────────────────────
BG2_DATA = "{#767676 #777777 #7d7d7d #767676 #717171 #787878 #7d7d7d #757575 #797979 #727272 #808080 #727272 #7a7a7a #797979 #757575 #797979} {#7d7d7d #bababa #bbbbbb #747474 #c6c6c6 #b9b9b9 #b7b7b7 #c2c2c2 #bababa #b6b6b6 #bababa #7c7c7c #bababa #c2c2c2 #bababa #757575} {#717171 #b2b2b2 #b0b0b0 #6b6b6b #afafaf #b5b5b5 #afafaf #adadad #b2b2b2 #b3b3b3 #b2b2b2 #6c6c6c #b2b2b2 #a7a7a7 #b4b4b4 #787878} {#838383 #a7a7a7 #acacac #838383 #777777 #737373 #797979 #757575 #7c7c7c #adadad #b1b1b1 #7c7c7c #afafaf #b1b1b1 #b2b2b2 #747474} {#6f6f6f #7f7f7f #727272 #7e7e7e #b7b7b7 #b9b9b9 #bebebe #b7b7b7 #737373 #7a7a7a #747474 #747474 #b9b9b9 #aeaeae #a5a5a5 #7f7f7f} {#7c7c7c #b1b1b1 #858585 #a6a6a6 #b4b4b4 #b2b2b2 #b2b2b2 #bbbbbb #bbbbbb #c2c2c2 #b6b6b6 #727272 #afafaf #b1b1b1 #b3b3b3 #727272} {#797979 #bbbbbb #757575 #b5b5b5 #a8a8a8 #b3b3b3 #b2b2b2 #aeaeae #adadad #acacac #c2c2c2 #7c7c7c #b3b3b3 #a3a3a3 #aeaeae #7c7c7c} {#757575 #bfbfbf #7b7b7b #ababab #bcbcbc #a3a3a3 #b3b3b3 #afafaf #b4b4b4 #acacac #bdbdbd #757575 #aeaeae #b6b6b6 #b5b5b5 #757575} {#757575 #c0c0c0 #777777 #767676 #707070 #787878 #7e7e7e #b2b2b2 #b2b2b2 #b2b2b2 #bababa #7a7a7a #727272 #797979 #787878 #7d7d7d} {#797979 #bdbdbd #adadad #c4c4c4 #cbcbcb #b5b5b5 #717171 #b0b0b0 #aaaaaa #aaaaaa #bfbfbf #747474 #bbbbbb #bfbfbf #bbbbbb #6d6d6d} {#777777 #b3b3b3 #b4b4b4 #b2b2b2 #a8a8a8 #aeaeae #7b7b7b #b2b2b2 #b4b4b4 #b2b2b2 #bdbdbd #7b7b7b #b1b1b1 #aeaeae #b4b4b4 #7e7e7e} {#757575 #b0b0b0 #a7a7a7 #aeaeae #afafaf #b6b6b6 #797979 #777777 #757575 #777777 #6f6f6f #757575 #b6b6b6 #a8a8a8 #b1b1b1 #767676} {#797979 #b9b9b9 #aeaeae #b1b1b1 #b8b8b8 #a7a7a7 #797979 #bbbbbb #c1c1c1 #b2b2b2 #d0d0d0 #717171 #787878 #787878 #747474 #797979} {#7b7b7b #666666 #7a7a7a #808080 #676767 #808080 #767676 #aaaaaa #b1b1b1 #aeaeae #6c6c6c #7f7f7f #b9b9b9 #bfbfbf #c4c4c4 #737373} {#7f7f7f #b7b7b7 #c5c5c5 #b9b9b9 #c0c0c0 #b5b5b5 #7c7c7c #b5b5b5 #ababab #b7b7b7 #797979 #ababab #b9b9b9 #acacac #a9a9a9 #7b7b7b} {#707070 #818181 #707070 #7a7a7a #757575 #797979 #737373 #777777 #777777 #787878 #767676 #727272 #808080 #707070 #7b7b7b #797979}"

# 내부를 채울 background1 타일
BG1_DATA = "{#d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9} {#d5e2e9 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #fafafa #eef3f5 #d5e2e9} {#d5e2e9 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #eef3f5 #d5e2e9} {#d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9 #d5e2e9}"

# ── 플레이어 스프라이트 (4방향: 아래/왼쪽/오른쪽/위) ──────────
PLAYER_DATA = [
    "{#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #ac3232 #dad9be #dad9be #000000 #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #000000 #dad9be #dad9be #639bff #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101}",
    "{#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #dad9be #ac3232 #dad9be #dad9be #000000 #dad9be #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #dad9be #000000 #dad9be #dad9be #639bff #dad9be #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101}",
    "{#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #99e550 #9aaa8a #9aaa8a #9aaa8a #99e550 #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #9aaa8a #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #dad9be #ac3232 #dad9be #dad9be #000000 #dad9be #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #dad9be #000000 #dad9be #dad9be #639bff #dad9be #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101}",
    "{#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #000000 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #000000 #000000 #000000 #000000 #000000 #000000 #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #000000 #000000 #000000 #000000 #000000 #000000 #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #000000 #000000 #000000 #000000 #000000 #000000 #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101} {#010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #000000 #000000 #dad9be #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #000000 #dad9be #dad9be #000000 #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #dad9be #dad9be #dad9be #dad9be #dad9be #dad9be #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101} {#010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101 #010101 #010101 #000000 #010101 #010101 #010101 #010101}",
]

TRANS_PX = [[[0, 0], [1, 0], [2, 0], [13, 0], [14, 0], [15, 0], [0, 1], [1, 1], [14, 1], [15, 1], [0, 2], [1, 2], [14, 2], [15, 2], [0, 3], [1, 3], [14, 3], [15, 3], [0, 4], [1, 4], [14, 4], [15, 4], [0, 5], [1, 5], [14, 5], [15, 5], [0, 6], [1, 6], [14, 6], [15, 6], [0, 7], [1, 7], [14, 7], [15, 7], [0, 8], [1, 8], [2, 8], [13, 8], [14, 8], [15, 8], [0, 9], [1, 9], [2, 9], [3, 9], [12, 9], [13, 9], [14, 9], [15, 9], [0, 10], [1, 10], [2, 10], [3, 10], [12, 10], [13, 10], [14, 10], [15, 10], [0, 11], [1, 11], [2, 11], [3, 11], [12, 11], [13, 11], [14, 11], [15, 11], [0, 12], [1, 12], [2, 12], [3, 12], [12, 12], [13, 12], [14, 12], [15, 12], [0, 13], [1, 13], [2, 13], [3, 13], [12, 13], [13, 13], [14, 13], [15, 13], [0, 14], [1, 14], [2, 14], [3, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [12, 14], [13, 14], [14, 14], [15, 14], [0, 15], [1, 15], [2, 15], [3, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [12, 15], [13, 15], [14, 15], [15, 15]], [[0, 0], [1, 0], [2, 0], [13, 0], [14, 0], [15, 0], [0, 1], [1, 1], [14, 1], [15, 1], [0, 2], [1, 2], [14, 2], [15, 2], [0, 3], [1, 3], [14, 3], [15, 3], [0, 4], [1, 4], [14, 4], [15, 4], [0, 5], [1, 5], [14, 5], [15, 5], [0, 6], [1, 6], [14, 6], [15, 6], [0, 7], [1, 7], [14, 7], [15, 7], [0, 8], [1, 8], [2, 8], [13, 8], [14, 8], [15, 8], [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [13, 9], [14, 9], [15, 9], [0, 10], [1, 10], [2, 10], [3, 10], [4, 10], [13, 10], [14, 10], [15, 10], [0, 11], [1, 11], [2, 11], [3, 11], [4, 11], [13, 11], [14, 11], [15, 11], [0, 12], [1, 12], [2, 12], [3, 12], [4, 12], [13, 12], [14, 12], [15, 12], [0, 13], [1, 13], [2, 13], [3, 13], [4, 13], [13, 13], [14, 13], [15, 13], [0, 14], [1, 14], [2, 14], [3, 14], [4, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [11, 14], [13, 14], [14, 14], [15, 14], [0, 15], [1, 15], [2, 15], [3, 15], [4, 15], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [11, 15], [13, 15], [14, 15], [15, 15]], [[0, 0], [1, 0], [2, 0], [13, 0], [14, 0], [15, 0], [0, 1], [1, 1], [14, 1], [15, 1], [0, 2], [1, 2], [14, 2], [15, 2], [0, 3], [1, 3], [14, 3], [15, 3], [0, 4], [1, 4], [14, 4], [15, 4], [0, 5], [1, 5], [14, 5], [15, 5], [0, 6], [1, 6], [14, 6], [15, 6], [0, 7], [1, 7], [14, 7], [15, 7], [0, 8], [1, 8], [2, 8], [13, 8], [14, 8], [15, 8], [0, 9], [1, 9], [2, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], [0, 10], [1, 10], [2, 10], [11, 10], [12, 10], [13, 10], [14, 10], [15, 10], [0, 11], [1, 11], [2, 11], [11, 11], [12, 11], [13, 11], [14, 11], [15, 11], [0, 12], [1, 12], [2, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [0, 13], [1, 13], [2, 13], [11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [0, 14], [1, 14], [2, 14], [4, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [11, 14], [12, 14], [13, 14], [14, 14], [15, 14], [0, 15], [1, 15], [2, 15], [4, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15]], [[0, 0], [1, 0], [2, 0], [13, 0], [14, 0], [15, 0], [0, 1], [1, 1], [14, 1], [15, 1], [0, 2], [1, 2], [14, 2], [15, 2], [0, 3], [1, 3], [14, 3], [15, 3], [0, 4], [1, 4], [14, 4], [15, 4], [0, 5], [1, 5], [14, 5], [15, 5], [0, 6], [1, 6], [14, 6], [15, 6], [0, 7], [1, 7], [14, 7], [15, 7], [0, 8], [1, 8], [2, 8], [13, 8], [14, 8], [15, 8], [0, 9], [1, 9], [2, 9], [3, 9], [12, 9], [13, 9], [14, 9], [15, 9], [0, 10], [1, 10], [2, 10], [3, 10], [12, 10], [13, 10], [14, 10], [15, 10], [0, 11], [1, 11], [2, 11], [3, 11], [12, 11], [13, 11], [14, 11], [15, 11], [0, 12], [1, 12], [2, 12], [3, 12], [12, 12], [13, 12], [14, 12], [15, 12], [0, 13], [1, 13], [2, 13], [3, 13], [12, 13], [13, 13], [14, 13], [15, 13], [0, 14], [1, 14], [2, 14], [3, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [12, 14], [13, 14], [14, 14], [15, 14], [0, 15], [1, 15], [2, 15], [3, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [12, 15], [13, 15], [14, 15], [15, 15]]]

DIR_IDX = {"down": 0, "left": 1, "right": 2, "up": 3}


def make_bg_map():
    """
    Sprite-0008 구조 재현:
    13×13 타일 배치
    - 테두리(0행, 12행, 0열, 12열): background2 회색 타일
    - 내부(1~11행, 1~11열): background1 타일을 11×11로 반복 배치
    단, (6,0), (6,12), (0,6), (12,6) 위치는 검정(출입구)
    """
    tile_w = TILE * MAP_TILES_X
    tile_h = TILE * MAP_TILES_Y
    img = tk.PhotoImage(width=tile_w, height=tile_h)

    # BG2 타일 데이터 행 파싱
    bg2_rows = BG2_DATA.split("} {")
    bg2_rows[0]  = bg2_rows[0].lstrip("{")
    bg2_rows[-1] = bg2_rows[-1].rstrip("}")

    # BG1 타일 데이터 행 파싱
    bg1_rows = BG1_DATA.split("} {")
    bg1_rows[0]  = bg1_rows[0].lstrip("{")
    bg1_rows[-1] = bg1_rows[-1].rstrip("}")


    # 검정 행 (출입구)
    black_row = " ".join(["#111111"] * TILE)

    for ty in range(MAP_TILES_Y):
        for tx in range(MAP_TILES_X):
            x0 = tx * TILE
            y0 = ty * TILE

            is_border = (tx == 0 or tx == MAP_TILES_X - 1 or
                         ty == 0 or ty == MAP_TILES_Y - 1)
            is_entrance = (
                (tx == 6 and ty == 0) or
                (tx == 6 and ty == MAP_TILES_Y - 1) or
                (tx == 0 and ty == 6) or
                (tx == MAP_TILES_X - 1 and ty == 6)
            )

            for row_idx in range(TILE):
                if is_entrance:
                    row_data = "{" + black_row + "}"
                elif is_border:
                    row_data = "{" + bg2_rows[row_idx] + "}"
                else:
                    row_data = "{" + bg1_rows[row_idx] + "}"
                img.put(row_data, (x0, y0 + row_idx))

    return img


def make_player_photos():
    photos = {}
    for dir_name, idx in DIR_IDX.items():
        base = tk.PhotoImage(width=PLAYER_W, height=PLAYER_H)
        base.put(PLAYER_DATA[idx])
        for (x, y) in TRANS_PX[idx]:
            base.transparency_set(x, y, True)
        zoomed = base.zoom(SCALE, SCALE)
        photos[dir_name] = zoomed
    return photos


class Game:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Pixel Adventure")
        root.resizable(False, False)

        # 맵 크기 (픽셀)
        self.map_w = TILE * MAP_TILES_X * SCALE
        self.map_h = TILE * MAP_TILES_Y * SCALE

        # 캔버스 크기 = 맵 크기
        self.cw = self.map_w
        self.ch = self.map_h

        self.psz_w = PLAYER_W * SCALE
        self.psz_h = PLAYER_H * SCALE

        self.canvas = tk.Canvas(root, width=self.cw, height=self.ch,
                                bg="black", highlightthickness=0)
        self.canvas.pack()

        # 이미지 생성
        print("맵 생성 중... 잠시 기다려 주세요")
        root.update()
        bg_small = make_bg_map()
        self.bg_img = bg_small.zoom(SCALE, SCALE)
        self.player_photos = make_player_photos()

        # ── 총알 이미지 로드 ──────────────────────────────────────
        try:
            self.bullet_img = tk.PhotoImage(file="shoot.png").zoom(SCALE, SCALE)
        except Exception:
            # shoot.png 없으면 간단한 초록 점으로 대체
            self.bullet_img = tk.PhotoImage(width=4*SCALE, height=4*SCALE)
            self.bullet_img.put("#99e550", to=(0, 0, 4*SCALE, 4*SCALE))

        # 총알 리스트: [canvas_item_id, x, y, dx, dy]
        self.bullets = []
        self.last_shoot_time = 0.0

        # ── 이동 가능 영역 계산 ──────────────────────────────────
        # 내부 background1 영역: 타일 1번 ~ 11번 (0-indexed)
        # 픽셀 기준 (SCALE 적용 후)
        border_px = BORDER_TILES * TILE * SCALE
        self.bound_left   = border_px
        self.bound_top    = border_px
        self.bound_right  = self.map_w - border_px - self.psz_w
        self.bound_bottom = self.map_h - border_px - self.psz_h

        # 플레이어 시작 위치 (내부 중앙)
        inner_w = self.map_w - 2 * border_px
        inner_h = self.map_h - 2 * border_px
        self.px = float(border_px + inner_w // 2 - self.psz_w // 2)
        self.py = float(border_px + inner_h // 2 - self.psz_h // 2)
        self.direction = "down"

        self.keys = set()
        root.bind("<KeyPress>",   lambda e: self.keys.add(e.keysym))
        root.bind("<KeyRelease>", lambda e: self.keys.discard(e.keysym))

        # 캔버스 아이템
        self.bg_item = self.canvas.create_image(0, 0, anchor="nw",
                                                image=self.bg_img)
        self.player_item = self.canvas.create_image(0, 0, anchor="nw",
                                                    image=self.player_photos["down"])
        self._loop()

    def _loop(self):
        dt = 1000 // FPS
        self._update()
        self._render()
        self.root.after(dt, self._loop)

    def _update(self):
        k = self.keys
        spd = SPEED * SCALE
        dx = dy = 0
        prev = self.direction

        # ── WASD: 이동 ────────────────────────────────────────────
        if "w" in k or "W" in k: dy -= spd; self.direction = "up"
        if "s" in k or "S" in k: dy += spd; self.direction = "down"
        if "a" in k or "A" in k: dx -= spd; self.direction = "left"
        if "d" in k or "D" in k: dx += spd; self.direction = "right"

        # 내부 background1 영역 안에서만 이동 가능
        self.px = max(self.bound_left,  min(self.bound_right,  self.px + dx))
        self.py = max(self.bound_top,   min(self.bound_bottom, self.py + dy))

        if self.direction != prev:
            self.canvas.itemconfig(self.player_item,
                                   image=self.player_photos[self.direction])

        # ── 방향키: 총알 발사 (8방향) ─────────────────────────────
        shoot_dx = shoot_dy = 0
        if "Up"    in k: shoot_dy -= 1
        if "Down"  in k: shoot_dy += 1
        if "Left"  in k: shoot_dx -= 1
        if "Right" in k: shoot_dx += 1

        if shoot_dx != 0 or shoot_dy != 0:
            now = time.time()
            if now - self.last_shoot_time >= BULLET_COOLDOWN:
                self.last_shoot_time = now
                # 방향 정규화 (대각선은 1/√2 속도 보정)
                length = math.hypot(shoot_dx, shoot_dy)
                ndx = shoot_dx / length
                ndy = shoot_dy / length
                bspd = BULLET_SPEED * SCALE
                # 총알 생성 위치: 플레이어 중앙
                bx = self.px + self.psz_w / 2
                by = self.py + self.psz_h / 2
                item = self.canvas.create_image(
                    int(bx), int(by), anchor="center", image=self.bullet_img
                )
                self.bullets.append([item, bx, by, ndx * bspd, ndy * bspd])

        # ── 총알 이동 & 화면 밖 제거 ─────────────────────────────
        alive = []
        for b in self.bullets:
            item, bx, by, bdx, bdy = b
            bx += bdx
            by += bdy
            if 0 <= bx <= self.cw and 0 <= by <= self.ch:
                b[1], b[2] = bx, by
                self.canvas.coords(item, int(bx), int(by))
                alive.append(b)
            else:
                self.canvas.delete(item)
        self.bullets = alive

    def _render(self):
        self.canvas.coords(self.bg_item, 0, 0)
        self.canvas.coords(self.player_item, int(self.px), int(self.py))
        self.canvas.tag_raise(self.player_item)
        for b in self.bullets:
            self.canvas.tag_raise(b[0])


if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
