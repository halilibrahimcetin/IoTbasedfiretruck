# Nesnelerin İnterneti Tabanlı Web Arayüzü Kontrollü MQTT ile Haberleşen Akıllı İtfaiye Aracı

Bu proje, bir itfaiye aracının uzaktan kontrolünü sağlayan akıllı bir sistemdir. Web arayüzü üzerinden kullanıcı; aracı yönlendirebilir, sireni ve su pompasını kontrol edebilir, sensör verilerini canlı olarak izleyebilir ve kamera görüntüsünü anlık görebilir. Sistem, MQTT protokolü üzerinden Raspberry Pi ile iletişim kurar.

## Özellikler
- Web arayüzü ile yön, siren ve su kontrolü
- Canlı kamera yayını (Raspberry Pi üzerinden)
- Alev ve su seviye sensör verilerinin gösterimi
- MQTT (WebSocket) ile çift yönlü iletişim
- Raspberry Pi 5 + VPS üzerinde MQTT broker (Mosquitto)
- Responsive web tasarımı

## Kullanılan Teknolojiler
- MQTT (Mosquitto)
- Raspberry Pi 5 (Python ile GPIO kontrolü)
- HTML / CSS / JavaScript (Web arayüzü)
- Flask (Video akışı için)
- ADS1115 (Analog sensör okuma)
- Cloudflare Tunnel (isteğe bağlı HTTPS için)

## Kurulum
1. Raspberry Pi üzerinde sensörleri ve motorları bağlayın.
2. MQTT broker'ı VPS sunucunuzda kurun (Mosquitto önerilir).
3. Web arayüzünü VPS veya yerel sunucuda barındırın.
4. `config.js` dosyasına broker adresini yazın.
5. Web arayüzü üzerinden kontrol sağlayın.

---

# IoT-Based Smart Fire Truck Controlled via Web Interface and Communicating with MQTT 

This project is an IoT-based smart fire truck system that enables remote control through a web interface. The user can steer the vehicle, activate the siren and water pump, view sensor data in real-time, and watch a live camera stream. The system communicates with a Raspberry Pi via the MQTT protocol.

## Features
- Web interface control for movement, siren, and water functions
- Live video stream (via Raspberry Pi)
- Real-time flame and water level sensor display
- Bidirectional communication using MQTT over WebSocket
- MQTT broker hosted on VPS (Mosquitto)
- Responsive web design

## Technologies Used
- MQTT (Mosquitto)
- Raspberry Pi 5 (Python with GPIO control)
- HTML / CSS / JavaScript (Web interface)
- Flask (for video streaming)
- ADS1115 (for analog sensor readings)
- Cloudflare Tunnel (optional for HTTPS)

## Setup
1. Connect sensors and motors to the Raspberry Pi.
2. Set up an MQTT broker on your VPS (e.g., Mosquitto).
3. Host the web interface on your server or locally.
4. Set the broker address in `config.js`.
5. Use the web interface to control the fire truck.
