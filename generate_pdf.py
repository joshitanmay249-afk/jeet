import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

pdf_path = r"c:\Users\Lenovo\Downloads\jeet\Plant_Stress_Detector_Project_Report_Updated.pdf"

# Dynamic section page recorder for exact table of contents / index page numbers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        # Don't draw running headers/footers on cover page (page 1)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#555555"))
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 36, 24, page_text)
            self.drawString(36, 24, "Plant Stress Detector - Class 12 CS & Biology Project")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(36, 34, 612 - 36, 34)
            self.restoreState()


class PageTracker(SimpleDocTemplate):
    """Subclass to record page numbers during build and insert into index in two passes or via canvas callback."""
    pass


def generate_report():
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=42
    )

    styles = getSampleStyleSheet()

    # Custom typography
    title_cover_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1,
        textColor=colors.HexColor("#1B2B1B")
    )

    subtitle_cover_style = ParagraphStyle(
        'CoverSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=colors.HexColor("#2E4A2E")
    )

    h1_style = ParagraphStyle(
        'ReportH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        spaceAfter=15,
        textColor=colors.HexColor("#1B2B1B")
    )

    h2_style = ParagraphStyle(
        'ReportH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor("#2E4A2E")
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=15,
        alignment=4,
        textColor=colors.HexColor("#222222")
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        leftIndent=15,
        textColor=colors.HexColor("#222222")
    )

    # Increased font size for code from 6.5pt to 8.5pt with leading 10.5pt
    code_style = ParagraphStyle(
        'ReportCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=10.5,
        textColor=colors.HexColor("#111111")
    )

    # Clean code content from main.py
    with open(r"c:\Users\Lenovo\Downloads\jeet\main.py", "r", encoding="utf-8") as f:
        raw_code = f.read()

    # Replace any potential Unicode box/dash characters with standard ASCII equivalents
    clean_code = (
        raw_code.replace('\u2500', '-')
                .replace('\u2550', '=')
                .replace('\u2014', '-')
                .replace('\u2013', '-')
                .replace('\u2022', '*')
    )

    code_lines = clean_code.splitlines()

    # Calculate page layout:
    # Page 1: Title/Cover
    # Page 2: Certificate
    # Page 3: Acknowledgement
    # Page 4: Index
    # Page 5: About the Project
    # Page 6: List of Functions
    # Page 7: List of Libraries
    # Page 8+: Source Code (main.py)
    # Following Source Code: Output and Database Verification
    # Following Output: Bibliography

    lines_per_code_page = 64
    code_page_count = (len(code_lines) + lines_per_code_page - 1) // lines_per_code_page
    
    code_start_page = 8
    code_end_page = code_start_page + code_page_count - 1
    output_start_page = code_end_page + 1
    # Output section has 2 pages (workflow + sample output / db schema)
    output_end_page = output_start_page + 1
    biblio_page = output_end_page + 1

    story = []

    # =========================================================================
    # PAGE 1: TITLE / COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 45))
    story.append(Paragraph("COMPUTER SCIENCE (083) &amp; BIOLOGY", subtitle_cover_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("PROJECT REPORT", subtitle_cover_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Academic Year 2026-2027", ParagraphStyle('CoverYear', parent=subtitle_cover_style, fontName='Helvetica', fontSize=11)))
    story.append(Spacer(1, 45))

    story.append(Paragraph("PLANT STRESS DETECTOR", title_cover_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Using Python 3, Tkinter, MySQL, and Matplotlib", ParagraphStyle('TechSub', parent=subtitle_cover_style, fontName='Helvetica', fontSize=12, textColor=colors.HexColor("#444444"))))
    story.append(Spacer(1, 60))

    cover_data = [
        [Paragraph("<b>Submitted by</b>", body_style), Paragraph("Jeet Yadav", body_style)],
        [Paragraph("<b>Class and Section</b>", body_style), Paragraph("Standard XII - A", body_style)],
        [Paragraph("<b>Roll Number</b>", body_style), Paragraph("____________________", body_style)],
        [Paragraph("<b>School</b>", body_style), Paragraph("Airport School Ahmedabad", body_style)],
        [Paragraph("<b>Subject</b>", body_style), Paragraph("Computer Science (083) / Biology", body_style)],
        [Paragraph("<b>Under the guidance of</b>", body_style), Paragraph("Mr. Arpit Desai", body_style)],
        [Paragraph("<b>Date of submission</b>", body_style), Paragraph("18/11/2026", body_style)]
    ]

    t_cover = Table(cover_data, colWidths=[200, 320])
    t_cover.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1.2, colors.HexColor("#2E4A2E")),
        ('INNERGRID', (0,0), (-1,-1), 0.6, colors.HexColor("#888888")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#EAEFEA")),
    ]))
    story.append(t_cover)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Certificate", h1_style))
    story.append(Spacer(1, 25))

    cert_text = (
        "This is to certify that <b>Jeet Yadav</b> of standard <b>XII</b> of <b>Airport School Ahmedabad</b> "
        "has successfully completed his project work in <b>Computer Science (083)</b> titled <b>\"Plant Stress Detective\"</b> "
        "under the guidance of <b>Mr. Arpit Desai</b> during the academic year 2026-2027.<br/><br/>"
        "The project was carried out as a part of the practical assessment for the subject. The work presented in this "
        "report is the original effort of the student, and the application described in it has been designed, coded, "
        "tested, and demonstrated by him on the school computer laboratory systems."
    )
    story.append(Paragraph(cert_text, body_style))
    story.append(Spacer(1, 80))

    sig_data_1 = [
        [Paragraph("<b>School Stamp:</b> ________________________", body_style),
         Paragraph("<b>Teacher's Signature:</b> ________________________", body_style)]
    ]
    t_sig1 = Table(sig_data_1, colWidths=[260, 260])
    t_sig1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t_sig1)
    story.append(Spacer(1, 40))

    sig_data_2 = [
        [Paragraph("<b>Principal's Signature:</b> ____________________", body_style),
         Paragraph("<b>Examiner's Signature:</b> ____________________", body_style)]
    ]
    t_sig2 = Table(sig_data_2, colWidths=[260, 260])
    t_sig2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t_sig2)
    story.append(Spacer(1, 40))

    sig_data_3 = [
        [Paragraph("<b>Examiner's Code:</b> ________________________", body_style),
         Paragraph("<b>Date:</b> ________________________", body_style)]
    ]
    t_sig3 = Table(sig_data_3, colWidths=[260, 260])
    t_sig3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
    story.append(t_sig3)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ACKNOWLEDGEMENT
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Acknowledgement", h1_style))
    story.append(Spacer(1, 20))

    ack_text1 = (
        "I would like to express a special token of gratitude to my Computer Science Teacher, <b>Mr. Arpit Desai</b>, "
        "for his constant guidance, valuable suggestions, and supervision throughout the development of this project. "
        "His insights helped me overcome technical hurdles and complete the project successfully."
    )
    ack_text2 = (
        "I am also deeply thankful to our Principal, <b>Ms. Shalini Dhanwani</b>, for providing the necessary facilities, "
        "computer laboratory resources, and encouragement to carry out this practical work."
    )
    ack_text3 = (
        "My sincere thanks go to my parents and friends for their continuous support, motivation, and help in finalizing "
        "this project within the given timeframe."
    )
    ack_text4 = (
        "Lastly, I thank all my classmates who directly or indirectly contributed with their constructive feedback and "
        "suggestions during the testing and demonstration phases of the application."
    )

    story.append(Paragraph(ack_text1, body_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph(ack_text2, body_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph(ack_text3, body_style))
    story.append(Spacer(1, 14))
    story.append(Paragraph(ack_text4, body_style))
    story.append(Spacer(1, 35))

    ack_table_data = [
        [Paragraph("<b>Student Name</b>", body_style), Paragraph("Jeet Yadav", body_style)],
        [Paragraph("<b>Class and Section</b>", body_style), Paragraph("Standard 12 - A", body_style)],
        [Paragraph("<b>Roll Number</b>", body_style), Paragraph("____________________", body_style)],
        [Paragraph("<b>Subject</b>", body_style), Paragraph("Computer Science (083)", body_style)],
        [Paragraph("<b>Date</b>", body_style), Paragraph("18/11/2026", body_style)],
        [Paragraph("<b>Signature</b>", body_style), Paragraph("____________________", body_style)]
    ]
    t_ack = Table(ack_table_data, colWidths=[200, 320])
    t_ack.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#2E4A2E")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#AAAAAA")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F5F8F5")),
    ]))
    story.append(t_ack)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: INDEX (Without Certificate and Acknowledgement, With Page Numbers)
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Index", h1_style))
    story.append(Spacer(1, 20))

    index_data = [
        [Paragraph("<b>Sr. No.</b>", body_style), Paragraph("<b>Topic</b>", body_style), Paragraph("<b>Page No.</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("About the Project", body_style), Paragraph("5", body_style)],
        [Paragraph("2", body_style), Paragraph("List of Functions", body_style), Paragraph("6", body_style)],
        [Paragraph("3", body_style), Paragraph("List of Libraries", body_style), Paragraph("7", body_style)],
        [Paragraph("4", body_style), Paragraph("Source Code (main.py)", body_style), Paragraph(f"{code_start_page} - {code_end_page}", body_style)],
        [Paragraph("5", body_style), Paragraph("Output and Database Verification", body_style), Paragraph(f"{output_start_page} - {output_end_page}", body_style)],
        [Paragraph("6", body_style), Paragraph("Bibliography", body_style), Paragraph(f"{biblio_page}", body_style)]
    ]
    t_index = Table(index_data, colWidths=[65, 375, 80])
    t_index.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#2E4A2E")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#AAAAAA")),
        ('TOPPADDING', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 9),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EAEFEA")),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
    ]))
    story.append(t_index)
    story.append(Spacer(1, 30))

    desc_index = (
        "Each topic of this report starts on a designated section. The report describes the biological "
        "theory behind the project, the functions and libraries used, the complete clean source code of the "
        "application, and the analytical outputs together with the records stored in the MySQL database."
    )
    story.append(Paragraph(desc_index, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: ABOUT THE PROJECT
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("About The Project", h1_style))
    story.append(Spacer(1, 10))

    about_p1 = (
        "<b>Plant Stress Detective</b> is an interdisciplinary desktop software solution engineered using "
        "<b>Python 3</b>, <b>MySQL Relational Database</b>, <b>Tkinter (GUI)</b>, and <b>Matplotlib</b>. The primary "
        "objective of the project is to provide higher secondary students with an interactive, data-driven "
        "analytical tool to observe, quantify, and analyze how varying environmental stressors "
        "(drought/water scarcity, overwatering, low light, extreme temperature) affect plant physiological "
        "growth metrics over time."
    )
    story.append(Paragraph(about_p1, body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Key Objectives and Educational Link", h2_style))
    about_p2 = (
        "In standard Class 12 Biology (Units covering <i>Plant Physiology, Photosynthesis in Higher Plants, "
        "and Plant Growth &amp; Development</i>), controlled experimentation is crucial to understand limiting "
        "factors (Blackman's Law of Limiting Factors). Students germinate seeds (such as <i>Vigna radiata</i> / "
        "Green Gram) under differentiated conditions:"
    )
    story.append(Paragraph(about_p2, body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("&bull; <b>Group A (Control / Optimal):</b> Regular watering schedule, adequate sunlight (8-10 hours/day), ambient temperature (22-28&deg;C).", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("&bull; <b>Group B (Water Stress):</b> Deficit hydration, desiccated soil conditions.", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("&bull; <b>Group C (Photoperiod / Light Stress):</b> Sub-optimal illuminance (&lt; 4 hours/day) leading to reduced photosynthetic assimilation and potential etiolation.", bullet_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("&bull; <b>Group D (Temperature Stress):</b> High or freezing temperatures triggering enzymatic inactivation.", bullet_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Technical Architecture", h2_style))
    story.append(Paragraph("The desktop system provides six modular components:", body_style))
    story.append(Spacer(1, 6))

    arch_points = [
        "<b>1. Database &amp; Authentication Manager:</b> Secure parameter configuration dialog connecting Python to the MySQL daemon with automatic database/schema creation.",
        "<b>2. Dashboard Overview:</b> Real-time summary statistics, experiment guidelines, biology syllabus correlation, and recent experimental batches.",
        "<b>3. Plant Registry Module:</b> Registration of experimental test subjects, biological taxonomy, and control vs. variable group designations stored in the Plants relation.",
        "<b>4. Observation Logger:</b> Numerical logging of observational days, stem height (cm), leaf count, diurnal light exposure, thermal conditions, and soil moisture grades.",
        "<b>5. Rule-Based Stress Detective:</b> Transparent if-then deduction engine detecting physiological anomalies (e.g., water deficit wilting, root hypoxia from overwatering, photosynthetic deficits, and severe growth decelerations) with educational citations.",
        "<b>6. Side-by-Side Multi-Plant Comparative Analytics:</b> Integrated Matplotlib visualization showing comparative average growth rate bar charts (cm/day), total vegetative height gain, overlaid day-by-day growth curves, and automated synthesis rankings."
    ]
    for pt in arch_points:
        story.append(Paragraph(pt, bullet_style))
        story.append(Spacer(1, 5))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: LIST OF FUNCTIONS
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("List of Functions", h1_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("The table below lists the library, module, and custom functions used in the project along with their purposes and functionality:", body_style))
    story.append(Spacer(1, 10))

    func_table_data = [
        [Paragraph("<b>Sr. No.</b>", body_style), Paragraph("<b>Name of Function</b>", body_style), Paragraph("<b>Library / Module</b>", body_style), Paragraph("<b>Purpose &amp; Functionality</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("mysql.connector.connect()", body_style), Paragraph("mysql.connector", body_style), Paragraph("Establishes a TCP connection session between Python and MySQL server.", body_style)],
        [Paragraph("2", body_style), Paragraph("cursor()", body_style), Paragraph("mysql.connector", body_style), Paragraph("Creates an active cursor object configured for query dispatch.", body_style)],
        [Paragraph("3", body_style), Paragraph("execute()", body_style), Paragraph("mysql.connector", body_style), Paragraph("Compiles and executes SQL DDL/DML statements.", body_style)],
        [Paragraph("4", body_style), Paragraph("fetchall()", body_style), Paragraph("mysql.connector", body_style), Paragraph("Retrieves all resultant records from SELECT query.", body_style)],
        [Paragraph("5", body_style), Paragraph("commit()", body_style), Paragraph("mysql.connector", body_style), Paragraph("Permanently saves transaction modifications executed on DB.", body_style)],
        [Paragraph("6", body_style), Paragraph("DatabaseManager.connect()", body_style), Paragraph("Custom Class", body_style), Paragraph("Authenticates, initializes database, and creates tables.", body_style)],
        [Paragraph("7", body_style), Paragraph("DatabaseManager.add_plant()", body_style), Paragraph("Custom Class", body_style), Paragraph("Inserts a new plant record into MySQL Plants table.", body_style)],
        [Paragraph("8", body_style), Paragraph("DatabaseManager.add_observation()", body_style), Paragraph("Custom Class", body_style), Paragraph("Inserts observation record into MySQL Observations table.", body_style)],
        [Paragraph("9", body_style), Paragraph("AnalysisEngine.growth_rate()", body_style), Paragraph("Custom Class", body_style), Paragraph("Calculates growth rate: (H2 - H1) / (t2 - t1).", body_style)],
        [Paragraph("10", body_style), Paragraph("AnalysisEngine.detect_stress()", body_style), Paragraph("Custom Class", body_style), Paragraph("Applies biological rules to detect stress conditions.", body_style)],
        [Paragraph("11", body_style), Paragraph("ttk.Style()", body_style), Paragraph("tkinter.ttk", body_style), Paragraph("Creates and manages widget appearance styles.", body_style)],
        [Paragraph("12", body_style), Paragraph("pack() / grid()", body_style), Paragraph("tkinter", body_style), Paragraph("Geometry managers placing and aligning UI widgets.", body_style)],
        [Paragraph("13", body_style), Paragraph("FigureCanvasTkAgg()", body_style), Paragraph("matplotlib.backends", body_style), Paragraph("Embeds Matplotlib scientific plots inside Tkinter frames.", body_style)]
    ]
    t_func = Table(func_table_data, colWidths=[45, 175, 115, 185])
    t_func.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#2E4A2E")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#AAAAAA")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EAEFEA")),
        ('ALIGN', (0,0), (0,-1), 'CENTER')
    ]))
    story.append(t_func)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: LIST OF LIBRARIES
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("List of Libraries", h1_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("The following software libraries and modules were used in developing the Plant Stress Detective system:", body_style))
    story.append(Spacer(1, 12))

    lib_table_data = [
        [Paragraph("<b>Sr. No.</b>", body_style), Paragraph("<b>Library Name</b>", body_style), Paragraph("<b>Module / Import Alias</b>", body_style), Paragraph("<b>Purpose in Project</b>", body_style)],
        [Paragraph("1", body_style), Paragraph("Tkinter", body_style), Paragraph("tkinter, ttk", body_style), Paragraph("Primary GUI engine used to construct the desktop window, layout navigation panels, input forms, and Treeviews.", body_style)],
        [Paragraph("2", body_style), Paragraph("Tkinter Dialogs", body_style), Paragraph("tkinter.messagebox, font", body_style), Paragraph("Provides native modal dialogue windows for notifications, validation warnings, and confirmation popups.", body_style)],
        [Paragraph("3", body_style), Paragraph("MySQL Connector", body_style), Paragraph("mysql.connector, Error", body_style), Paragraph("Database driver enabling standard Python Database API v2.0 communication with the MySQL server.", body_style)],
        [Paragraph("4", body_style), Paragraph("Matplotlib", body_style), Paragraph("matplotlib, pyplot", body_style), Paragraph("Data visualization library employed to plot comparative vegetative growth rates and overlaid growth trajectories.", body_style)],
        [Paragraph("5", body_style), Paragraph("Matplotlib Tk Backend", body_style), Paragraph("matplotlib.backends.backend_tkagg", body_style), Paragraph("Provides FigureCanvasTkAgg to embed Matplotlib figures directly onto Tkinter frames.", body_style)],
        [Paragraph("6", body_style), Paragraph("Datetime", body_style), Paragraph("datetime", body_style), Paragraph("Handles system clock ticks and observation timestamps.", body_style)]
    ]
    t_lib = Table(lib_table_data, colWidths=[45, 115, 140, 220])
    t_lib.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#2E4A2E")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#AAAAAA")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EAEFEA")),
        ('ALIGN', (0,0), (0,-1), 'CENTER')
    ]))
    story.append(t_lib)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8+: SOURCE CODE (Clean, Increased Font Size 8.5pt)
    # =========================================================================
    for idx, i in enumerate(range(0, len(code_lines), lines_per_code_page)):
        page_num_code = idx + 1
        story.append(Paragraph(f"Source Code (main.py) - Part {page_num_code}", ParagraphStyle('CodeHeading', parent=h1_style, fontSize=14, spaceAfter=8)))
        chunk = "\n".join(code_lines[i:i+lines_per_code_page])
        story.append(Preformatted(chunk, code_style))
        story.append(PageBreak())

    # =========================================================================
    # OUTPUT AND DATABASE VERIFICATION
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Output and Database Verification", h1_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("The application execution sequence adheres to the following step-by-step graphical workflow:", body_style))
    story.append(Spacer(1, 8))

    workflow_ascii = """+-----------------------------------------------------------------------+
| STEP 1: DATABASE AUTHENTICATION DIALOG (LoginWindow)                  |
| - Prompts for MySQL Host, Port, User, Password, Database Name.        |
| - Automatically creates database 'plant_stress_db' and tables.        |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 2: CENTRAL OVERVIEW DASHBOARD (_tab_dashboard)                   |
| - Displays live metric cards: Total Plants, Total Observations, Date.  |
| - Summarizes CBSE Class 12 Biology theoretical topics.                |
| - Lists recently registered experimental plants in a data grid.       |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 3: REGISTER EXPERIMENTAL SPECIMENS (_tab_add_plant)              |
| - User specifies Plant ID, Botanical/Common Species, Experiment Group |
|   (Control, Less Water, Excess Water, Low Light, High Temp).          |
| - Direct interactive table with Delete Plant capabilities.            |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 4: LOG OBSERVATIONS (_tab_add_obs)                               |
| - User inputs Day number, Height (cm), Leaf count, Temperature,       |
|   Photoperiod (hrs/day), Water regime, and Soil moisture condition.   |
| - Validates numerical limits and updates the 'Observations' table.    |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 5: TABULAR OBSERVATION REVIEW (_tab_view_data)                   |
| - Full scrollable Treeview showing all recorded observations.         |
| - Single-click row deletion for outlier / mistake pruning.            |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 6: EDUCATIONAL STRESS CLUES (_tab_stress)                        |
| - Evaluates rule engine against the selected plant's dataset.         |
| - Outputs Stress Flags (Water Stress, Low Light, Heat Stress, etc.)   |
| - Displays mathematical average growth velocity and deduction notes.  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
| STEP 7: MULTI-PLANT COMPARATIVE ANALYTICS (_tab_compare)              |
| - Embeds 3 Matplotlib plots:                                          |
|   1. Bar chart: Average Growth Rate (cm/day) per plant.               |
|   2. Bar chart: Total Vegetative Height Gain (cm).                    |
|   3. Line plot: Overlaid multi-plant day-by-day growth curves.        |
| - Outputs text ranking from fastest to slowest growth with margins.   |
+-----------------------------------------------------------------------+"""

    story.append(Preformatted(workflow_ascii, ParagraphStyle('AsciiStyle', fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1A1A1A"))))
    story.append(PageBreak())

    story.append(Spacer(1, 10))
    story.append(Paragraph("Output and Database Verification (Contd.)", h1_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Sample Analytical Run Output (Simulated Experiment Data)", h2_style))
    story.append(Spacer(1, 6))

    sample_output_ascii = """=======================================================
AUTOMATIC EXPERIMENT SUMMARY
=======================================================
Average Growth Rate Ranking (highest to lowest):
1. Plant A (Regular Water) => 0.6857 cm/day
2. Plant C (Low Light) => 0.3143 cm/day
3. Plant B (Less Water Stress) => 0.1857 cm/day

Plant A grew fastest; Plant B grew slowest.
Difference in average growth rate: 0.5000 cm/day

Stress Flags per Plant:
* Plant A: None
* Plant B: Water Stress
* Plant C: Low-Light Stress

NOTE: These are educational pattern observations.
Real causation requires controlled experiments."""

    story.append(Preformatted(sample_output_ascii, ParagraphStyle('SampleStyle', fontName='Courier', fontSize=8.5, leading=11, textColor=colors.HexColor("#004400"))))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Database Verification (MySQL Relations)", h2_style))
    story.append(Spacer(1, 6))

    db_schema_text = """TABLE: Plants
+------------+--------------+------+-----+-------------------+----------------+
| Field      | Type         | Null | Key | Default           | Extra          |
+------------+--------------+------+-----+-------------------+----------------+
| plant_id   | int          | NO   | PRI | NULL              | auto_increment |
| plant_name | varchar(100) | NO   |     | NULL              |                |
| species    | varchar(100) | YES  |     | Green Gram (Moong)|                |
| grp        | varchar(50)  | NO   |     | NULL              |                |
| created_at | datetime     | YES  |     | CURRENT_TIMESTAMP |                |
+------------+--------------+------+-----+-------------------+----------------+

TABLE: Observations
+---------------+-------------+------+-----+-------------------+----------------+
| Field         | Type        | Null | Key | Default           | Extra          |
+---------------+-------------+------+-----+-------------------+----------------+
| obs_id        | int         | NO   | PRI | NULL              | auto_increment |
| plant_id      | int         | NO   | MUL | NULL              |                |
| obs_day       | int         | NO   |     | NULL              |                |
| height_cm     | float       | NO   |     | NULL              |                |
| leaf_count    | int         | NO   |     | NULL              |                |
| temperature   | float       | YES  |     | 25.0              |                |
| light_hours   | float       | YES  |     | 8.0               |                |
| watering      | varchar(20) | YES  |     | Regular           |                |
| soil_moisture | varchar(20) | YES  |     | Moist             |                |
| notes         | text        | YES  |     | NULL              |                |
| recorded_at   | datetime    | YES  |     | CURRENT_TIMESTAMP |                |
+---------------+-------------+------+-----+-------------------+----------------+"""

    story.append(Preformatted(db_schema_text, ParagraphStyle('DbStyle', fontName='Courier', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#1A1A1A"))))
    story.append(PageBreak())

    # =========================================================================
    # BIBLIOGRAPHY
    # =========================================================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("Bibliography", h1_style))
    story.append(Spacer(1, 15))

    bib_items = [
        "1. <b>NCERT Biology Class XII Textbook</b> - Unit IV: Plant Physiology, Photosynthesis in Higher Plants, and Plant Growth &amp; Development.",
        "2. <b>Computer Science with Python by Sumita Arora (Class XII)</b> - Dhanpat Rai &amp; Co. (Modules on Tkinter GUI, File Handling, and MySQL Connectivity).",
        "3. <b>Python Official Documentation (v3.13)</b> - <i>https://docs.python.org/3/</i> (Standard library, <code>tkinter</code>, <code>datetime</code>).",
        "4. <b>MySQL Connector/Python Developer Guide</b> - Oracle Corporation, <i>https://dev.mysql.com/doc/connector-python/en/</i>.",
        "5. <b>Matplotlib: Visualization with Python</b> - John D. Hunter et al., <i>https://matplotlib.org/</i> (Embedding in Tkinter with <code>FigureCanvasTkAgg</code>).",
        "6. <b>Blackman, F.F. (1905)</b> - <i>Optima and Limiting Factors</i>, Annals of Botany (Biological foundation for physiological growth limitations)."
    ]

    for item in bib_items:
        story.append(Paragraph(item, body_style))
        story.append(Spacer(1, 10))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("New updated PDF generated successfully!")

if __name__ == "__main__":
    generate_report()
