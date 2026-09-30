"""Interactive IE313 dashboard with one shared filter context.

Run from the project folder with:
    python3 -m streamlit run dashboard.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from analysis_core import (
    MEMBERSHIPS,
    MISSING_SATISFACTION,
    SATISFACTION_LEVELS,
    SEGMENT_ORDER,
    SPEND_AXIS_LABEL,
    SPEND_UNIT,
    apply_filters,
    assign_customer_segments,
    city_behavior_profile,
    compute_kpis,
    fixed_segmentation_thresholds,
    load_clean_data,
)


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "E-commerce_Customer_Behavior.csv"
COLORS = {"Bronze": "#36B9B5", "Silver": "#678CF0", "Gold": "#E9AD51"}
SAT_COLORS = {"Unsatisfied": "#E98294", "Neutral": "#678CF0", "Satisfied": "#36B9B5"}
SEGMENT_COLORS = {
    "Chi tiêu cao · mua gần đây": "#0F8C86",
    "Chi tiêu cao · mua đã lâu": "#E98294",
    "Chi tiêu thấp · mua gần đây": "#678CF0",
    "Chi tiêu thấp · mua đã lâu": "#9AA5B5",
}
CITY_PROFILE_METRICS = [
    "Chi tiêu trung vị",
    "Sản phẩm trung vị",
    "Điểm đánh giá TB",
    "Tỷ lệ hài lòng (%)",
    "Tỷ lệ giảm giá (%)",
    "Ngày chưa mua trung vị",
]


@st.cache_data
def get_clean_data() -> tuple[pd.DataFrame, dict]:
    """Cache the shared, auditable cleaning result for the dashboard session."""
    return load_clean_data(DATA)


def theme(fig: go.Figure, title: str, x_title: str = "", y_title: str = "") -> go.Figure:
    """Apply the same readable light theme to every Plotly figure."""
    fig.update_layout(
        title={"text": title, "x": 0.02, "xanchor": "left"},
        height=430,
        margin={"l": 60, "r": 24, "t": 72, "b": 65},
        paper_bgcolor="#F6F8FC",
        plot_bgcolor="#FFFFFF",
        font={"color": "#162033", "family": "Arial"},
        legend={"orientation": "h", "y": 1.04, "x": 0},
        hoverlabel={"bgcolor": "#162033", "font": {"color": "#FFFFFF"}},
        bargap=0.24,
        bargroupgap=0.08,
    )
    fig.update_xaxes(title=x_title, gridcolor="#D9E1EE", zeroline=False)
    fig.update_yaxes(title=y_title, gridcolor="#D9E1EE", zeroline=False)
    return fig


def add_linear_trend(fig: go.Figure, data: pd.DataFrame, x_column: str) -> None:
    """Add a descriptive linear trend without implying causality."""
    valid = data[[x_column, "Total Spend"]].dropna()
    if len(valid) < 2 or valid[x_column].nunique() < 2:
        return
    slope, intercept = np.polyfit(valid[x_column], valid["Total Spend"], 1)
    x_values = np.array([valid[x_column].min(), valid[x_column].max()])
    fig.add_trace(go.Scatter(
        x=x_values,
        y=slope * x_values + intercept,
        mode="lines",
        name="Xu hướng tuyến tính",
        line={"color": "#162033", "dash": "dash", "width": 2},
        hoverinfo="skip",
    ))


def reset_filters(defaults: dict) -> None:
    """Restore every shared filter to its full-data selection."""
    for key, value in defaults.items():
        st.session_state[key] = value


def shared_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render always-visible global filters and return one filtered dataset."""
    cities = sorted(df["City"].dropna().unique().tolist())
    genders = sorted(df["Gender"].dropna().unique().tolist())
    discounts = [False, True]
    satisfaction_options = SATISFACTION_LEVELS + [MISSING_SATISFACTION]
    age_bounds = (int(df["Age"].min()), int(df["Age"].max()))
    defaults = {
        "filter_city": cities,
        "filter_gender": genders,
        "filter_membership": MEMBERSHIPS,
        "filter_discount": discounts,
        "filter_age": age_bounds,
        "filter_satisfaction": satisfaction_options,
    }

    with st.expander("Bộ lọc chung — áp dụng cho KPI và tất cả biểu đồ", expanded=True):
        row1 = st.columns(3)
        with row1[0]:
            selected_cities = st.multiselect("Thành phố", cities, default=cities, key="filter_city")
        with row1[1]:
            selected_genders = st.multiselect("Giới tính", genders, default=genders, key="filter_gender")
        with row1[2]:
            selected_memberships = st.multiselect(
                "Hạng thành viên", MEMBERSHIPS, default=MEMBERSHIPS, key="filter_membership"
            )
        row2 = st.columns(3)
        with row2[0]:
            selected_discounts = st.multiselect(
                "Sử dụng giảm giá",
                discounts,
                default=discounts,
                format_func=lambda value: "Có" if value else "Không",
                key="filter_discount",
            )
        with row2[1]:
            selected_age = st.slider(
                "Khoảng tuổi", age_bounds[0], age_bounds[1], age_bounds, key="filter_age"
            )
        with row2[2]:
            selected_satisfaction = st.multiselect(
                "Mức độ hài lòng",
                satisfaction_options,
                default=satisfaction_options,
                key="filter_satisfaction",
            )
        st.button("Đặt lại bộ lọc", on_click=reset_filters, args=(defaults,), use_container_width=False)

    return apply_filters(
        df,
        cities=selected_cities,
        genders=selected_genders,
        memberships=selected_memberships,
        discounts=selected_discounts,
        age_range=selected_age,
        satisfaction=selected_satisfaction,
    )


def value_or_dash(value: float | int | None, pattern: str) -> str:
    return "—" if value is None or pd.isna(value) else pattern.format(value)


def show_kpis(data: pd.DataFrame) -> None:
    """Display KPI01–KPI06 calculated from the same filtered rows."""
    kpi = compute_kpis(data)
    columns = st.columns(6)
    columns[0].metric("Số khách hàng", f"{kpi['customers']:,}")
    columns[0].caption("Customer ID duy nhất")
    columns[1].metric("Tổng chi tiêu ghi nhận", value_or_dash(kpi["total_spend"], "{:,.1f}"))
    columns[1].caption(SPEND_UNIT)
    columns[2].metric("Chi tiêu trung vị/khách", value_or_dash(kpi["median_spend"], "{:,.1f}"))
    columns[2].caption(SPEND_UNIT)
    columns[3].metric("Điểm đánh giá TB", value_or_dash(kpi["mean_rating"], "{:.2f}"))
    columns[3].caption(f"n hợp lệ = {kpi['rating_n']}")
    columns[4].metric("Tỷ lệ có giảm giá", value_or_dash(kpi["discount_rate"], "{:.1f}%"))
    columns[4].caption(f"mẫu số = {kpi['discount_n']}")
    columns[5].metric("Trung vị ngày chưa mua", value_or_dash(kpi["median_days"], "{:.1f}"))
    columns[5].caption("Không phải tỷ lệ rời bỏ")


def chart_age(data: pd.DataFrame) -> None:
    fig = px.histogram(data, x="Age", color_discrete_sequence=["#36B9B5"])
    start = int(data["Age"].min()) // 5 * 5
    fig.update_traces(xbins={"start": start, "end": int(data["Age"].max()) + 5, "size": 5})
    theme(fig, "CH01 · Phân phối độ tuổi", "Tuổi (khoảng 5 năm)", "Số khách")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Nguồn: `Age` · Tổng số đếm kiểm tra = {len(data)} khách có tuổi hợp lệ.")


def chart_city(data: pd.DataFrame) -> None:
    counts = data.groupby("City", observed=True)["Customer ID"].nunique().sort_values(ascending=False)
    frame = counts.rename("Số khách").reset_index()
    fig = px.bar(frame, x="City", y="Số khách", text="Số khách", color_discrete_sequence=["#678CF0"])
    fig.update_traces(textposition="outside")
    theme(fig, "CH02 · Số khách theo thành phố", "Thành phố", "Số khách")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Nguồn: `City`, `Customer ID` · Thành phố được sắp xếp theo số khách giảm dần.")


def build_city_profile_chart(data: pd.DataFrame) -> go.Figure:
    """Build CH10 with actual city values and per-metric 0–100 color scaling."""
    profile = city_behavior_profile(data)
    actual = profile[CITY_PROFILE_METRICS]
    normalized = actual.copy().astype(float)
    for column in CITY_PROFILE_METRICS:
        values = actual[column]
        minimum, maximum = values.min(), values.max()
        if pd.isna(minimum) or pd.isna(maximum):
            normalized[column] = np.nan
        elif maximum == minimum:
            normalized[column] = 50.0
        else:
            normalized[column] = (values - minimum) / (maximum - minimum) * 100

    city_labels = [f"{city} (n={int(profile.loc[city, 'Số khách'])})" for city in profile.index]
    cell_text = [
        ["—" if pd.isna(value) else f"{value:,.1f}" for value in row]
        for row in actual.to_numpy()
    ]
    fig = go.Figure(go.Heatmap(
        z=normalized.to_numpy(),
        x=CITY_PROFILE_METRICS,
        y=city_labels,
        customdata=actual.to_numpy(),
        text=cell_text,
        texttemplate="%{text}",
        hovertemplate="%{y}<br>%{x}: %{customdata:,.2f}<br>Mức tương đối: %{z:.1f}/100<extra></extra>",
        colorscale=[[0, "#EEF2FF"], [0.5, "#678CF0"], [1, "#0F8C86"]],
        zmin=0,
        zmax=100,
        colorbar={"title": "Tương đối<br>0–100"},
        hoverongaps=False,
    ))
    theme(fig, "CH10 · Hồ sơ hành vi theo thành phố", "Chỉ tiêu", "Thành phố")
    fig.update_layout(height=max(430, 70 * len(profile) + 210))
    fig.update_xaxes(side="top")
    return fig


def chart_city_profile(data: pd.DataFrame) -> None:
    st.plotly_chart(build_city_profile_chart(data), use_container_width=True)
    st.caption(
        "Số trong ô là giá trị thực · Màu được chuẩn hóa 0–100 riêng cho từng chỉ tiêu; "
        "100 là thành phố cao nhất trong tập đang lọc. Tỷ lệ hài lòng chỉ dùng khách có dữ liệu hợp lệ."
    )


def chart_membership(data: pd.DataFrame) -> None:
    counts = data.groupby("Membership Type", observed=True)["Customer ID"].nunique()
    counts = counts.reindex(MEMBERSHIPS, fill_value=0)
    frame = counts.rename("Số khách").reset_index()
    frame["Tỷ trọng"] = frame["Số khách"] / frame["Số khách"].sum()
    fig = px.pie(
        frame,
        names="Membership Type",
        values="Số khách",
        color="Membership Type",
        color_discrete_map=COLORS,
        category_orders={"Membership Type": MEMBERSHIPS},
        custom_data=["Tỷ trọng"],
        hole=0.48,
    )
    fig.update_traces(
        texttemplate="%{label}<br>%{value} khách · %{percent:.1%}",
        textposition="inside",
        hovertemplate="%{label}<br>Số khách: %{value}<br>Tỷ trọng: %{percent:.1%}<extra></extra>",
        sort=False,
        direction="clockwise",
    )
    theme(fig, "CH03 · Cơ cấu hạng thành viên")
    fig.update_layout(
        legend_title_text="Hạng thành viên",
        uniformtext_minsize=12,
        uniformtext_mode="hide",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Nguồn: `Membership Type`, `Customer ID` · Tỷ trọng các hạng cộng thành 100%.")


def chart_spend_distribution(data: pd.DataFrame) -> None:
    spend = data["Total Spend"].dropna()
    fig = px.histogram(data, x="Total Spend", nbins=12, color_discrete_sequence=["#678CF0"])
    if not spend.empty:
        fig.add_vline(x=spend.mean(), line_dash="dot", line_color="#E98294",
                      annotation_text=f"Mean {spend.mean():,.1f}")
        fig.add_vline(x=spend.median(), line_dash="dash", line_color="#162033",
                      annotation_text=f"Median {spend.median():,.1f}")
    theme(fig, "CH04 · Phân phối tổng chi tiêu", SPEND_AXIS_LABEL, "Số khách")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Nguồn: `Total Spend` · Ngoại lệ không bị xóa chỉ vì nằm ngoài ngưỡng boxplot.")


def chart_spend_membership(data: pd.DataFrame) -> None:
    counts = data.groupby("Membership Type", observed=True)["Customer ID"].nunique()
    part = data.copy()
    part["Hạng (n)"] = part["Membership Type"].map(
        lambda value: f"{value} (n={counts.get(value, 0)})"
    )
    order = [f"{value} (n={counts.get(value, 0)})" for value in MEMBERSHIPS if value in counts.index]
    fig = px.box(
        part,
        x="Hạng (n)",
        y="Total Spend",
        color="Membership Type",
        category_orders={"Hạng (n)": order},
        color_discrete_map=COLORS,
        points="outliers",
    )
    theme(fig, "CH05 · Chi tiêu theo hạng thành viên", "Hạng thành viên", SPEND_AXIS_LABEL)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Nguồn: `Membership Type`, `Total Spend` · Hộp thể hiện trung vị và IQR; ngoại lệ vẫn hiển thị.")


def chart_items_spend(data: pd.DataFrame) -> None:
    valid = data[["Customer ID", "Items Purchased", "Total Spend", "Membership Type"]].dropna()
    correlation = valid["Items Purchased"].corr(valid["Total Spend"])
    fig = px.scatter(
        valid,
        x="Items Purchased",
        y="Total Spend",
        color="Membership Type",
        color_discrete_map=COLORS,
        hover_data=["Customer ID"],
        opacity=0.65,
    )
    add_linear_trend(fig, valid, "Items Purchased")
    r_text = "—" if pd.isna(correlation) else f"{correlation:+.3f}"
    theme(fig, f"CH06 · Số sản phẩm và chi tiêu · Pearson r = {r_text}",
          "Số sản phẩm đã mua", SPEND_AXIS_LABEL)
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Mỗi điểm là một khách · `Items Purchased` là số sản phẩm, không phải số lần đặt hàng.")


def build_segment_chart(data: pd.DataFrame, spend_cut: float, days_cut: float) -> go.Figure:
    """Build CH07 as four spend/recency customer regions."""
    segmented = assign_customer_segments(data, spend_cut=spend_cut, days_cut=days_cut)
    fig = px.scatter(
        segmented,
        x="Days Since Last Purchase",
        y="Total Spend",
        color="Customer Segment",
        category_orders={"Customer Segment": SEGMENT_ORDER},
        color_discrete_map=SEGMENT_COLORS,
        hover_data=["Customer ID", "Membership Type"],
        opacity=0.72,
    )
    fig.add_vline(
        x=days_cut,
        line_dash="dash",
        line_color="#162033",
        annotation_text=f"Trung vị ngày = {days_cut:,.1f}",
    )
    fig.add_hline(
        y=spend_cut,
        line_dash="dash",
        line_color="#162033",
        annotation_text=f"Trung vị chi tiêu = {spend_cut:,.1f}",
    )
    quadrant_labels = [
        (0.18, 0.94, "Giá trị cao · đang hoạt động"),
        (0.82, 0.94, "Ưu tiên tái kích hoạt"),
        (0.18, 0.06, "Tiềm năng phát triển"),
        (0.82, 0.06, "Ưu tiên thấp hơn"),
    ]
    for x, y, label in quadrant_labels:
        fig.add_annotation(
            x=x,
            y=y,
            xref="paper",
            yref="paper",
            text=label,
            showarrow=False,
            bgcolor="rgba(255,255,255,0.82)",
            bordercolor="#D9E1EE",
            font={"size": 11},
        )
    theme(fig, "CH07 · Phân vùng khách hàng theo chi tiêu và lần mua gần nhất",
          "Số ngày từ lần mua gần nhất", SPEND_AXIS_LABEL)
    return fig


def chart_days_spend(data: pd.DataFrame, spend_cut: float, days_cut: float) -> None:
    fig = build_segment_chart(data, spend_cut, days_cut)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"Mỗi điểm là một khách · Ngưỡng cố định từ toàn bộ dữ liệu sạch: chi tiêu {spend_cut:,.1f}, "
        f"số ngày {days_cut:,.1f}. Nhóm 'mua đã lâu' là dấu hiệu cần tái kích hoạt, không phải nhãn rời bỏ."
    )


def chart_satisfaction(data: pd.DataFrame) -> None:
    valid = data.dropna(subset=["Satisfaction Level"]).copy()
    counts = pd.crosstab(valid["Membership Type"], valid["Satisfaction Level"])
    counts = counts.reindex(index=MEMBERSHIPS, columns=SATISFACTION_LEVELS, fill_value=0)
    counts = counts.loc[counts.sum(axis=1) > 0]
    percentages = counts.div(counts.sum(axis=1), axis=0) * 100
    long = percentages.reset_index().melt(
        id_vars="Membership Type", var_name="Satisfaction Level", value_name="Tỷ lệ (%)"
    )
    valid_n = counts.sum(axis=1).to_dict()
    long["Hạng (n hợp lệ)"] = long["Membership Type"].map(
        lambda value: f"{value} (n={valid_n.get(value, 0)})"
    )
    fig = px.bar(
        long,
        x="Hạng (n hợp lệ)",
        y="Tỷ lệ (%)",
        color="Satisfaction Level",
        barmode="stack",
        category_orders={"Satisfaction Level": SATISFACTION_LEVELS},
        color_discrete_map=SAT_COLORS,
        text=long["Tỷ lệ (%)"].map(lambda value: f"{value:.0f}%" if value >= 5 else ""),
    )
    theme(fig, "CH08 · Cơ cấu hài lòng theo hạng", "Hạng thành viên", "Tỷ lệ trong hạng (%)")
    fig.update_yaxes(range=[0, 100])
    fig.update_traces(textposition="inside")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"Mẫu số riêng theo từng hạng · {len(valid)} khách có mức hài lòng hợp lệ; "
        f"{len(data) - len(valid)} khách thiếu trong tập đang lọc."
    )


def build_discount_comparison_chart(data: pd.DataFrame) -> go.Figure:
    """Build CH09 with spend and purchased-item comparisons side by side."""
    counts = data.groupby("Discount Applied", observed=True)["Customer ID"].nunique()
    labels = {False: "Không", True: "Có"}
    colors = {False: "#678CF0", True: "#36B9B5"}
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Tổng chi tiêu", "Số sản phẩm đã mua"),
        horizontal_spacing=0.12,
    )
    for column_index, measure in enumerate(["Total Spend", "Items Purchased"], start=1):
        for discount in [False, True]:
            values = data.loc[data["Discount Applied"].eq(discount), measure].dropna()
            fig.add_trace(
                go.Box(
                    y=values,
                    name=f"{labels[discount]} (n={counts.get(discount, 0)})",
                    marker_color=colors[discount],
                    boxpoints="outliers",
                    legendgroup=str(discount),
                    showlegend=column_index == 1,
                    hovertemplate=f"Giảm giá: {labels[discount]}<br>{measure}: %{{y:,.1f}}<extra></extra>",
                ),
                row=1,
                col=column_index,
            )
    theme(fig, "CH09 · Chi tiêu và số sản phẩm theo tình trạng giảm giá")
    fig.update_xaxes(title_text="Sử dụng giảm giá", row=1, col=1)
    fig.update_xaxes(title_text="Sử dụng giảm giá", row=1, col=2)
    fig.update_yaxes(title_text=SPEND_AXIS_LABEL, row=1, col=1)
    fig.update_yaxes(title_text="Số sản phẩm đã mua", row=1, col=2)
    fig.update_layout(boxgap=0.3, legend_title_text="Giảm giá")
    return fig


def chart_discount(data: pd.DataFrame) -> None:
    fig = build_discount_comparison_chart(data)
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Nguồn: `Discount Applied`, `Total Spend`, `Items Purchased` · So sánh median, IQR và ngoại lệ; "
        "khác biệt quan sát được không chứng minh tác động nhân quả."
    )


def cleaning_note(audit: dict) -> None:
    with st.expander("Ghi chú dữ liệu và phương pháp", expanded=False):
        st.markdown(
            f"""
            - Dữ liệu gốc: `{DATA.relative_to(ROOT)}`; {audit['rows_before']} dòng, {audit['columns']} cột.
            - Sau làm sạch: {audit['rows_after']} dòng và {audit['unique_customers_after']} Customer ID duy nhất.
            - Dòng trùng hoàn toàn đã loại: {audit['exact_duplicates']}; dòng lõi không hợp lệ đã loại: {audit['invalid_core_rows_removed']}.
            - Thiếu `Satisfaction Level`: {audit['missing_satisfaction_after']} dòng; chỉ loại khỏi CH08.
            - `Total Spend`: {SPEND_UNIT}; CSV không xác nhận USD/VND hoặc thời điểm chốt.
            - `Average Rating` được kiểm tra trong thang 1–5; khoảng quan sát được công bố trong notebook.
            - Tất cả KPI và biểu đồ dùng cùng tập sau bộ lọc chung. So sánh nhóm và tương quan không chứng minh nhân quả.
            """
        )


def main() -> None:
    st.set_page_config(page_title="IE313 · Dashboard", page_icon="📊", layout="wide")
    st.markdown(
        """
        <style>
        .stApp { background: #F6F8FC; }
        [data-testid="stHeader"] { background: #F6F8FC; }
        [data-testid="stMetricValue"] { color: #0F8C86; }
        [data-testid="stExpander"] { background: #FFFFFF; border: 1px solid #D9E1EE; border-radius: 10px; }
        h1, h2, h3 { color: #162033; }
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    clean, audit = get_clean_data()
    spend_cut, days_cut = fixed_segmentation_thresholds(clean)
    st.title("IE313 · Phân tích hành vi khách hàng")
    st.caption(
        "Thống kê mô tả và so sánh nhóm · Mỗi dòng là một khách hàng · "
        "Thời điểm chốt và đơn vị tiền tệ chưa được nguồn xác nhận"
    )

    filtered = shared_filters(clean)
    customer_n = filtered["Customer ID"].nunique()
    st.subheader(f"N = {customer_n:,} khách hàng đang được phân tích")

    if filtered.empty:
        st.warning("Không có dữ liệu phù hợp với bộ lọc hiện tại. Hãy đặt lại hoặc nới rộng bộ lọc.")
        cleaning_note(audit)
        return

    show_kpis(filtered)
    overview, behavior, satisfaction = st.tabs([
        "01 · Tổng quan", "02 · Chi tiêu & hành vi mua", "03 · Hài lòng & giảm giá"
    ])
    with overview:
        left, right = st.columns(2)
        with left:
            chart_age(filtered)
        with right:
            chart_city(filtered)
        chart_membership(filtered)
        chart_city_profile(filtered)
    with behavior:
        left, right = st.columns(2)
        with left:
            chart_spend_distribution(filtered)
        with right:
            chart_spend_membership(filtered)
        left, right = st.columns(2)
        with left:
            chart_items_spend(filtered)
        with right:
            chart_days_spend(filtered, spend_cut, days_cut)
    with satisfaction:
        chart_satisfaction(filtered)
        chart_discount(filtered)
    cleaning_note(audit)


if __name__ == "__main__":
    main()
