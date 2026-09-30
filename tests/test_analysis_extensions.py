import unittest

import pandas as pd

import analysis_core
import dashboard


def sample_customers() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Customer ID": [1, 2, 3, 4],
            "City": ["A", "A", "B", "B"],
            "Membership Type": ["Bronze", "Silver", "Gold", "Bronze"],
            "Total Spend": [100.0, 300.0, 200.0, 400.0],
            "Items Purchased": [2, 4, 3, 5],
            "Average Rating": [4.0, 2.0, 5.0, 3.0],
            "Discount Applied": [True, False, True, True],
            "Days Since Last Purchase": [5, 15, 10, 20],
            "Satisfaction Level": ["Satisfied", pd.NA, "Neutral", "Satisfied"],
        }
    )


class CustomerSegmentationTest(unittest.TestCase):
    def test_threshold_boundaries_create_four_business_segments(self):
        assign = getattr(analysis_core, "assign_customer_segments", None)
        self.assertIsNotNone(assign, "Cần hàm phân vùng khách hàng dùng chung")
        data = pd.DataFrame(
            {
                "Total Spend": [200.0, 201.0, 199.0, 199.0],
                "Days Since Last Purchase": [10, 11, 10, 11],
            }
        )

        result = assign(data, spend_cut=200.0, days_cut=10.0)

        self.assertEqual(
            result["Customer Segment"].tolist(),
            [
                "Chi tiêu cao · mua gần đây",
                "Chi tiêu cao · mua đã lâu",
                "Chi tiêu thấp · mua gần đây",
                "Chi tiêu thấp · mua đã lâu",
            ],
        )

    def test_ch07_figure_contains_every_customer_and_both_thresholds(self):
        builder = getattr(dashboard, "build_segment_chart", None)
        self.assertIsNotNone(builder, "Cần bộ dựng biểu đồ phân vùng CH07")
        data = pd.DataFrame(
            {
                "Customer ID": [1, 2, 3, 4],
                "Membership Type": ["Gold", "Gold", "Bronze", "Bronze"],
                "Total Spend": [300.0, 300.0, 100.0, 100.0],
                "Days Since Last Purchase": [5, 15, 5, 15],
            }
        )

        figure = builder(data, spend_cut=200.0, days_cut=10.0)

        self.assertEqual(sum(len(trace.x) for trace in figure.data), 4)
        self.assertEqual(
            {trace.name for trace in figure.data},
            {
                "Chi tiêu cao · mua gần đây",
                "Chi tiêu cao · mua đã lâu",
                "Chi tiêu thấp · mua gần đây",
                "Chi tiêu thấp · mua đã lâu",
            },
        )
        vertical = [shape for shape in figure.layout.shapes if shape.x0 == shape.x1 == 10.0]
        horizontal = [shape for shape in figure.layout.shapes if shape.y0 == shape.y1 == 200.0]
        self.assertEqual(len(vertical), 1)
        self.assertEqual(len(horizontal), 1)


class DiscountComparisonTest(unittest.TestCase):
    def test_ch09_compares_spend_and_items_for_both_discount_groups(self):
        builder = getattr(dashboard, "build_discount_comparison_chart", None)
        self.assertIsNotNone(builder, "Cần bộ dựng CH09 gồm hai chỉ tiêu")

        figure = builder(sample_customers())

        self.assertEqual(len(figure.data), 4)
        self.assertTrue(all(trace.type == "box" for trace in figure.data))
        self.assertEqual({trace.yaxis for trace in figure.data}, {"y", "y2"})
        spend_values = sorted(value for trace in figure.data[:2] for value in trace.y)
        item_values = sorted(value for trace in figure.data[2:] for value in trace.y)
        self.assertEqual(spend_values, [100.0, 200.0, 300.0, 400.0])
        self.assertEqual(item_values, [2, 3, 4, 5])


class CityProfileTest(unittest.TestCase):
    def test_city_profile_uses_valid_satisfaction_denominator(self):
        build_profile = getattr(analysis_core, "city_behavior_profile", None)
        self.assertIsNotNone(build_profile, "Cần bảng hồ sơ hành vi theo thành phố")

        profile = build_profile(sample_customers())

        self.assertEqual(profile.loc["A", "Số khách"], 2)
        self.assertEqual(profile.loc["A", "Chi tiêu trung vị"], 200.0)
        self.assertEqual(profile.loc["A", "Sản phẩm trung vị"], 3.0)
        self.assertEqual(profile.loc["A", "Điểm đánh giá TB"], 3.0)
        self.assertEqual(profile.loc["A", "Tỷ lệ hài lòng (%)"], 100.0)
        self.assertEqual(profile.loc["A", "Tỷ lệ giảm giá (%)"], 50.0)
        self.assertEqual(profile.loc["A", "Ngày chưa mua trung vị"], 10.0)
        self.assertEqual(profile.loc["B", "Tỷ lệ hài lòng (%)"], 50.0)

    def test_city_heatmap_contains_actual_values_and_normalized_colors(self):
        builder = getattr(dashboard, "build_city_profile_chart", None)
        self.assertIsNotNone(builder, "Cần bộ dựng heatmap hồ sơ thành phố")

        figure = builder(sample_customers())
        trace = figure.data[0]

        self.assertEqual(trace.type, "heatmap")
        self.assertEqual(len(trace.y), 2)
        self.assertEqual(len(trace.x), 6)
        self.assertGreaterEqual(min(value for row in trace.z for value in row), 0.0)
        self.assertLessEqual(max(value for row in trace.z for value in row), 100.0)
        self.assertEqual(float(trace.customdata[0][0]), 200.0)


if __name__ == "__main__":
    unittest.main()
