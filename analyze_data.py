"""Data Analysis and Visualization for F6S Kazakhstan Companies"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import re

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Create charts directory
Path("charts").mkdir(exist_ok=True)

# Load data
print("Loading data...")
df = pd.read_csv('f6s_kazakhstan_companies.csv')
print(f"Total companies: {len(df)}")

# Data cleaning and preprocessing
print("\n" + "="*60)
print("DATA QUALITY OVERVIEW")
print("="*60)

# Clean funding amounts
def parse_funding(value):
    if pd.isna(value) or value == '':
        return 0
    value = str(value).upper().replace('$', '').replace(',', '').strip()
    multiplier = 1
    if 'K' in value:
        multiplier = 1000
        value = value.replace('K', '')
    elif 'M' in value:
        multiplier = 1000000
        value = value.replace('M', '')
    elif 'B' in value:
        multiplier = 1000000000
        value = value.replace('B', '')
    try:
        return float(value) * multiplier
    except:
        return 0

df['funding_numeric'] = df['funding_amount'].apply(parse_funding)
df['has_funding'] = df['funding_numeric'] > 0

# Parse founded year
df['founded_year_numeric'] = pd.to_numeric(df['founded_year'], errors='coerce')

# Categories
df['has_investors'] = df['investors'].notna() & (df['investors'] != '')
df['has_team'] = df['team_members'].notna() & (df['team_members'] != '')
df['has_description'] = df['description'].notna() & (df['description'] != '')

# Extract cities from location
def extract_city(location):
    if pd.isna(location) or location == '':
        return 'Unknown'
    # Take first part before comma
    city = location.split(',')[0].strip()
    return city

df['city'] = df['location'].apply(extract_city)

# Categorize by industry based on description and tagline
def categorize_industry(row):
    text = str(row['description']) + ' ' + str(row['tagline'])
    text = text.lower()

    if any(word in text for word in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'neural']):
        return 'AI & Machine Learning'
    elif any(word in text for word in ['fintech', 'payment', 'banking', 'neobank', 'financial', 'investment', 'credit']):
        return 'FinTech'
    elif any(word in text for word in ['saas', 'software', 'platform', 'cloud', 'crm']):
        return 'SaaS & Enterprise Software'
    elif any(word in text for word in ['game', 'gaming', 'mobile game']):
        return 'Gaming'
    elif any(word in text for word in ['blockchain', 'web3', 'crypto', 'bitcoin']):
        return 'Blockchain & Web3'
    elif any(word in text for word in ['health', 'medical', 'healthcare', 'diagnostic']):
        return 'HealthTech'
    elif any(word in text for word in ['energy', 'solar', 'wind', 'renewable']):
        return 'Clean Energy'
    elif any(word in text for word in ['ecommerce', 'e-commerce', 'marketplace', 'retail']):
        return 'E-commerce'
    elif any(word in text for word in ['education', 'learning', 'school', 'course']):
        return 'EdTech'
    else:
        return 'Other'

df['industry'] = df.apply(categorize_industry, axis=1)

# Print summary
print(f"\nCompanies with funding: {df['has_funding'].sum()} ({df['has_funding'].sum()/len(df)*100:.1f}%)")
print(f"Companies with investors: {df['has_investors'].sum()} ({df['has_investors'].sum()/len(df)*100:.1f}%)")
print(f"Companies with team info: {df['has_team'].sum()} ({df['has_team'].sum()/len(df)*100:.1f}%)")
print(f"Companies with description: {df['has_description'].sum()} ({df['has_description'].sum()/len(df)*100:.1f}%)")
print(f"\nTotal funding: ${df['funding_numeric'].sum():,.0f}")
print(f"Average funding (funded companies): ${df[df['has_funding']]['funding_numeric'].mean():,.0f}")

# ========================================
# CHART 1: Funding Distribution
# ========================================
print("\n[1/8] Creating funding distribution chart...")
fig, ax = plt.subplots(figsize=(14, 8))

funded = df[df['has_funding']].sort_values('funding_numeric', ascending=True)
colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(funded)))

bars = ax.barh(funded['company_name'], funded['funding_numeric'], color=colors)
ax.set_xlabel('Funding Amount ($)', fontsize=12, fontweight='bold')
ax.set_title('Top Funded Kazakhstan Startups from F6S', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, funded['funding_numeric'].max() * 1.1)

# Add value labels
for i, (idx, row) in enumerate(funded.iterrows()):
    value = row['funding_numeric']
    if value >= 1000000:
        label = f"${value/1000000:.1f}M"
    elif value >= 1000:
        label = f"${value/1000:.0f}K"
    else:
        label = f"${value:.0f}"
    ax.text(value, i, f'  {label}', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/01_funding_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/01_funding_distribution.png")
plt.close()

# ========================================
# CHART 2: Geographic Distribution
# ========================================
print("[2/8] Creating geographic distribution chart...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Pie chart
city_counts = df['city'].value_counts()
colors_pie = plt.cm.Set3(range(len(city_counts)))
wedges, texts, autotexts = ax1.pie(city_counts.values, labels=city_counts.index, autopct='%1.1f%%',
                                     colors=colors_pie, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)
ax1.set_title('Companies by City (Distribution)', fontsize=14, fontweight='bold', pad=20)

# Bar chart
city_counts.plot(kind='barh', ax=ax2, color=colors_pie[:len(city_counts)])
ax2.set_xlabel('Number of Companies', fontsize=11, fontweight='bold')
ax2.set_ylabel('City', fontsize=11, fontweight='bold')
ax2.set_title('Companies by City (Count)', fontsize=14, fontweight='bold', pad=20)

# Add value labels on bars
for i, v in enumerate(city_counts.values):
    ax2.text(v + 0.5, i, str(v), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/02_geographic_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/02_geographic_distribution.png")
plt.close()

# ========================================
# CHART 3: Industry Distribution
# ========================================
print("[3/8] Creating industry distribution chart...")
fig, ax = plt.subplots(figsize=(14, 8))

industry_counts = df['industry'].value_counts()
colors_ind = plt.cm.tab20(range(len(industry_counts)))

bars = ax.barh(industry_counts.index, industry_counts.values, color=colors_ind)
ax.set_xlabel('Number of Companies', fontsize=12, fontweight='bold')
ax.set_title('Kazakhstan Startups by Industry Sector', fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, v in enumerate(industry_counts.values):
    ax.text(v + 0.3, i, str(v), va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/03_industry_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/03_industry_distribution.png")
plt.close()

# ========================================
# CHART 4: Founded Year Timeline
# ========================================
print("[4/8] Creating founding year timeline...")
fig, ax = plt.subplots(figsize=(14, 8))

founded_years = df[df['founded_year_numeric'].notna()]['founded_year_numeric'].astype(int)
year_counts = founded_years.value_counts().sort_index()

ax.plot(year_counts.index, year_counts.values, marker='o', linewidth=3, markersize=8, color='#2E86AB')
ax.fill_between(year_counts.index, year_counts.values, alpha=0.3, color='#2E86AB')
ax.set_xlabel('Year Founded', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Companies', fontsize=12, fontweight='bold')
ax.set_title('Startup Founding Timeline (2009-2025)', fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3)

# Add value labels on peaks
for x, y in zip(year_counts.index, year_counts.values):
    if y >= 3:  # Only label significant peaks
        ax.text(x, y + 0.3, str(y), ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/04_founding_timeline.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/04_founding_timeline.png")
plt.close()

# ========================================
# CHART 5: Funding by Industry
# ========================================
print("[5/8] Creating funding by industry chart...")
fig, ax = plt.subplots(figsize=(14, 8))

industry_funding = df.groupby('industry')['funding_numeric'].sum().sort_values(ascending=True)
colors_fund = plt.cm.plasma(np.linspace(0.2, 0.9, len(industry_funding)))

bars = ax.barh(industry_funding.index, industry_funding.values, color=colors_fund)
ax.set_xlabel('Total Funding ($)', fontsize=12, fontweight='bold')
ax.set_title('Total Funding by Industry Sector', fontsize=16, fontweight='bold', pad=20)

# Add value labels
for i, (idx, value) in enumerate(industry_funding.items()):
    if value >= 1000000:
        label = f"${value/1000000:.1f}M"
    elif value >= 1000:
        label = f"${value/1000:.0f}K"
    else:
        label = f"${value:.0f}"
    if value > 0:
        ax.text(value, i, f'  {label}', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/05_funding_by_industry.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/05_funding_by_industry.png")
plt.close()

# ========================================
# CHART 6: Company Maturity & Team Size
# ========================================
print("[6/8] Creating company maturity analysis...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Company age distribution
df_with_year = df[df['founded_year_numeric'].notna()].copy()
df_with_year['age'] = 2024 - df_with_year['founded_year_numeric']
age_bins = [0, 2, 5, 10, 20]
age_labels = ['0-2 years', '3-5 years', '6-10 years', '10+ years']
df_with_year['age_group'] = pd.cut(df_with_year['age'], bins=age_bins, labels=age_labels)

age_counts = df_with_year['age_group'].value_counts().reindex(age_labels, fill_value=0)
colors_age = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
age_counts.plot(kind='bar', ax=ax1, color=colors_age, width=0.7)
ax1.set_xlabel('Company Age', fontsize=11, fontweight='bold')
ax1.set_ylabel('Number of Companies', fontsize=11, fontweight='bold')
ax1.set_title('Company Maturity Distribution', fontsize=14, fontweight='bold', pad=20)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')

# Add value labels
for i, v in enumerate(age_counts.values):
    if v > 0:
        ax1.text(i, v + 0.5, str(v), ha='center', fontweight='bold')

# Team size distribution
df['team_count_numeric'] = pd.to_numeric(df['team_count'], errors='coerce').fillna(0).astype(int)
team_bins = [0, 1, 2, 3, 10]
team_labels = ['No team info', '1 member', '2 members', '3+ members']
df['team_size'] = pd.cut(df['team_count_numeric'], bins=team_bins, labels=team_labels)

team_counts = df['team_size'].value_counts().reindex(team_labels, fill_value=0)
colors_team = ['#DDA15E', '#BC6C25', '#606C38', '#283618']
team_counts.plot(kind='bar', ax=ax2, color=colors_team, width=0.7)
ax2.set_xlabel('Team Size', fontsize=11, fontweight='bold')
ax2.set_ylabel('Number of Companies', fontsize=11, fontweight='bold')
ax2.set_title('Team Size Distribution', fontsize=14, fontweight='bold', pad=20)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

# Add value labels
for i, v in enumerate(team_counts.values):
    if v > 0:
        ax2.text(i, v + 1, str(v), ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/06_maturity_and_team.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/06_maturity_and_team.png")
plt.close()

# ========================================
# CHART 7: Investor Engagement
# ========================================
print("[7/8] Creating investor engagement analysis...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Companies with/without investors
investor_status = df['has_investors'].value_counts()
labels = ['No Investors', 'Has Investors']
colors_inv = ['#E63946', '#06D6A0']
sizes = [investor_status.get(False, 0), investor_status.get(True, 0)]

wedges, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                                     colors=colors_inv, startangle=90)
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(12)
ax1.set_title('Investor Engagement Overview', fontsize=14, fontweight='bold', pad=20)

# Top investors by number of investments
all_investors = []
for investors in df[df['has_investors']]['investors']:
    if pd.notna(investors) and investors != '':
        investor_list = [inv.strip() for inv in str(investors).split(',')]
        all_investors.extend(investor_list)

if all_investors:
    investor_counts = pd.Series(all_investors).value_counts().head(10)
    colors_top = plt.cm.Spectral(np.linspace(0.1, 0.9, len(investor_counts)))
    investor_counts.plot(kind='barh', ax=ax2, color=colors_top)
    ax2.set_xlabel('Number of Investments', fontsize=11, fontweight='bold')
    ax2.set_title('Top 10 Most Active Investors', fontsize=14, fontweight='bold', pad=20)

    # Add value labels
    for i, v in enumerate(investor_counts.values):
        ax2.text(v + 0.1, i, str(v), va='center', fontweight='bold')
else:
    ax2.text(0.5, 0.5, 'No investor data available', ha='center', va='center',
             transform=ax2.transAxes, fontsize=12)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)

plt.tight_layout()
plt.savefig('charts/07_investor_engagement.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/07_investor_engagement.png")
plt.close()

# ========================================
# CHART 8: Data Completeness Heatmap
# ========================================
print("[8/8] Creating data quality heatmap...")
fig, ax = plt.subplots(figsize=(10, 8))

# Calculate completeness for each field
fields = ['company_name', 'tagline', 'location', 'founded_year', 'funding_amount',
          'investors', 'team_members', 'description']
completeness = []

for field in fields:
    if field in df.columns:
        non_empty = df[field].notna() & (df[field] != '')
        completeness.append(non_empty.sum() / len(df) * 100)
    else:
        completeness.append(0)

# Create bar chart
colors_comp = plt.cm.RdYlGn(np.array(completeness) / 100)
bars = ax.barh(fields, completeness, color=colors_comp)
ax.set_xlabel('Completeness (%)', fontsize=12, fontweight='bold')
ax.set_title('Dataset Completeness by Field', fontsize=16, fontweight='bold', pad=20)
ax.set_xlim(0, 105)

# Add percentage labels
for i, (field, pct) in enumerate(zip(fields, completeness)):
    ax.text(pct + 2, i, f'{pct:.1f}%', va='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_data_completeness.png', dpi=300, bbox_inches='tight')
print("   Saved: charts/08_data_completeness.png")
plt.close()

# ========================================
# Generate Summary Statistics
# ========================================
print("\n" + "="*60)
print("ANALYSIS COMPLETE - KEY STATISTICS")
print("="*60)
print(f"\nTotal Companies: {len(df)}")
print(f"Cities Represented: {df['city'].nunique()}")
print(f"Industries: {df['industry'].nunique()}")
print(f"Total Funding: ${df['funding_numeric'].sum():,.0f}")
print(f"Companies with Funding: {df['has_funding'].sum()}")
print(f"Companies with Investors: {df['has_investors'].sum()}")
print(f"Average Team Size: {df['team_count_numeric'].mean():.1f}")

print(f"\nTop City: {df['city'].value_counts().index[0]} ({df['city'].value_counts().values[0]} companies)")
print(f"Top Industry: {df['industry'].value_counts().index[0]} ({df['industry'].value_counts().values[0]} companies)")

if df['has_funding'].sum() > 0:
    print(f"\nMost Funded Company: {df.loc[df['funding_numeric'].idxmax(), 'company_name']}")
    print(f"Amount: ${df['funding_numeric'].max():,.0f}")

print("\n" + "="*60)
print("All charts saved successfully to /charts directory!")
print("="*60)
