#!/usr/bin/env python3
"""Rebuild the four bilingual PDF resumes from one synchronized content model.
Run: python tools/build_cvs.py
Requires: reportlab, Pillow, and system Lato fonts; no font files are bundled.
"""
from pathlib import Path
import shutil
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, PageBreak, KeepTogether, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'/'cv'
OUT.mkdir(parents=True, exist_ok=True)
PHOTO=ROOT/'assets'/'img'/'antonio-hernandez-pinto.jpg'
FONTPATH=Path('/usr/share/fonts/truetype/lato')
for n,fn in [('Lato','Lato-Regular.ttf'),('Lato-Bold','Lato-Bold.ttf'),('Lato-Light','Lato-Light.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONTPATH/fn)))
pdfmetrics.registerFontFamily('Lato',normal='Lato',bold='Lato-Bold',italic='Lato',boldItalic='Lato-Bold')
NAVY=HexColor('#142546'); INK=HexColor('#1b2c49'); MUTED=HexColor('#435674'); SOFT=HexColor('#71839e'); AQUA=HexColor('#72dcd9'); LINE=HexColor('#b9dfe4')
W,H=A4
PAGES={
 'es': {
  'subtitle':'SENIOR QA AUTOMATION ENGINEER  |  SDET', 'profile':'PERFIL PROFESIONAL', 'technologies':'TECNOLOGÍAS',
  'career':'EXPERIENCIA PROFESIONAL', 'othercareer':'TRAYECTORIA ANTERIOR', 'expertise':'COMPETENCIAS CLAVE',
  'projects':'PROYECTOS SELECCIONADOS', 'international':'EXPERIENCIA INTERNACIONAL', 'education':'FORMACIÓN',
  'certifications':'CERTIFICACIONES Y CURSOS', 'links':'ENLACES', 'foot':'Currículum',
  'summary':'Profesional de QA y automatización de pruebas con experiencia en calidad de software desde 2007. Automatización con Python desde 2019, testing web y API, frameworks y CI/CD. Trayectoria previa con Java y coordinación de equipos QA.',
  'tech':'Python · pytest · Selenium · Playwright · API testing · Java · Behave/Gherkin · Jenkins · Docker · Git / Bitbucket · Jira · SQL · RabbitMQ · Google SecOps',
  'current':'Telefónica Tech (ElevenPaths) — empleador actual', 'currentdate':'Abr. 2019 – Actualidad',
  'phase1':'Proyecto Thanos para BBVA · Oct. 2026 – Actualidad',
  'phase1text':'Diseño, planificación y ejecución de playbooks de Google SecOps para BBVA desde Telefónica Tech.',
  'phase2':'QA Automation / SDET · Abr. 2019 – Sep. 2026',
  'phase2text':'Automatización de pruebas con Python: escenarios Gherkin, pruebas web y API, mensajería RabbitMQ y ejecución automatizada mediante CI/CD.',
  'locken':'Senior QA Test Lead & DevOps Engineer · Locken Ibérica', 'lockendate':'Ene. 2016 – Abr. 2019',
  'lockentext':'Coordinación de QA, pipelines Jenkins, shell scripting y reporting automatizado para detectar incidencias y dar seguimiento a las entregas.',
  'tgt':'QA Lead · MTP / Telefónica Global Technology', 'tgtdate':'Jun. 2015 – Dic. 2015',
  'tgttext':'Coordinación de QA en entornos Data Warehouse (Oracle); análisis de incidencias y defectos críticos.',
  'vodafone':'QA Engineer · MTP / Vodafone', 'vodafonedate':'Jul. 2013 – Jun. 2015',
  'vodafonetext':'Pruebas de facturación y coordinación de un equipo de tres testers.',
  'movistar':'QA Engineer · MTP / Movistar', 'movistardate':'Sep. 2007 – Jul. 2013',
  'movistartext':'Análisis de requisitos, planes de prueba y detección de defectos en servicios de telecomunicaciones.',
  'canon':'HelpDesk · Canon', 'canondate':'Oct. 2003 – Sep. 2007',
  'canontext':'Soporte técnico y resolución de incidencias de hardware y software.',
  'skills':[
   '<b>Testing:</b> funcional, regresión, smoke, GUI y UAT; diseño y ejecución de pruebas web y API.',
   '<b>Automatización:</b> Python, pytest, Selenium, Playwright, Java, Behave/Gherkin.',
   '<b>CI/CD y gestión:</b> Jenkins, Docker, Kubernetes, Git, Bitbucket, Jira y Redmine.',
   '<b>Datos y sistemas:</b> SQL, MySQL, Elasticsearch, Oracle; Windows, Ubuntu, Android e iOS.'
  ],
  'projecttext':'SandasGRC (ElevenPaths) · Dinoflux · Vamps · Tu Empresa Segura · Tu Gestor Tecnológico.',
  'internationaltext':'Consultoría QA para Movistar en México (marzo de 2014): implantación de un laboratorio de QA y detección de problemas críticos en recargas prepago.',
  'educationtext':['Maestro en Educación Primaria (Diplomatura), 1998–2001 · Centro Fray Luis de León (Valladolid).',
                   'Técnico Superior en Desarrollo de Aplicaciones Informáticas, 2001–2003 · Centro Gregorio Fernández (Valladolid).',
                   'Formación complementaria en COBOL.'],
  'certtext':'ISTQB Foundation (2011), Advanced (2015), Agile Extension (2015) · Kubernetes Essentials (2019) · Business Intelligence (2016) · AWS Technical Essentials y Generative AI (2025).',
  'priorbrief':'Locken Ibérica (Senior QA Test Lead & DevOps, 2016–2019) · MTP / Telefónica Global Technology (QA Lead, 2015) · MTP / Vodafone (QA, 2013–2015) · MTP / Movistar (QA, 2007–2013) · Canon (HelpDesk, 2003–2007).'
 },
 'en': {
  'subtitle':'SENIOR QA AUTOMATION ENGINEER  |  SDET', 'profile':'PROFESSIONAL PROFILE', 'technologies':'TECHNOLOGIES',
  'career':'PROFESSIONAL EXPERIENCE', 'othercareer':'EARLIER EXPERIENCE', 'expertise':'CORE COMPETENCIES',
  'projects':'SELECTED PROJECTS', 'international':'INTERNATIONAL EXPERIENCE', 'education':'EDUCATION',
  'certifications':'CERTIFICATIONS & TRAINING', 'links':'LINKS', 'foot':'Resume',
  'summary':'QA and test automation professional with software quality experience since 2007. Focused on Python automation since 2019, web and API testing, frameworks and CI/CD. Earlier experience with Java automation and QA team coordination.',
  'tech':'Python · pytest · Selenium · Playwright · API testing · Java · Behave/Gherkin · Jenkins · Docker · Git / Bitbucket · Jira · SQL · RabbitMQ · Google SecOps',
  'current':'Telefónica Tech (ElevenPaths) — current employer', 'currentdate':'Apr 2019 – Present',
  'phase1':'Thanos project for BBVA · Oct 2026 – Present',
  'phase1text':'Design, planning and execution of Google SecOps playbooks for BBVA through Telefónica Tech.',
  'phase2':'QA Automation / SDET · Apr 2019 – Sep 2026',
  'phase2text':'Python test automation: Gherkin scenarios, web and API testing, RabbitMQ messaging and automated execution in CI/CD.',
  'locken':'Senior QA Test Lead & DevOps Engineer · Locken Ibérica', 'lockendate':'Jan 2016 – Apr 2019',
  'lockentext':'QA team coordination, Jenkins pipelines, shell scripting and automated quality reporting to identify defects and track deliveries.',
  'tgt':'QA Lead · MTP / Telefónica Global Technology', 'tgtdate':'Jun 2015 – Dec 2015',
  'tgttext':'QA coordination in Oracle Data Warehouse environments; critical defect investigation and analysis.',
  'vodafone':'QA Engineer · MTP / Vodafone', 'vodafonedate':'Jul 2013 – Jun 2015',
  'vodafonetext':'Billing process testing and coordination of a three-person QA team.',
  'movistar':'QA Engineer · MTP / Movistar', 'movistardate':'Sep 2007 – Jul 2013',
  'movistartext':'Requirements analysis, test plans and defect identification for telecom services.',
  'canon':'HelpDesk · Canon', 'canondate':'Oct 2003 – Sep 2007',
  'canontext':'Technical support and troubleshooting of hardware and software issues.',
  'skills':[
   '<b>Testing:</b> functional, regression, smoke, GUI and UAT; web and API test design and execution.',
   '<b>Automation:</b> Python, pytest, Selenium, Playwright, Java, Behave/Gherkin.',
   '<b>CI/CD &amp; management:</b> Jenkins, Docker, Kubernetes, Git, Bitbucket, Jira and Redmine.',
   '<b>Data &amp; systems:</b> SQL, MySQL, Elasticsearch, Oracle; Windows, Ubuntu, Android and iOS.'
  ],
  'projecttext':'SandasGRC (ElevenPaths) · Dinoflux · Vamps · Tu Empresa Segura · Tu Gestor Tecnológico.',
  'internationaltext':'QA consulting for Movistar in Mexico (March 2014): setting up a QA lab and identifying critical prepaid top-up issues.',
  'educationtext':['Diploma in Primary Education Teaching, 1998–2001 · Fray Luis de León (Valladolid, Spain).',
                   'Higher Vocational Diploma in Computer Application Development, 2001–2003 · Gregorio Fernández (Valladolid, Spain).',
                   'Additional training in COBOL.'],
  'certtext':'ISTQB Foundation (2011), Advanced (2015), Agile Extension (2015) · Kubernetes Essentials (2019) · Business Intelligence (2016) · AWS Technical Essentials and Generative AI (2025).',
  'priorbrief':'Locken Ibérica (Senior QA Test Lead & DevOps, 2016–2019) · MTP / Telefónica Global Technology (QA Lead, 2015) · MTP / Vodafone (QA, 2013–2015) · MTP / Movistar (QA, 2007–2013) · Canon (HelpDesk, 2003–2007).'
 }
}


# Consistent, print-friendly executive (one page) and detailed (two pages) design.
# The sole public contact destinations are the website and LinkedIn.
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.enums import TA_LEFT

WEBSITE='https://antoniohernandezpinto.com/'
LINKEDIN='https://www.linkedin.com/in/antonio-hernandez-pinto/'
PAPER=HexColor('#FFFFFF')
MIST=HexColor('#F2F7F9')
PALE=HexColor('#E9F3F4')
DEEP=HexColor('#152742')
SEA=HexColor('#087F83')
GREY=HexColor('#526277')
BORDER=HexColor('#D9E3E9')
LIGHT_TXT=HexColor('#E3EDF1')


def tx(c,x,y,s,font='Lato',size=9.2,color=INK):
    c.setFont(font,size);c.setFillColor(color);c.drawString(x,y,s)


def para(c,txt,x,y,width,font_size=9.65,lead=13.8,color=INK,kind='Lato',after=0,markup=False):
    style=ParagraphStyle('p',fontName=kind,fontSize=font_size,leading=lead,textColor=color,spaceAfter=0,allowWidows=0,allowOrphans=0)
    pp=Paragraph(txt if markup else escape(txt),style)
    _,hh=pp.wrap(width,1200)
    pp.drawOn(c,x,y-hh)
    return y-hh-after


def section(c,label,x,y,width,accent=True):
    if accent:
        c.setFillColor(SEA);c.roundRect(x,y-13,3,14,1.4,fill=1,stroke=0)
    tx(c,x+11,y-10,label.upper(),'Lato-Bold',9.2,DEEP)
    c.setStrokeColor(BORDER);c.setLineWidth(.75)
    c.line(x,y-20,x+width,y-20)
    return y-31


def link(c,x,y,label,url,size=8.6,color=LIGHT_TXT):
    tx(c,x,y,label,'Lato',size,color)
    width=pdfmetrics.stringWidth(label,'Lato',size)
    c.linkURL(url,(x,y-3,x+width,y+11),relative=0,thickness=0)
    return x+width


def header(c,content,page=1,full=False):
    c.setFillColor(DEEP);c.rect(0,H-123,W,123,fill=1,stroke=0)
    c.setFillColor(SEA);c.rect(0,H-123,7,123,fill=1,stroke=0)
    c.setFillColor(AQUA);c.roundRect(46,H-33,42,3,1.5,fill=1,stroke=0)
    tx(c,46,H-61,'ANTONIO HERNÁNDEZ PINTO','Lato-Bold',20.5,colors.white)
    tx(c,47,H-82,content['subtitle'],'Lato',10.2,LIGHT_TXT)
    end=link(c,47,H-106,'antoniohernandezpinto.com',WEBSITE,8.4)
    tx(c,end+9,H-106,'|','Lato',8.3,LIGHT_TXT)
    link(c,end+21,H-106,'linkedin.com/in/antonio-hernandez-pinto',LINKEDIN,8.4)
    if PHOTO.exists():
        px,py,pw,ph=W-130,H-109,79,86
        c.setFillColor(colors.white)
        c.roundRect(px-3,py-3,pw+6,ph+6,9,fill=1,stroke=0)
        c.drawImage(ImageReader(str(PHOTO)),px,py,pw,ph,preserveAspectRatio=False,mask='auto')
    c.setStrokeColor(BORDER);c.setLineWidth(.7);c.line(46,53,W-46,53)
    tx(c,46,36,'ANTONIO HERNÁNDEZ PINTO','Lato-Bold',7.4,GREY)
    tx(c,46,22,'antoniohernandezpinto.com','Lato',7.4,GREY)
    c.setFont('Lato',7.4);c.setFillColor(GREY)
    c.drawRightString(W-46,29, ('CV ejecutivo' if not full else 'CV completo') if content['foot']=='Currículum' else ('Executive resume' if not full else 'Full resume'))
    c.drawRightString(W-46,19,str(page))


def phase(c,title,desc,x,y,width,short=False):
    y=para(c,title,x,y,width,9.45,12.8,SEA,'Lato-Bold',after=3)
    y=para(c,desc,x,y,width,9.05 if short else 9.55,12.65 if short else 13.2,GREY,after=10)
    return y


def current_employer(c,data,x,y,width,short=False):
    # Highlight the same employer across both projects without inventing a job change.
    text_width=width-26
    h1=Paragraph(escape(data['phase1text']),ParagraphStyle('m',fontName='Lato',fontSize=9.05 if short else 9.55,leading=12.65 if short else 13.2)).wrap(text_width-3,500)[1]
    h2=Paragraph(escape(data['phase2text']),ParagraphStyle('m2',fontName='Lato',fontSize=9.05 if short else 9.55,leading=12.65 if short else 13.2)).wrap(text_width-3,500)[1]
    h=39+14+3+h1+10+14+3+h2+13
    c.setFillColor(MIST);c.roundRect(x,y-h,width,h,10,fill=1,stroke=0)
    c.setFillColor(SEA);c.roundRect(x,y-h,3,h,1.5,fill=1,stroke=0)
    cursor=y-19
    tx(c,x+13,cursor,'TELEFÓNICA TECH','Lato-Bold',11.5,DEEP)
    c.setFont('Lato',8.4);c.setFillColor(GREY);c.drawRightString(x+width-13,cursor,data['currentdate'])
    cursor-=19
    cursor=phase(c,data['phase1'],data['phase1text'],x+13,cursor,text_width-3,short)
    cursor=phase(c,data['phase2'],data['phase2text'],x+13,cursor,text_width-3,short)
    return y-h-15


def past_job(c,role,date,desc,x,y,width,short=False):
    # Separating date from role avoids overlong lines and clipped labels.
    title,sep,organization=role.partition(' · ')
    tx(c,x,y-9,title,'Lato-Bold',9.8 if short else 10.4,DEEP)
    yy=y-23
    orgline=organization
    yy=para(c,orgline+'   ·   '+date,x,yy,width,8.7 if short else 9.15,11.7,GREY,after=4)
    if not short:
        yy=para(c,desc,x,yy,width,9.45,13.0,GREY,after=4)
    c.setStrokeColor(BORDER);c.setLineWidth(.45);c.line(x,yy,x+width,yy)
    return yy-(10 if short else 17)


def bullet(c,text,x,y,width,size=9.45,lead=13.2,gap=10):
    c.setFillColor(SEA);c.circle(x+3,y-7,2,fill=1,stroke=0)
    return para(c,text,x+13,y,width-13,size,lead,GREY,after=gap,markup=True)


def sidebar_section(c,title,x,y,w,lines):
    y=section(c,title,x,y,w)
    for text in lines:
        y=para(c,text,x,y,w,9.0,12.8,GREY,after=10)
    return y-8


def executive(c,d):
    header(c,d)
    xx=46
    y=section(c,d['profile'],xx,H-146,W-92)
    y=para(c,d['summary'],xx,y,W-92,10.3,15.2,INK,after=19)
    # A clear two-column reading order: professional trajectory, then toolbox/education.
    left=46; lw=335; right=399; rw=150
    y_left=section(c,d['career'],left,y,lw)
    y_left=current_employer(c,d,left,y_left,lw,short=True)
    y_left=section(c,d['othercareer'],left,y_left+4,lw)
    jobs=[('locken','lockendate','lockentext'),('tgt','tgtdate','tgttext'),('vodafone','vodafonedate','vodafonetext'),('movistar','movistardate','movistartext'),('canon','canondate','canontext')]
    for a,b,desc in jobs:
        y_left=past_job(c,d[a],d[b],d[desc],left,y_left,lw,short=True)
    # Sidebar has a subtle background and three well-delimited categories.
    side_top=y+5
    c.setFillColor(MIST);c.roundRect(right-12,74,rw+24,side_top-74+14,9,fill=1,stroke=0)
    y_side=section(c,d['technologies'],right,side_top-13,rw)
    techlines=[
       '<b>Python</b> · pytest · Selenium · Playwright',
       '<b>APIs</b> · Behave / Gherkin · Java',
       '<b>CI/CD</b> · Jenkins · Docker · Git',
       '<b>Otros</b> · SQL · RabbitMQ · Google SecOps',
    ] if d['foot']=='Currículum' else [
       '<b>Python</b> · pytest · Selenium · Playwright',
       '<b>APIs</b> · Behave / Gherkin · Java',
       '<b>CI/CD</b> · Jenkins · Docker · Git',
       '<b>Other</b> · SQL · RabbitMQ · Google SecOps',
    ]
    for line in techlines: y_side=para(c,line,right,y_side,rw,8.8,12.3,GREY,markup=True,after=9)
    y_side=section(c,d['education'],right,y_side-6,rw)
    for line in d['educationtext'][:2]: y_side=para(c,line,right,y_side,rw,8.7,12.2,GREY,after=9)
    y_side=section(c,d['certifications'],right,y_side-6,rw)
    y_side=para(c,d['certtext'],right,y_side,rw,8.65,12.4,GREY,after=3)
    if y_left < 65 or y_side < 66:
        raise ValueError(f'Executive page overflows: {d["foot"]}, left {y_left:.1f}, right {y_side:.1f}')


def detailed_page1(c,d):
    header(c,d,page=1,full=True)
    x=46;w=W-92
    y=section(c,d['profile'],x,H-146,w)
    y=para(c,d['summary'],x,y,w,10.5,15.3,INK,after=18)
    # Horizontal compact expertise strip visually connects page 1 with page 2.
    strip='Python  ·  pytest  ·  Selenium  ·  Playwright  ·  API testing  ·  Jenkins / CI-CD  ·  Google SecOps'
    c.setFillColor(PALE);c.roundRect(x,y-31,w,34,7,fill=1,stroke=0)
    tx(c,x+11,y-21,strip,'Lato-Bold',8.9,SEA)
    y-=50
    y=section(c,d['career'],x,y,w)
    y=current_employer(c,d,x,y,w,short=False)
    jobs=[('locken','lockendate','lockentext'),('tgt','tgtdate','tgttext'),('vodafone','vodafonedate','vodafonetext'),('movistar','movistardate','movistartext'),('canon','canondate','canontext')]
    for a,b,desc in jobs[:3]:
        y=past_job(c,d[a],d[b],d[desc],x,y,w,short=False)
    if y < 60: raise ValueError(f'Detailed page1 overflows: {d["foot"]}, {y:.1f}')


def detailed_page2(c,d):
    header(c,d,page=2,full=True)
    lx=46;lw=258;rx=333;rw=216
    ly=section(c,d['othercareer'],lx,H-150,lw)
    ly=past_job(c,d['movistar'],d['movistardate'],d['movistartext'],lx,ly,lw,short=False)
    ly=past_job(c,d['canon'],d['canondate'],d['canontext'],lx,ly,lw,short=False)
    ly=section(c,d['expertise'],lx,ly-4,lw)
    for line in d['skills']:
        ly=bullet(c,line,lx,ly,lw,9.45,13.3,12)
    ly=section(c,d['projects'],lx,ly-10,lw)
    ly=para(c,d['projecttext'],lx,ly,lw,10.0,14.7,GREY,after=22)
    ly=section(c,d['international'],lx,ly,lw)
    ly=para(c,d['internationaltext'],lx,ly,lw,10.0,14.7,GREY,after=16)
    ry=section(c,d['education'],rx,H-150,rw)
    for line in d['educationtext']:
        ry=bullet(c,escape(line),rx,ry,rw,9.5,13.6,11)
    ry=section(c,d['certifications'],rx,ry-13,rw)
    cert_items=[
      ('ISTQB', 'Foundation (2011), Advanced (2015), Agile Extension (2015)'),
      ('Kubernetes', 'Essentials (2019)'),
      ('Business Intelligence', '(2016)'),
      ('AWS', 'Technical Essentials and Generative AI (2025)' if d['foot'] != 'Currículum' else 'Technical Essentials y Generative AI (2025)'),
    ]
    for title,desc in cert_items:
        ry=para(c,f'<b>{escape(title)}:</b> {escape(desc)}',rx,ry,rw,9.5,13.5,GREY,after=11,markup=True)
    ry=section(c,d['technologies'],rx,ry-10,rw)
    ry=para(c,d['tech'],rx,ry,rw,9.25,14.3,GREY,after=12)
    if min(ry,ly)<65: raise ValueError(f'Detailed page2 overflows: {d["foot"]}, left {ly:.1f}, right {ry:.1f}')


def build(lang='es',short=False):
    d=PAGES[lang]
    filename=OUT/('Antonio_Hernandez_Pinto_CV_'+lang.upper()+('_1pagina.pdf' if lang=='es' and short else '_1page.pdf' if short else '_completo.pdf' if lang=='es' else '_full.pdf'))
    c=pdfcanvas.Canvas(str(filename),pagesize=A4,pageCompression=1)
    c.setTitle('Antonio Hernández Pinto - '+('CV ejecutivo' if short and lang=='es' else 'Executive resume' if short else 'Currículum' if lang=='es' else 'Full resume'))
    c.setAuthor('Antonio Hernández Pinto')
    c.setSubject('QA Automation | SDET | Telefónica Tech')
    if short:
        executive(c,d)
        c.showPage()
    else:
        detailed_page1(c,d);c.showPage()
        detailed_page2(c,d);c.showPage()
    c.save()
    return filename

if __name__=='__main__':
    for lang in ('es','en'):
        for short in (False,True):
            print(build(lang,short))
    shutil.copyfile(OUT/'Antonio_Hernandez_Pinto_CV_ES_completo.pdf',OUT/'Antonio_Hernandez_Pinto_RESUME_linkedIn_version.pdf')
