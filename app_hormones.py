import streamlit as st

# --- 1. Layout Config ---
st.set_page_config(page_title="Hormone Panel Interpreter", layout="wide")

st.title("🧬 Male Hormone Panel Interpreter")
st.markdown("แปลผลฮอร์โมนชายแบบครบวงจร — วินิจฉัย · ปรับสมดุล · เฝ้าระวังความปลอดภัย")
st.markdown("*(อ้างอิง Endocrine Society 2018, AUA 2018, SIAMS/SIE 2022, EAU 2025)*")
st.divider()

# --- 2. Input Section (Wrapped in st.form) ---
col_in, col_gap, col_out = st.columns([1, 0.05, 2])

with col_in:
    st.subheader("📋 กรอกผลเลือด")

    # ครอบด้วย st.form เพื่อป้องกันปัญหาจอรันใหม่ทุกครั้งที่กรอกข้อมูล
    with st.form("trt_input_form"):
        st.markdown("**กลุ่มวินิจฉัย**")
        testosterone = st.number_input("Testosterone (ng/mL)", min_value=0.0, max_value=20.0, value=0.0, step=0.01)
        lh = st.number_input("LH (mIU/mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.1)

        st.markdown("---")
        st.markdown("**กลุ่มปรับสมดุล**")
        e2 = st.number_input("Estradiol / E2 (pg/mL)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)

        st.markdown("---")
        st.markdown("**กลุ่มเฝ้าระวังความปลอดภัย**")
        hct = st.number_input("Hematocrit / Hct (%)", min_value=0.0, max_value=70.0, value=0.0, step=0.1)
        
        # เพิ่มช่องกรอก PSA ทั้งปัจจุบันและค่าเดิม
        psa = st.number_input("PSA ปัจจุบัน (ng/mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.01)
        baseline_psa = st.number_input("Baseline PSA เดิม (ng/mL) *ถ้ามี*", min_value=0.0, max_value=50.0, value=0.0, step=0.01)

        st.markdown("---")
        st.markdown("**ข้อมูลคนไข้**")
        age = st.number_input("อายุคนไข้ (ปี)", min_value=18, max_value=95, value=40)
        on_trt = st.checkbox("คนไข้กำลังรับ TRT อยู่")

        # เปลี่ยนเป็น st.form_submit_button
        analyze = st.form_submit_button("🔍 แปลผล", use_container_width=True)

# --- 3. Interpret Logic ---
with col_out:
    st.subheader("📊 ผลการแปลผล")

    if not analyze:
        st.info("💡 กรอกผลเลือดด้านซ้ายแล้วกด 'แปลผล' เพื่อเริ่มการวิเคราะห์")
    else:
        any_input = testosterone > 0 or lh > 0 or e2 > 0 or hct > 0 or psa > 0
        if not any_input:
            st.warning("กรุณากรอกผลเลือดอย่างน้อย 1 ค่าก่อนแปลผล")
        else:

            # =============================================
            # BLOCK A: Testosterone + LH → วินิจฉัย
            # =============================================
            if testosterone > 0 or lh > 0:
                st.markdown("### 🔵 การวินิจฉัยภาวะ Hypogonadism")
                c1, c2 = st.columns(2)

                with c1:
                    if testosterone == 0:
                        st.info("ไม่ได้กรอกค่า Testosterone")
                    elif testosterone >= 4.0:
                        st.success(f"**Testosterone: {testosterone:.2f} ng/mL** ✅\nอยู่ในเกณฑ์ปกติ-ดี (≥ 4.00 ng/mL)")
                    elif testosterone >= 2.64:
                        st.warning(f"**Testosterone: {testosterone:.2f} ng/mL** ⚠️\nอยู่ในเกณฑ์ปกติแต่ค่อนข้างต่ำ (2.64–3.99 ng/mL)\nพิจารณาร่วมกับอาการทางคลินิก")
                    else:
                        st.error(f"**Testosterone: {testosterone:.2f} ng/mL** 🚨\nต่ำกว่าเกณฑ์ (< 2.64 ng/mL)\nสอดคล้องกับภาวะ Hypogonadism")

                with c2:
                    if lh == 0:
                        st.info("ไม่ได้กรอกค่า LH")
                    elif lh >= 9.4:
                        st.error(f"**LH: {lh:.1f} mIU/mL** 🚨\nสูง (≥ 9.4 mIU/mL)\nชี้ต่อ Primary Hypogonadism (Testicular failure)")
                    elif lh >= 1.5:
                        st.success(f"**LH: {lh:.1f} mIU/mL** ✅\nอยู่ในเกณฑ์ปกติ (1.5–9.3 mIU/mL)")
                    else:
                        st.warning(f"**LH: {lh:.1f} mIU/mL** ⚠️\nต่ำ (< 1.5 mIU/mL)\nชี้ต่อ Secondary Hypogonadism (Pituitary/Hypothalamic)")

                if testosterone > 0 and lh > 0:
                    st.markdown("#### 🧠 Pattern Analysis: T + LH")
                    t_low = testosterone < 2.64
                    lh_high = lh >= 9.4
                    lh_low = lh < 1.5

                    if t_low and lh_high:
                        st.error("**Primary Hypogonadism** — T ต่ำ + LH สูง\nอัณฑะตอบสนองต่อสัญญาณ LH ไม่เพียงพอ\n➡️ พิจารณา: Klinefelter, orchitis, trauma, radiation")
                    elif t_low and lh_low:
                        st.error("**Secondary Hypogonadism** — T ต่ำ + LH ต่ำ/ปกติ\nปัญหาที่ Pituitary หรือ Hypothalamus\n➡️ พิจารณา: MRI sella, Prolactin, วัด FSH เพิ่มเติม")
                    elif t_low and not lh_high and not lh_low:
                        st.warning("**T ต่ำ + LH ปกติ** — Compensated / Functional\nอาจเกิดจาก Obesity, Metabolic syndrome, ยา\n➡️ พิจารณา SHBG, Free
