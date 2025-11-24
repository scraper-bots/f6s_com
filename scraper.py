"""F6S Kazakhstan Companies Scraper - Fixed Selectors"""
from DrissionPage import ChromiumPage
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def clean_text(text):
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text.strip())

def extract_company_data(block):
    """Extract all available data from company block"""
    data = {
        'company_name': '',
        'tagline': '',
        'company_url': '',
        'logo_url': '',
        'location': '',
        'founded_year': '',
        'funding_amount': '',
        'investors': '',
        'investor_count': '',
        'team_members': '',
        'team_count': '',
        'description': ''
    }

    try:
        # Company Name & URL
        name_elem = block.find('h2', class_='company-entry-title')
        if name_elem:
            link = name_elem.find('a')
            if link:
                data['company_name'] = clean_text(link.get_text())
                href = link.get('href', '')
                if href:
                    data['company_url'] = f"https://www.f6s.com{href}" if href.startswith('/') else href

        # Tagline
        tagline = block.find('h3', class_='mt4 mb8')
        if tagline:
            data['tagline'] = clean_text(tagline.get_text())

        # Logo
        logo_img = block.find('img', class_='f6s-thumbnail')
        if logo_img and logo_img.get('src'):
            data['logo_url'] = logo_img.get('src')

        # Location - must have location icon
        location_divs = block.find_all('div', class_='centered-content g8')
        for div in location_divs:
            svg = div.find('svg')
            if svg:
                use = svg.find('use')
                if use and use.get('xlink:href') == '#location':
                    data['location'] = clean_text(div.get_text())
                    break

        # Founded Year - must have clock icon
        founded_paras = block.find_all('p', class_='centered-content g8 mt8')
        for p in founded_paras:
            svg = p.find('svg')
            if svg:
                use = svg.find('use')
                if use and use.get('xlink:href') == '#clock':
                    text = p.get_text()
                    match = re.search(r'Founded\s+(\d{4})', text)
                    if match:
                        data['founded_year'] = match.group(1)
                        break

        # Funding & Investors - must have trend icon
        funding_divs = block.find_all('div', class_='centered-content mt8')
        for div in funding_divs:
            svg = div.find('svg')
            if svg:
                use = svg.find('use')
                if use and use.get('xlink:href') == '#trend':
                    content = div.find('div', class_='overview-line-content ml8')
                    if content:
                        text = content.get_text()

                        # Extract funding amount
                        amount_match = re.search(r'\$[\d.]+[kmb]?', text, re.I)
                        if amount_match:
                            data['funding_amount'] = amount_match.group(0)

                        # Extract investor names - SKIP LINKS WITH IMAGES
                        investor_links = content.find_all('a', target='_blank')
                        investor_names = []

                        for link in investor_links:
                            # Skip if link contains an image
                            if link.find('img'):
                                continue

                            # Get text
                            name = clean_text(link.get_text())

                            # Skip empty, "See all", etc
                            if not name or len(name) < 3:
                                continue
                            if any(x in name.lower() for x in ['see', 'all', 'investor', 'more']):
                                continue

                            # Add unique investors only
                            if name and name not in investor_names:
                                investor_names.append(name)

                        if investor_names:
                            data['investors'] = ', '.join(investor_names)

                        # Get total investor count from "and X more"
                        more_match = re.search(r'and\s+(\d+)\s+more', text)
                        if more_match:
                            additional = int(more_match.group(1))
                            total_count = len(investor_names) + additional
                            data['investor_count'] = str(total_count)
                        elif investor_names:
                            data['investor_count'] = str(len(investor_names))
                        else:
                            data['investor_count'] = '0'

                    break

        # Team Members
        team_wrapper = block.find('div', class_='collection-team-summary-wrapper mb16')
        if team_wrapper:
            team_links = team_wrapper.find_all('a', class_='accent hand')
            team_names = []

            for link in team_links:
                name = clean_text(link.get_text())
                if name and len(name) > 1 and name not in team_names:
                    team_names.append(name)

            if team_names:
                data['team_members'] = ', '.join(team_names)

            # Check for "and X more" in team section
            team_text = team_wrapper.get_text()
            more_team = re.search(r'and\s+(\d+)\s+more', team_text)
            if more_team:
                additional = int(more_team.group(1))
                total_count = len(team_names) + additional
                data['team_count'] = str(total_count)
            elif team_names:
                data['team_count'] = str(len(team_names))
            else:
                data['team_count'] = '0'
        else:
            data['team_count'] = '0'

        # Description
        desc_div = block.find('div', class_='profile-description mb16')
        if desc_div:
            inner_div = desc_div.find('div', class_='break-word')
            if inner_div:
                # Remove buttons
                for button in inner_div.find_all('button'):
                    button.decompose()

                paragraphs = inner_div.find_all('p')
                desc_parts = [clean_text(p.get_text()) for p in paragraphs if clean_text(p.get_text())]
                data['description'] = ' '.join(desc_parts)[:2000]

    except Exception as e:
        print(f"    Error: {str(e)[:80]}")

    return data

print("Initializing browser...")
page = ChromiumPage()

try:
    url = "https://www.f6s.com/companies/kazakhstan/lo"
    print(f"Loading {url}...")
    page.get(url)
    time.sleep(5)

    print("Scrolling to load all companies...")
    for i in range(15):
        page.scroll.to_bottom()
        time.sleep(2)
        if (i+1) % 5 == 0:
            print(f"  {i+1}/15")

    time.sleep(3)

    print("\nExtracting data...")
    html = page.html
    soup = BeautifulSoup(html, 'html.parser')
    blocks = soup.find_all('div', class_='company-block')

    print(f"Found {len(blocks)} companies\n")

    companies = []
    for idx, block in enumerate(blocks, 1):
        data = extract_company_data(block)
        if data['company_name']:
            companies.append(data)
            print(f"[{idx:3d}] {data['company_name']}")

    if companies:
        df = pd.DataFrame(companies)
        df.to_csv('f6s_kazakhstan_companies.csv', index=False, encoding='utf-8-sig')

        print(f"\n{'='*60}")
        print(f"SUCCESS! Saved {len(companies)} companies")
        print(f"File: f6s_kazakhstan_companies.csv")
        print(f"{'='*60}")

        print("\nDATA QUALITY:")
        print(f"  With funding: {(df['funding_amount'] != '').sum()}")
        print(f"  With investors: {(df['investors'] != '').sum()}")
        print(f"  With team info: {(df['team_members'] != '').sum()}")
        print(f"  With descriptions: {(df['description'] != '').sum()}")

        # Show sample with investors
        sample = df[df['investors'] != ''].head(3)
        if len(sample) > 0:
            print(f"\nSAMPLE INVESTOR DATA:")
            for _, row in sample.iterrows():
                print(f"  {row['company_name']}: {row['investors']} (count: {row['investor_count']})")
    else:
        print("No companies extracted")

finally:
    page.quit()
