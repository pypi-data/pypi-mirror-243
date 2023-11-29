from pathlib import Path

import chex
from scipy.stats import binom
import matplotlib
from matplotlib import pyplot as plt

from mubelnet.calibration import plot_calibration_histogram


class TestCase(chex.TestCase):
    # Show calibration plot and pause unit test when histogram not uniform.
    plot = True
    # Number of false positives we are willing to accept.
    false_positive_rate = 0.1
    # Number of replicates to use when doing simulation based calibration test.
    n_replicates = 480
    ARTIFACT_DIR = Path(__file__).parent / ".." / "test_results"

    def setUp(self):
        super().setUp()
        self.ARTIFACT_DIR.mkdir(exist_ok=True, parents=True)
        matplotlib.use("agg")

    def assertUniform(self, histogram, alpha: float = 0.1, name: str | None = None):
        """Assert if histogram is uniformly distributed.

        Args:
            alpha: Probability of false positive.
        """
        # Since the histogram is supposed to be uniform, the count in each bucket is
        # binomially distributed.
        n_bins = len(histogram)
        n_replicates = histogram.sum(dtype=int)
        kwargs = {"n": n_replicates, "p": 1 / n_bins}

        # We divide by the number of bins because one bin (by accident) may be out of
        # the bands.
        q_value = alpha / n_bins
        y_lower = binom.ppf(q=q_value / 2, **kwargs)
        y_upper = binom.ppf(q=1.0 - q_value / 2, **kwargs)

        # Validate that the counts in the binds all fall within the 1-alpha % expected
        # variation around uniform distribution.
        in_bands = (histogram < y_upper) & (histogram > y_lower)
        if not all(in_bands):
            if self.plot:
                f = plt.figure(figsize=(4, 3))
                plot_calibration_histogram(histogram, n_replicates, alpha, ax=f.gca())
                if name is not None:
                    plt.title(name)
                    target_dir = self.ARTIFACT_DIR / self.__class__.__name__
                    target_dir.mkdir(exist_ok=True, parents=True)
                    f.savefig(target_dir / (name + ".png"))
            mean = n_replicates / n_bins
            raise AssertionError(
                "Deviation from uniform distribution.\n"
                f"Expected (for n={n_replicates} replicates): {mean:.0f}; Range "
                f"between:\n({y_lower:.0f}, {y_upper:.0f}), "
                f"probability: {(1-q_value)*100:.2f}%.\n"
                f"Histogram:\n{histogram}."
            )
