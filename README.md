# **IPL Franchise ROI Analytics Dashboard**

**Duration:** Aug 2025 – Sept 2025
**Tech Stack:** SQL | Python (pandas, NumPy, statsmodels) | Power BI
**Domain:** Sports Analytics | Moneyball Analysis

---

## **Overview**

This project analyzes **player and franchise return on investment (ROI)** in the **Indian Premier League (IPL)** across all seasons (2008–2025).
It combines **auction data**, **match-by-match delivery data**, and **season standings** to answer the question —

> *“Do expensive players actually perform better?”*

The study models ROI for both **players** and **franchises** by integrating **financial (auction)** and **performance (match)** data, accounting for **inflation** and **phase-wise performance metrics** such as powerplay, middle, and death overs.

---

## **Key Objectives**

1. Quantify the **ROI of players and franchises** across IPL seasons.
2. Compare **batting vs bowling efficiency** and identify top performers.
3. Analyze whether **auction spending translates to success** in standings.
4. Build an **interactive Power BI dashboard** visualizing franchise performance trends.

---

## **Data Engineering**

### **Sources**

* `matches.csv` and `deliveries.csv` from IPL dataset.
* `auction_data.csv` — manually cleaned and augmented.
* `ipl_standings.csv` — created from Wikipedia (2008–2025 standings).

### **Schema Highlights**

* **Matches Table:** season, venue, teams, winner, toss_decision.
* **Deliveries Table:** ball-level details — runs, wickets, extras, over number, bowler, batsman.
* **Auctions Table:** player, price, team, year, and career stats.

---

## **Methodology**

### **Phase-Based Performance Segmentation**

Each innings was divided into **three phases:**

* **Powerplay (1–6 overs)**
* **Middle overs (7–15)**
* **Death overs (16–20)**

This was done for both batting and bowling, resulting in six detailed datasets:

* `bat_pp`, `bat_mid`, `bat_death`
* `bowl_pp`, `bowl_mid`, `bowl_death`

---

### **Metrics Defined**

**For Batsmen**

* Runs
* Strike Rate
* Boundary %
* Dot Ball %
* Average (later dropped due to skew from dismissals)

**For Bowlers**

* Wickets
* Economy
* Dot Ball %
* Boundary % Conceded

Each stat was **Z-score standardized** within the same season and phase to ensure fair comparison across years and match conditions.

---

### **Phase-Wise Weighting**

Cricketing intuition guided **different weights** for each metric across phases.
Example (simplified):

| Metric      | Powerplay | Middle | Death |
| ----------- | --------- | ------ | ----- |
| Runs        | 0.8       | 0.8    | 0.8   |
| Strike Rate | 0.5       | 0.4    | 0.6   |
| Dot Ball %  | -0.3      | -0.2   | -0.4  |
| Boundary %  | 0.3       | 0.3    | 0.4   |
| Wickets     | 1.5       | 1.5    | 1.5   |
| Economy     | 0.8       | 0.8    | 0.8   |

---

### **Inflation Adjustment**

Auction prices were **adjusted for inflation** to 2025 Rupees using India’s CPI data (2012–2024).
Example:

> ₹1 crore in 2012 ≈ ₹2.12 crore in 2025

This ensured **ROI comparability** across seasons.

---

### **ROI Calculation**

**ROI (Return on Investment)** was defined as:
[
ROI = \frac{Z_{performance}}{Adjusted_Price}
]

where ( Z_{performance} ) is the weighted sum of standardized metrics.
ROI was computed for:

* **Each player per phase**
* **Each team per season** (aggregated mean ROI)
* **Overall franchise ROI** (across all years)

---

## **Key Insights**

### **1. Top ROI Players (Phase-Wise)**

| Phase            | Player                                        | Season | Franchise              |
| ---------------- | --------------------------------------------- | ------ | ---------------------- |
| Bat – Death      | Hardik Pandya                                 | 2015   | Mumbai Indians         |
| Bat – Middle     | Suryakumar Yadav                              | 2023   | Mumbai Indians         |
| Bat – Powerplay  | Rahul Tripathi (2017), Abhishek Sharma (2024) | SRH    |                        |
| Bowl – Death     | Jaydev Unadkat                                | 2017   | Rising Pune Supergiant |
| Bowl – Middle    | Amit Mishra                                   | 2016   | Delhi Daredevils       |
| Bowl – Powerplay | Sandeep Sharma                                | 2014   | Punjab Kings           |

These players delivered **exceptional ROI** relative to their auction price — perfect examples of *Moneyball efficiency*.

---

### **2. Franchise ROI Insights**

* **Average ROI across teams:** ~**12%**, meaning every ₹100 crore invested yielded ₹112 crore in on-field performance value (in normalized units).
* **CSK, MI, and KKR** consistently achieved high ROI due to **strategic retention and low churn.**
* **RCB** and **Punjab** showed **negative ROI volatility**, suggesting overpayment for marquee players without proportional on-field impact.
* Teams with **younger domestic cores** (e.g., GT 2022, LSG 2023) showed **higher ROI efficiency.**

---

### **3. ROI vs League Standing**

* **Weak but visible trend**: teams with higher ROI tended to finish higher in the standings.
* However, the **correlation was statistically insignificant (p > 0.05)** — mainly due to missing retention salary data.
* Notably, **Mumbai Indians (2015–2020)** and **CSK (2018–2021)** achieved *positive ROI–success alignment*, validating their auction efficiency.
* **Outliers:** RCB’s spending rarely converted into consistent high standings — the *“Moneyball gap.”*

---

## **Visualization (Power BI)**

**Dashboard Components:**

1. **Franchise ROI Over Time** — ROI trend line (2008–2025)
2. **Phase-wise Player ROI Heatmap** — showing player efficiency by overs and seasons.
3. **ROI vs Standing Scatter Plot** — highlighting whether smarter spending translated into success.

---

## **Limitations**

* Lack of **retention salary data** limits ROI completeness.
* Does not account for **injuries**, **bench players**, or **non-performance impacts** (leadership, fielding).
* Z-score scaling assumes **normal distribution** of performance stats — not always the case.

---

## **Conclusion**

This project showcases how **data-driven analysis can quantify cricketing efficiency**, much like the *Moneyball* philosophy in baseball.
Even with imperfect data, the model reveals consistent patterns —

> **Smarter spending and phase-aware player utilization drive ROI more than raw spending.**

---

## **Next Steps**

* Integrate retention and replacement costs from BCCI auction PDFs.
* Introduce **Win Contribution Models** using regression of match outcomes.
* Automate Power BI updates using a live SQL pipeline.

---

**Author:** *Atharva Sharma*
**Project:** *IPL Franchise ROI Analytics (Moneyball for Cricket)*
**Goal:** *Quantifying on-field performance efficiency from auction investments.*
