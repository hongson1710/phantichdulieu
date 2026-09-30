import unittest
from unittest.mock import patch

from analysis_core import load_clean_data
from dashboard import COLORS, DATA, MEMBERSHIPS, chart_membership


class MembershipChartTest(unittest.TestCase):
    def test_ch03_is_donut_with_counts_and_complete_share(self):
        data, _ = load_clean_data(DATA)

        with patch("dashboard.st.plotly_chart") as render, patch("dashboard.st.caption"):
            chart_membership(data)

        figure = render.call_args.args[0]
        self.assertEqual(len(figure.data), 1)
        trace = figure.data[0]
        self.assertEqual(trace.type, "pie")
        self.assertGreater(trace.hole, 0)
        self.assertEqual(list(trace.labels), MEMBERSHIPS)
        self.assertEqual(sum(trace.values), data["Customer ID"].nunique())
        self.assertAlmostEqual(sum(trace.values) / sum(trace.values) * 100, 100.0)
        self.assertEqual(list(trace.marker.colors), [COLORS[name] for name in MEMBERSHIPS])


if __name__ == "__main__":
    unittest.main()
