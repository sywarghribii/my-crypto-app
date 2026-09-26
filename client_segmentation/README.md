# 👥 Client Segmentation Project

## Overview
Customer segmentation and risk prediction system for 50,000 cryptocurrency traders using KMeans clustering, DBSCAN, and Random Forest regression.

## 🎯 Key Results

### Customer Segmentation (KMeans)
- **3 Segments Identified:**
  - **Prudent:** 17,609 users (35%) - Conservative, low-risk traders
  - **Équilibré:** 22,508 users (45%) - Balanced, moderate-risk traders
  - **Aventurier:** 9,883 users (20%) - Aggressive, high-risk traders

### Risk Prediction Model (Enhanced Random Forest)
- **R² Score:** 86.76% - Excellent predictive power
- **MAE:** 0.0767 - Very low prediction error
- **RMSE:** 0.0916 - Strong overall accuracy
- **Prediction Accuracy:** 71.79%

## 📁 Files
- `client.ipynb` - Main notebook with complete analysis pipeline
- `crypto_users_50000.csv` - Dataset with 50,000 user trading profiles

## 🔧 Technical Features

### Input Features (5)
1. `trade_frequency_per_week` - Trading activity level
2. `portfolio_value_usd` - Total portfolio size
3. `avg_holding_days` - Average holding period
4. `volatility_exposure` - Exposure to volatile assets
5. `risk_score` - Overall risk profile

### Enhanced Features (3 Interaction Terms)
- `freq_x_volatility` - Frequency × Volatility interaction
- `portfolio_x_volatility` - Portfolio × Volatility interaction
- `freq_over_holding` - Trading frequency relative to holding period

## 📊 Models Used

### 1. KMeans Clustering
- Optimal k=3 determined by elbow method and silhouette analysis
- Clear cluster separation validated by PCA visualization
- Business-friendly segment labels

### 2. DBSCAN (Density-Based)
- Outlier detection and anomaly identification
- Parameters: eps=0.7, min_samples=15
- Useful for fraud detection

### 3. Random Forest Regressor (Enhanced)
- 500 decision trees
- Optimized hyperparameters (max_depth=15, min_samples_split=10)
- Feature importance analysis
- Top features: avg_holding_days (26.8%), freq_over_holding (25.4%)

## 🎨 Visualizations
- Elbow method and silhouette score plots
- PCA 2D cluster visualization
- Actual vs Predicted risk score scatter plot
- Residual distribution histogram

## 💼 Business Applications
1. **Targeted Marketing** - Customized strategies per segment
2. **Risk Management** - Predict and monitor high-risk users (86.76% accuracy)
3. **Product Development** - Tailored products for each user profile
4. **Customer Support** - Prioritize support based on segment needs
5. **Personalized Recommendations** - Custom trading advice based on risk scores

## 🚀 Usage
1. Open `client.ipynb` in Jupyter Notebook or VS Code
2. Run all cells sequentially to:
   - Load and explore data
   - Perform feature engineering
   - Find optimal clusters
   - Train segmentation models
   - Build risk prediction model
   - Generate visualizations

## 📈 Model Performance Summary
| Metric | Value | Interpretation |
|--------|-------|----------------|
| R² Score | 86.76% | Model explains 86.76% of risk variance |
| MAE | 0.0767 | Average error ±0.0767 risk points |
| RMSE | 0.0916 | Root mean squared error |
| Accuracy | 71.79% | Typical prediction accuracy |

## 🔄 Next Steps
1. Deploy models to production environment
2. Monitor model performance over time (retrain quarterly)
3. A/B test marketing strategies per segment
4. Implement real-time risk scoring API
5. Collect user feedback and refine segments
