import streamlit as st

# --- 1. Layout Config ---
st.set_page_config(page_title="Hormone Panel Interpreter", layout="wide")

st.title("🧬 Male Hormone Panel Interpreter")
st.markdown("แปลผลฮอร์โมนชายแบบครบวงจร — วินิจฉัย · ปรับสมดุล · เฝ้าระวังความปลอดภัย")
st.markdown("*(อ้างอิง Endocrine Society 2018, AUA 2018, SIAMS/SIE 2022, EAU 2025)*")
st.divider()

# --- 2. Input Section ---
col_in, col_gap, col_out = st.columns([1, 0.05, 2])

with col_in:
    st.subheader("📋 กรอกผลเลือด")

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
        psa = st.number_input("PSA ปัจจุบัน (ng/mL)", min_value=0.0, max_value=50.0, value=0.0, step=0.01)
        baseline_psa = st.number_input("Baseline PSA เดิม (ng/mL) *ถ้ามี*", min_value=0.0, max_value=50.0, value=0.0, step=0.01)

        st.markdown("---")
        st.markdown("**ข้อมูลคนไข้**")
        age = st.number_input("อายุคนไข้ (ปี)", min_value=18, max_value=95, value=40)
        on_trt = st.checkbox("คนไข้กำลังรับ TRT อยู่")

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
            # BLOCK A: Testosterone + LH
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
                        st.warning("**T ต่ำ + LH ปกติ** — Compensated / Functional\nอาจเกิดจาก Obesity, Metabolic syndrome, ยา\n➡️ พิจารณา SHBG, Free Testosterone")
                    elif not t_low and lh_high:
                        st.warning("**Compensated Primary Hypogonadism** — T ปกติ + LH สูง\nอัณฑะยังชดเชยได้แต่ทำงานหนักเกิน\n➡️ Monitor closely, อาจเริ่มลดลงในอนาคต")
                    else:
                        st.success("**T และ LH อยู่ในเกณฑ์ปกติ** — ไม่พบลักษณะ Hypogonadism ทางชีวเคมี")

                st.divider()

            # =============================================
            # BLOCK B: E2
            # =============================================
            if e2 > 0:
                st.markdown("### 🟣 สมดุล Estradiol (E2)")
                c1, c2 = st.columns(2)
                with c1:
                    if e2 > 40:
                        st.error(f"**E2: {e2:.1f} pg/mL** 🚨 สูงเกินเกณฑ์ (> 40 pg/mL)\nเสี่ยง Gynecomastia, Water retention, Libido ลดลง\n➡️ ประเมิน Aromatization: BMI, ยา, โรคตับ")
                    elif e2 >= 20:
                        st.success(f"**E2: {e2:.1f} pg/mL** ✅ Sweet spot (20–40 pg/mL)\nสมดุลดี — Libido ดี, กระดูกแข็งแรง, แทบไม่มีผลข้างเคียง")
                    elif e2 >= 10:
                        st.warning(f"**E2: {e2:.1f} pg/mL** ⚠️ ค่อนข้างต่ำ (10–19 pg/mL)\nอาจมีผลต่อ Libido, Bone density, อารมณ์")
                    else:
                        st.error(f"**E2: {e2:.1f} pg/mL** 🚨 ต่ำมาก (< 10 pg/mL)\nเสี่ยง Osteoporosis, ข้อเสื่อม, Mood ผิดปกติ\n➡️ ตรวจสอบการใช้ Aromatase Inhibitor เกินขนาด")

                with c2:
                    if testosterone > 0:
                        t_ngdl = testosterone * 100  # ng/mL → ng/dL
                        ratio = t_ngdl / e2          # T:E2 = ng/dL / pg/mL
                        st.metric("T:E2 Ratio", f"{ratio:.1f}")
                        if ratio < 10:
                            st.warning("T:E2 ต่ำ (< 10) → Aromatization สูง\nพบบ่อยใน Obesity, Insulin resistance, โรคตับ")
                        elif ratio > 25:
                            st.warning("T:E2 สูง (> 25) → E2 ต่ำเกิน\nพบใน Low body fat หรือใช้ AI เกินขนาด")
                        else:
                            st.success("T:E2 Ratio อยู่ในช่วงสมดุล (10–25)")
                    else:
                        st.info("กรอกค่า Testosterone เพิ่มเติมเพื่อคำนวณ T:E2 Ratio")

                st.divider()

            # =============================================
            # BLOCK C: Hct
            # =============================================
            if hct > 0:
                st.markdown("### 🔴 Hematocrit — ความปลอดภัยด้านโลหิต")
                if hct > 54:
                    st.error(f"**Hct: {hct:.1f}%** 🚨 วิกฤต (> 54%)\n**หยุด TRT ทันที** จนกว่า Hct จะลดลงสู่ระดับปลอดภัย\nประเมิน Sleep Apnea, Hypoxia\nพิจารณา Phlebotomy\n*(Endocrine Society / EAU 2025)*")
                elif hct > 52:
                    st.error(f"**Hct: {hct:.1f}%** 🚨 สูงเกินเกณฑ์เฝ้าระวัง (> 52%)\nเสี่ยง MACE/VTE เพิ่มขึ้น 35%\n➡️ ลด TRT dose หรือเปลี่ยนรูปแบบ (Injectable → Transdermal)\nพิจารณา Phlebotomy")
                elif hct > 50:
                    st.warning(f"**Hct: {hct:.1f}%** ⚠️ Relative Contraindication (> 50%)\n➡️ ระวังก่อนเริ่ม/ปรับ TRT, ติดตามใกล้ชิด\n*(AUA Guidelines)*")
                elif hct >= 40:
                    st.success(f"**Hct: {hct:.1f}%** ✅ ปกติ (40–50%)")
                else:
                    st.warning(f"**Hct: {hct:.1f}%** ⚠️ ต่ำกว่าปกติ (< 40%)\nประเมินภาวะ Anemia ก่อนพิจารณา TRT")

                st.divider()

            # =============================================
            # BLOCK D: PSA
            # =============================================
            if psa > 0:
                st.markdown("### 🟢 PSA — คัดกรองความเสี่ยงต่อมลูกหมาก")
                c1, c2 = st.columns(2)
                with c1:
                    if psa > 4.0:
                        st.error(f"**PSA: {psa:.2f} ng/mL** 🚨 สูงเกิน 4.0 ng/mL\n**ส่ง Consult Urology ทันที**\nห้ามเริ่มหรือดำเนิน TRT จนกว่าจะได้รับการประเมิน\n*(Endocrine Society 2018)*")
                    elif psa > 0.6 and age >= 40:
                        st.warning(f"**PSA: {psa:.2f} ng/mL** ⚠️ > 0.6 ng/mL ในคนไข้อายุ ≥ 40 ปี\nนัดติดตาม PSA ซ้ำที่ 3–6 เดือนหลังเริ่ม TRT\nหาก PSA เพิ่ม > 1.4 ng/mL จาก baseline → Consult Uro")
                    else:
                        st.success(f"**PSA: {psa:.2f} ng/mL** ✅ อยู่ในเกณฑ์ปกติ")

                with c2:
                    if on_trt and psa > 0:
                        if baseline_psa > 0:
                            delta = psa - baseline_psa
                            st.metric("PSA Delta จาก Baseline", f"{delta:+.2f} ng/mL")
                            if delta > 1.4:
                                st.error(f"PSA เพิ่มขึ้น {delta:.2f} ng/mL จาก baseline\nเกินเกณฑ์ 1.4 ng/mL → **Consult Urology ทันที**")
                            elif delta > 0.5:
                                st.warning(f"PSA เพิ่มขึ้น {delta:.2f} ng/mL — ติดตามใกล้ชิด")
                            else:
                                st.success(f"PSA delta อยู่ในเกณฑ์ปกติ ({delta:+.2f} ng/mL)")
                        else:
                            st.info(f"📌 **On TRT Monitoring**\nBaseline PSA ปัจจุบัน: {psa:.2f} ng/mL\nAlert threshold: {psa + 1.4:.2f} ng/mL\nถ้าค่าถัดไปเกิน {psa + 1.4:.2f} → Consult Uro")

                st.divider()

            # =============================================
            # BLOCK E: Clinical Summary
            # =============================================
            st.markdown("### 📝 สรุปภาพรวม")
            flags = []

            if testosterone > 0 and testosterone < 2.64:
                flags.append("⚠️ Testosterone ต่ำกว่าเกณฑ์ — พิจารณา TRT")
            if lh > 0 and lh >= 9.4 and testosterone > 0 and testosterone < 2.64:
                flags.append("🔴 Primary Hypogonadism — ตรวจหาสาเหตุที่อัณฑะ")
            if lh > 0 and lh < 1.5 and testosterone > 0 and testosterone < 2.64:
                flags.append("🔴 Secondary Hypogonadism — MRI Sella + Prolactin")
            if e2 > 40:
                flags.append("⚠️ E2 สูง — ประเมิน Aromatization")
            if e2 > 0 and e2 < 10:
                flags.append("⚠️ E2 ต่ำมาก — ตรวจสอบ AI dose")
            if hct > 54:
                flags.append("🚨 Hct วิกฤต — หยุด TRT ทันที")
            if hct > 50 and hct <= 54:
                flags.append("⚠️ Hct สูง — ลด dose หรือ Phlebotomy")
            if psa > 4.0:
                flags.append("🚨 PSA สูง — Consult Urology ด่วน")
            if psa > 0.6 and age >= 40:
                flags.append("📌 PSA > 0.6 ในคนไข้ ≥ 40 ปี — นัด monitor 3–6 เดือน")
            if on_trt and baseline_psa > 0 and psa > 0 and (psa - baseline_psa) > 1.4:
                flags.append("🚨 PSA delta > 1.4 ng/mL — Consult Urology ทันที")

            if flags:
                for f in flags:
                    st.markdown(f"- {f}")
            else:
                st.success("✅ ไม่พบ flag ที่ต้องดำเนินการเพิ่มเติม — ผลฮอร์โมนอยู่ในเกณฑ์ปกติทุกตัว")

            st.warning(
                "⚠️ **ข้อจำกัด:** โปรแกรมนี้ใช้ประกอบการตัดสินใจทางคลินิกเท่านั้น "
                "การวินิจฉัยและรักษาต้องอาศัยดุลยพินิจของแพทย์ร่วมกับอาการทางคลินิกเสมอ "
                "ไม่ควรใช้ผลแปลผลจากโปรแกรมนี้เป็นเกณฑ์เดียวในการตัดสินใจ"
            )

# --- 4. Reference Footer ---
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📚 References ทั้งหมด"):
    st.markdown("""
    - **Bhasin S et al.** Testosterone Therapy in Men With Hypogonadism: An Endocrine Society Clinical Practice Guideline. *JCEM* 2018;103(5):1715–1744
    - **Mulhall JP et al.** Evaluation and Management of Testosterone Deficiency: AUA Guideline. *J Urol* 2018;200(2):423–432
    - **Zitzmann M et al.** SIAMS/SIE Guidelines on Adult-onset Male Hypogonadism. *PMC9415259* 2022
    - **Ramasamy R et al.** Secondary Polycythemia in Men Receiving Testosterone Therapy Increases Risk of MACE/VTE. *J Urol* 2022
    - **EAU Guidelines on Male Hypogonadism** 2025
    """)
