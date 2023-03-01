from utils import generate_md_str, get_outline
import bibtexparser
import os
import numpy as np
from collections import OrderedDict

repository_url = "https://github.com/DapengFeng/PaperChest"
bibfile_dir = 'bibtex'
bibfile_names = os.listdir(bibfile_dir)
add_comments = False

def plot_years_title(year):
  return '\n' + "## Papers in " + year[0] + '\n'

all_outline = []
all_md_str = ''
all_md_dict = OrderedDict()
for bibfile_name in bibfile_names:
  with open(os.path.join(bibfile_dir, bibfile_name)) as bibtex_file:
    bibtex_str = bibtex_file.read()

  bib_db = bibtexparser.loads(bibtex_str)

  years = []
  for i in range(1950, 3000):
      years.append([str(i)])
  years.reverse()

  md_dict_str, outline_list = generate_md_str(DB=bib_db,
                  list_classif=years,
                  key="year",
                  plot_title_fct=plot_years_title,
                  bibfile=os.path.join(bibfile_dir, bibfile_name),
                  add_comments=add_comments)
  
  for key, value in md_dict_str.items():
    if key in all_md_dict:
      all_md_dict[key] += value
    else:
      all_md_dict[key] = value
  all_outline += outline_list

all_outline = list(set(np.concatenate(all_outline)))
all_outline.sort()
all_outline.reverse()
all_outline = np.array(all_outline).reshape(-1,1)
str_outline = get_outline(all_outline, repository_url, 'README.md', plot_years_title)

all_md_dict = OrderedDict(sorted(all_md_dict.items(), reverse=True))
for key, value in all_md_dict.items():
  all_md_str += (key + value)

all_md_str = str_outline + all_md_str
with open('README.md', 'w') as output:
  output.write(all_md_str)
  output.close()