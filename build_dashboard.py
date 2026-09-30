"""Generate slide-ready IE313 charts and dashboard pages from the local CSV.

Run from any directory with: python build_dashboard.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "E-commerce_Customer_Behavior.csv"
CHARTS = ROOT / "charts"

BG = "#0A1020"
PANEL = "#121D31"
GRID = "#283950"
TEXT = "#F3F6FB"
MUTED = "#A6B6CC"
CYAN = "#52D6D0"
GOLD = "#F1BE6A"
BLUE = "#789BFF"
ROSE = "#F18E9B"
COLORS = {"Gold": GOLD, "Silver": BLUE, "Bronze": CYAN}
MEMBERSHIPS = ["Bronze", "Silver", "Gold"]

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "text.color": TEXT,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "font.size": 10,
        "savefig.facecolor": BG,
    }
)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA)
    required = {
        "Customer ID", "Age", "Membership Type", "Total Spend",
        "Items Purchased", "Days Since Last Purchase", "Satisfaction Level",
        "Discount Applied",
    }
    missing_columns = required - set(df.columns)
    if missing_columns:
        raise ValueError(f"CSV thiếu cột: {', '.join(sorted(missing_columns))}")
    if df["Customer ID"].duplicated().any():
        raise ValueError("Customer ID bị trùng; cần kiểm tra dữ liệu trước khi vẽ.")
    for column in ("Age", "Total Spend", "Items Purchased", "Days Since Last Purchase"):
        df[column] = pd.to_numeric(df[column], errors="raise")
    if df[list(required - {"Satisfaction Level"})].isna().any().any():
        raise ValueError("Có giá trị thiếu ở trường cần cho biểu đồ.")
    if not set(df["Membership Type"]).issubset(set(MEMBERSHIPS)):
        raise ValueError("Membership Type có nhãn ngoài Gold, Silver, Bronze.")
    if not set(df["Satisfaction Level"].dropna()).issubset(
        {"Satisfied", "Neutral", "Unsatisfied"}
    ):
        raise ValueError("Satisfaction Level có nhãn không hợp lệ.")
    if not pd.api.types.is_bool_dtype(df["Discount Applied"]):
        mapped = df["Discount Applied"].astype(str).str.lower().map({"true": True, "false": False})
        if mapped.isna().any():
            raise ValueError("Discount Applied phải có giá trị TRUE/FALSE.")
        df["Discount Applied"] = mapped.astype(bool)
    return df


def style_ax(ax, *, ygrid: bool = True) -> None:
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=6, labelsize=9)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.8)
        ax.set_axisbelow(True)


def card(fig, box, title: str, subtitle: str, *, bottom_note: str = ""):
    x, y, w, h = box
    fig.add_artist(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.004,rounding_size=0.013",
            transform=fig.transFigure,
            facecolor=PANEL,
            edgecolor=GRID,
            linewidth=0.7,
            zorder=0,
        )
    )
    fig.text(x + 0.018, y + h - 0.043, title, size=15, weight="bold", color=TEXT)
    fig.text(x + 0.018, y + h - 0.067, subtitle, size=9.3, color=MUTED)
    if bottom_note:
        fig.text(x + 0.018, y + 0.015, bottom_note, size=8.7, color=MUTED)
    return [x + 0.048, y + 0.066, w - 0.072, h - 0.155]


def chart_age(df, fig, area):
    ax = fig.add_axes(area)
    style_ax(ax)
    bins = np.arange(25.5, 44.6, 2)
    ax.hist(df["Age"], bins=bins, color=CYAN, edgecolor=BG, linewidth=1.2)
    ax.set_xlabel("Tuổi")
    ax.set_ylabel("Số khách")
    ax.set_xticks([26, 30, 34, 38, 42])
    ax.set_xlim(25.5, 44.5)
    return ax


def chart_membership(df, fig, area):
    ax = fig.add_axes(area)
    counts = df["Membership Type"].value_counts().reindex(MEMBERSHIPS, fill_value=0)
    wedges, _, autotexts = ax.pie(
        counts,
        labels=MEMBERSHIPS,
        colors=[COLORS[x] for x in MEMBERSHIPS],
        autopct=lambda pct: f"{pct:.1f}%",
        startangle=90,
        wedgeprops={"width": 0.42, "edgecolor": BG, "linewidth": 2},
        pctdistance=0.78,
        textprops={"color": TEXT, "fontsize": 9},
    )
    for text_item in autotexts:
        text_item.set_color(BG)
        text_item.set_weight("bold")
    ax.text(0, 0, f"{counts.sum()}\nkhách", ha="center", va="center",
            color=TEXT, weight="bold", fontsize=11)
    ax.set_aspect("equal")
    return ax


def chart_spend_distribution(df, fig, area):
    x, y, w, h = area
    ax = fig.add_axes([x, y + h * 0.23, w, h * 0.77])
    style_ax(ax)
    values = df["Total Spend"]
    ax.hist(values, bins=np.arange(400, 1601, 100), color=BLUE, edgecolor=BG, linewidth=1.2)
    ax.set_ylabel("Số khách")
    ax.tick_params(labelbottom=False)
    bx = fig.add_axes([x, y, w, h * 0.17], sharex=ax)
    style_ax(bx, ygrid=False)
    bx.boxplot(
        values, vert=False, widths=0.5, patch_artist=True,
        boxprops={"facecolor": GOLD, "edgecolor": GOLD},
        medianprops={"color": BG, "linewidth": 2},
        whiskerprops={"color": GOLD}, capprops={"color": GOLD},
        flierprops={"marker": "o", "markerfacecolor": ROSE, "markersize": 4},
    )
    bx.set_yticks([])
    bx.set_xlabel("Tổng chi tiêu (đơn vị chưa xác định)")
    bx.set_xticks([400, 700, 1000, 1300, 1600])
    bx.set_xlim(400, 1600)
    return ax


def chart_spend_membership(df, fig, area):
    ax = fig.add_axes(area)
    style_ax(ax)
    groups = [df.loc[df["Membership Type"] == m, "Total Spend"] for m in MEMBERSHIPS]
    bp = ax.boxplot(
        groups, patch_artist=True, widths=0.45,
        medianprops={"color": BG, "linewidth": 2},
        whiskerprops={"color": MUTED}, capprops={"color": MUTED},
        flierprops={"marker": "o", "markerfacecolor": ROSE, "markeredgecolor": ROSE, "markersize": 4},
    )
    for patch, member in zip(bp["boxes"], MEMBERSHIPS):
        patch.set_facecolor(COLORS[member])
        patch.set_edgecolor(COLORS[member])
    ax.set_xticks([1, 2, 3], MEMBERSHIPS)
    ax.set_ylabel("Tổng chi tiêu (đơn vị chưa xác định)")
    ax.set_ylim(300, 1640)
    for i, group in enumerate(groups, start=1):
        ax.text(i, group.median() + 55, f"{group.median():,.0f}",
                color=TEXT, ha="center", size=9, weight="bold")
    return ax


def chart_scatter(df, fig, area, xcol: str, xlabel: str, r: float):
    ax = fig.add_axes(area)
    style_ax(ax)
    for member in MEMBERSHIPS:
        subset = df[df["Membership Type"] == member]
        ax.scatter(subset[xcol], subset["Total Spend"], s=23,
                   color=COLORS[member], alpha=0.63, edgecolors="none", label=member)
    slope, intercept = np.polyfit(df[xcol], df["Total Spend"], 1)
    xs = np.array([df[xcol].min(), df[xcol].max()])
    ax.plot(xs, slope * xs + intercept, color=TEXT, alpha=0.8,
            linestyle="--", linewidth=1.3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Tổng chi tiêu (đơn vị chưa xác định)")
    ax.text(0.98, 0.95, f"Pearson r = {r:+.2f}", transform=ax.transAxes,
            ha="right", va="top", color=TEXT, size=10, weight="bold",
            bbox={"facecolor": PANEL, "edgecolor": GRID, "pad": 4})
    return ax


def chart_satisfaction(df, fig, area):
    ax = fig.add_axes(area)
    style_ax(ax, ygrid=False)
    levels = ["Unsatisfied", "Neutral", "Satisfied"]
    level_colors = [ROSE, BLUE, CYAN]
    table = pd.crosstab(df["Membership Type"], df["Satisfaction Level"])
    table = table.reindex(index=MEMBERSHIPS, columns=levels, fill_value=0)
    pct = table.div(table.sum(axis=1), axis=0).fillna(0) * 100
    left = np.zeros(len(MEMBERSHIPS))
    for level, color in zip(levels, level_colors):
        vals = pct[level].to_numpy()
        bars = ax.barh(MEMBERSHIPS, vals, left=left, color=color, height=0.54,
                       label=level, edgecolor=PANEL, linewidth=1)
        for bar, value in zip(bars, vals):
            if value >= 10:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + bar.get_height() / 2,
                        f"{value:.0f}%", ha="center", va="center",
                        color=BG if level == "Satisfied" else TEXT,
                        weight="bold", size=9)
        left += vals
    ax.set_xlim(0, 100)
    ax.set_xlabel("Tỷ lệ trong hạng thành viên (%)")
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.invert_yaxis()
    legend_y = area[1] + area[3] + 0.022
    for legend_x, level, color in zip(
        [area[0], area[0] + 0.125, area[0] + 0.235], levels, level_colors
    ):
        fig.add_artist(
            plt.Line2D([legend_x, legend_x + 0.012], [legend_y, legend_y],
                       transform=fig.transFigure, color=color, linewidth=7)
        )
        fig.text(legend_x + 0.018, legend_y - 0.004, level, color=MUTED, size=8.3)
    return ax


def chart_discount(df, fig, area):
    ax = fig.add_axes(area)
    style_ax(ax)
    groups = [df.loc[df["Discount Applied"] == b, "Total Spend"] for b in [False, True]]
    bp = ax.boxplot(
        groups, patch_artist=True, widths=0.45,
        medianprops={"color": BG, "linewidth": 2},
        whiskerprops={"color": MUTED}, capprops={"color": MUTED},
        flierprops={"marker": "o", "markerfacecolor": ROSE, "markeredgecolor": ROSE, "markersize": 4},
    )
    for patch, color in zip(bp["boxes"], [BLUE, CYAN]):
        patch.set_facecolor(color)
        patch.set_edgecolor(color)
    ax.set_xticks([1, 2], ["Không giảm giá", "Có giảm giá"])
    ax.set_ylabel("Tổng chi tiêu (đơn vị chưa xác định)")
    ax.set_ylim(300, 1640)
    for i, group in enumerate(groups, start=1):
        ax.text(i, group.median() + 55, f"Trung vị {group.median():,.0f}",
                color=TEXT, ha="center", size=9, weight="bold")
    return ax


def dashboard_header(fig, section: str, number: str, metrics: list[tuple[str, str]]):
    fig.patch.set_facecolor(BG)
    fig.text(0.045, 0.954, "IE313  /  PHÂN TÍCH HÀNH VI KHÁCH HÀNG", color=CYAN,
             size=10, weight="bold")
    fig.text(0.045, 0.904, section, color=TEXT, size=28, weight="bold")
    fig.text(0.955, 0.951, f"DASHBOARD  {number} / 02", ha="right", color=MUTED, size=10)
    for i, (label, value) in enumerate(metrics):
        x = 0.045 + i * 0.235
        fig.text(x, 0.846, value, color=TEXT,
                 size=18 if len(value) >= 7 else 21, weight="bold")
        fig.text(x, 0.820, label, color=MUTED, size=9.5)
    fig.add_artist(plt.Line2D([0.045, 0.955], [0.800, 0.800], transform=fig.transFigure,
                              color=GRID, linewidth=1))


def dashboard_footer(fig, insight: str, caveat: str):
    fig.text(0.045, 0.062, "ĐỌC NHANH", color=CYAN, size=9.2, weight="bold")
    fig.text(0.127, 0.062, insight, color=TEXT, size=10.5)
    fig.text(0.045, 0.025, caveat, color=MUTED, size=8.4)
    fig.text(0.955, 0.025, "Nguồn: data/E-commerce_Customer_Behavior.csv", ha="right",
             color=MUTED, size=8.4)


def build_dashboard(df: pd.DataFrame):
    boxes = [(0.045, 0.465, 0.442, 0.313), (0.513, 0.465, 0.442, 0.313),
             (0.045, 0.130, 0.442, 0.313), (0.513, 0.130, 0.442, 0.313)]
    median_spend = df["Total Spend"].median()
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    dashboard_header(fig, "Chân dung & mức chi tiêu", "01", [
        ("Khách hàng", f"{len(df):,}"),
        ("Trung vị chi tiêu", f"{median_spend:,.1f}"),
        ("Tuổi trung vị", f"{df['Age'].median():g}"),
        ("Thiếu mức hài lòng", f"{df['Satisfaction Level'].isna().sum()} dòng"),
    ])
    chart_age(df, fig, card(fig, boxes[0], "01  Phân phối tuổi", "Độ tuổi phổ biến trong mẫu"))
    chart_membership(df, fig, card(fig, boxes[1], "02  Cơ cấu hạng thành viên", "Số lượng và tỷ trọng từng hạng"))
    chart_spend_distribution(df, fig, card(fig, boxes[2], "03  Phân phối chi tiêu", "Histogram và boxplot cùng thang đo"))
    chart_spend_membership(df, fig, card(fig, boxes[3], "04  Chi tiêu theo hạng", "Số trong hộp là trung vị"))
    med = df.groupby("Membership Type")["Total Spend"].median()
    dashboard_footer(
        fig,
        f"Gold có trung vị chi tiêu {med['Gold']:,.1f}; Bronze {med['Bronze']:,.1f} (đơn vị chưa xác định).",
        "Thống kê mô tả trên 350 dòng; CSV không xác nhận đơn vị tiền tệ của Total Spend.",
    )
    fig.savefig(CHARTS / "dashboard_01_tong_quan.png", dpi=100)
    plt.close(fig)

    r_items = df["Items Purchased"].corr(df["Total Spend"])
    r_days = df["Days Since Last Purchase"].corr(df["Total Spend"])
    sat_valid = df["Satisfaction Level"].notna().sum()
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    dashboard_header(fig, "Mối liên hệ & so sánh nhóm", "02", [
        ("r: số SP / chi tiêu", f"{r_items:+.2f}"),
        ("r: số ngày / chi tiêu", f"{r_days:+.2f}"),
        ("Có mức hài lòng", f"{sat_valid}/{len(df)}"),
        ("Số khách mỗi nhóm giảm giá", f"{df['Discount Applied'].value_counts().min()}"),
    ])
    chart_scatter(df, fig, card(fig, boxes[0], "05  Số sản phẩm & chi tiêu", "Mỗi chấm là một khách hàng"),
                  "Items Purchased", "Số sản phẩm đã mua", r_items)
    chart_scatter(df, fig, card(fig, boxes[1], "06  Ngày từ lần mua gần nhất & chi tiêu", "Đường đứt là xu hướng tuyến tính"),
                  "Days Since Last Purchase", "Số ngày từ lần mua gần nhất", r_days)
    chart_satisfaction(df, fig, card(fig, boxes[2], "07  Hài lòng theo hạng", ""))
    chart_discount(df, fig, card(fig, boxes[3], "08  Chi tiêu & giảm giá", "So sánh phân phối hai nhóm"))
    dashboard_footer(
        fig,
        "Số sản phẩm liên hệ dương mạnh với chi tiêu; số ngày từ lần mua gần nhất liên hệ âm vừa.",
        f"Biểu đồ hài lòng chỉ loại {len(df) - sat_valid} dòng thiếu; tương quan và chênh lệch nhóm không chứng minh nhân quả.",
    )
    fig.savefig(CHARTS / "dashboard_02_moi_lien_he.png", dpi=100)
    plt.close(fig)


def build_individual_charts(df: pd.DataFrame):
    r_items = df["Items Purchased"].corr(df["Total Spend"])
    r_days = df["Days Since Last Purchase"].corr(df["Total Spend"])
    specs = [
        ("01_phan_phoi_tu.png", "Phân phối tuổi", "Histogram Age", chart_age),
        ("02_co_cau_hang_thanh_vien.png", "Cơ cấu hạng thành viên", "Số lượng và tỷ trọng", chart_membership),
        ("03_phan_phoi_chi_tieu.png", "Phân phối chi tiêu", "Histogram và boxplot Total Spend", chart_spend_distribution),
        ("04_chi_tieu_theo_hang.png", "Chi tiêu theo hạng thành viên", "Boxplot Total Spend theo Membership Type", chart_spend_membership),
        ("05_so_san_pham_va_chi_tieu.png", "Số sản phẩm và chi tiêu", f"Pearson r = {r_items:+.3f}",
         lambda d, f, a: chart_scatter(d, f, a, "Items Purchased", "Số sản phẩm đã mua", r_items)),
        ("06_so_ngay_va_chi_tieu.png", "Ngày từ lần mua gần nhất và chi tiêu", f"Pearson r = {r_days:+.3f}",
         lambda d, f, a: chart_scatter(d, f, a, "Days Since Last Purchase", "Số ngày từ lần mua gần nhất", r_days)),
        ("07_hai_long_theo_hang.png", "Mức hài lòng theo hạng", "Tỷ lệ %; chỉ tính dòng không thiếu",
         chart_satisfaction),
        ("08_chi_tieu_theo_giam_gia.png", "Chi tiêu theo áp dụng giảm giá", "Boxplot; không suy diễn tác động nhân quả",
         chart_discount),
    ]
    for filename, title, subtitle, draw in specs:
        fig = plt.figure(figsize=(12.8, 7.2), dpi=150, facecolor=BG)
        fig.text(0.07, 0.92, "IE313  /  E-COMMERCE CUSTOMER BEHAVIOR", color=CYAN, size=10, weight="bold")
        fig.text(0.07, 0.855, title, color=TEXT, size=23, weight="bold")
        fig.text(0.07, 0.812, subtitle, color=MUTED, size=11)
        area = card(fig, (0.07, 0.115, 0.86, 0.645), "", "")
        draw(df, fig, area)
        fig.text(0.07, 0.055, "Nguồn: data/E-commerce_Customer_Behavior.csv", color=MUTED, size=9)
        fig.savefig(CHARTS / filename, dpi=150)
        plt.close(fig)


def main():
    CHARTS.mkdir(exist_ok=True)
    df = load_data()
    build_dashboard(df)
    build_individual_charts(df)
    print(f"Đã tạo 2 dashboard 1920×1080 và 8 biểu đồ trong {CHARTS}")
    print(f"Dòng dữ liệu: {len(df)}; thiếu Satisfaction Level: {df['Satisfaction Level'].isna().sum()}")


if __name__ == "__main__":
    main()
