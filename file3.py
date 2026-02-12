import os
import sys
import requests
import arcade

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 450
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"

class GameView(arcade.Window):
    def setup(self):
        self.c1 = 30.288758
        self.c2 = 60.026829
        self.c3 = 0.0033
        self.c4 = 0.003302
        self.keys_pressed = set()
        self.get_image()

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = '162f1a1a-c131-476b-839e-0dceb33ac0e2'
        ll_spn = f'll={self.c1},{self.c2}&spn={self.c3},{self.c4}'
        # Готовим запрос.

        map_request = f"{server_address}{ll_spn}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def on_update(self, delta_time):
        dx, dy = 0, 0
        f = False
        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            if self.c1 < 179.999:
                self.c1 -= 0.001
                f = True
        if arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            if self.c1 > -179.999:
                self.c1 += 0.001
                f = True
        if arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed:
            if self.c2 < 89.999:
                self.c2 += 0.001
                f = True
        if arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed:
            if self.c2 > -89.999:
                self.c2 += 0.001
                f = True
        if f:
            self.get_image()

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    # Удаляем за собой файл с изображением.
    os.remove(MAP_FILE)


if __name__ == "__main__":

    main()
