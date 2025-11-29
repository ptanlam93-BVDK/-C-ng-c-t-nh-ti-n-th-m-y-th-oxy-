import streamlit as st

# =========================
# CẤU HÌNH & GIỚI THIỆU
# =========================
st.set_page_config(page_title="Công cụ tính giờ thở máy/thở oxy", layout="centered")

st.title("💻 Công cụ tính giờ thở máy / thở oxy cho điều dưỡng")

st.markdown(
    """
    Công cụ này chỉ dùng để **tính toán và hiển thị kết quả**, không lưu dữ liệu.  
    Hỗ trợ sử dụng ** Qui đổi thời gian **.

    **Được xây dựng bởi:** CNĐD **Phan Tấn Lãm**  
    **Đơn vị:** Khoa Hồi sức tích cực - Chống độc,  
    **Bệnh viện:** 🏥 Bệnh viện Đa khoa Đồng Tháp.
    """
)

tab_may, tab_oxy = st.tabs(["🔴 Giờ thở máy + ngày giường", "🔵 Giờ thở oxy"])


# =========================
# HÀM XỬ LÝ GIỜ CHUNG
# =========================
def doi_sang_phut(text: str):
    """
    Chấp nhận các dạng:
    - 09:15
    - 09h15 / 9h15 / 9H15
    - 9h / 9H / 9
    Có thể thêm 'phút', 'phut', 'p' ở cuối (bỏ qua).
    Trả về: (tổng_phút, lỗi)
    """
    try:
        t = text.strip().lower()

        # bỏ hậu tố phút
        for suffix in ["phút", "phut", "p", "’", "'"]:
            if t.endswith(suffix):
                t = t[: -len(suffix)].strip()

        t = t.replace("giờ", "h")
        t = t.replace(" ", "")
        t = t.replace("h", ":")

        if ":" not in t:
            t = t + ":00"

        parts = t.split(":")
        if len(parts) != 2:
            return None, "Định dạng giờ không hợp lệ. Ví dụ: 09:15 hoặc 09h15."

        h = int(parts[0]) if parts[0] != "" else 0
        m = int(parts[1]) if parts[1] != "" else 0

        if h < 0 or h > 24 or m < 0 or m > 59:
            return None, "Giờ hoặc phút không hợp lệ (giờ 0–24, phút 0–59)."

        if h == 24 and m > 0:
            return None, "24 giờ chỉ được nhập là 24:00."

        return h * 60 + m, None

    except Exception:
        return None, "Phải nhập giờ đúng kiểu 09:15, 9h15, 9h hoặc 9."


def tinh_phut(t_bd: str, t_kt: str):
    """Tính tổng phút trong cùng 1 ngày, tối đa 24h."""
    bd, err1 = doi_sang_phut(t_bd)
    kt, err2 = doi_sang_phut(t_kt)

    if err1:
        return None, err1
    if err2:
        return None, err2

    if kt <= bd:
        return None, "Giờ kết thúc phải LỚN HƠN giờ bắt đầu (trong cùng 1 ngày)."

    tong = kt - bd
    if tong > 1440:
        return None, "Tổng thời gian không được vượt quá 24 giờ."

    return tong, None


# ===============================
# ⏰ TAB: GIỜ THỞ MÁY + NGÀY GIƯỜNG
# ===============================
with tab_may:
    st.subheader("💊 Tính GIỜ THỞ MÁY và NGÀY GIƯỜNG")

    st.markdown("Nhập giờ dạng: `09h15`, `13:40`, `22h`, `24:00` …")

    col1, col2 = st.columns(2)
    with col1:
        bd_may = st.text_input("Giờ bắt đầu thở máy", placeholder="VD: 10h00")
    with col2:
        kt_may = st.text_input("Giờ kết thúc thở máy", placeholder="VD: 24:00")

    # NÚT BẤM TÍNH GIỜ THỞ MÁY
    if st.button("✅ TÍNH GIỜ THỞ MÁY"):
        tong_phut, err = tinh_phut(bd_may, kt_may)

        if err:
            st.error("⛔ " + err)
        else:
            # Tổng giờ thở máy
            tong_gio = tong_phut / 60
            # Quy đổi theo 24h
            ket_qua = round(tong_gio / 24, 3)

            # PHÂN LOẠI NGÀY GIƯỜNG THEO KẾT QUẢ
            if ket_qua < 0.3:
                loai_text = "1 ngày giường HSCC"
                tomtat_color = "#4da6ff"   # xanh
            elif 0.3 <= ket_qua <= 0.8:
                loai_text = "0.5 ngày HSCC + 0.5 ngày HSTC"
                tomtat_color = "#ffa500"   # cam
            else:
                loai_text = "1 ngày giường HSTC"
                tomtat_color = "#ff4d4d"   # đỏ

            st.markdown("---")

            # HỘP KẾT QUẢ GIỜ THỞ MÁY + /24
            st.markdown(
                f"""
                <div style='text-align:center; padding:18px; border:2px solid red;
                border-radius:14px; background-color:#fff0f0;'>
                    <div style='font-size:22pxcolor; #0066FF !important; font-weight:600;'>⏰ Tổng thời gian thở máy</div>
                    <div style='font-size:34px; font-weight:bold; color:red;'>
                        {tong_gio:.2f} GIỜ ({tong_phut} phút)
                    </div>
                    <br>
                    <div style='font-size:22px color; #0066FF !important; font-weight:600;'>🛃�
            Kết quả quy đổi /24</div>
                    <div style='font-size:42px; font-weight:bold; color:red;'>
                        {ket_qua}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # TÓM TẮT NHANH NGÀY GIƯỜNG (GIỐNG VÙNG TÓM TẮT)
            st.markdown("---")
            st.subheader("📌 Tóm tắt nhanh – Ngày giường thở máy")

            st.markdown(
                f"""
                <div style="
                    text-align:center;
                    padding:18px;
                    border-radius:14px;
                    background-color:{tomtat_color};
                    color:white;
                    font-size:28px;
                    font-weight:bold;">
                    ✅ {loai_text}
                </div>
                """,
                unsafe_allow_html=True
            )


# ===============================
# 🔵 TAB: GIỜ THỞ OXY
# ===============================
with tab_oxy:
    st.subheader("🔵 Tính GIỜ THỞ OXY (giờ thẳng)")

    st.markdown("Nhập giờ dạng: `09h15`, `13:30`, `22h`, `24:00` …")

    col3, col4 = st.columns(2)
    with col3:
        bd_oxy = st.text_input("Giờ bắt đầu thở oxy", placeholder="VD: 13h30", key="oxy_bd")
    with col4:
        kt_oxy = st.text_input("Giờ kết thúc thở oxy", placeholder="VD: 24:00", key="oxy_kt")

    # NÚT BẤM TÍNH GIỜ THỞ OXY
    if st.button("✅ TÍNH GIỜ THỞ OXY"):
        tong_phut_oxy, err_oxy = tinh_phut(bd_oxy, kt_oxy)

        if err_oxy:
            st.error("⛔ " + err_oxy)
        else:
            tong_gio_oxy = tong_phut_oxy / 60
            ket_qua_oxy = round(tong_gio_oxy, 2)

            st.markdown("---")

            # HỘP KẾT QUẢ GIỜ OXY
            st.markdown(
                f"""
                <div style='text-align:center; padding:18px; border:2px solid red;
                border-radius:14px; background-color:#fff0f0;'>
                    <div style='font-size:22px;'>🕒 Tổng thời gian thở oxy</div>
                    <div style='font-size:34px; font-weight:bold; color:red;'>
                        {tong_gio_oxy:.2f} GIỜ ({tong_phut_oxy} phút)
                    </div>
                    <br>
                    <div style='font-size:22px;'>📘 Giờ oxy (giờ thẳng)</div>
                    <div style='font-size:42px; font-weight:bold; color:red;'>
                        {ket_qua_oxy}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
