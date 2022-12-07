from pdflatex import PDFLaTeX


def create_pdf(name='', age='', education=[], work_experience=[], skills=[], email='', tel=''):
    print(name, age, education, work_experience, skills, email, tel)
    text = '''
    \\documentclass{article}
    \\usepackage[utf8]{inputenc}

    \\title{Resume}
    \\author{ ''' + name + ''' }

    \\begin{document}

    \\maketitle

    \\section{Age}
        \\text{ \\;\\;\\;\\; ''' + age + '''}

    \\section{Education}
        \\begin{itemize}'''

    for ed in education:
        text += '\\item ' + ed
    text += '''
        \\end{itemize}

    \\section{Work Experience}
        \\begin{itemize}'''

    for we in work_experience:
        text += '\\item ' + we
    text += '''
        \\end{itemize}

    \\section{Skills}
        \\begin{itemize}'''

    for skill in skills:
        text += '\\item ' + skill
    text += '''
        \\end{itemize}

    \\section{Contacts}
        \\begin{itemize}
            \\item ''' + email + '''
            \\item ''' + tel + '''
        \\end{itemize}
    \\end{document}
    '''

    with open('resume.tex', 'w') as resume_tex:
        resume_tex.write(text)

    pdfl = PDFLaTeX.from_texfile('resume.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

# create_pdf('Ilya', '19', ['HSE'], ['NO'], ['programming', 'maths', 'thinking'], 'ivgerman@edu.hse.ru', '89056660346')
