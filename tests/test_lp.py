"""Check that the local projection recovers a known impulse response."""

import numpy as np
import pandas as pd
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code" / "python"))
from lp import local_projection  # noqa: E402

RHO = 0.4
B = [0.04, 0.02, 0.01]  # direct effect of x_t, x_{t-1}, x_{t-2} on y_t


def true_irf(H):
    """Response of y_{t+h} to a unit x_t when y_t = RHO*y_{t-1} + sum_j B_j x_{t-j} + e."""
    irf = []
    for h in range(H + 1):
        prev = irf[-1] if irf else 0.0
        irf.append(RHO * prev + (B[h] if h < len(B) else 0.0))
    return np.array(irf)


def simulate(n_units, T, seed=0):
    rng = np.random.default_rng(seed)
    frames = []
    for i in range(n_units):
        x = rng.normal(0, 3, T)
        y = np.zeros(T)
        for t in range(T):
            y[t] = 0.002 * (i % 5) + RHO * (y[t - 1] if t else 0) + rng.normal(0, 0.2)
            y[t] += sum(b * x[t - j] for j, b in enumerate(B) if t - j >= 0)
        frames.append(pd.DataFrame({"unit": i, "t": np.arange(T), "y": y, "x": x}))
    return pd.concat(frames, ignore_index=True)


@pytest.mark.parametrize("unit,se", [(None, "newey_west"), ("unit", "cluster"), ("unit", "driscoll_kraay")])
def test_recovers_irf(unit, se):
    df = simulate(1 if unit is None else 20, 3000 if unit is None else 400)
    res = local_projection(df, "y", "x", time="t", unit=unit, horizons=6, p=12, se=se)
    est = res.loc[res.term == "shock", "beta"].to_numpy()
    np.testing.assert_allclose(est, true_irf(6), atol=0.006)


def test_cumulative_is_running_sum():
    df = simulate(10, 400, seed=1)
    m = local_projection(df, "y", "x", time="t", unit="unit", horizons=4, p=6)
    c = local_projection(df, "y", "x", time="t", unit="unit", horizons=4, p=6, cumulative=True)
    np.testing.assert_allclose(c.beta, np.cumsum(true_irf(4)), atol=0.01)
    assert np.all(c.se.to_numpy()[1:] > 0) and len(m) == len(c)


def test_interaction_detects_group_difference():
    df = simulate(20, 400, seed=2)
    df["G"] = (df.unit % 2).astype(float)
    df["y"] += 0.03 * df.G * df.x  # extra impact effect in group G
    res = local_projection(df, "y", "x", time="t", unit="unit", horizons=0, p=6, interact=("G",))
    theta = res.loc[res.term == "shock_x_G", "beta"].iloc[0]
    assert abs(theta - 0.03) < 0.005


def test_full_leads_remove_h1_bias_with_persistent_shocks():
    """With x_t = 0.6 x_{t-1} + u_t, leads 1..h-1 leave h = 1 biased (no lead); leads 1..h (tz="full") do not."""
    rng = np.random.default_rng(3)
    T = 4000
    u, e = rng.normal(0, 3, T), rng.normal(0, 0.2, T)
    x, y = np.zeros(T), np.zeros(T)
    for t in range(T):
        x[t] = (0.6 * x[t - 1] if t else 0) + u[t]
        y[t] = (RHO * y[t - 1] if t else 0) + e[t] + sum(b * x[t - j] for j, b in enumerate(B) if t - j >= 0)
    df = pd.DataFrame({"t": np.arange(T), "y": y, "x": x})
    paper = local_projection(df, "y", "x", time="t", horizons=3, p=12, se="newey_west")
    full = local_projection(df, "y", "x", time="t", horizons=3, p=12, se="newey_west", tz="full")
    truth = true_irf(3)
    assert abs(paper.beta.iloc[1] - truth[1]) > 0.015          # the h = 1 bias of the reference lead set
    np.testing.assert_allclose(full.beta.to_numpy(), truth, atol=0.006)
