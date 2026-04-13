import base64, io
import pygame

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  스프라이트 시트 Base64 데이터
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SHEET_B64 = "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"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  설정
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCREEN_W, SCREEN_H = 480, 320
FRAME_W, FRAME_H   = 32, 32
COLS               = 8
FRAME_DELAY        = 150   # ms
DISPLAY_SCALE      = 4     # 화면 확대 배율

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Sprite Animation Demo")
clock = pygame.time.Clock()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  시트 로드 → 프레임 리스트
#  인덱스 0 ~ 31 (총 32개)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sheet_bytes = base64.b64decode(SHEET_B64)
player_sheet = pygame.image.load(io.BytesIO(sheet_bytes)).convert_alpha()

player_frames = []
for i in range(32):
    row, col = divmod(i, COLS)
    rect = pygame.Rect(col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H)
    player_frames.append(player_sheet.subsurface(rect))

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  walk_frames: 선택한 프레임 순서
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
walk_frames = [player_frames[i] for i in [0, 1, 2, 3, 4, 5, 6, 7]]

frame_index = 0
frame_timer = 0
x = SCREEN_W // 2 - (FRAME_W * DISPLAY_SCALE) // 2
y = SCREEN_H // 2 - (FRAME_H * DISPLAY_SCALE) // 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  게임 루프
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    frame_timer += dt
    if frame_timer >= FRAME_DELAY:
        frame_index = (frame_index + 1) % len(walk_frames)
        frame_timer = 0

    screen.fill((30, 30, 40))
    frame_img = pygame.transform.scale(
        walk_frames[frame_index],
        (FRAME_W * DISPLAY_SCALE, FRAME_H * DISPLAY_SCALE)
    )
    screen.blit(frame_img, (x, y))
    pygame.display.flip()

pygame.quit()
