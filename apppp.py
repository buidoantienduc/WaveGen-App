import streamlit as st
import numpy as np
import io
from scipy.io import wavfile
from scipy import signal

# --- 1. TỐI ƯU SEO (PHẢI ĐẶT ĐẦU TRANG) ---
st.set_page_config(
    page_title="WaveGen UTT - Trình tạo tín hiệu Vi mạch Nhóm 46",
    page_icon="⚡",
    layout="wide" # Để giao diện rộng rãi, chuyên nghiệp hơn
)

# --- 2. NỘI DUNG CHÍNH (GOOGLE SẼ QUÉT CÁC DÒNG NÀY) ---
st.title("WaveGen UTT: Công cụ mô phỏng tín hiệu điện tử")
st.markdown("""
Đây là ứng dụng tạo và phân tích dạng sóng (Sin, Vuông, Tam giác) phục vụ nghiên cứu **Thiết kế vi mạch** tại **Đại học Công nghệ Giao thông Vận tải (UTT)**.


""")

# --- 3. PHẦN ĐIỀU KHIỂN (SIDEBAR) ---
st.sidebar.header("⚙️ Thông số tín hiệu")
wave_type = st.sidebar.selectbox("Loại sóng", ["Sóng Sin", "Xung Vuông (PWM)", "Sóng Tam Giác"])
frequency = st.sidebar.slider("Tần số (Hz)", min_value=20, max_value=2000, value=440, step=10)

duty_cycle = 0.5
if wave_type == "Xung Vuông (PWM)":
    duty_cycle = st.sidebar.slider("Duty Cycle (%)", min_value=1, max_value=99, value=50) / 100

noise_level = st.sidebar.slider("Mức độ nhiễu (Noise)", min_value=0.0, max_value=1.0, value=0.0, step=0.05)

# --- 4. XỬ LÝ TOÁN HỌC (DSP) ---
fs = 44100
duration = 1.0
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

if wave_type == "Sóng Sin":
    wave = np.sin(2 * np.pi * frequency * t)
elif wave_type == "Xung Vuông (PWM)":
    wave = signal.square(2 * np.pi * frequency * t, duty=duty_cycle)
elif wave_type == "Sóng Tam Giác":
    wave = signal.sawtooth(2 * np.pi * frequency * t, width=0.5)

if noise_level > 0:
    wave += np.random.normal(0, noise_level, wave.shape)

wave = np.clip(wave, -1.0, 1.0)

# --- 5. HIỂN THỊ ĐỒ THỊ ---
st.subheader("📈 Hình ảnh dạng sóng (Time Domain)")
num_periods = 4
samples_to_show = int(fs * (num_periods / frequency))
st.line_chart(wave[:samples_to_show])

# --- 6. PHÁT ÂM THANH ---
st.subheader("🔊 Nghe thử tín hiệu thực tế")
audio_data = np.int16(wave * 32767)
virtual_file = io.BytesIO()
wavfile.write(virtual_file, fs, audio_data)
st.audio(virtual_file, format="audio/wav")

# Dòng này giúp Google biết trang web thuộc về UTT
st.divider()
st.caption("© 2026 Dự án WaveGen - Sinh viên Kỹ năng mềm UTT - Nhóm 46")
