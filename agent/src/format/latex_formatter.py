
class LatexFormatter:

    @staticmethod
    def format_resume(highlights : str = "", experiences : str = "", skills: str = "", projects: str = ""):
        return f"""
\\documentclass[letterpaper,11pt]{{article}}
\\usepackage{{latexsym}}
\\usepackage[empty]{{fullpage}}
\\usepackage{{titlesec}}
\\usepackage{{marvosym}}
\\usepackage[usenames,dvipsnames]{{color}}
\\usepackage{{verbatim}}
\\usepackage{{enumitem}}
\\usepackage[hidelinks]{{hyperref}}
\\usepackage{{fancyhdr}}
\\usepackage[english]{{babel}}
\\usepackage{{tabularx}}
\\usepackage{{fontawesome5}}
\\input{{glyphtounicode}}

\\usepackage{{lmodern}}

\\pagestyle{{fancy}}
\\fancyhf{{}}
\\fancyfoot{{}}
\\renewcommand{{\\headrulewidth}}{{0pt}}
\\renewcommand{{\\footrulewidth}}{{0pt}}
\\addtolength{{\\oddsidemargin}}{{-0.5in}}
\\addtolength{{\\evensidemargin}}{{-0.5in}}
\\addtolength{{\\textwidth}}{{1in}}
\\addtolength{{\\topmargin}}{{-.5in}}
\\addtolength{{\\textheight}}{{1.0in}}

\\urlstyle{{same}}

\\raggedbottom
\\setlength{{\\tabcolsep}}{{0in}}

\\titleformat{{\\section}}{{
  \\vspace{{-4pt}}\\scshape\\raggedright\\large
}}{{}}{{0em}}{{}}[\\color{{black}}\\titlerule \\vspace{{-5pt}}]

\\pdfgentounicode=1

\\newcommand{{\\resumeItem}}[1]{{
  \\item\\small{{
    #1 \\vspace{{0pt}}
  }}
}}

\\newcommand{{\\resumeSubheading}}[4]{{
  \\vspace{{-2pt}}\\item
    \\begin{{tabular*}}{{0.97\\textwidth}}[t]{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\textbf{{#1}} & #2 \\\\
      \\textit{{\\small#3}} & \\textit{{\\small #4}} \\\\
    \\end{{tabular*}}\\vspace{{-3pt}}
}}

\\newcommand{{\\resumeSubSubheading}}[2]{{
    \\item
    \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\textit{{\\small#1}} & \\textit{{\\small #2}} \\\\
    \\end{{tabular*}}\\vspace{{0pt}}
}}

\\newcommand{{\\resumeProjectHeading}}[2]{{
    \\item
    \\begin{{tabular*}}{{0.97\\textwidth}}{{l@{{\\extracolsep{{\\fill}}}}r}}
      \\small#1 & #2 \\\\
    \\end{{tabular*}}\\vspace{{-3pt}}
}}

\\newcommand{{\\resumeSubItem}}[1]{{\\resumeItem{{#1}}\\vspace{{0pt}}}}

\\renewcommand\\labelitemii{{$\\vcenter{{\\hbox{{\\tiny$\\bullet$}}}}$}}

\\newcommand{{\\resumeSubHeadingListStart}}{{\\begin{{itemize}}[leftmargin=0.15in, label={{}}]}}
\\newcommand{{\\resumeSubHeadingListEnd}}{{\\end{{itemize}}}}
\\newcommand{{\\resumeItemListStart}}{{\\begin{{itemize}}}}
\\newcommand{{\\resumeItemListEnd}}{{\\end{{itemize}}\\vspace{{-5pt}}}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{{document}}
\\include{{custom-commands}}

%----------HEADING----------%
\\begin{{center}}
    \\textbf{{\\Huge \\scshape Amirreza Sokhankhosh}} \\\\ \\vspace{{1pt}}
    \\faPhone \\small 431-293-6515 \\quad
    \\href{{mailto:amirreza.skhn@gmail.com}}{{\\faEnvelope \\ \\underline{{amirreza.skhn@gmail.com}}}} \\quad
    \\href{{https://www.linkedin.com/in/amirrezakh/}}{{\\faLinkedin \\ \\underline{{LinkedIn}}}} \\quad
    \\href{{https://github.com/amirrezaskh}}{{\\faGithub \\ \\underline{{GitHub}}}} \\quad
    \\href{{https://amirrezaskh.com}}{{\\faBriefcase \\ \\underline{{Portfolio}}}}
\\end{{center}}

%----------Highlight of Qualifications----------%
\\section{{Highlight of Qualifications}}
\\resumeItemListStart
{highlights}
\\resumeItemListEnd
%-----------EXPERIENCE-----------%
\\section{{Experience}}
\\resumeSubHeadingListStart

{experiences}

\\resumeSubHeadingListEnd

%-----------Projects-----------%
\\section{{Projects}}
\\resumeSubHeadingListStart

{projects}

\\resumeSubHeadingListEnd

%-----------EDUCATION-----------
\\section{{Education}}
    \\resumeSubHeadingListStart

    \\resumeSubheading
    {{University of Manitoba}}{{Sep 2023 – Aug 2025}}
    {{Master of Science in Computer Science (GPA: 4.4 / 4.5)}}{{Winnipeg, Canada}}
    \\resumeItemListStart
        \\resumeItem{{\\textbf{{Relevant Coursework:}}  Security \\& Privacy, Deep Generative Modeling, Blockchain \\& Distributed Systems: A+}}
    \\resumeItemListEnd

    \\resumeSubheading
    {{K.N. Toosi University of Technology}}{{Sep 2018 – Feb 2023}}
    {{Bachelor of Science in Computer Engineering}}{{}}

    \\resumeSubHeadingListEnd

%-----------Technical Skills-----------
\\section{{Technical Skills}}

{skills}

%-------------------------------------------
\\end{{document}}
"""
    
    @staticmethod
    def format_cover_letter(position, company, cover_letter):
        return f"""
\\documentclass[10pt,letter]{{letter}}
\\usepackage[utf8]{{inputenc}}

\\NeedsTeXFormat{{LaTeX2e}}
\\ProvidesPackage{{TLCcoverletter}}[12/27/21 cover letter package]

\\RequirePackage[T1]{{fontenc}}
\\RequirePackage[default,semibold]{{sourcesanspro}}
\\RequirePackage[12pt]{{moresize}}
\\usepackage{{anyfontsize}}
\\RequirePackage{{csquotes}}

\\RequirePackage[margin=.5in]{{geometry}}
\\setlength{{\\parskip}}{{1em}}

\\RequirePackage{{xcolor}}

\\RequirePackage{{hyperref}}
\\hypersetup{{colorlinks=true,urlcolor=highlight}}


\\pagenumbering{{gobble}}

\\RequirePackage{{standalone}}
\\RequirePackage{{import}}

\\RequirePackage[english]{{babel}}
\\RequirePackage{{blindtext}}

\\def\\name{{Amirreza Sokhankhosh}}
\\signature{{\\name}}
\\address{{111 Steeles Ave E\\\\
North York, ON\\\\
L3T 1A4}}
\\def\\phone{{(431) 293-6515}}
\\def\\email{{amirreza.skhn@gmail.com}}
\\def\\LinkedIn{{amirrezaskh}}
\\def\\github{{amirrezaskh}}
\\def\\role{{ {position} }}


\\RequirePackage{{fancyhdr}}
\\fancypagestyle{{plain}}{{
\\fancyhf{{}}
\\lhead{{\\phone \\\\
	    \\href{{mailto:\\email}}{{\\email}}}}
	\\chead{{
	    \\centering {{\\Large \\textbf\\name}} \\\\
	    {{\\color{{highlight}} \\large{{\\role}}}}}}
	    \\rhead{{
	    Portfolio: \\href{{https://amirrezaskh.com}}{{amirrezaskh.com}}\\\\
	    \\href{{https://github.com/\\github}}{{github.com/\\github}} \\\\
	    \\href{{https://www.linkedin.com/in/\\LinkedIn}}{{linkedin.com/in/\\LinkedIn}}}}
\\renewcommand{{\\headrulewidth}}{{2pt}}
\\renewcommand{{\\headrule}}{{\\hbox to\\headwidth{{
  \\color{{highlight}}\\leaders\\hrule height \\headrulewidth\\hfill}}}}
}}
\\pagestyle{{plain}}

\\setlength{{\\headheight}}{{90pt}}
\\setlength{{\\headsep}}{{0pt}}

\\makeatletter
\\let\\ps@empty\\ps@plain
\\let\\ps@firstpage\\ps@plain
\\makeatother

\\begin{{document}}
\\definecolor{{highlight}}{{RGB}}{{61, 90, 128}}
\\begin{{letter}}{{
Hiring Team \\\\ 
{position} \\\\
{company} }}

\\opening{{Dear Hiring Team,}}

\\setlength\\parindent{{.5in}}

{cover_letter}

\\closing{{Sincerely,}}
\\end{{letter}}

\\end{{document}}
"""