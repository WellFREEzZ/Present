import os.path
import pygame as pg
import cv2
from numba import njit
from moviepy.editor import VideoFileClip
import settings
import datetime as dt


@njit(fastmath=True)
def accelerate_conversion(image, w, h, char_indices, step):
    array_of_values = []
    for x in range(0, w, step):
        for y in range(0, h, step):
            char_index = char_indices[x, y]
            if char_index:
                array_of_values.append((char_index, (x, y)))
    return array_of_values


class ArtConverter:
    def __init__(self, name='input.mp4', font_size=settings.font_size, threshold=settings.threshold):
        pg.init()
        self.work = True
        self.record = False
        self.threshold = threshold
        self.name = name
        self.path = os.path.join(settings.input_dir, name)
        self.capture = cv2.VideoCapture(self.path)
        self.image = self.get_image()
        if not self.work:
            return
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()

        self.ASCII_CHARS = ' `.,:;!"~-+*xmo#W&8@'
        self.ASCII_KOEFF = 255 // (len(self.ASCII_CHARS) - 1)

        self.font = pg.font.SysFont('Courer', font_size, bold=True)
        if font_size > 12:
            self.step_koeff = 0.9
        elif font_size > 7:
            self.step_koeff = 0.8
        else:
            self.step_koeff = 1
        self.CHAR_STEP = int(font_size * self.step_koeff)
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]

        self.m_vid = VideoFileClip(self.path)
        if self.m_vid.audio:
            self.m_vid.audio.set_fps(self.capture.get(cv2.CAP_PROP_FPS))
            self.m_vid.audio.write_audiofile(os.path.join(settings.audio_dir, name.replace('mp4', 'mp3')))
            pg.mixer.music.load(os.path.join(settings.audio_dir, name.replace('mp4', 'mp3')))

        self.rec_fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.recorder = None

    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        return cv2.transpose(frame)

    def record_frame(self):
        if self.record:
            if self.recorder is None:
                self.recorder = cv2.VideoWriter(os.path.join(settings.output_dir, self.name), cv2.VideoWriter_fourcc(*'mp4v'), self.rec_fps, self.RES)
            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow('Recording... (Hold "Esc" for stop)', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                self.record = not self.record
                cv2.destroyAllWindows()

    def draw_converted_image(self):
        self.image = self.get_image()
        if self.image is not None:
            char_indices = self.image // self.ASCII_KOEFF - self.threshold
            array_of_values = accelerate_conversion(self.image, self.WIDTH, self.HEIGHT, char_indices, self.CHAR_STEP)
            for char_index, (x, y) in array_of_values:
                if char_index < len(self.RENDERED_ASCII_CHARS):
                    self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (x, y))
        else:
            self.end()

    def end(self):
        cv2.destroyAllWindows()
        if self.record:
            self.record = not self.record
        pg.quit()
        self.work = False

    def get_image(self):
        ret, self.cv2_image = self.capture.read()
        if not ret:
            self.end()
        else:
            transposed_img = cv2.transpose(self.cv2_image)
            gray_img = cv2.cvtColor(transposed_img, cv2.COLOR_BGR2GRAY)
            return gray_img

    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        print(f'writing {self.name.replace(".mp4", "")}_{dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg')
        cv2.imwrite(os.path.join(settings.output_dir, f'{self.name.replace(".mp4", "")}_{dt.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg'), cv2_img)
        print('done!')

    def run(self):
        pg.mixer.music.set_volume(0.1)
        while self.work:
            self.clock.tick(self.capture.get(cv2.CAP_PROP_FPS) + 0.5)
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    self.end()
                    return
                elif i.type == pg.KEYDOWN:
                    if i.key == pg.K_s:
                        self.save_image()
                    if i.key == pg.K_r:
                        self.record = not self.record
                    if i.key == pg.K_ESCAPE:
                        self.end()
                        return
            if self.work:
                self.record_frame()
                self.draw()
                pg.display.set_caption(str(self.clock.get_fps()))
                pg.display.flip()
                if not pg.mixer.music.get_busy() and self.m_vid.audio is not None:
                    pg.mixer.music.play(start=1)


if __name__ == '__main__':
    app = ArtConverter()
    app.run()
