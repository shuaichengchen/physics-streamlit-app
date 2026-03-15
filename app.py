import io
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

st.set_page_config(
    page_title="物理前沿知识融入初中物理教学交互平台",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 避免云端字体缺失导致图表中文乱码：图表中只用英文/缩写
plt.rcParams["axes.unicode_minus"] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(BASE_DIR, "assets")
FIGURE_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

CUSTOM_CSS = """
<style>
:root {
    --primary: #214e7a;
    --accent: #3b82f6;
    --card: #ffffff;
    --text: #1f2937;
    --muted: #6b7280;
    --border: #dbe4f0;
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1240px;
}
.hero {
    background: linear-gradient(135deg, rgba(33,78,122,0.98), rgba(59,130,246,0.88));
    padding: 1.35rem 1.6rem;
    border-radius: 18px;
    color: white;
    box-shadow: 0 10px 32px rgba(33,78,122,0.18);
    margin-bottom: 1rem;
}
.hero h1 {margin: 0 0 0.35rem 0; font-size: 2rem; font-weight: 800;}
.hero p {margin: 0.2rem 0; font-size: 1rem; opacity: 0.95;}
.section-title {font-size: 1.28rem; font-weight: 800; color: var(--primary); margin: 0.5rem 0 0.8rem 0;}
.card {
    background: var(--card); border: 1px solid var(--border); border-radius: 16px;
    padding: 1rem 1rem 0.9rem 1rem; box-shadow: 0 6px 18px rgba(32, 71, 120, 0.06); height: 100%;
}
.metric-card {
    background: linear-gradient(180deg, #ffffff, #f7fbff); border: 1px solid var(--border);
    border-radius: 16px; padding: 1rem; box-shadow: 0 6px 18px rgba(32, 71, 120, 0.06);
}
.metric-title {color: var(--muted); font-size: 0.9rem; margin-bottom: 0.25rem;}
.metric-value {color: var(--primary); font-size: 1.55rem; font-weight: 800; line-height: 1.2;}
.small-muted {color: var(--muted); font-size: 0.92rem;}
.note-box {
    background: #f8fbff; border-left: 4px solid var(--accent); padding: 0.85rem 1rem;
    border-radius: 10px; color: var(--text);
}
.case-pill {
    display: inline-block; background: #eaf2ff; color: var(--primary); border-radius: 999px;
    padding: 0.25rem 0.7rem; margin-right: 0.4rem; margin-bottom: 0.4rem; font-size: 0.85rem; font-weight: 700;
}
.footer-box {background: #fbfdff; border: 1px dashed var(--border); border-radius: 14px; padding: 1rem;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def header_block(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def card_html(title: str, body: str):
    st.markdown(
        f"""
        <div class="card">
            <h4 style="margin-top:0;color:#214e7a;">{title}</h4>
            <div style="color:#1f2937;line-height:1.7;">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="small-muted">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pil_placeholder(title: str, subtitle: str, accent=(33, 78, 122)) -> Image.Image:
    img = Image.new("RGB", (1200, 700), (245, 249, 255))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
        font_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        font_big = ImageFont.load_default()
    draw.rounded_rectangle((40, 40, 1160, 660), radius=28, outline=accent, width=5, fill=(255, 255, 255))
    draw.rectangle((40, 40, 1160, 170), fill=accent)
    draw.text((80, 78), title, fill=(255, 255, 255), font=font_title)
    draw.text((85, 230), "IMAGE PLACEHOLDER", fill=accent, font=font_big)
    draw.text((85, 410), subtitle, fill=(70, 80, 95), font=font_sub)
    draw.text((85, 460), "请在 assets 文件夹放入对应图片，或在侧边栏上传图片。", fill=(90, 100, 115), font=font_sub)
    return img


def find_existing_image(paths):
    for path in paths:
        if os.path.exists(path):
            return path
    return None


def get_case_image(case_key: str, local_candidates, title: str, subtitle: str):
    session_key = f"upload_{case_key}"
    if session_key in st.session_state and st.session_state[session_key] is not None:
        return Image.open(st.session_state[session_key])
    found = find_existing_image(local_candidates)
    if found:
        try:
            return Image.open(found)
        except Exception:
            pass
    return pil_placeholder(title, subtitle)


def fig_to_bytes(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    return buf.read()


# ---------- 图表函数（只用英文/缩写） ----------
def make_depth_pressure_figure(max_depth: int = 11000, rho: float = 1025.0, g: float = 9.81):
    depth = np.linspace(0, max_depth, 300)
    p0 = 101325
    pressure_pa = p0 + rho * g * depth
    pressure_mpa = pressure_pa / 1e6
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.plot(depth, pressure_mpa, linewidth=2.5)
    ax.set_title("DPD")
    ax.set_xlabel("Depth / m")
    ax.set_ylabel("Pressure / MPa")
    ax.grid(True, linestyle="--", alpha=0.5)
    for d in [1000, 4000, min(7000, max_depth), max_depth]:
        p = (p0 + rho * g * d) / 1e6
        ax.scatter([d], [p], s=40)
        ax.text(d, p, f" {d} m\n {p:.1f} MPa", fontsize=9, va="bottom")
    fig.tight_layout()
    return fig


def make_lidar_figure(distance_m: float = 30.0, angle_deg: float = 0.0):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis("off")
    target_y = 3.0 + np.tan(np.radians(angle_deg)) * 2.8
    target_y = float(np.clip(target_y, 1.3, 4.8))
    sensor = plt.Rectangle((0.8, 2.2), 1.2, 1.6, fill=False, linewidth=2)
    target = plt.Rectangle((9.2, target_y - 1.0), 1.0, 2.0, fill=False, linewidth=2)
    ax.add_patch(sensor)
    ax.add_patch(target)
    ax.text(1.4, 3.0, "LiDAR", ha="center", va="center", fontsize=12)
    ax.text(9.7, target_y, "OBJ", ha="center", va="center", fontsize=12)
    ax.annotate("", xy=(9.2, target_y), xytext=(2.0, 3.2), arrowprops=dict(arrowstyle="->", lw=2))
    ax.annotate("", xy=(2.0, 2.8), xytext=(9.2, target_y - 0.2), arrowprops=dict(arrowstyle="->", lw=2, linestyle="--"))
    ax.text(5.5, 4.5, "Pulse Out", fontsize=11)
    ax.text(5.4, 1.8, "Echo Back", fontsize=11)
    ax.text(6.0, 5.25, r"$d=\frac{ct}{2}$", fontsize=16, ha="center")
    ax.set_title("LiDAR-RM")
    fig.tight_layout()
    return fig


def make_battery_figure(n_series: int = 4, n_parallel: int = 2):
    def draw_battery(ax, x, y, w=0.7, h=1.4, label=""):
        rect = plt.Rectangle((x, y), w, h, fill=False, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=9)

    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.axis("off")
    ax.set_xlim(0, max(8, n_series * 1.1 + 3))
    ax.set_ylim(0, max(5.5, n_parallel * 2.0 + 2))
    start_x = 1.0
    start_y = 1.0
    for row in range(n_parallel):
        y = start_y + row * 1.9
        for col in range(n_series):
            x = start_x + col * 1.0
            draw_battery(ax, x, y, label=f"C{row+1}-{col+1}")
            if col < n_series - 1:
                ax.plot([x + 0.7, x + 1.0], [y + 0.7, y + 0.7], linewidth=2)
        ax.plot([start_x - 0.3, start_x], [y + 0.7, y + 0.7], linewidth=2)
        ax.plot([start_x + (n_series - 1) * 1.0 + 0.7, start_x + (n_series - 1) * 1.0 + 1.0], [y + 0.7, y + 0.7], linewidth=2)
    left_bus_x = start_x - 0.3
    right_bus_x = start_x + (n_series - 1) * 1.0 + 1.0
    if n_parallel > 1:
        ax.plot([left_bus_x, left_bus_x], [start_y + 0.7, start_y + (n_parallel - 1) * 1.9 + 0.7], linewidth=2)
        ax.plot([right_bus_x, right_bus_x], [start_y + 0.7, start_y + (n_parallel - 1) * 1.9 + 0.7], linewidth=2)
    ax.text((left_bus_x + right_bus_x) / 2, start_y + n_parallel * 1.9 + 0.6, "EV-BSP", fontsize=14, ha="center")
    fig.tight_layout()
    return fig


def make_mapping_figure():
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis("off")
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)

    def add_box(x, y, w, h, txt):
        rect = plt.Rectangle((x, y), w, h, fill=False, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=11, wrap=True)

    ax.text(2.2, 9.2, "Case", fontsize=13, fontweight="bold")
    ax.text(7.2, 9.2, "Physics", fontsize=13, fontweight="bold")
    ax.text(12.2, 9.2, "Value", fontsize=13, fontweight="bold")
    rows = [
        ("Submarine\nOcean Probe", "Buoyancy\nArchimedes\nPressure", "Application\nEngineering", 7.0),
        ("LiDAR\nAuto Drive", "Reflection\nRanging", "Principle\nInterest", 4.2),
        ("EV\nBattery Pack", "I/U\nSeries-Parallel\nE Transfer", "Electricity\nGreen Energy", 1.4),
    ]
    for left, mid, right, y in rows:
        add_box(0.8, y, 3.0, 1.6, left)
        add_box(5.8, y, 3.2, 1.6, mid)
        add_box(10.8, y, 3.4, 1.6, right)
        ax.plot([3.8, 5.8], [y + 0.8, y + 0.8], linestyle="--", linewidth=1.5)
        ax.plot([9.0, 10.8], [y + 0.8, y + 0.8], linestyle="--", linewidth=1.5)
    ax.set_title("CM")
    fig.tight_layout()
    return fig


def make_interest_comparison(df: pd.DataFrame, case_col: str, pre_col: str, post_col: str):
    grouped = df.groupby(case_col)[[pre_col, post_col]].mean().reset_index()
    x = np.arange(len(grouped))
    width = 0.35
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.bar(x - width / 2, grouped[pre_col], width, label="Pre")
    ax.bar(x + width / 2, grouped[post_col], width, label="Post")
    ax.set_xticks(x)
    ax.set_xticklabels(grouped[case_col])
    ax.set_ylabel("Mean Score")
    ax.set_title("PIC")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    return fig


# ---------- 侧边栏 ----------
st.sidebar.title("📚 导航菜单")
page = st.sidebar.radio(
    "选择页面",
    [
        "首页总览",
        "案例一：深海探测与浮力",
        "案例二：激光雷达与光现象",
        "案例三：新能源汽车与电学",
        "综合关系图",
        "研究数据分析",
        "图片资料库",
        "附录说明",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**图片资源建议**")
st.sidebar.caption("请确保以下文件存在于 assets 文件夹中。")
st.sidebar.code(
    "assets/\n  submarine_structure.png\n  lidar_scan.jpg\n  ev_platform.jpg\n\n或直接与 app.py 放在同一目录",
    language="bash",
)
with st.sidebar.expander("可上传本次会话图片"):
    st.session_state["upload_submarine"] = st.file_uploader("上传潜航器/深海探测图片", type=["png", "jpg", "jpeg"], key="u1")
    st.session_state["upload_lidar"] = st.file_uploader("上传激光雷达/自动驾驶图片", type=["png", "jpg", "jpeg"], key="u2")
    st.session_state["upload_ev"] = st.file_uploader("上传新能源汽车图片", type=["png", "jpg", "jpeg"], key="u3")


# ---------- 页面 ----------
if page == "首页总览":
    header_block(
        "物理前沿知识融入初中物理教学交互平台",
        "围绕深海探测、激光雷达、新能源汽车三个案例，构建可视化、可交互、可用于硕士论文展示的研究型界面。",
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("案例数量", "3", "浮力 / 光学 / 电学")
    with c2:
        metric_card("研究维度", "4", "知识、情境、素养、应用")
    with c3:
        metric_card("图表模块", "5+", "原理图、关系图、数据分析")
    with c4:
        metric_card("交互功能", "完整", "参数调节、图片库、数据上传")

    section_title("研究目标")
    col1, col2 = st.columns([1.15, 1])
    with col1:
        card_html(
            "总体说明",
            "本应用围绕“物理前沿知识在初中物理教学中的融合”这一主题，采用案例化展示方式，将深海探测、激光雷达、新能源汽车三个前沿情境，与初中物理中的浮力、光现象和电学知识建立对应关系。应用既可作为论文展示界面，也可作为课堂汇报或答辩辅助材料。",
        )
    with col2:
        st.image(
            get_case_image(
                "submarine",
                [os.path.join(ASSET_DIR, "submarine_structure.png"), os.path.join(BASE_DIR, "submarine_structure.png"), "submarine_structure.png"],
                "Submarine Case",
                "Core structure and buoyancy principle",
            ),
            use_container_width=True,
        )

    section_title("案例概览")
    col1, col2, col3 = st.columns(3)
    with col1:
        card_html("案例一：浮力与深海探测", "以深海潜航器和海洋探测器为情境，把浮力、阿基米德原理、浮沉条件与液体压强联系起来，帮助学生理解浮力知识在深海工程中的实际作用。")
    with col2:
        card_html("案例二：光现象与激光雷达", "通过自动驾驶中的激光雷达，引导学生理解光的传播、反射与测距思想，认识光学知识在现代智能交通中的技术价值。")
    with col3:
        card_html("案例三：电学与新能源汽车", "围绕电池、电机和充电系统，连接电流、电压、电阻、串并联和电能转化知识，让学生感受电学与绿色能源技术的现实联系。")

    st.markdown(
        """
        <div class="note-box">
        <b>使用建议：</b> 首页适合在答辩或汇报中展示研究框架；三大案例页可分别截屏作为论文附图；数据分析页适合展示问卷或课堂前后测结果；图片资料库页则方便在不同场合快速切换素材。
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "案例一：深海探测与浮力":
    header_block("案例一：浮力教学与深海探测技术融合", "将深海潜航器、海洋探测器等前沿技术情境引入浮力教学。")
    left, right = st.columns([1.1, 1])
    with left:
        section_title("情境图片")
        st.image(
            get_case_image(
                "submarine",
                [os.path.join(ASSET_DIR, "submarine_structure.png"), os.path.join(BASE_DIR, "submarine_structure.png"), "submarine_structure.png"],
                "Submarine Case",
                "Core structure and buoyancy principle",
            ),
            use_container_width=True,
        )
    with right:
        section_title("教学融合说明")
        st.markdown("<span class='case-pill'>浮力</span><span class='case-pill'>阿基米德原理</span><span class='case-pill'>浮沉条件</span><span class='case-pill'>液体压强</span>", unsafe_allow_html=True)
        st.write("在讲浮力的时候，可以引入深海潜航器和海洋探测器。设备在海中运行时，不仅要解决下沉和上浮的问题，还要适应深海环境中的巨大压强。通过这个案例，学生能够明白浮力知识并不只用于判断物体是否漂浮，还能服务于真实工程技术。")
        with st.expander("可直接写入论文的表述"):
            st.write("深海探测技术为浮力教学提供了真实问题情境。通过分析潜航器在深海中下潜、悬停和上浮的条件，学生能够将浮力、阿基米德原理、浮沉条件和液体压强等知识联系起来，从而增强对物理知识实际应用价值的理解。")

    section_title("交互图表：深海压强随深度变化")
    c1, c2, c3 = st.columns(3)
    with c1:
        max_depth = st.slider("最大深度（m）", 1000, 11000, 11000, 500)
    with c2:
        rho = st.slider("海水密度（kg/m³）", 1000, 1100, 1025, 5)
    with c3:
        g = st.slider("重力加速度（m/s²）", 9.7, 9.9, 9.81, 0.01)
    fig = make_depth_pressure_figure(max_depth=max_depth, rho=float(rho), g=float(g))
    st.pyplot(fig, use_container_width=True)
    st.caption("缩写说明：DPD = 深海压强随深度变化图（Depth-Pressure Diagram）")
    st.caption("参数说明：rho = 海水密度，g = 重力加速度")
    st.download_button("下载图1（PNG）", data=fig_to_bytes(fig), file_name="图1_深海压强随深度变化图.png", mime="image/png")
    plt.close(fig)
    c1, c2 = st.columns(2)
    with c1:
        card_html("课堂可提问题", "1. 为什么深海潜航器不能只考虑会不会浮？<br>2. 深度越大，外壳为什么要更坚固？<br>3. 如果要让探测器重新上浮，可以改变哪些条件？")
    with c2:
        card_html("素养提升点", "帮助学生理解物理规律在复杂工程环境中的综合应用，形成从“单一知识点”走向“系统思考”的学习视角。")

elif page == "案例二：激光雷达与光现象":
    header_block("案例二：光现象教学与激光雷达融合", "通过自动驾驶中的激光雷达技术，建立光的反射、测距原理与现代传感的联系。")
    left, right = st.columns([1.05, 1])
    with left:
        st.image(
            get_case_image(
                "lidar",
                [os.path.join(ASSET_DIR, "lidar_scan.jpg"), os.path.join(BASE_DIR, "lidar_scan.jpg"), "lidar_scan.jpg"],
                "LiDAR Case",
                "LiDAR ranging and environment sensing",
            ),
            use_container_width=True,
        )
    with right:
        section_title("教学融合说明")
        st.markdown("<span class='case-pill'>光的传播</span><span class='case-pill'>光的反射</span><span class='case-pill'>测距原理</span><span class='case-pill'>现代传感</span>", unsafe_allow_html=True)
        st.write("激光雷达的基本原理是发射光信号，再接收反射回来的光，通过光的往返时间判断前方物体的位置和距离。这个案例能把课本中的光学知识转化为实际测量方法，让学生理解光不仅能“看见”物体，还能“测量”物体。")
        with st.expander("适合课堂导入的问题"):
            st.write("自动驾驶汽车为什么能够知道前方是否有障碍物、障碍物离自己有多远？")

    section_title("交互图表：激光雷达测距原理")
    c1, c2, c3 = st.columns(3)
    with c1:
        distance = st.slider("目标距离（m）", 1.0, 100.0, 30.0, 1.0)
    with c2:
        angle = st.slider("目标方位角（°）", -30, 30, 0, 1)
    with c3:
        c = st.number_input("光速（m/s）", value=3.0e8, format="%.2e")
    tof = 2 * distance / c
    fig = make_lidar_figure(distance_m=distance, angle_deg=float(angle))
    st.pyplot(fig, use_container_width=True)
    st.caption("缩写说明：LiDAR-RM = 激光雷达测距原理图；OBJ = 前方目标物体")
    st.caption("公式说明：d = ct/2，其中 d 为距离，c 为光速，t 为往返时间")
    st.download_button("下载图2（PNG）", data=fig_to_bytes(fig), file_name="图2_激光雷达测距原理图.png", mime="image/png")
    plt.close(fig)
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("目标距离", f"{distance:.1f} m", "当前演示参数")
    with m2:
        metric_card("往返时间", f"{tof:.2e} s", "按 d = ct/2 计算")
    with m3:
        metric_card("教学关键词", "反射 + 测距", "从现象到应用")
    c1, c2 = st.columns(2)
    with c1:
        card_html("课堂可提问题", "1. 光信号为什么能用于测距？<br>2. 为什么激光雷达不仅要发光，还要接收反射光？<br>3. 如果前方环境更复杂，设备为什么要连续扫描多个方向？")
    with c2:
        card_html("论文可写价值", "该案例将光的传播与反射从静态现象转化为信息获取手段，有利于学生理解现代传感技术与基础光学知识之间的内在联系。")

elif page == "案例三：新能源汽车与电学":
    header_block("案例三：电学教学与新能源汽车融合", "围绕新能源汽车的电池系统、充电系统和能量转换过程，讲清初中电学知识的实际应用。")
    left, right = st.columns([1.05, 1])
    with left:
        st.image(
            get_case_image(
                "ev",
                [os.path.join(ASSET_DIR, "ev_platform.jpg"), os.path.join(BASE_DIR, "ev_platform.jpg"), "ev_platform.jpg"],
                "EV Case",
                "Core layout of EV battery, motor and control system",
            ),
            use_container_width=True,
        )
    with right:
        section_title("教学融合说明")
        st.markdown("<span class='case-pill'>电流</span><span class='case-pill'>电压</span><span class='case-pill'>串并联</span><span class='case-pill'>电能转化</span><span class='case-pill'>安全用电</span>", unsafe_allow_html=True)
        st.write("新能源汽车中涉及电池、电机和充电系统，与初中电学中的电流、电压、电阻和电路连接知识密切相关。通过这个案例，学生可以理解电池串并联的实际意义，认识电能如何转化为机械能，并增强安全用电意识。")
        with st.expander("适合写入论文的简洁表述"):
            st.write("新能源汽车案例把抽象的电学知识放入生活化、时代化的技术情境中，能够帮助学生理解电路连接、电能转化和安全用电等内容的现实意义。")

    section_title("交互图表：新能源汽车电池串并联")
    c1, c2, c3 = st.columns(3)
    with c1:
        n_series = st.slider("串联节数", 2, 10, 4, 1)
    with c2:
        n_parallel = st.slider("并联支路数", 1, 5, 2, 1)
    with c3:
        cell_voltage = st.number_input("单体电池标称电压（V）", min_value=1.0, max_value=5.0, value=3.7, step=0.1)
    cell_capacity = st.number_input("单体电池容量（Ah）", min_value=1.0, max_value=200.0, value=50.0, step=1.0)
    total_voltage = n_series * cell_voltage
    total_capacity = n_parallel * cell_capacity
    total_energy = total_voltage * total_capacity / 1000
    fig = make_battery_figure(n_series=n_series, n_parallel=n_parallel)
    st.pyplot(fig, use_container_width=True)
    st.caption("缩写说明：EV-BSP = 新能源汽车电池串并联示意图（EV Battery Series-Parallel）")
    st.caption("图中 C1-1、C1-2 等表示单体电池编号")
    st.download_button("下载图3（PNG）", data=fig_to_bytes(fig), file_name="图3_新能源汽车电池串并联示意图.png", mime="image/png")
    plt.close(fig)
    m1, m2, m3 = st.columns(3)
    with m1:
        metric_card("总电压", f"{total_voltage:.1f} V", "串联决定电压")
    with m2:
        metric_card("总容量", f"{total_capacity:.1f} Ah", "并联增强容量")
    with m3:
        metric_card("理论能量", f"{total_energy:.2f} kWh", "E≈U×Q")
    c1, c2 = st.columns(2)
    with c1:
        card_html("课堂可提问题", "1. 为什么汽车电池不是一节，而是很多节组合？<br>2. 想提高总电压，应该怎么接？<br>3. 为什么充电过程中必须强调安全？")
    with c2:
        card_html("教学价值", "该案例与学生日常生活联系紧密，能够增强电学学习的现实感和时代感，同时帮助学生建立绿色能源和技术应用的基本认识。")

elif page == "综合关系图":
    header_block("前沿知识融入初中物理教学的案例对应关系", "通过关系图集中呈现三个案例与物理知识、教学价值之间的对应结构。")
    fig = make_mapping_figure()
    st.pyplot(fig, use_container_width=True)
    st.caption("缩写说明：CM = 案例对应关系图（Case Mapping）")
    st.caption("Submarine/Ocean Probe = 深海潜航器与海洋探测；LiDAR/Auto Drive = 激光雷达与自动驾驶；EV/Battery Pack = 新能源汽车电池系统")
    st.download_button("下载图4（PNG）", data=fig_to_bytes(fig), file_name="图4_前沿知识融入初中物理教学的案例对应关系图.png", mime="image/png")
    plt.close(fig)
    section_title("论文写作提示")
    c1, c2 = st.columns(2)
    with c1:
        card_html("正文可配套表述", "三个案例分别对应初中物理中的浮力、光学和电学内容，具有较强的代表性和现实意义。通过将深海探测、激光雷达和新能源汽车等现代技术引入课堂，能够帮助学生更直观地理解物理知识在实际生活和科技发展中的作用。")
    with c2:
        card_html("答辩展示建议", "先展示关系图，再逐一进入三个案例页面，可以形成“总—分—总”的展示逻辑，使论文结构更清楚、论证更完整。")

elif page == "研究数据分析":
    header_block("研究数据分析模块", "支持上传课堂前后测、问卷或访谈整理后的 CSV 数据，自动生成适合论文展示的统计图。")
    section_title("示例数据格式")
    demo_df = pd.DataFrame(
        {
            "案例": ["深海探测", "深海探测", "激光雷达", "激光雷达", "新能源汽车", "新能源汽车"],
            "兴趣前测": [3.1, 3.3, 3.4, 3.5, 3.2, 3.6],
            "兴趣后测": [4.2, 4.1, 4.5, 4.4, 4.3, 4.2],
            "成绩前测": [68, 72, 71, 73, 69, 74],
            "成绩后测": [82, 85, 86, 84, 83, 88],
        }
    )
    st.dataframe(demo_df, use_container_width=True)
    csv_data = demo_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("下载示例 CSV 模板", data=csv_data, file_name="sample_survey.csv", mime="text/csv")
    uploaded = st.file_uploader("上传你的 CSV 数据", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.success("数据读取成功。")
        except Exception as e:
            st.error(f"读取失败：{e}")
            df = None
    else:
        df = demo_df.copy()
        st.info("当前展示的是示例数据。")

    if df is not None:
        section_title("字段设置")
        cols = df.columns.tolist()
        c1, c2, c3 = st.columns(3)
        with c1:
            case_col = st.selectbox("案例字段", cols, index=0)
        with c2:
            pre_col = st.selectbox("前测字段", cols, index=1 if len(cols) > 1 else 0)
        with c3:
            post_col = st.selectbox("后测字段", cols, index=2 if len(cols) > 2 else 0)
        fig = make_interest_comparison(df, case_col, pre_col, post_col)
        st.pyplot(fig, use_container_width=True)
        st.caption("缩写说明：PIC = 前后测对比图（Pre/Post Interest Comparison）")
        st.download_button("下载兴趣变化图（PNG）", data=fig_to_bytes(fig), file_name="兴趣变化对比图.png", mime="image/png")
        plt.close(fig)
        section_title("统计摘要")
        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("样本行数", str(len(df)), "当前数据记录数")
        with c2:
            metric_card("前测均值", f"{pd.to_numeric(df[pre_col], errors='coerce').mean():.2f}", "按选定字段计算")
        with c3:
            metric_card("后测均值", f"{pd.to_numeric(df[post_col], errors='coerce').mean():.2f}", "按选定字段计算")
        with st.expander("论文中可以这样写"):
            st.write("为更直观地呈现案例教学的实施效果，本文借助 Python 对学生前后测数据进行了统计处理和图形化展示。结果表明，前沿科技案例引入课堂后，学生在学习兴趣和理解程度方面均表现出一定提升。")

elif page == "图片资料库":
    header_block("图片资料库与素材管理", "适合在论文写作、答辩展示和课堂汇报中快速切换深海探测、激光雷达和新能源汽车的图片资源。")
    tabs = st.tabs(["深海探测", "激光雷达", "新能源汽车"])
    configs = [
        (tabs[0], "submarine", [os.path.join(ASSET_DIR, "submarine_structure.png"), os.path.join(BASE_DIR, "submarine_structure.png"), "submarine_structure.png"], "Submarine Case", "Core structure and buoyancy principle"),
        (tabs[1], "lidar", [os.path.join(ASSET_DIR, "lidar_scan.jpg"), os.path.join(BASE_DIR, "lidar_scan.jpg"), "lidar_scan.jpg"], "LiDAR Case", "LiDAR ranging and environment sensing"),
        (tabs[2], "ev", [os.path.join(ASSET_DIR, "ev_platform.jpg"), os.path.join(BASE_DIR, "ev_platform.jpg"), "ev_platform.jpg"], "EV Case", "Core layout of EV battery, motor and control system"),
    ]
    for tab, key, candidates, title, desc in configs:
        with tab:
            col1, col2 = st.columns([1.1, 1])
            with col1:
                st.image(get_case_image(key, candidates, title, desc), use_container_width=True)
            with col2:
                card_html("素材说明", f"当前模块用于管理 {title}。建议图片风格尽量统一，便于整篇论文和答辩 PPT 的视觉呈现。若没有本地图片，系统会显示占位图。")
                st.markdown("**调用的本地文件名：**")
                st.code("\n".join(candidates), language="bash")
                st.markdown("**推荐图注：**")
                st.write(f"图：{desc}")

elif page == "附录说明":
    header_block("附录说明与运行指南", "帮助你把本应用用于论文写作、课堂展示和硕士答辩。")
    section_title("运行方式")
    st.code("streamlit run app.py", language="bash")
    section_title("推荐目录结构")
    st.code(
        """
project/
├─ app.py
├─ submarine_structure.png
├─ lidar_scan.jpg
├─ ev_platform.jpg
├─ assets/
│  ├─ submarine_structure.png
│  ├─ lidar_scan.jpg
│  └─ ev_platform.jpg
└─ figures/
        """.strip(),
        language="bash",
    )
    c1, c2 = st.columns(2)
    with c1:
        card_html("适合写进论文的方法说明", "本文借助 Python 与 Streamlit 构建了可视化交互平台，用于呈现深海探测、激光雷达和新能源汽车三个前沿案例与初中物理知识之间的对应关系。平台集成了原理图展示、案例讲解、图片管理和数据分析功能，可提升研究结果的直观性与展示效果。")
    with c2:
        card_html("答辩使用建议", "答辩时建议先展示首页总览，再依次进入三个案例页面，最后展示综合关系图和数据分析页。这样既能体现理论框架，也能展示研究设计与可视化成果。")
    st.markdown(
        """
        <div class="footer-box">
        <b>说明：</b> 本应用为单文件版本，便于直接作为论文配套程序提交。若后续需要继续升级，可以进一步拆分为 pages、components、data 等模块化结构。
        </div>
        """,
        unsafe_allow_html=True,
    )
