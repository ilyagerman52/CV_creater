from pdflatex import PDFLaTeX


def create_pdf(name='', age='', education=[], work_experience=[], skills=[], email='', tel='', pict=None):
    print(name, age, education, work_experience, skills, email, tel, pict)
    text = '''
    \\documentclass{article}
    \\usepackage[utf8]{inputenc}
    \\usepackage{graphicx}

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
        
    \\section{Photo}
        \\includegraphics[scale=0.8]{ ''' + pict +'''}
    \\end{document}
    '''

    with open('resume.tex', 'w') as resume_tex:
        resume_tex.write(text)

    pdfl = PDFLaTeX.from_texfile('resume.tex')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=True)

# create_pdf('Petrov Timur', '88', ['HSE'], ['Ozon', 'Parrot farm', 'HSE'], ['Python', 'Parrot distinguishability'], 'tpetrov@hse.ru', '27269', 'photo.jpg')
