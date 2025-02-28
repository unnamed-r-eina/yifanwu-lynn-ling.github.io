
# coding: utf-8

# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# 
# TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
# 

# ## Data format
# 
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# 
# - `excerpt` and `paper_url` can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`


# ## Import pandas
# 
# We are using the very handy pandas library for dataframes.

# In[2]:

import pandas as pd


# ## Import TSV
# 
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# 
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# In[3]:

#publications = pd.read_csv("publications.tsv", sep="\t", header=0)

# Read the CSV file with UTF-8 encoding
publications = pd.read_csv("pubs.csv", dtype=str, encoding="utf-8")

# Debugging print to check the columns
print("Columns found:", publications.columns)



publications


# ## Escape special characters
# 
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# In[4]:

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


# ## Creating the markdown files
# 
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page. If you don't want something to appear (like the "Recommended citation")

# In[5]:

import os
print(publications.columns)

grouped_pubs = publications.groupby("category")

md_content = "# Publications\n\n"

# Define output directory
output_dir = "../_publications"
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

def clean_value(value):
    """Replace '--' with an empty string."""
    return "" if pd.isna(value) or value == "--" else str(value)

for category, items in grouped_pubs:
    md_content += f"## {category}\n\n"

    for _, item in items.iterrows():
        authors = clean_value(item["authors"])
        title = clean_value(item["title"])
        pub_date = clean_value(item["pub_date"])
        journal = clean_value(item["journal"])
        volume = clean_value(item["volume"])
        issue = clean_value(item["issue"])
        pages = clean_value(item["pages"])
        paper_url = clean_value(item["paper_url"])
        category = clean_value(item["category"])

        # Construct YAML metadata
        yaml_block = "---\n"
        yaml_block += f'title: "{title}"\n'
        if authors:
            yaml_block += f'authors: "{authors}"\n'
        if pub_date:
            yaml_block += f'pub_date: "{pub_date}"\n'
        if journal:
            yaml_block += f'journal: "{journal}"\n'
        if volume:
            yaml_block += f'volume: "{volume}"\n'
        if issue:
            yaml_block += f'issue: "{issue}"\n'
        if pages:
            yaml_block += f'pages: "{pages}"\n'
        if paper_url:
            yaml_block += f'paper_url: "{paper_url}"\n'
        yaml_block += f'category: "{category}"\n'
        yaml_block += "---\n\n"
        
        filename = f"{pub_date}-{journal}.md"
        output_path = os.path.join(output_dir, filename)
        
        # Save the markdown file
        print(f"Saving file: {output_path}")
        with open(output_path, 'w', encoding="utf-8") as f:
            f.write(yaml_block)