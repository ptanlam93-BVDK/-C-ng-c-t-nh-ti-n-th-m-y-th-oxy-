import streamlit as st

st.set_page_config(page_title="Thở máy - Thở oxy - Ngày giường", layout="centered")

st.title("🧾 TÍCH HỢP QUY ĐỔI THỞ MÁY – THỞ OXY – PHÂN LOẠI NGÀY GIƯỜNG")

st.write("""
🔴 **Thở máy:** (Giờ kết thúc – Giờ bắt đầu) / 24  
🔵 **Thở oxy:** (Giờ kết thúc – Giờ bắt đầu) → GIỜ THẲNG  
📌 **Phân loại ngày giường tự động theo kết quả thở máy**
""")

tab1, tab2 = st.tabs(["🔴 THỞ MÁY + NGÀY GIƯỜNG", "🔵 THỞ OXY"])

# =========================================================
# 🔴 TAB 1: THỞ MÁY + PHÂN LOẠI NGÀY GIƯỜNG
# =========================================================
with tab1:
    st.subheader("🔴 BẢNG TÍNH GIỜ THỞ MÁY (≤ 24h, cùng ngày)")

    gio_bat_dau = st.number_input("Giờ bắt đầu thở máy (0–23)", 0, 23, 0)
    gio_ket_thuc = st.number_input("Giờ kết thúc thở máy (1–24)", 1, 24, 24)

    st.markdown("---")

    if gio_ket_thuc <= gio_bat_dau:
        st.error("⛔ Giờ kết thúc phải LỚN HƠN giờ bắt đầu.")
    else:
        tong_gio = gio_ket_thuc - gio_bat_dau

        if tong_gio > 24:
            st.error("⛔ Tổng giờ không được vượt quá 24h.")
        else:
            ket_qua = round(tong_gio / 24, 3)

            # ✅ PHÂN LOẠI NGÀY GIƯỜNG
            if ket_qua < 0.3:
                loai_giuong = "✅ NGÀY GIƯỜNG HSCC"
            elif 0.3 <= ket_qua <= 0.8:
                loai_giuong = "🟡 1/2 NGÀY GIƯỜNG HSCC + 1/2 NGÀY GIƯỜNG HSTC"
            else:
                loai_giuong = "🔴 NGÀY GIƯỜNG HSTC"

            st.subheader("📊 KẾT QUẢ THỞ MÁY")
            st.write(f"🕒 **Tổng số giờ thở máy:** `{tong_gio}` giờ")
            st.write(f"📘 **Kết quả quy đổi theo 24h:** `{ket_qua}`")
            st.success(f"📌 **Phân loại ngày giường:** {loai_giuong}")

            st.caption("Ví dụ: 14h/24h = 0.583 → 1/2 HSCC + 1/2 HSTC")

# =========================================================
# 🔵 TAB 2: THỞ OXY
# =========================================================
with tab2:
    st.subheader("🔵 BẢNG TÍNH GIỜ THỞ OXY (≤ 24h, cùng ngày)")

    gio_bd_oxy = st.number_input("Giờ bắt đầu thở oxy (0–23)", 0, 23, 0, key="oxy1")
    gio_kt_oxy = st.number_input("Giờ kết thúc thở oxy (1–24)", 1, 24, 24, key="oxy2")

    st.markdown("---")

    if gio_kt_oxy <= gio_bd_oxy:
        st.error("⛔ Giờ kết thúc phải LỚN HƠN giờ bắt đầu.")
    else:
        tong_gio_oxy = gio_kt_oxy - gio_bd_oxy

        if tong_gio_oxy > 24:
            st.error("⛔ Tổng giờ oxy không được vượt quá 24h.")
        else:
            ket_qua_oxy = round(tong_gio_oxy, 2)

            st.subheader("📊 KẾT QUẢ THỞ OXY")
            st.write(f"🕒 **Tổng số giờ thở oxy:** `{tong_gio_oxy}` giờ")
            st.info(f"📘 **Kết quả giờ oxy (giờ thẳng):** `{ket_qua_oxy}`")

            st.caption("Ví dụ: 22h → 24h = 2 giờ oxy → kết quả = 2.00")
