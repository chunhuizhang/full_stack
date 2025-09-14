
import asyncio
from playwright.async_api import async_playwright
import os
import re
import requests

async def main():
    # Setup
    if not os.path.exists('pdbs'):
        os.makedirs('pdbs')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        start_url = "https://alphafold.ebi.ac.uk/search/text/Terpene%20synthase"
        print(f"Navigating to {start_url}")
        await page.goto(start_url, wait_until='networkidle')

        protein_links_set = set()
        # Scrape links from first 2 pages
        print("Collecting protein links from the first 2 pages...")
        for i in range(2):
            print(f"Scraping page {i+1}...")
            await page.wait_for_load_state('networkidle')
            all_links = await page.eval_on_selector_all('a', 'elements => elements.map(a => a.href)')
            protein_entry_links = [link for link in all_links if link and '/entry/' in link]
            for link in protein_entry_links:
                protein_links_set.add(link)

            # Go to next page
            next_button = page.locator('li.next a')
            if i < 1 and await next_button.is_visible(): # Only click for the first page
                await next_button.click()
            else:
                break # No more pages or we've done 2 pages
        
        protein_links = list(protein_links_set)
        print(f"Found {len(protein_links)} unique protein links.")

        with open('protein_summary.md', 'w', encoding='utf-8') as md_file:
            md_file.write('| Protein Name | Summary and Model Confidence |\n')
            md_file.write('|--------------|------------------------------|\n')

            for i, link in enumerate(protein_links):
                try:
                    print(f"Processing link {i+1}/{len(protein_links)}: {link}")
                    await page.goto(link, wait_until='networkidle', timeout=60000)

                    # Handle cookie consent
                    cookie_button = page.locator('button:has-text("Accept all")')
                    if await cookie_button.is_visible(timeout=5000):
                        print("Accepting cookies...")
                        await cookie_button.click()

                    await page.wait_for_selector('h1.heading-1', timeout=60000)

                    # Extract protein name
                    protein_name_element = await page.query_selector('h1.heading-1')
                    protein_name = await protein_name_element.inner_text() if protein_name_element else "Unknown Protein"
                    sanitized_protein_name = re.sub(r'[<>:"/\\|?*]', '_', protein_name) # Sanitize for filename

                    # Extract Summary and Model Confidence from domain-info class
                    summary_div = page.locator('section.domain-info')
                    await summary_div.wait_for()
                    summary_text = await summary_div.inner_text()
                    summary_text = summary_text.replace('\n', ' ').strip()
                    summary_text_md = summary_text.replace('|', '\\|') # Escape pipe for markdown table

                    # Extract UniProt ID from the link and construct PDB download URL
                    uniprot_id = link.split('/')[-1]  # Extract ID from URL like /entry/A0A3L6G998
                    pdb_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
                    
                    print(f"Constructed PDB URL: {pdb_url}")
                    
                    try:
                        # Download the file using requests library
                        response = requests.get(pdb_url, timeout=30)
                        if response.status_code == 200:
                            pdb_filepath = f"pdbs/{sanitized_protein_name}.pdb"
                            with open(pdb_filepath, "wb") as f:
                                f.write(response.content)
                            print(f"Downloaded PDB file to {pdb_filepath}")
                        else:
                            print(f"Failed to download PDB file, status: {response.status_code}")
                    except Exception as e:
                        print(f"Error downloading PDB file: {e}")

                    # Append to markdown
                    md_file.write(f'| {protein_name} | {summary_text_md} |\n')
                    print(f"Successfully processed: {protein_name}")

                except Exception as e:
                    print(f"Failed to process {link}: {e}")
                    filename_part = link.split('/')[-1]
                    screenshot_path = f"error_{filename_part}.png"
                    await page.screenshot(path=screenshot_path)
                    print(f"Saved screenshot of error page to {screenshot_path}")

        await browser.close()
    print("Scraping finished.")

if __name__ == '__main__':
    asyncio.run(main())
