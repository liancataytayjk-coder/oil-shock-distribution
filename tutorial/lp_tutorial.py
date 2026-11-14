"""Local projections from scratch: the companion script to tutorial/README.md.

Run from the repository root:   .venv/bin/python tutorial/lp_tutorial.py

It works through the tutorial in five steps and prints every number the README quotes:
  1. simulate data with a known impulse response and recover it by hand;
  2. show why the Teulings-Zubanov leads matter when shocks come in runs;
  3. estimate the national model on the study's data, one horizon at a time, by hand;
  4. check the hand-made estimates against the project's estimator (code/python/lp.py);
  5. estimate the regional panel with fixed effects and Driscoll-Kraay errors.
Figures go to tutorial/figures/.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import statsmodels.api as sm  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code" / "python"))
from lp import local_projection  # noqa: E402

FIG = ROOT / "tutorial" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False})
Z90 = 1.645  # 90% band


# ---------------------------------------------------------------- step 1
def simulate(T=3000, rho=0.4, b=(0.04, 0.02, 0.01), shock_ar=0.0, seed=0):
    """y_t = rho*y_{t-1} + b0*x_t + b1*x_{t-1} + b2*x_{t-2} + e_t;  x_t = shock_ar*x_{t-1} + u_t."""
    rng = np.random.default_rng(seed)
    u, e = rng.normal(0, 3, T), rng.normal(0, 0.2, T)
    x, y = np.zeros(T), np.zeros(T)
    for t in range(T):
        x[t] = (shock_ar * x[t - 1] if t else 0) + u[t]
        y[t] = (rho * y[t - 1] if t else 0) + e[t] + sum(bj * x[t - j] for j, bj in enumerate(b) if t - j >= 0)
    return pd.DataFrame({"t": np.arange(T), "y": y, "x": x})


def true_irf(H, rho=0.4, b=(0.04, 0.02, 0.01)):
    """Response of y_{t+h} to a one-unit, one-time x_t (other x held at zero)."""
    out = []
    for h in range(H + 1):
        out.append(rho * (out[-1] if out else 0) + (b[h] if h < len(b) else 0))
    return np.array(out)


def one_horizon(df, y, x, h, p=12, leads=True, trend=True, maxlags=None):
    """Regress y_{t+h} on x_t, p lags of y and x, (optionally) the leads x_{t+1..t+h-1}, a trend."""
    X = pd.DataFrame({"x": df[x]})
    for q in range(1, p + 1):
        X[f"y_l{q}"] = df[y].shift(q)
        X[f"x_l{q}"] = df[x].shift(q)
    if leads:
        for lead in range(1, h):
            X[f"x_f{lead}"] = df[x].shift(-lead)
    if trend:
        X["trend"] = df["t"]
    dep = df[y].shift(-h)
    d = X.assign(dep=dep).dropna()
    res = sm.OLS(d["dep"], sm.add_constant(d.drop(columns="dep"))).fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags if maxlags is not None else h + 1})
    return res.params["x"], res.bse["x"], int(res.nobs)


def step1():
    H = 12
    df = simulate()
    est = [one_horizon(df, "y", "x", h) for h in range(H + 1)]
    beta = np.array([b for b, _, _ in est])
    se = np.array([s for _, s, _ in est])
    tru = true_irf(H)
    print("STEP 1  simulated data, true vs estimated response")
    print(pd.DataFrame({"h": range(H + 1), "true": tru, "estimate": beta, "se": se}).round(4).to_string(index=False))
    print("max |error| =", round(float(np.abs(beta - tru).max()), 4))
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.fill_between(range(H + 1), beta - Z90 * se, beta + Z90 * se, color="0.85", linewidth=0)
    ax.plot(range(H + 1), beta, "o-", color="k", markersize=3.5, label="Local projection estimate (90% band)")
    ax.plot(range(H + 1), tru, "s--", color="k", markerfacecolor="white", markersize=3.5, label="True response")
    ax.axhline(0, color="k", linewidth=0.6)
    ax.set_xlabel("Months after the shock (h)")
    ax.set_ylabel("Response of y to a one-unit x")
    ax.legend()
    fig.savefig(FIG / "step1_simulation.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    return float(np.abs(beta - tru).max())


# ---------------------------------------------------------------- step 2
def step2():
    """When shocks are persistent, leaving out the leads mixes in the effect of later shocks."""
    H = 8
    df = simulate(shock_ar=0.6, seed=1)
    tru = true_irf(H)
    with_l = np.array([one_horizon(df, "y", "x", h, leads=True)[0] for h in range(H + 1)])
    without = np.array([one_horizon(df, "y", "x", h, leads=False)[0] for h in range(H + 1)])
    print("\nSTEP 2  persistent shocks (x_t = 0.6 x_t-1 + u_t)")
    print(pd.DataFrame({"h": range(H + 1), "true": tru, "with leads": with_l, "without leads": without})
          .round(4).to_string(index=False))
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.plot(range(H + 1), tru, "s--", color="k", markerfacecolor="white", markersize=3.5, label="True response to a one-time shock")
    ax.plot(range(H + 1), with_l, "o-", color="k", markersize=3.5, label="With Teulings-Zubanov leads")
    ax.plot(range(H + 1), without, "^:", color="0.4", markersize=3.5, label="Without leads")
    ax.axhline(0, color="k", linewidth=0.6)
    ax.set_xlabel("Months after the shock (h)")
    ax.legend()
    fig.savefig(FIG / "step2_leads.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    return with_l, without, tru


# ---------------------------------------------------------------- step 3 and 4
def load_national():
    d = pd.read_csv(ROOT / "data" / "clean" / "national_monthly.csv", parse_dates=["date"])
    return d.sort_values("date").reset_index(drop=True)


def step3_4():
    nat = load_national()
    H = 12
    rows = []
    for h in range(H + 1):
        # the sample is restricted AFTER building lags and leads, so earlier months still supply the lags
        X = pd.DataFrame({"x": nat["d_fuel"]})
        for q in range(1, 13):
            X[f"y_l{q}"] = nat["d_cpi_all"].shift(q)
            X[f"x_l{q}"] = nat["d_fuel"].shift(q)
        for lead in range(1, h):
            X[f"x_f{lead}"] = nat["d_fuel"].shift(-lead)
        X["trend"] = nat["t"]
        per = nat["d_cpi_all"].shift(-h)                                            # one month, h ahead
        cum = sum(nat["d_cpi_all"].shift(-j) for j in range(h + 1))                 # sum from t to t+h
        keep = nat["date"] >= "2001-01-01"
        out = {}
        for name, dep in [("per", per), ("cum", cum)]:
            d = X.assign(dep=dep)[keep].dropna()
            r = sm.OLS(d["dep"], sm.add_constant(d.drop(columns="dep"))).fit(
                cov_type="HAC", cov_kwds={"maxlags": h + 1})
            out[name] = (r.params["x"], r.bse["x"], int(r.nobs))
        rows.append({"h": h, "beta_h": out["per"][0], "se": out["per"][1],
                     "running_sum": None, "B_h (cumulative outcome)": out["cum"][0], "se_B": out["cum"][1],
                     "nobs": out["cum"][2]})
    hand = pd.DataFrame(rows)
    hand["running_sum"] = hand.beta_h.cumsum()
    print("\nSTEP 3  national model by hand: all-income CPI on the fuel index, 2001-2026")
    print(hand.round(4).to_string(index=False))

    pkg = local_projection(nat, "d_cpi_all", "d_fuel", time="t", horizons=H, p=12, se="newey_west",
                           sample=nat.date >= "2001-01-01", cumulative=True)
    diff = float(np.abs(pkg.beta.to_numpy() - hand["B_h (cumulative outcome)"].to_numpy()).max())
    print("\nSTEP 4  project estimator (lp.py) vs the hand-made version: max |difference| =", f"{diff:.2e}")

    b30 = local_projection(nat, "d_cpi_b30", "d_fuel", time="t", horizons=H, p=12, se="newey_west",
                           sample=nat.date >= "2001-01-01", cumulative=True)
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    for q, style, lab in [(pkg, dict(marker="o", linestyle="-"), "All income"),
                          (b30, dict(marker="s", linestyle="--", markerfacecolor="white"), "Bottom 30%")]:
        ax.plot(q.h, q.beta, color="k", markersize=3.5, label=lab, **style)
    ax.fill_between(pkg.h, pkg.lo, pkg.hi, color="0.85", linewidth=0)
    ax.axhline(0, color="k", linewidth=0.6)
    ax.set_xlabel("Months after the shock (h)")
    ax.set_ylabel("Cumulative response (pp per 1% fuel)")
    ax.legend(loc="lower right")
    fig.savefig(FIG / "step3_national.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    return hand, diff


# ---------------------------------------------------------------- step 5
def step5():
    reg = pd.read_csv(ROOT / "data" / "clean" / "regional_panel.csv", parse_dates=["date"])
    reg = reg.sort_values(["region", "date"]).reset_index(drop=True)
    pan = local_projection(reg, "d_ratio", "d_fuel", time="t", unit="region", horizons=12, p=12,
                           se="driscoll_kraay", sample=reg.date >= "2001-01-01", cumulative=True)
    nat = load_national()
    natg = local_projection(nat, "d_ratio", "d_fuel", time="t", horizons=12, p=12, se="newey_west",
                            sample=nat.date >= "2001-01-01", cumulative=True)
    print("\nSTEP 5  the gap: national (Newey-West) vs 17-region panel (fixed effects, Driscoll-Kraay)")
    print(pd.DataFrame({"h": pan.h, "national": natg.beta, "se_nat": natg.se, "panel": pan.beta,
                        "se_panel": pan.se, "panel_obs": pan.nobs}).iloc[[0, 3, 6, 9, 12]].round(4).to_string(index=False))
    return pan, natg


if __name__ == "__main__":
    err = step1()
    step2()
    step3_4()
    step5()
    print("\nfigures written to", FIG)
