import threading
import time
import paho.mqtt.client as mqtt
from gpiozero import Servo, LED
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from flask import Flask, Response, render_template_string
from picamera2 import Picamera2
import cv2


# --- Donanım ve sensör kurulumu ---
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
ads2 = ADS.ADS1115(i2c, address=0x49)


servo = Servo(12, min_pulse_width=0.70/1000, max_pulse_width=2.5/1000)
sag_ileri = LED(19)
sag_geri = LED(26)
sol_ileri = LED(20)
sol_geri = LED(21)
sirenkirmizi = LED(17)
sirenmavi = LED(27)
sirenbeyaz = LED(22)
horn = LED(6)
pompa = LED(13)


def set_servo_angle(angle):
    angle = max(0, min(180, int(angle)))
    servo.value =(angle / 90) - 1
    print(f"Servo açısı: {angle}")


MQTT_BROKER = "VPS_IP"
MQTT_TOPICS = [("servo/veri", 0), ("ileri/veri", 0), ("sag/veri", 0),
               ("sol/veri", 0), ("geri/veri", 0), ("siren/veri", 0), ("pompa/veri", 0), ("flame/veri", 0), ("su/veri", 0)]

def on_connect(client, userdata, flags, rc):
    print("MQTT Bağlantı durumu:", 1-rc)
    client.subscribe(MQTT_TOPICS)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    # Burada senin mevcut mesaj işleme fonksiyonun olabilir
    # Örneğin servo, led kontrol kodları buraya...

    if topic == "servo/veri":
        try:
            derece = float(payload)
            set_servo_angle(derece)
        except:
            pass
    if topic == "sag/veri":
        sagpayload = msg.payload.decode()
        if sagpayload == "1":
            sag_geri.on()
            sag_ileri.off()
            sol_ileri.on()
            sol_geri.off()
            print("Sağa dönülüyor")
        elif sagpayload == "0":
            sag_geri.off()
            sag_ileri.off()
            sol_ileri.off()
            sol_geri.off()
            print("Sağa dönülme işlemi bitti")
    else:
        pass

    if topic == "ileri/veri":
        ileripayload = msg.payload.decode()
        if ileripayload == "1":
            sag_geri.off()
            sag_ileri.on()
            sol_ileri.on()
            sol_geri.off()
            print("İleri gidiliyor")
        elif ileripayload == "0":
            sag_geri.off()
            sag_ileri.off()
            sol_ileri.off()
            sol_geri.off()
            print("İleri gitme işlemi bitti")
    else:
        pass

    if topic == "sol/veri":
        solpayload = msg.payload.decode()
        if solpayload == "1":
            sag_geri.off()
            sag_ileri.on()
            sol_ileri.off()
            sol_geri.on()
            print("Sola dönülüyor")
        elif solpayload == "0":
            sag_geri.off()
            sag_ileri.off()
            sol_ileri.off()
            sol_geri.off()
            print("Sola dönülme işlemi bitti")
    else:
        pass

    if topic == "geri/veri":
        geripayload = msg.payload.decode()
        if geripayload == "1":
            sag_geri.on()
            sag_ileri.off()
            sol_ileri.off()
            sol_geri.on()
            print("Geri gidiliyor")
        elif geripayload == "0":
            sag_geri.off()
            sag_ileri.off()
            sol_ileri.off()
            sol_geri.off()
            print("Geri gitme işlemi bitti")
    else:
        pass

    if topic == "siren/veri":
        sirenpayload = msg.payload.decode()
        if sirenpayload == "1":
            print("Siren Açık")
            sirenkirmizi.blink(on_time=0.5,off_time=0.2)
            sirenbeyaz.blink(off_time=0.1,on_time=0.1)
            sirenmavi.blink(off_time=0.3,on_time=0.2)
            horn.blink(off_time=0.3,on_time=0.2)

        elif sirenpayload == "0":
            print("Siren Kapalı")
            sirenkirmizi.off()
            sirenbeyaz.off()
            sirenmavi.off()
            horn.off()
    else:
        pass

    if topic == "pompa/veri":
        pompapayload = msg.payload.decode()
        if pompapayload == "1":
            print("Pompa Açık")
            pompa.on()
        elif pompapayload == "0":
            print("Pompa Kapalı")
            pompa.off()
    else:
        pass

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def flame_sensor_and_samandira_loop():
    while True:
        try:
            front_sensor = AnalogIn(ads, ADS.P0)
            right_sensor = AnalogIn(ads, ADS.P1)
            left_sensor = AnalogIn(ads, ADS.P2)
            back_sensor = AnalogIn(ads, ADS.P3)
            samandira_sensor = AnalogIn(ads2, ADS.P0)
            samandiraraw = samandira_sensor.value
            su_seviyesi = max(0, min(100, (samandiraraw / 5500) * 100))
            ##print("Su seviyesi:", int(su_seviyesi))
            client.publish("su/veri", int(su_seviyesi))

            values = [front_sensor.value, right_sensor.value, left_sensor.value, back_sensor.value]

            if front_sensor.value < min(back_sensor.value, right_sensor.value, left_sensor.value):
                payload = "^"
            elif right_sensor.value < min(back_sensor.value, left_sensor.value, front_sensor.value):
                payload = ">"
            elif back_sensor.value < min(front_sensor.value, left_sensor.value, right_sensor.value):
                payload = "V"
            elif left_sensor.value < min(front_sensor.value, back_sensor.value, right_sensor.value):
                payload = "<"
            else:
                payload = "-"
            client.publish("flame/veri", payload)

        except Exception as e:
            print("Sensör okuma hatası:", e)
        time.sleep(1)

# --- MQTT client ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

# --- Flask uygulaması ---
app = Flask(__name__)

# Kamera başlatma
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

HTML_PAGE = """
<!doctype html>
<html>
<head>
    <title>Raspberry Pi Kamera Yayını</title>
    <style>
        body { text-align: center; font-family: Arial; background-color: #f2f2f2; }
        h1 { margin-top: 20px; }
        img { border: 2px solid #555; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🚒 Raspberry Pi Kamera Yayını</h1>
    <img src="{{ url_for('video_feed') }}" width="640" height="480">
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # MQTT döngüsünü başlat
    client.loop_start()

    # Sensör izleme threadini başlat
    flame_thread = threading.Thread(target=flame_sensor_and_samandira_loop)
    flame_thread.daemon = True
    flame_thread.start()

    # Flask uygulamasını başlat
    app.run(host='0.0.0.0', port=5000, debug=False)
