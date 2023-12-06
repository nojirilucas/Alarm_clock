import time
import threading
import os
import pygame

class AlarmClock:
    def __init__(self):
        self.is_running = False
        self.alarm_time = None
        self.alarm_thread = None
        self.audio_thread = None

    def set_alarm(self, hours, minutes):
        now = time.localtime()
        alarm_time = time.struct_time((now.tm_year, now.tm_mon, now.tm_mday, hours, minutes, 0, now.tm_wday, now.tm_yday, now.tm_isdst))
        self.alarm_time = time.mktime(alarm_time)

    def start(self):
        self.is_running = True
        self.alarm_thread = threading.Thread(target=self._run)
        self.alarm_thread.start()

    def stop(self):
        self.is_running = False
        if self.alarm_thread:
            self.alarm_thread.join()

    def _run(self):
        while self.is_running:
            current_time = time.time()
            if current_time >= self.alarm_time:
                self._start_alarm()
                break
            time.sleep(1)

    def _start_alarm(self):
        os.system("clear" if os.name == "posix" else "cls")  # Limpa o terminal
        ascii_art = """
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣥⣤⣾⠟⡛⠿⠿⣭⣻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⡟⣿⣽⡟⡏⢩⣦⡝⠋⢸⣶⠄⢲⡟⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣯⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣌⡳⣜⢿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢀⡛⢌⢿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠄⠙⠌⣸⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⡿⠉⠉⠉⠉⢿⣿⣿⣿⠏⠉⠉⠉⠉⠉⠆⠄⠁⠄⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⡗⠫⠿⠆⠄⠸⢿⣿⣿⠂⠒⠲⡿⠛⠛⠂⠄⠄⢠⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⡛⣧⡔⠢⠴⣃⣠⣼⣿⣧⡀⠘⢢⣀⠄⠄⠄⠄⢈⠁⢿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⠄⠄⠄⣸⠆⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⢿⣿⣿⣿⡀⠄⠘⡀⢠⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⡌⠿⣫⣿⣦⠬⢭⣥⣶⣬⣾⣿⢿⣿⡟⠄⢀⣿⣶⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣧⠘⣉⠛⢻⣛⣛⣛⣻⡶⠮⠙⠃⣉⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⣿⣿⣿⣿⣿⣿⡆⠸⣿⣶⢾⣿⣯⣤⣄⣀⣾⡟⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⠟⠿⠿⠿⠿⢿⣷⠄⣿⣿⣎⣹⢻⣿⣿⡿⡿⠁⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
        ⠄⠄⠄⠄⠄⠄⠄⣠⠘⣿⣿⣿⣿⣿⣿⡟⠁⣀⣀⣀⠄⠘⠿⣿⣿⣿⣿⣿⣿⣿⣿
        """

        print(ascii_art)

        # Inicia a reprodução do áudio em uma thread separada
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

        # Aguarde até a música terminar de tocar antes de continuar
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        # Encerra o programa quando a música termina
        self.is_running = False

    def _play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "/Exemplo/Caminho/a.mp3"))
        pygame.mixer.music.play()
        duration = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "/Exemplo/Caminho/a.mp3")).get_length()

        # Imprime "ALARME!" enquanto o áudio está tocando
        while pygame.mixer.music.get_busy():
            print("ALARME!", end="\r")
            time.sleep(1)

        # Quando a duração do áudio chega a 0, encerra o programa
        print("Tempo do áudio chegou a 0. Encerrando o programa.")
        self.is_running = False

if __name__ == "__main__":
    try:
        alarm_clock = AlarmClock()

        # Solicite ao usuário que insira a hora e os minutos para definir o alarme
        alarm_hours = int(input("Digite a hora do alarme (0-23): "))
        alarm_minutes = int(input("Digite os minutos do alarme (0-59): "))

        # Verifique se os valores inseridos são válidos
        if 0 <= alarm_hours <= 23 and 0 <= alarm_minutes <= 59:
            # Defina o alarme com base nos valores inseridos
            alarm_clock.set_alarm(alarm_hours, alarm_minutes)

            # Inicie o relógio
            alarm_clock.start()

            # Aguarde até o usuário interromper o programa
            input("Pressione Enter para parar o relógio.")
        else:
            print("Entrada inválida. Certifique-se de inserir uma hora entre 0 e 23 e minutos entre 0 e 59.")

    finally:
        # Certifique-se de parar o relógio antes de sair
        alarm_clock.stop()

