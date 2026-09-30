"""Shared cleaning, filtering and KPI logic for the IE313 analysis."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = [
    "Customer ID",
    "Gender",
    "Age",
    "City",
    "Membership Type",
    "Total Spend",
    "Items Purchased",
    "Average Rating",
    "Discount Applied",
    "Days Since Last Purchase",
    "Satisfaction Level",
]
NUMERIC_COLUMNS = [
    "Age",
    "Total Spend",
    "Items Purchased",
    "Average Rating",
    "Days Since Last Purchase",
]
TEXT_COLUMNS = ["Gender", "City", "Membership Type", "Satisfaction Level"]
MEMBERSHIPS = ["Bronze", "Silver", "Gold"]
SATISFACTION_LEVELS = ["Unsatisfied", "Neutral", "Satisfied"]
MISSING_SATISFACTION = "Thiếu dữ liệu"
SEGMENT_ORDER = [
    "Chi tiêu cao · mua gần đây",
    "Chi tiêu cao · mua đã lâu",
    "Chi tiêu thấp · mua gần đây",
    "Chi tiêu thấp · mua đã lâu",
]
SPEND_UNIT = "đơn vị chưa xác định"
SPEND_AXIS_LABEL = f"Tổng chi tiêu ({SPEND_UNIT})"


def load_clean_data(path: str | Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load the original CSV and apply explicit, auditable cleaning rules.

    Invalid core rows are removed instead of being replaced with zero. Missing or
    invalid satisfaction values are retained as missing because other columns in
    those rows can still contribute to non-satisfaction analyses.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {path}")

    raw = pd.read_csv(path)
    missing_columns = set(REQUIRED_COLUMNS) - set(raw.columns)
    if missing_columns:
        raise ValueError(f"CSV thiếu cột: {', '.join(sorted(missing_columns))}")

    audit: dict[str, Any] = {
        "rows_before": len(raw),
        "columns": raw.shape[1],
        "exact_duplicates": int(raw.duplicated().sum()),
        "missing_before": raw.isna().sum().to_dict(),
    }

    df = raw.copy()
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates().copy()

    for column in TEXT_COLUMNS:
        df[column] = df[column].astype("string").str.strip()
        df.loc[df[column].eq(""), column] = pd.NA

    numeric_invalid: dict[str, int] = {}
    for column in NUMERIC_COLUMNS:
        converted = pd.to_numeric(df[column], errors="coerce")
        numeric_invalid[column] = int(converted.isna().sum() - df[column].isna().sum())
        df[column] = converted

    discount_text = df["Discount Applied"].astype("string").str.strip().str.lower()
    discount_map = {
        "true": True, "false": False, "1": True, "0": False,
        "yes": True, "no": False, "có": True, "không": False,
    }
    df["Discount Applied"] = discount_text.map(discount_map).astype("boolean")

    invalid_rules = {
        "Age": df["Age"].isna() | ~df["Age"].between(0, 120),
        "Total Spend": df["Total Spend"].isna() | (df["Total Spend"] < 0),
        "Items Purchased": (
            df["Items Purchased"].isna()
            | (df["Items Purchased"] < 0)
            | (df["Items Purchased"] % 1 != 0)
        ),
        "Average Rating": df["Average Rating"].isna() | ~df["Average Rating"].between(1, 5),
        "Discount Applied": df["Discount Applied"].isna(),
        "Days Since Last Purchase": (
            df["Days Since Last Purchase"].isna()
            | (df["Days Since Last Purchase"] < 0)
            | (df["Days Since Last Purchase"] % 1 != 0)
        ),
        "Gender": df["Gender"].isna(),
        "City": df["City"].isna(),
        "Membership Type": df["Membership Type"].isna(),
        "Customer ID": df["Customer ID"].isna(),
    }
    invalid_counts = {name: int(mask.sum()) for name, mask in invalid_rules.items()}
    invalid_core = pd.concat(invalid_rules.values(), axis=1).any(axis=1)

    # Invalid satisfaction labels become missing, but those customer rows remain.
    invalid_satisfaction = (
        df["Satisfaction Level"].notna()
        & ~df["Satisfaction Level"].isin(SATISFACTION_LEVELS)
    )
    audit["invalid_satisfaction_labels"] = int(invalid_satisfaction.sum())
    df.loc[invalid_satisfaction, "Satisfaction Level"] = pd.NA

    df = df.loc[~invalid_core].copy()
    duplicate_ids = int(df["Customer ID"].duplicated().sum())
    if duplicate_ids:
        raise ValueError(
            f"Có {duplicate_ids} Customer ID bị trùng sau làm sạch. "
            "Cần xác định quy tắc gộp trước khi tính KPI."
        )

    df["Age"] = df["Age"].astype("int64")
    df["Items Purchased"] = df["Items Purchased"].astype("int64")
    df["Days Since Last Purchase"] = df["Days Since Last Purchase"].astype("int64")
    df["Discount Applied"] = df["Discount Applied"].astype(bool)

    audit.update({
        "numeric_parse_invalid": numeric_invalid,
        "invalid_by_rule": invalid_counts,
        "invalid_core_rows_removed": int(invalid_core.sum()),
        "duplicate_customer_ids": duplicate_ids,
        "rows_after": len(df),
        "unique_customers_after": int(df["Customer ID"].nunique()),
        "missing_satisfaction_after": int(df["Satisfaction Level"].isna().sum()),
    })
    return df, audit


def apply_filters(
    df: pd.DataFrame,
    *,
    cities: Iterable[str] | None = None,
    genders: Iterable[str] | None = None,
    memberships: Iterable[str] | None = None,
    discounts: Iterable[bool] | None = None,
    age_range: tuple[int, int] | None = None,
    satisfaction: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Apply the one shared filter definition used by every KPI and chart."""
    mask = pd.Series(True, index=df.index)
    if cities is not None:
        mask &= df["City"].isin(list(cities))
    if genders is not None:
        mask &= df["Gender"].isin(list(genders))
    if memberships is not None:
        mask &= df["Membership Type"].isin(list(memberships))
    if discounts is not None:
        mask &= df["Discount Applied"].isin(list(discounts))
    if age_range is not None:
        mask &= df["Age"].between(age_range[0], age_range[1])
    if satisfaction is not None:
        selected = set(satisfaction)
        satisfaction_mask = df["Satisfaction Level"].isin(selected)
        if MISSING_SATISFACTION in selected:
            satisfaction_mask |= df["Satisfaction Level"].isna()
        mask &= satisfaction_mask
    return df.loc[mask].copy()


def compute_kpis(df: pd.DataFrame) -> dict[str, float | int | None]:
    """Compute KPI01–KPI06 on one already-filtered customer dataset."""
    if df.empty:
        return {
            "customers": 0,
            "total_spend": None,
            "median_spend": None,
            "mean_rating": None,
            "rating_n": 0,
            "discount_rate": None,
            "discount_n": 0,
            "median_days": None,
        }

    spend = df["Total Spend"].dropna()
    ratings = df["Average Rating"].dropna()
    discounts = df["Discount Applied"].dropna()
    days = df["Days Since Last Purchase"].dropna()
    return {
        "customers": int(df["Customer ID"].nunique()),
        "total_spend": float(spend.sum()) if not spend.empty else None,
        "median_spend": float(spend.median()) if not spend.empty else None,
        "mean_rating": float(ratings.mean()) if not ratings.empty else None,
        "rating_n": int(ratings.size),
        "discount_rate": float(discounts.mean() * 100) if not discounts.empty else None,
        "discount_n": int(discounts.size),
        "median_days": float(days.median()) if not days.empty else None,
    }


def fixed_segmentation_thresholds(df: pd.DataFrame) -> tuple[float, float]:
    """Return full-clean-data thresholds so segments stay comparable after filters."""
    return float(df["Total Spend"].median()), float(df["Days Since Last Purchase"].median())


def assign_customer_segments(
    df: pd.DataFrame,
    *,
    spend_cut: float,
    days_cut: float,
) -> pd.DataFrame:
    """Assign four transparent spend/recency segments using fixed thresholds."""
    segmented = df.copy()
    high_spend = segmented["Total Spend"] >= spend_cut
    recent_purchase = segmented["Days Since Last Purchase"] <= days_cut
    segmented["Customer Segment"] = np.select(
        [
            high_spend & recent_purchase,
            high_spend & ~recent_purchase,
            ~high_spend & recent_purchase,
            ~high_spend & ~recent_purchase,
        ],
        SEGMENT_ORDER,
        default="Chưa phân nhóm",
    )
    return segmented


def city_behavior_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize comparable customer behavior indicators for each city."""
    columns = [
        "Số khách",
        "Chi tiêu trung vị",
        "Sản phẩm trung vị",
        "Điểm đánh giá TB",
        "Tỷ lệ hài lòng (%)",
        "Tỷ lệ giảm giá (%)",
        "Ngày chưa mua trung vị",
    ]
    if df.empty:
        return pd.DataFrame(columns=columns).rename_axis("City")

    profile = df.groupby("City", observed=True).agg(
        **{
            "Số khách": ("Customer ID", "nunique"),
            "Chi tiêu trung vị": ("Total Spend", "median"),
            "Sản phẩm trung vị": ("Items Purchased", "median"),
            "Điểm đánh giá TB": ("Average Rating", "mean"),
            "Tỷ lệ giảm giá (%)": ("Discount Applied", lambda values: values.mean() * 100),
            "Ngày chưa mua trung vị": ("Days Since Last Purchase", "median"),
        }
    )
    valid_satisfaction = df.dropna(subset=["Satisfaction Level"])
    satisfaction_rate = valid_satisfaction.groupby("City", observed=True)["Satisfaction Level"].agg(
        lambda values: values.eq("Satisfied").mean() * 100
    )
    profile["Tỷ lệ hài lòng (%)"] = satisfaction_rate.reindex(profile.index)
    return profile[columns].sort_values("Số khách", ascending=False, kind="stable")
