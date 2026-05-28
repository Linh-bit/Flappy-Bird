import pygame
import random
import os

pygame.init()

script_dir = os.path.dirname(os.path.abspath(__file__))

# =========================
# ÂM THANH
# =========================
pygame.mixer.init()
sound_enabled = True
jump_sound = None
die_sound = None
hit_sound = None
point_sound = None

sounds_dir = os.path.join(script_dir, "sounds")
os.makedirs(sounds_dir, exist_ok=True)

jump_sound_path = os.path.join(sounds_dir, "jump.wav")
die_sound_path = os.path.join(sounds_dir, "die.wav")
hit_sound_path = os.path.join(sounds_dir, "hit.wav")
point_sound_path = os.path.join(sounds_dir, "point.wav")


def load_sound(path, volume=0.6):
    if os.path.exists(path):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    print(f"Warning: sound file not found: {path}")
    return None

jump_sound = load_sound(jump_sound_path, 0.6)
die_sound = load_sound(die_sound_path, 0.6)
hit_sound = load_sound(hit_sound_path, 0.6)
point_sound = load_sound(point_sound_path, 0.6)

# =========================
# CÀI ĐẶT
# =========================

CHIEU_RONG = 800
CHIEU_CAO = 600
FPS = 60
CHIEU_CAO_ONG = 400

man_hinh = pygame.display.set_mode((CHIEU_RONG, CHIEU_CAO))
pygame.display.set_caption("Flappy Bird")

dong_ho = pygame.time.Clock()

font = pygame.font.SysFont("Comic Sans MS", 40)
font_menu = pygame.font.SysFont("Comic Sans MS", 60)
font_small = pygame.font.SysFont("Comic Sans MS", 30)

background = pygame.image.load(os.path.join(script_dir, "images/background.png")).convert()
background = pygame.transform.scale(background, (CHIEU_RONG, CHIEU_CAO))

ground = pygame.image.load(os.path.join(script_dir, "images/ground.png")).convert_alpha()
ground = pygame.transform.scale(ground, (1200, 100))

bird_img = pygame.image.load(os.path.join(script_dir, "images/bird.png")).convert_alpha()
bird_img = pygame.transform.scale(bird_img, (50, 50))

costumes = [bird_img]
new_costume_path = os.path.join(script_dir, "images/2.png")
if os.path.exists(new_costume_path):
    costumes.append(pygame.transform.scale(pygame.image.load(new_costume_path).convert_alpha(), (50, 50)))

pipe_img = pygame.image.load(os.path.join(script_dir, "images/pipe.png")).convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (80, CHIEU_CAO_ONG))

current_costume_index = 0
menu_costume_index = 0

# =========================
# TRẠNG THÁI MENU
# =========================

TRANG_THAI_MENU = "menu"
TRANG_THAI_CHOI = "choi"
TRANG_THAI_TRANG_PHUC = "trang_phuc"

MENU_CHOI = 0
MENU_TRANG_PHUC = 1

# =========================
# CHIM
# =========================

class Bird:
    def __init__(self, x, y, costume):
        self.x = x
        self.y = y
        self.van_toc = 0
        self.trong_luc = 0.5
        self.luc_nhay = -8
        self.anh = costume
        self.width = 50
        self.height = 50

    def nhay(self):
        self.van_toc = self.luc_nhay

    def cap_nhat(self):
        self.van_toc += self.trong_luc
        self.y += self.van_toc

    def ve(self):
        man_hinh.blit(self.anh, (self.x, self.y))

    def hitbox(self):
        return pygame.Rect(self.x + 8, self.y + 8, 34, 34)

# =========================
# ỐNG NƯỚC
# =========================

class Pipe:
    WIDTH = 80
    SPEED = 4

    def __init__(self, x):
        self.x = x
        self.khoang_trong = 180
        self.chieu_cao = random.randint(120, 350)
        self.da_cong_diem = False

    def cap_nhat(self):
        self.x -= self.SPEED

    def ve(self):
        ong_tren = pygame.transform.flip(pipe_img, False, True)
        man_hinh.blit(ong_tren, (self.x, self.chieu_cao - CHIEU_CAO_ONG))
        man_hinh.blit(pipe_img, (self.x, self.chieu_cao + self.khoang_trong))

    def va_cham(self, chim):
        hitbox_chim = chim.hitbox()
        rect_tren = pygame.Rect(self.x + 5, 0, self.WIDTH - 10, self.chieu_cao)
        rect_duoi = pygame.Rect(self.x + 5, self.chieu_cao + self.khoang_trong, self.WIDTH - 10, CHIEU_CAO)
        return hitbox_chim.colliderect(rect_tren) or hitbox_chim.colliderect(rect_duoi)

# =========================
# HÀM VẼ MENU
# =========================

def ve_menu_chinh(lua_chon):
    text_tieu_de = font_menu.render("FLAPPY BIRD", True, (255, 255, 0))
    man_hinh.blit(text_tieu_de, (200, 80))

    if lua_chon == MENU_CHOI:
        rect_choi_color = (255, 255, 255)
        rect_choi_border = (216, 191, 216)  # light purple
        text_choi_color = (50, 50, 50)
    else:
        rect_choi_color = (200, 200, 200)
        rect_choi_border = (120, 120, 120)
        text_choi_color = (80, 80, 80)

    rect_choi = pygame.Rect(250, 230, 300, 80)
    pygame.draw.rect(man_hinh, rect_choi_color, rect_choi, border_radius=30)
    pygame.draw.rect(man_hinh, rect_choi_border, rect_choi, 4, border_radius=30)
    text_choi = font_menu.render("Choi", True, text_choi_color)
    text_choi_rect = text_choi.get_rect(center=rect_choi.center)
    man_hinh.blit(text_choi, text_choi_rect)

    if lua_chon == MENU_TRANG_PHUC:
        rect_trang_phuc_color = (255, 255, 255)
        rect_trang_phuc_border = (216, 191, 216)  # light purple
        text_trang_phuc_color = (50, 50, 50)
    else:
        rect_trang_phuc_color = (200, 200, 200)
        rect_trang_phuc_border = (120, 120, 120)
        text_trang_phuc_color = (80, 80, 80)

    rect_trang_phuc = pygame.Rect(150, 340, 500, 80)
    pygame.draw.rect(man_hinh, rect_trang_phuc_color, rect_trang_phuc, border_radius=30)
    pygame.draw.rect(man_hinh, rect_trang_phuc_border, rect_trang_phuc, 4, border_radius=30)
    text_trang_phuc = font_menu.render("Trang phuc", True, text_trang_phuc_color)
    text_trang_phuc_rect = text_trang_phuc.get_rect(center=rect_trang_phuc.center)
    man_hinh.blit(text_trang_phuc, text_trang_phuc_rect)

    text_huong_dan = font_small.render("UP/DOWN Chon | SPACE Xac nhan", True, (255, 255, 102))
    man_hinh.blit(text_huong_dan, (150, 500))


def ve_man_hinh_trang_phuc():
    text_tieu_de = font_menu.render("Trang phuc", True, (0, 0, 0))
    text_tieu_de_rect = text_tieu_de.get_rect(center=(CHIEU_RONG // 2, 120))
    man_hinh.blit(text_tieu_de, text_tieu_de_rect)

    preview = costumes[menu_costume_index]
    preview_large = pygame.transform.scale(preview, (150, 150))
    preview_rect = preview_large.get_rect(center=(CHIEU_RONG // 2, 300))
    man_hinh.blit(preview_large, preview_rect)

    text_thong_bao = font_small.render(
        f"Costume {menu_costume_index + 1} / {len(costumes)}",
        True,
        (0, 0, 0)
    )
    man_hinh.blit(text_thong_bao, (CHIEU_RONG // 2 - text_thong_bao.get_width() // 2, 370))

    text_huong_dan = font_small.render("LEFT/RIGHT de thay doi | SPACE de chon", True, (0, 0, 0))
    text_huong_dan_rect = text_huong_dan.get_rect(center=(CHIEU_RONG // 2, 430))
    man_hinh.blit(text_huong_dan, text_huong_dan_rect)

    text_quay_lai = font_small.render("Nhan ESC de quay lai menu", True, (0, 0, 0))
    text_quay_lai_rect = text_quay_lai.get_rect(center=(CHIEU_RONG // 2, 470))
    man_hinh.blit(text_quay_lai, text_quay_lai_rect)

# =========================
# HÀM RESET GAME
# =========================

def reset_game():
    chim = Bird(150, 250, costumes[current_costume_index])
    danh_sach_ong = [Pipe(CHIEU_RONG)]
    diem = 0
    dem_ong = 0
    ground_x = 0
    game_over = False
    game_bat_dau = False
    return chim, danh_sach_ong, diem, dem_ong, ground_x, game_over, game_bat_dau

chim, danh_sach_ong, diem, dem_ong, ground_x, game_over, game_bat_dau = reset_game()

trang_thai = TRANG_THAI_MENU
lua_chon_menu = MENU_CHOI

ground_rect = pygame.Rect(0, CHIEU_CAO - 100, CHIEU_RONG, 100)

while True:
    dong_ho.tick(FPS)

    for su_kien in pygame.event.get():
        if su_kien.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if su_kien.type == pygame.KEYDOWN:
            if trang_thai == TRANG_THAI_MENU:
                if su_kien.key == pygame.K_UP:
                    lua_chon_menu = MENU_CHOI
                elif su_kien.key == pygame.K_DOWN:
                    lua_chon_menu = MENU_TRANG_PHUC
                elif su_kien.key == pygame.K_SPACE:
                    if lua_chon_menu == MENU_CHOI:
                        trang_thai = TRANG_THAI_CHOI
                        chim, danh_sach_ong, diem, dem_ong, ground_x, game_over, game_bat_dau = reset_game()
                    else:
                        trang_thai = TRANG_THAI_TRANG_PHUC
            elif trang_thai == TRANG_THAI_TRANG_PHUC:
                if su_kien.key == pygame.K_ESCAPE:
                    trang_thai = TRANG_THAI_MENU
                elif su_kien.key == pygame.K_LEFT:
                    menu_costume_index = max(0, menu_costume_index - 1)
                elif su_kien.key == pygame.K_RIGHT:
                    menu_costume_index = min(len(costumes) - 1, menu_costume_index + 1)
                elif su_kien.key == pygame.K_SPACE:
                    current_costume_index = menu_costume_index
                    trang_thai = TRANG_THAI_MENU
            elif trang_thai == TRANG_THAI_CHOI:
                if su_kien.key == pygame.K_SPACE:
                    if not game_bat_dau:
                        game_bat_dau = True
                        if jump_sound:
                            jump_sound.play()
                    elif not game_over:
                        chim.nhay()
                        if jump_sound:
                            jump_sound.play()
                if su_kien.key == pygame.K_r and game_over:
                    chim, danh_sach_ong, diem, dem_ong, ground_x, game_over, game_bat_dau = reset_game()
                if su_kien.key == pygame.K_ESCAPE:
                    trang_thai = TRANG_THAI_MENU
                    chim, danh_sach_ong, diem, dem_ong, ground_x, game_over, game_bat_dau = reset_game()

    if trang_thai == TRANG_THAI_CHOI and not game_over and game_bat_dau:
        chim.cap_nhat()
        dem_ong += 1

        if dem_ong >= 90:
            danh_sach_ong.append(Pipe(CHIEU_RONG))
            dem_ong = 0

        for ong in danh_sach_ong:
            ong.cap_nhat()
            if ong.x + Pipe.WIDTH < chim.x and not ong.da_cong_diem:
                diem += 1
                ong.da_cong_diem = True
                if point_sound:
                    point_sound.play()
            if ong.va_cham(chim):
                if not game_over:
                    if hit_sound:
                        hit_sound.play()
                game_over = True

        danh_sach_ong = [ong for ong in danh_sach_ong if ong.x > -100]

        if chim.hitbox().colliderect(ground_rect) or chim.y < -50 or chim.y + chim.height >= CHIEU_CAO - 100:
            if not game_over:
                if die_sound:
                    die_sound.play()
            game_over = True

        ground_x -= 4
        if ground_x <= -1200:
            ground_x = 0

    if trang_thai == TRANG_THAI_MENU:
        man_hinh.blit(background, (0, 0))
        ve_menu_chinh(lua_chon_menu)
    elif trang_thai == TRANG_THAI_TRANG_PHUC:
        man_hinh.blit(background, (0, 0))
        ve_man_hinh_trang_phuc()
    else:
        man_hinh.blit(background, (0, 0))
        for ong in danh_sach_ong:
            ong.ve()
        chim.ve()
        man_hinh.blit(ground, (ground_x, CHIEU_CAO - 100))
        man_hinh.blit(ground, (ground_x + 1200, CHIEU_CAO - 100))

        text_diem = font.render(str(diem), True, (255, 255, 255))
        man_hinh.blit(text_diem, (CHIEU_RONG // 2 - text_diem.get_width() // 2, 30))

        text_esc = font_small.render("ESC: Quay lai menu", True, (200, 200, 200))
        man_hinh.blit(text_esc, (550, 30))

        if not game_bat_dau:
            text_start = font.render("PRESS SPACE TO START", True, (255, 255, 255))
            man_hinh.blit(text_start, (140, 250))

        if game_over:
            text_over = font.render("GAME OVER", True, (255, 0, 0))
            text_restart = font.render("Nhan R de choi lai", True, (255, 255, 255))
            text_menu = font_small.render("Nhan ESC ve menu", True, (255, 255, 255))
            man_hinh.blit(text_over, (260, 220))
            man_hinh.blit(text_restart, (180, 300))
            man_hinh.blit(text_menu, (220, 370))

    pygame.display.update()
