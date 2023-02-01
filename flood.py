from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import random
# sensors
hub = PrimeHub()
motor_pair_odin = MotorPair('F', 'A')
motor_pair_dva = MotorPair('B', 'E')
distance = DistanceSensor('C')
force = ForceSensor('D')
# consts -> pypy.wlr
push_mod = True
init_required = False
is_up = False
# tips for admin
tips = [
    "update.thesb0pybot-api.kro.kr에서 이 프로그램에 대한 무료 업데이트를 받을 수 있습니다.",
    "ko-script.thesb0pybot-api.kro.kr에서 이 프로그램의 한국어 스크립트를 확인 할 수 있습니다. (Default: Russian)",
    "ForceSensor(을)를 너무 강하게 누르지 마세요. 너무 강하게 누르면, 모드 변경이 실행됩니다.",
    "ForceSensor(을)를 눌러 모드를 바꿔보세요. 모드를 다시 되돌리기 위해서는 ForceSensor(을)를 다시 한번 꾹 누르시면 됩니다.",
    "허브가 올라가는 기준이 되는 거리는 기본적으로는 20cm 반경이지만, setting.hub_up_distance 값을 수정해 그 값을 바꿀 수 있습니다",
    "거리에 관한 모든 값은 음수일 경우, 0으로 초기화 되고, 200 초과일 경우 200으로 재설정됩니다.",
    "허브를 올릴때 사용하는 모터는, 4개가 동시에 움직이는 것이 아닌, 모터 2개씩 2 쌍을 이루어 작동하고 있습니다.",
    "DistanceSensor(이)가 감지하기까지 최대 5초가 걸릴 수 있습니다.",
    "기본적으로 프로그램이 정지(sleep, delay)상태일 경우, 정지 해제까지 남은 시간을 디스플레이로 표시합니다.",
    "시간에 대한 모든 값들은, 19초 이하 0초 이상이어야만 합니다.",
    "시간에 대한 모든 값들은, 특별한 경우를 제외하고, 음수면 0초로, 20초 이상이면 19초로 재설정됩니다.",
    "print 함수와 달리, 저희가 직접 작성한 printf 함수는 문자열을 오직 하나만 출력할 수 있습니다.",
    "printf는 같은 내용의 문자열이 중복 표시되는것을 방지하는 효과가 있습니다.",
    "프로그램을 너무 오래 실행하면, 여러 지역 변수로 인해, 프로그램 속도가 매우 느려질 수 있습니다. 적당한 시간 동안만 사용하는 것을 권장합니다.",
    "이 프로그램은, 색 관련 변수 값의 검증 과정이 없습니다.",
    "setting.motor_pair_mo 값을 수정해, 모터가 한번 움직일 때, 얼마나 회전할 지 설정할 수 있답니다.",
    "프로그램 내부에서는 True는 setting.true로, False은 setting.false로 표현합니다.",
    "허브의 상태 색은, 프로그램 상태에 따라 바뀝니다.",
    "노란색 상태 등은, 현재 기본 상태, 즉, 프로그램이 아무것도 처리하지 않고 있다는 의미입니다",
    "주황색 상태 등은, 특정 반경 안에, 어떠한 객체가 접근했음을 의미합니다. 이 상태등의 우선순위는 기본 상태등보다 높습니다."
    "초록색 상태 등은, 허브가 내려가고 있다는 의미입니다!",
    "빨간색 상태 등은, 허브가 올라가고 있다는 의미입니다!",
    "setting.undefined는 None과 동일한 값입니다. 그저 개발자가 JavaScript에 익숙할 뿐이에요",
    "setting.hub_beep_standard를 수정해, 허브가 올라가거나, 내려갈 때, 혹은 에러 발생 시 발생하는 비프음의 기본값을 설정할 수 있습니다",
    "setting.motor_stdunit을 수정해, 모터가 움직일 때 사용할 단위를 변경할 수 있습니다. 기본 값은 cm입니다.",
    "setting.safe_distance는, Mode가 Push Mode인 이상은 절대 사용될 일이 없습니다. 사실 v1.1.3 부터 사용하지 않는 데이터입니다.",
    "만약 인터넷이 가능하고, 당신이 파이썬에 익숙하다면, thesb0pybot-api.kro.kr에서 세팅 데이터를 받아올 수 있습니다",
    "모든 버전 기록은 olds.thesb0pybot-api.kro.kr에서 확인 할 수 있습니다.",
    "ForceSensor(을)를 눌러 모드를 바꾸면, None-Push Mode, Push Mode 순으로 연속해 변경됩니다."
]
# settings for non-programmers
setting = {
    "zero": 0,
    "safe_distance":40,
    "warning_distance": 30,
    "hub_up_distance": 20,
    "hub_up_steps": 7,
    "hub_beep_standard": 84,
    "beep_stddur": 0.5,
    "motor_stdunit": 'cm',
    "hub_down_newton": 5,
    "force_down_percentage": 50,
    "default_color": 'yellow',
    "hub_up_color": 'red',
    "hub_warning_color": 'orange',
    "hub_down_color": 'green',
    "motor_pair_mo": 1,
    "undefined": None,
    "true": True,
    "false": False
}
# this uses in printf function (def printf)
messages_list = ["INIT_DEVELOPER"]
# class Flood for fun. function is fun (in kt hah!)
class Flood:
    def __init__(self, hub:PrimeHub):
        self.hub = hub
        self.is_up = setting["false"]
    # light method controls status_light of hub
    def light(self, color: str) -> bool:
        if not color:self.hub.status_light.on(setting["default_color"])
        else:self.hub.status_light.on(color)
        return setting["true"]
    # static method tip returns random values in tips!
    @staticmethod
    def tip() -> str:
        return random.choice(tips)
    # static method msgs returns list[str] type(messages_list!)
    @staticmethod
    def msgs() -> list[str]:
        return messages_list
    # static method last_msg returns last values of Flood.msgs() (-> messages_list)
    @staticmethod
    def last_msg() -> str:
        return Flood.msgs()[-1]
    # static method add_msg adds message type in messages_list!
    @staticmethod
    def add_msg(message_code: str = "NULL") -> bool:
        messages_list.append(message_code)
        return setting["true"]
    # static method display_wait is display times in screen
    @staticmethod
    def display_wait(dur: int) -> bool:
        for i in range(dur, 0, -1):
            hub.light_matrix.write(i) # non-tested method
            wait_for_seconds(1)
        return setting["true"]
    # static method wait calls Flood.display_wait in inside of code
    @staticmethod
    def wait(dur: int) -> bool:
        Flood.display_wait(dur)
        return setting["true"]
    # set Flood.is_up variable
    def set_is_up(self, value: bool) -> bool:
        if value == self.is_up: return setting["false"]
        self.is_up = value
        return setting["true"]
    # check hub is upable
    def upable(self) -> bool:
        if self.is_up: return setting["false"]
        return setting["true"]
# most important of this program! printf function
# printf function requires 2 params. must give message params
def printf(message: str, message_code: str = "NULL") -> bool:
    if message_code == Flood.last_msg(): return setting["false"]
    print(message)
    Flood.add_msg(message_code)
    return setting["true"]
# intro and initing process
distance.light_up_all() # горит датчик расстояния!
hub.status_light.on(setting["default_color"])
printf("Это набор из нескольких простых техник! Надеюсь, вам понравится!", "PROGRAM_INTRO")
printf("Handshaking With Hub! 🤝 Nice To Meet you Hub!", "HANDSHAKE_HUB")
printf("Как тебя зовут?", "WHAT_IS_YOUR_NAME")
name = "test_dogeblock_ru_account"
printf("привет, \"{0}\"! 👋 приятно встретить тебя!".format(name), "HELLO_USER")
print("=" * 50)
printf("ты знаешь? \"{0}\"".format(Flood.tip()), "INTRO_TIPS")
print("=" * 50)
Flood.wait(1)
# hub_down function to hub down
def hub_down():
    printf("Я спускаюсь, 🍂 привет земля! 🌍", "HELLO_GROUND") # 문법에 안맞는 개소맄ㅋㅋㅋㅋ
    hub.status_light.on(setting["hub_down_color"])
    for i in range(setting["zero"], setting["hub_up_steps"]):
        hub.speaker.beep(setting["hub_beep_standard"], setting["beep_stddur"])
        motor_pair_odin.move(setting["motor_pair_mo"], setting["motor_stdunit"], -100, 100)
        motor_pair_dva.move(setting["motor_pair_mo"], setting["motor_stdunit"], -100, -100)
    hub.status_light.on(setting["default_color"])
# while True
flood = Flood(hub)
while setting["true"]:
    if init_required == setting["true"]:
        printf("я запускаю Hub.... он будет завершен в любые секунды! 😊", "INITING_HUB")
        distance.light_up_all(100)
        init_required = setting["false"]
    # force is_pressed() is true, then call test force.get_force_newton()!
    if force.is_pressed() and (force.get_force_newton() != setting["undefined"]):
        if flood.is_up == setting["false"]:
            printf("Ignore", "IGNORE_FORCES_PRESS")
        elif (force.get_force_newton() >= setting["hub_down_newton"]) or (force.get_force_percentage() >= setting["force_down_percentage"]):
            hub_down();
            flood.set_is_up(setting["false"])
            init_required = setting["true"]
            continue;
    # distance.get_distance_cm()를 여러번 호출하면 가끔 한두개씩 undefined가 떠서 안됨 ㅅㄱ
    _distance = distance.get_distance_cm()
    if _distance == setting["undefined"]:
        continue;
    if _distance <= 1:
        printf("Program exiting... (code: 1)", "PrOgRaM_eXiT")
        break;
    # 만약 거리가 undefined에 해당하지 아니하는 경우
    if _distance != setting["undefined"]:
        # Hub Warning!
        if flood.upable() and _distance <= setting["warning_distance"]:
            printf("⚠️ Предупреждение! Что-то приближается! ⚠️", "SOMETHING_APPROACHING")
            hub.status_light.on(setting["hub_warning_color"])
        # 허브가 올라간다!
        if _distance <= setting["hub_up_distance"]:
            if not flood.upable():
                printf("[DEBUG] ⛔ hub is not upable! ⛔", "NOT_UPABLE")
                continue;
            printf("Я поднимаюсь! Здравствуй, 👋 Голубое Небо! ☁️", "HELLO_SKY") # 존나 웃기네 ㅋㅋㅋㅋㅋㅋㅋ
            distance.light_up_all(setting["zero"])
            hub.status_light.on(setting["hub_up_color"])
            for i in range(setting["zero"], setting["hub_up_steps"]):
                hub.speaker.beep(setting["hub_beep_standard"], setting["beep_stddur"])
                motor_pair_odin.move(setting["motor_pair_mo"], setting["motor_stdunit"], 100, 100)
                motor_pair_dva.move(setting["motor_pair_mo"], setting["motor_stdunit"], 100, -100)
            hub.status_light.on(setting["default_color"])
            flood.set_is_up(setting["true"])
            # wait_for_seconds(5)
            continue;
