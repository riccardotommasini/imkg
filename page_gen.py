import markdown
import re
import os

downloadables = list(filter(lambda s: s.endswith(".md") and s not in {"README.md", "contributors.md"}, os.listdir(".")))
dl_names = [s[:-3] for s in downloadables]

main_md = open('README.md').read()
dl_mds = [open(f"{fn}").read() for fn in downloadables]

main_html, *dl_htmls = [markdown.markdown(md) for md in [main_md, *dl_mds]]

title, *dl_titles = [md.split("\n", 1)[0][2:].strip() for md in [main_md, *dl_mds]]

dl_links = [re.search(r"<a.*/a>", md).group(0) for md in dl_htmls]

contributors = re.findall("<li>(.*?)</li>" ,markdown.markdown(open('contributors.md', encoding='utf8').read()))
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@500&family=Roboto:wght@300&display=swap');
body {
    font-family: 'Roboto', sans-serif;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    overflow: hidden;
    -webkit-box-pack: center;
        -ms-flex-pack: center;
            justify-content: center;
    margin: 0;
    height: 100%;
}

body > * {
    margin: 0 15;
    scrollbar-width: none;
}

h1 {
    font-family: 'Roboto Slab', serif;
    font-size: xxx-large;
}
.dl {
    padding: 10;
    margin: 10;
    background-color: aliceblue;
    border-radius: 15px;
    cursor: pointer;
    text-align: left;
}
::-webkit-scrollbar {
    width: 0;
}

.page h1 {
    margin-top: 50px;
}

.page p, ol {
    -webkit-margin-before: 0.3em;
            margin-block-start: 0.3em;
    -webkit-margin-after: 0.3em;
            margin-block-end: 0.3em;

}

#dls {
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    margin-top: 50px;
    margin-bottom: 30px;
    -webkit-box-orient: vertical;
    -webkit-box-direction: normal;
        -ms-flex-direction: column;
            flex-direction: column;
    overflow: scroll;
}

.contributors {
    overflow: scroll;
    margin-top: 50;
    padding: 10;
    background-color: aliceblue;
    border-radius: 15px;
    height: -webkit-fit-content;
    height: -moz-fit-content;
    height: fit-content;
}

a h2 {
    text-decoration: none;
}
.page {
    width: 700px;
    text-align: justify;
    overflow: scroll;
    padding-bottom: 100;
}
"""

JS = """
function navTo(s) {
  window.location.href = s + ".html";
}
"""

def dl_button(i):
    return f"<div class=\"dl\" onclick=\"navTo('{dl_names[i]}')\"><h2>{dl_titles[i]}</h2>{dl_links[i]}</div>"

def contributor(i):
    return f"<div class=\"contributor\"><h3>{contributors[i]}</h3></div>"

MAIN_HTML = f"""
<HTML>
    <HEAD>
        <meta charset="UTF-8">
        <TITLE>{title}</TITLE>
        <style>
        {CSS}
        </style>
        <script>
        {JS}
        </script>
    </HEAD>
    <BODY>
        <div class="contributors">
            <h2>Contributors</h2>
            {"".join(contributor(i) for i in range(len(contributors)))}
        </div>
        <div class="page">
            {main_html}
        </div>
        <div id="dls">
            {"".join(dl_button(i) for i in range(len(downloadables)))}
        </div>
    </BODY>
</HTML>
"""
PAGE_HTMLS = [f"""
<HTML>
    <HEAD>
        <TITLE>{dl_titles[i]}</TITLE>
        <style>
        {CSS}
        </style>
    </HEAD>
    <BODY>
        <div class="page">
        <a href="index.html"><- back</a>
            {dl_htmls[i]}
        </div>
    </BODY>
</HTML>
""" for i in range(len(downloadables))]

with open('index.html', 'w', encoding='utf8') as f:
    f.write(MAIN_HTML)

for i in range(len(downloadables)):
    with open(f'{dl_names[i]}.html', 'w', encoding='utf8') as f:
        f.write(PAGE_HTMLS[i])