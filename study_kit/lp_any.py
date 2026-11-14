"""Run a local projection on any dataset, from the command line.

    python lp_any.py data.csv --y inflation --x shock --time date
    python lp_any.py panel.csv --y gap --x fuel --time date --unit region
    python lp_any.py --demo                     # simulated data with a known answer

It estimates, for h = 0..H, the regression of y (by default the SUM of y from t to t+h, i.e. the
cumulative response; --onemonth for y at t+h only) on x_t, p lags of y and x, the leads of x
(Teulings-Zubanov; --leads paper = 1..h-1 as in Kpodar and Liu, full = 1..h, none), optional controls
(current value and p lags), a linear trend and a constant. Standard errors: Newey-West with h+1 lags for
one series; for a panel (--unit), unit fixed effects with Driscoll-Kraay errors (needs linearmodels),
or --se cluster / robust.

Rules it applies for you: monthly (or any regular) calendar completed before lagging; lags and leads built
within units; the --start/--end window selects SHOCK DATES only, after the lags are built.

Output: a table on screen, <out>.csv and, unless --noplot, <out>.png (black and white, 90% band).
Needs pandas, numpy, statsmodels, matplotlib (and linearmodels for Driscoll-Kraay).
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


def prepare(df, time, unit=None, freq="MS"):
    """Sort, parse the time column, complete the calendar (gaps become empty rows), add a trend."""
    df = df.copy()
    if not pd.api.types.is_numeric_dtype(df[time]):
        df[time] = pd.to_datetime(df[time])
    groups = [(None, df)] if unit is None else list(df.groupby(unit, sort=True))
    out = []
    for key, g in groups:
        g = g.sort_values(time).drop_duplicates(time)
        if pd.api.types.is_datetime64_any_dtype(g[time]):
            full = pd.date_range(g[time].min(), g[time].max(), freq=freq)
        else:
            full = np.arange(g[time].min(), g[time].max() + 1)
        missing = len(full) - len(g)
        if missing:
            print(f"note: {missing} missing period(s){'' if key is None else ' in ' + str(key)} filled with empty rows")
        g = g.set_index(time).reindex(full).rename_axis(time).reset_index()
        if unit is not None:
            g[unit] = key
        out.append(g)
    df = pd.concat(out, ignore_index=True)
    first = df[time].min()
    if pd.api.types.is_datetime64_any_dtype(df[time]) and freq == "MS":
        df["_trend"] = (df[time].dt.year - first.year) * 12 + df[time].dt.month - first.month
    else:
        df["_trend"] = df.groupby(unit)[time].rank(method="first") - 1 if unit else np.arange(len(df))
    return df


def design(df, y, x, h, p, leads, controls, cumulative, unit):
    sh = (lambda c, k: df.groupby(unit)[c].shift(k)) if unit else (lambda c, k: df[c].shift(k))
    X = pd.DataFrame({"x": df[x]}, index=df.index)
    for q in range(1, p + 1):
        X[f"y_l{q}"], X[f"x_l{q}"] = sh(y, q), sh(x, q)
    last = {"paper": h - 1, "full": h, "none": 0}[leads]
    for lead in range(1, last + 1):
        X[f"x_f{lead}"] = sh(x, -lead)
    for c in controls:
        X[c] = df[c]
        for q in range(1, p + 1):
            X[f"{c}_l{q}"] = sh(c, q)
    X["trend"] = df["_trend"]
    dep = sum(sh(y, -j) for j in range(h + 1)) if cumulative else sh(y, -h)
    return X, dep


def estimate(df, y, x, time, unit=None, horizons=12, p=12, leads="paper", controls=(), cumulative=True,
             start=None, end=None, se=None, level=0.90):
    df = prepare(df, time, unit)
    mask = pd.Series(True, index=df.index)
    if start is not None:
        mask &= df[time] >= (pd.Timestamp(start) if pd.api.types.is_datetime64_any_dtype(df[time]) else float(start))
    if end is not None:
        mask &= df[time] <= (pd.Timestamp(end) if pd.api.types.is_datetime64_any_dtype(df[time]) else float(end))
    se = se or ("driscoll_kraay" if unit else "newey_west")
    z = stats.norm.ppf(0.5 + level / 2)
    rows = []
    for h in range(horizons + 1):
        X, dep = design(df, y, x, h, p, leads, list(controls), cumulative, unit)
        d = X.assign(dep=dep)[mask]
        if unit:
            d[unit], d["_time"] = df.loc[d.index, unit], df.loc[d.index, time]
        d = d.dropna()
        regs = [c for c in X.columns if d[c].nunique() > 1]
        if unit:
            from linearmodels.panel import PanelOLS
            idx = pd.MultiIndex.from_arrays([d[unit], d["_time"]])
            mod = PanelOLS(d["dep"].set_axis(idx), d[regs].set_axis(idx).assign(const=1.0), entity_effects=True,
                           drop_absorbed=True)
            kw = {"driscoll_kraay": dict(cov_type="kernel", kernel="bartlett", bandwidth=h + 1),
                  "cluster": dict(cov_type="clustered", cluster_entity=True), "robust": dict(cov_type="robust")}[se]
            res = mod.fit(**kw)
            b, s, n = res.params["x"], res.std_errors["x"], int(res.nobs)
        else:
            mod = sm.OLS(d["dep"], sm.add_constant(d[regs]))
            res = mod.fit(cov_type="HAC", cov_kwds={"maxlags": h + 1}) if se == "newey_west" else mod.fit(cov_type="HC1")
            b, s, n = res.params["x"], res.bse["x"], int(res.nobs)
        rows.append({"h": h, "beta": b, "se": s, "lo": b - z * s, "hi": b + z * s, "nobs": n})
    return pd.DataFrame(rows)


def plot(res, path, ylabel):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5.2, 3.2))
    ax.fill_between(res.h, res.lo, res.hi, color="0.85", linewidth=0)
    ax.plot(res.h, res.beta, "o-", color="k", markersize=3.5)
    ax.axhline(0, color="k", linewidth=0.6)
    ax.set_xlabel("Periods after the shock (h)")
    ax.set_ylabel(ylabel)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def demo_data(T=1500, seed=0):
    """y_t = 0.5 y_{t-1} + 0.3 x_t + e_t, x i.i.d.: true cumulative response = 0.3 * sum_{j<=h} 0.5^j."""
    rng = np.random.default_rng(seed)
    x, e, y = rng.normal(size=T), rng.normal(scale=0.5, size=T), np.zeros(T)
    for t in range(T):
        y[t] = (0.5 * y[t - 1] if t else 0) + 0.3 * x[t] + e[t]
    return pd.DataFrame({"period": np.arange(T), "y": y, "x": x})


def main(argv=None):
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("csv", nargs="?", help="input CSV file")
    a.add_argument("--y", help="outcome column (e.g. monthly inflation, 100 x dln)")
    a.add_argument("--x", help="shock column (e.g. monthly fuel price change, 100 x dln)")
    a.add_argument("--time", default="date", help="time column: dates (monthly) or integers")
    a.add_argument("--unit", help="unit column for a panel (e.g. region)")
    a.add_argument("--horizons", type=int, default=12)
    a.add_argument("--lags", type=int, default=12)
    a.add_argument("--leads", choices=["paper", "full", "none"], default="paper")
    a.add_argument("--controls", default="", help="comma-separated control columns")
    a.add_argument("--onemonth", action="store_true", help="outcome at t+h only (not cumulative)")
    a.add_argument("--start", help="first shock date (e.g. 2001-01-01)")
    a.add_argument("--end", help="last shock date")
    a.add_argument("--se", choices=["newey_west", "driscoll_kraay", "cluster", "robust"])
    a.add_argument("--out", default="lp_result", help="output file prefix")
    a.add_argument("--noplot", action="store_true")
    a.add_argument("--demo", action="store_true", help="run on simulated data with a known answer")
    o = a.parse_args(argv)

    if o.demo:
        df, o.y, o.x, o.time, o.lags = demo_data(), "y", "x", "period", 4
        truth = 0.3 * np.cumsum(0.5 ** np.arange(o.horizons + 1))
    else:
        if not (o.csv and o.y and o.x):
            a.error("give a CSV file with --y and --x, or use --demo")
        df, truth = pd.read_csv(o.csv), None
    controls = [c for c in o.controls.split(",") if c]
    res = estimate(df, o.y, o.x, o.time, unit=o.unit, horizons=o.horizons, p=o.lags, leads=o.leads,
                   controls=controls, cumulative=not o.onemonth, start=o.start, end=o.end, se=o.se)
    if truth is not None:
        res["true"] = truth
    print(res.round(4).to_string(index=False))
    res.to_csv(f"{o.out}.csv", index=False)
    if not o.noplot:
        plot(res, f"{o.out}.png", "Cumulative response" if not o.onemonth else "Response")
    print(f"\nwrote {o.out}.csv" + ("" if o.noplot else f" and {o.out}.png"))


if __name__ == "__main__":
    sys.exit(main())
