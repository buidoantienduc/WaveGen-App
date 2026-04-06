import streamlit as st
import numpy as np
import io
from scipy.io import wavfile
from scipy import signal

# Thiết lập giao diện Web
st.set_page_config(page_title="WaveGen App", layout="centered")
st.title("🌊 WaveGen - Trình Tạo Tín Hiệu Cơ Bản")
st.markdown("Mô phỏng tín hiệu điện tử, hỗ trợ học tập và thiết kế mạch.")

# --- THANH CÔNG CỤ ĐIỀU KHIỂN (SIDEBAR) ---
st.sidebar.header("⚙️ Thông số tín hiệu")
wave_type = st.sidebar.selectbox("Loại sóng", ["Sóng Sin", "Xung Vuông (PWM)", "Sóng Tam Giác"])
frequency = st.sidebar.slider("Tần số (Hz)", min_value=20, max_value=2000, value=440, step=10)

# Hiện thanh chỉnh Duty Cycle nếu chọn Xung Vuông
duty_cycle = 0.5
if wave_type == "Xung Vuông (PWM)":
    duty_cycle = st.sidebar.slider("Duty Cycle (%) - Độ rộng xung", min_value=1, max_value=99, value=50) / 100

noise_level = st.sidebar.slider("Mức độ nhiễu (Noise)", min_value=0.0, max_value=1.0, value=0.0, step=0.05)

# --- XỬ LÝ TOÁN HỌC (DSP) ---
fs = 44100  # Tần số lấy mẫu (Sample rate) chuẩn Audio
duration = 1.0  # Tạo 1 giây dữ liệu để phát âm thanh
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Tạo dạng sóng dựa trên lựa chọn
if wave_type == "Sóng Sin":
    wave = np.sin(2 * np.pi * frequency * t)
elif wave_type == "Xung Vuông (PWM)":
    wave = signal.square(2 * np.pi * frequency * t, duty=duty_cycle)
elif wave_type == "Sóng Tam Giác":
    wave = signal.sawtooth(2 * np.pi * frequency * t, width=0.5)

# Thêm nhiễu vào tín hiệu thực tế
if noise_level > 0:
    noise = np.random.normal(0, noise_level, wave.shape)
    wave = wave + noise

# Cắt gọt biên độ về khoảng [-1, 1] để âm thanh không bị vỡ (clipping)
wave = np.clip(wave, -1.0, 1.0)

# --- HIỂN THỊ TRỰC QUAN (VISUALIZATION) ---
st.subheader("📈 Hình ảnh dạng sóng")
# Chỉ trích xuất khoảng 4-5 chu kỳ đầu tiên để đồ thị dễ nhìn, không bị đen đặc
num_periods = 4
samples_to_show = int(fs * (num_periods / frequency))
st.line_chart(wave[:samples_to_show])

# --- PHÁT ÂM THANH ---
st.subheader("🔊 Nghe thử tín hiệu")
# Chuyển đổi dữ liệu từ dạng float (số thực) sang dạng int16 chuẩn của Audio
audio_data = np.int16(wave * 32767)

# Tạo một file wav ảo trong bộ nhớ RAM thay vì lưu ra ổ cứng
virtual_file = io.BytesIO()
wavfile.write(virtual_file, fs, audio_data)

st.audio(virtual_file, format="audio/wav")

st.info("💡 Mẹo: Kéo thanh Tần số để thấy sóng co giãn, kéo Duty Cycle để thấy độ rộng xung PWM thay đổi giống như khi cấu hình vi điều khiển.")