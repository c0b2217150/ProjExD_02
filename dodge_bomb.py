import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900

delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
    # pg.K_0:(-5,-5),
    # pg.K_1:(+5,-5),
    # pg.K_2:(-5,+5),
    # pg.K_3:(+5,+5)

    # pg.K_UP and pg.K_LEFT:(-5,-5),
    # pg.K_UP and pg.K_RIGHT:(+5,-5),
    # pg.K_DOWN and pg.K_LEFT:(-5,+5),
    # pg.K_DOWN and pg.K_RIGHT:(+5,+5)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    be_img = pg.image.load("ex02/fig/6.png")
    be_img = pg.transform.rotozoom(be_img,0, 2.0)
    bb_img = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習１：赤い半径10の円を描く
    bb_rct = bb_img.get_rect()  # 練習１：爆弾SurfaceのRectを抽出する
    bb_rct.center = random.randint(0, WIDTH),random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習２：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    kk_direction = 0  # 初期向きは右, 追加の変数と画像をロード

    # Rectが画面内にあるかどうかを判定する関数
    def is_inside_screen(rect):
        return (
            0 <= rect.left <= WIDTH and
            0 <= rect.right <= WIDTH and
            0 <= rect.top <= HEIGHT and
            0 <= rect.bottom <= HEIGHT
        )

    # 爆弾のリストを生成
    bomb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bomb_imgs.append(bb_img)
    
    clock = pg.time.Clock()

    # こうかとんと爆弾の初期位置の設定
    kk_rect = kk_img.get_rect(topleft=(900, 400))
    bomb_rect = bomb_imgs[0].get_rect(topleft=(random.randint(0, WIDTH - bomb_imgs[0].get_width()), random.randint(0, HEIGHT - bomb_imgs[0].get_height())))

    while True:
        for event in pg.event.get():
            if kk_rect.colliderect(bomb_rect):
                kk_img_collision = pg.image.load("ex02/fig/8.png")
                kk_img_collision = pg.transform.rotozoom(kk_img_collision, 0, 3.0)
                screen.blit(bg_img, [0, 0])
                screen.blit(kk_img_collision, kk_rect.topleft)
                time = tmr // 50  # 1フレームが1/50秒
                text = font.render(f"Time: {time} seconds", True, (0, 0, 0))
                screen.blit(text, (700, 100))
                pg.display.update()
                pg.time.wait(1000)
                return
        
        

        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            return
            
        screen.blit(bg_img, [0, 0])
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
#------------------------------------------------
                
                if k == pg.K_RIGHT:
                    kk_direction = 0
                elif k == pg.K_UP:
                    kk_direction = 1
                elif k == pg.K_DOWN:
                    kk_direction = 2
                elif k == pg.K_LEFT:
                    kk_direction = 3
                elif k == (pg.K_UP and pg.K_LEFT):
                    kk_direction = 4
                elif k == (pg.K_UP and pg.K_RIGHT):
                    kk_direction = 5
                elif k == (pg.K_DOWN and pg.K_LEFT):
                    kk_direction = 6
                elif k == (pg.K_DOWN and pg.K_RIGHT):
                    kk_direction = 7
                

                
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # kk_directionに応じて画像を回転して表示

        if kk_direction == 0:  # 右向き
            rotated_kk_img = pg.transform.flip(kk_img, True, False)
        elif kk_direction == 1:  # 上向き
            rotated_kk_img = pg.transform.flip(pg.transform.rotate(kk_img, 90), False, True)
        elif kk_direction == 2:  # 下向き
            rotated_kk_img = pg.transform.flip(pg.transform.rotate(kk_img, 270), False, True)
        elif kk_direction == 3:  # 左向き
            rotated_kk_img = kk_img
        elif kk_direction == 4:  # 右上斜め
            rotated_kk_img = pg.transform.flip(pg.transform.rotate(kk_img, 45, False, True))
        elif kk_direction == 5:  # 左上斜め
            rotated_kk_img = pg.transform.rotate(kk_img, -45, False, True)
        elif kk_direction == 6:  # 右下斜め
            rotated_kk_img = pg.transform.flip(pg.transform.rotate(kk_img, -45), False, True)
        elif kk_direction == 7:  # 左下斜め
            rotated_kk_img = pg.transform.rotate(kk_img, 45, True, False)
        


        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        #screen.blit(kk_img, kk_rct)  # 練習３：こうかとんを移動させる
        screen.blit(rotated_kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        bb_rct.move_ip(vx, vy) 
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()