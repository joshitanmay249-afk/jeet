# =============================================================================
#  PLANT STRESS DETECTIVE
#  Class 12 Biology + Python + MySQL + Tkinter Project
#  Author: Student Project | Technologies: Python 3, Tkinter, MySQL, Matplotlib
# =============================================================================

import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import mysql.connector
from mysql.connector import Error
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import re

# -----------------------------------------------------------------------------
#  COLOUR PALETTE  (earthy greens / biology theme)
# -----------------------------------------------------------------------------
BG_MAIN    = "#1B2B1B"   # dark green-black (window background)
BG_PANEL   = "#243324"   # panel background
BG_CARD    = "#2E4A2E"   # card / frame background
BG_ENTRY   = "#1E2E1E"   # entry field background
FG_MAIN    = "#D4E8C2"   # main text (light green)
FG_ACCENT  = "#7EC850"   # accent green
FG_WARN    = "#F4A261"   # warning orange
FG_DANGER  = "#E76F51"   # danger red
FG_INFO    = "#90CAF9"   # info blue
FG_MUTED   = "#7A9B6A"   # muted text
BTN_GREEN  = "#4CAF50"
BTN_HOVER  = "#66BB6A"
BTN_BLUE   = "#1565C0"
BTN_RED    = "#C62828"
BORDER     = "#3E6B3E"

# -----------------------------------------------------------------------------
#  DATABASE MANAGER
# -----------------------------------------------------------------------------
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host     = host
        self.user     = user
        self.password = password
        self.database = database
        self.conn     = None

    # -- connect --------------------------------------------------------------
    def connect(self):
        try:
            # first connect without DB to create it if missing
            temp = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password
            )
            cur = temp.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{self.database}`")
            temp.close()

            self.conn = mysql.connector.connect(
                host=self.host, user=self.user,
                password=self.password, database=self.database
            )
            self._create_tables()
            return True
        except Error as e:
            raise ConnectionError(str(e))

    # -- schema ----------------------------------------------------------------
    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Plants (
                plant_id    INT AUTO_INCREMENT PRIMARY KEY,
                plant_name  VARCHAR(100) NOT NULL,
                species     VARCHAR(100) DEFAULT 'Green Gram (Moong)',
                grp         VARCHAR(50)  NOT NULL
                            COMMENT 'Regular Water / Less Water / Low Light / Excess Water',
                created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Observations (
                obs_id        INT AUTO_INCREMENT PRIMARY KEY,
                plant_id      INT NOT NULL,
                obs_day       INT NOT NULL,
                height_cm     FLOAT NOT NULL,
                leaf_count    INT   NOT NULL,
                temperature   FLOAT DEFAULT 25.0,
                light_hours   FLOAT DEFAULT 8.0,
                watering      VARCHAR(20) DEFAULT 'Regular'
                              COMMENT 'Regular / Less / Excess',
                soil_moisture VARCHAR(20) DEFAULT 'Moist'
                              COMMENT 'Dry / Moist / Wet',
                notes         TEXT,
                recorded_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
                    ON DELETE CASCADE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS AnalysisResults (
                result_id      INT AUTO_INCREMENT PRIMARY KEY,
                plant_id       INT NOT NULL,
                growth_rate    FLOAT,
                avg_growth     FLOAT,
                stress_flag    VARCHAR(50),
                summary_text   TEXT,
                analysed_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plant_id) REFERENCES Plants(plant_id)
                    ON DELETE CASCADE
            )
        """)
        self.conn.commit()
        cur.close()

    # -- plants ----------------------------------------------------------------
    def add_plant(self, name, species, group):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO Plants (plant_name, species, grp) VALUES (%s,%s,%s)",
            (name, species, group)
        )
        self.conn.commit()
        pid = cur.lastrowid
        cur.close()
        return pid

    def get_plants(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM Plants ORDER BY created_at DESC")
        rows = cur.fetchall()
        cur.close()
        return rows

    def delete_plant(self, plant_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Plants WHERE plant_id=%s", (plant_id,))
        self.conn.commit()
        cur.close()

    # -- observations ----------------------------------------------------------
    def add_observation(self, plant_id, day, height, leaves,
                        temp, light, watering, soil, notes=""):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO Observations
              (plant_id, obs_day, height_cm, leaf_count, temperature,
               light_hours, watering, soil_moisture, notes)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (plant_id, day, height, leaves, temp, light, watering, soil, notes))
        self.conn.commit()
        cur.close()

    def get_observations(self, plant_id=None):
        cur = self.conn.cursor(dictionary=True)
        if plant_id:
            cur.execute("""
                SELECT o.*, p.plant_name, p.grp
                FROM Observations o JOIN Plants p ON o.plant_id=p.plant_id
                WHERE o.plant_id=%s ORDER BY o.obs_day
            """, (plant_id,))
        else:
            cur.execute("""
                SELECT o.*, p.plant_name, p.grp
                FROM Observations o JOIN Plants p ON o.plant_id=p.plant_id
                ORDER BY p.plant_name, o.obs_day
            """)
        rows = cur.fetchall()
        cur.close()
        return rows

    def delete_observation(self, obs_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM Observations WHERE obs_id=%s", (obs_id,))
        self.conn.commit()
        cur.close()

    # -- analysis results ------------------------------------------------------
    def save_analysis(self, plant_id, growth_rate, avg_growth,
                      stress_flag, summary):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO AnalysisResults
              (plant_id, growth_rate, avg_growth, stress_flag, summary_text)
            VALUES (%s,%s,%s,%s,%s)
        """, (plant_id, growth_rate, avg_growth, stress_flag, summary))
        self.conn.commit()
        cur.close()

    def get_analysis_history(self):
        cur = self.conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*, p.plant_name, p.grp
            FROM AnalysisResults a JOIN Plants p ON a.plant_id=p.plant_id
            ORDER BY a.analysed_at DESC LIMIT 50
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

# -----------------------------------------------------------------------------
#  GROWTH / STRESS ANALYSIS LOGIC
# -----------------------------------------------------------------------------
class AnalysisEngine:
    # growth rate between two consecutive observations
    @staticmethod
    def growth_rate(h1, h2, t1, t2):
        dt = t2 - t1
        if dt == 0:
            return 0.0
        return round((h2 - h1) / dt, 4)

    # list of daily growth rates for a plant's observations
    @staticmethod
    def all_growth_rates(obs_list):
        rates = []
        for i in range(1, len(obs_list)):
            r = AnalysisEngine.growth_rate(
                obs_list[i-1]["height_cm"], obs_list[i]["height_cm"],
                obs_list[i-1]["obs_day"],   obs_list[i]["obs_day"]
            )
            rates.append(r)
        return rates

    @staticmethod
    def average_growth(obs_list):
        if len(obs_list) < 2:
            return 0.0
        total_h = obs_list[-1]["height_cm"] - obs_list[0]["height_cm"]
        total_t = obs_list[-1]["obs_day"]   - obs_list[0]["obs_day"]
        return round(total_h / total_t, 4) if total_t else 0.0

    # rule-based stress detection
    @staticmethod
    def detect_stress(obs_list):
        flags  = []
        detail = []

        if not obs_list:
            return "None", ["No observations to analyse."]

        for o in obs_list:
            # water stress (less watering + dry soil)
            if o["watering"] == "Less" and o["soil_moisture"] == "Dry":
                flags.append("WaterStress")
                detail.append(
                    f"Day {o['obs_day']}: Less watering + Dry soil - "
                    "consistent with possible water stress (wilting, reduced turgor)."
                )
            # excess water warning
            if o["watering"] == "Excess" and o["soil_moisture"] == "Wet":
                flags.append("ExcessWater")
                detail.append(
                    f"Day {o['obs_day']}: Excess water + Wet soil - "
                    "risk of root hypoxia / waterlogging."
                )
            # low light
            if o["light_hours"] is not None and o["light_hours"] < 4:
                flags.append("LowLight")
                detail.append(
                    f"Day {o['obs_day']}: Only {o['light_hours']}h light - "
                    "below 4h may limit photosynthesis (etiolation risk)."
                )
            # heat stress
            if o["temperature"] is not None and o["temperature"] > 38:
                flags.append("HeatStress")
                detail.append(
                    f"Day {o['obs_day']}: Temperature {o['temperature']}C - "
                    "above 38C may denature enzymes, reduce photosynthesis."
                )
            # cold stress
            if o["temperature"] is not None and o["temperature"] < 10:
                flags.append("ColdStress")
                detail.append(
                    f"Day {o['obs_day']}: Temperature {o['temperature']}C - "
                    "below 10C may slow metabolic activity."
                )

        # growth slow-down check
        rates = AnalysisEngine.all_growth_rates(obs_list)
        if rates and len(rates) >= 2:
            avg_r = sum(rates) / len(rates)
            for i, r in enumerate(rates):
                if r < avg_r * 0.4 and avg_r > 0:
                    day = obs_list[i+1]["obs_day"]
                    detail.append(
                        f"Day {day}: Growth rate ({r:.3f} cm/day) is 60% below "
                        f"average ({avg_r:.3f} cm/day) - investigate conditions."
                    )

        primary = "None"
        if "WaterStress"  in flags: primary = "Water Stress"
        if "LowLight"     in flags: primary = "Low-Light Stress"
        if "HeatStress"   in flags: primary = "Heat Stress"
        if "ColdStress"   in flags: primary = "Cold Stress"
        if "ExcessWater"  in flags: primary = "Excess Water / Waterlogging"
        if len(set(flags)) > 1:     primary  = "Multiple Stressors"

        if not detail:
            detail = ["No stress indicators detected based on entered data."]
        return primary, detail

    # automatic experiment summary
    @staticmethod
    def experiment_summary(plants_data: dict):
        lines = []
        rankings = []
        for name, obs in plants_data.items():
            avg = AnalysisEngine.average_growth(obs)
            rankings.append((name, avg))

        rankings.sort(key=lambda x: x[1], reverse=True)
        lines.append("=" * 55)
        lines.append("   AUTOMATIC EXPERIMENT SUMMARY")
        lines.append("=" * 55)
        lines.append("")
        lines.append("Average Growth Rate Ranking (highest to lowest):")
        for rank, (name, avg) in enumerate(rankings, 1):
            lines.append(f"   {rank}. {name}  =>  {avg:.4f} cm/day")

        lines.append("")
        if len(rankings) >= 2:
            best  = rankings[0]
            worst = rankings[-1]
            diff  = round(best[1] - worst[1], 4)
            lines.append(f"{best[0]} grew fastest; {worst[0]} grew slowest.")
            lines.append(f"Difference in average growth rate: {diff:.4f} cm/day")

        lines.append("")
        lines.append("Stress Flags per Plant:")
        for name, obs in plants_data.items():
            flag, _ = AnalysisEngine.detect_stress(obs)
            lines.append(f"   * {name}: {flag}")

        lines.append("")
        lines.append("NOTE: These are educational pattern observations.")
        lines.append("Real causation requires controlled experiments.")
        return lines

    # what-if analysis
    @staticmethod
    def what_if(base_height, days, watering, light_hours, temperature):
        rate = 0.6   # base growth rate cm/day (Green Gram typical)

        if watering == "Less":    rate *= 0.55
        if watering == "Excess":  rate *= 0.75
        if light_hours < 4:       rate *= 0.50
        if light_hours > 10:      rate *= 1.10
        if temperature > 38:      rate *= 0.60
        if temperature < 10:      rate *= 0.40
        if 20 <= temperature <= 32: rate *= 1.05

        est = round(base_height + rate * days, 2)
        commentary = []
        commentary.append(f"Estimated height after {days} days: {est} cm")
        commentary.append(f"Growth rate under these conditions: {rate:.3f} cm/day")
        if watering == "Less":
            commentary.append("WARNING: Less water => reduced turgor, possible wilting")
        if light_hours < 4:
            commentary.append("WARNING: Low light (<4h) => reduced photosynthesis, slower growth")
        if temperature > 38:
            commentary.append("WARNING: High temperature => enzyme stress, reduced growth")
        if temperature < 10:
            commentary.append("WARNING: Low temperature => slow metabolic rate")
        if watering == "Regular" and 4 <= light_hours <= 10 and 20 <= temperature <= 32:
            commentary.append("GOOD: Ideal conditions => optimal growth expected")
        return est, commentary


# -----------------------------------------------------------------------------
#  REUSABLE UI HELPERS
# -----------------------------------------------------------------------------
def styled_label(parent, text, size=11, bold=False, color=FG_MAIN, **kw):
    weight = "bold" if bold else "normal"
    return tk.Label(parent, text=text,
                    font=("Segoe UI", size, weight),
                    fg=color, bg=parent["bg"], **kw)

def styled_entry(parent, textvariable=None, width=22):
    e = tk.Entry(parent, textvariable=textvariable, width=width,
                 bg=BG_ENTRY, fg=FG_MAIN, insertbackground=FG_MAIN,
                 relief="flat", highlightthickness=1,
                 highlightcolor=FG_ACCENT, highlightbackground=BORDER,
                 font=("Segoe UI", 11))
    return e

def styled_combo(parent, textvariable, values, width=20):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Dark.TCombobox",
                    fieldbackground=BG_ENTRY, background=BG_CARD,
                    foreground=FG_MAIN, selectbackground=BG_CARD,
                    selectforeground=FG_ACCENT, bordercolor=BORDER,
                    arrowcolor=FG_ACCENT)
    c = ttk.Combobox(parent, textvariable=textvariable, values=values,
                     width=width, style="Dark.TCombobox",
                     font=("Segoe UI", 11), state="readonly")
    return c

def styled_button(parent, text, command, color=BTN_GREEN,
                  fg="white", width=18, **kw):
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg=fg, activebackground=BTN_HOVER,
                    activeforeground="white",
                    font=("Segoe UI", 10, "bold"),
                    relief="flat", cursor="hand2",
                    padx=10, pady=6, width=width, **kw)
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=BG_CARD, relief="flat",
                    highlightthickness=1, highlightbackground=BORDER, **kw)

def section_header(parent, title):
    f = tk.Frame(parent, bg=BG_PANEL)
    tk.Label(f, text=title,
             font=("Segoe UI", 15, "bold"),
             fg=FG_ACCENT, bg=BG_PANEL).pack(anchor="w", pady=(0, 2))
    tk.Frame(f, bg=FG_ACCENT, height=2).pack(fill="x")
    return f

def scrollable_text(parent, height=12, width=70):
    frame = tk.Frame(parent, bg=BG_CARD)
    sb    = tk.Scrollbar(frame)
    txt   = tk.Text(frame, height=height, width=width,
                    bg=BG_ENTRY, fg=FG_MAIN, font=("Consolas", 10),
                    relief="flat", wrap="word",
                    yscrollcommand=sb.set, insertbackground=FG_MAIN)
    sb.config(command=txt.yview)
    txt.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return frame, txt


# -----------------------------------------------------------------------------
#  LOGIN / CONNECTION WINDOW
# -----------------------------------------------------------------------------
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Plant Stress Detective - MySQL Login")
        self.geometry("480x440")
        self.resizable(False, False)
        self.configure(bg=BG_MAIN)
        self.db = None
        self._build_ui()
        self.eval("tk::PlaceWindow . center")

    def _build_ui(self):
        # logo banner
        banner = tk.Frame(self, bg="#2E5F2E", pady=14)
        banner.pack(fill="x")
        tk.Label(banner, text="  Plant Stress Detective",
                 font=("Segoe UI", 18, "bold"),
                 fg=FG_ACCENT, bg="#2E5F2E").pack()
        tk.Label(banner, text="Class 12 Biology  |  Python  |  MySQL  |  Tkinter",
                 font=("Segoe UI", 9),
                 fg=FG_MUTED, bg="#2E5F2E").pack()

        body = card_frame(self, padx=30, pady=20)
        body.pack(expand=True, fill="both", padx=30, pady=20)

        styled_label(body, "MySQL Connection", 13, bold=True,
                     color=FG_ACCENT).grid(row=0, columnspan=2,
                                           pady=(0, 14), sticky="w")

        fields = [
            ("Host",     "localhost"),
            ("Port",     "3306"),
            ("User",     "root"),
            ("Password", ""),
            ("Database", "plant_stress_db"),
        ]
        self.vars = {}
        for i, (label, default) in enumerate(fields, start=1):
            styled_label(body, label + ":", 10,
                         color=FG_MUTED).grid(row=i, column=0,
                                              sticky="e", padx=(0, 8),
                                              pady=4)
            var = tk.StringVar(value=default)
            self.vars[label] = var
            show = "*" if label == "Password" else ""
            e = styled_entry(body, textvariable=var, width=24)
            e.config(show=show)
            e.grid(row=i, column=1, pady=4, sticky="w")

        btn_frame = tk.Frame(body, bg=BG_CARD)
        btn_frame.grid(row=len(fields)+1, columnspan=2, pady=18)
        styled_button(btn_frame, "Connect & Launch",
                      self._connect, width=22).pack()

        self.status_var = tk.StringVar()
        tk.Label(body, textvariable=self.status_var,
                 font=("Segoe UI", 9), fg=FG_WARN,
                 bg=BG_CARD, wraplength=360).grid(
                     row=len(fields)+2, columnspan=2)

    def _connect(self):
        v    = self.vars
        host = v["Host"].get().strip()
        user = v["User"].get().strip()
        pwd  = v["Password"].get()
        db   = v["Database"].get().strip()

        if not host or not user or not db:
            self.status_var.set("Host, User and Database are required.")
            return

        self.status_var.set("Connecting...")
        self.update()
        try:
            mgr = DatabaseManager(host, user, pwd, db)
            mgr.connect()
            self.db = mgr
            self.destroy()
        except Exception as e:
            self.status_var.set(f"Error: {e}")


# -----------------------------------------------------------------------------
#  MAIN APPLICATION
# -----------------------------------------------------------------------------
class PlantStressApp(tk.Tk):
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db  = db
        self.eng = AnalysisEngine()

        self.title("Plant Stress Detective - Class 12 Biology Project")
        self.geometry("1200x750")
        self.minsize(900, 600)
        self.configure(bg=BG_MAIN)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._build_header()
        self._build_nav()
        self._build_content_area()
        self._show_tab("dashboard")
        self.eval("tk::PlaceWindow . center")

    # -- header ----------------------------------------------------------------
    def _build_header(self):
        hdr = tk.Frame(self, bg="#1D3D1D", pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="  Plant Stress Detective",
                 font=("Segoe UI", 20, "bold"),
                 fg=FG_ACCENT, bg="#1D3D1D").pack(side="left", padx=20)
        self.clock_var = tk.StringVar()
        tk.Label(hdr, textvariable=self.clock_var,
                 font=("Segoe UI", 10), fg=FG_MUTED,
                 bg="#1D3D1D").pack(side="right", padx=20)
        self._tick()

    def _tick(self):
        self.clock_var.set(
            datetime.datetime.now().strftime("  %d %b %Y   %H:%M:%S")
        )
        self.after(1000, self._tick)

    # -- left nav --------------------------------------------------------------
    def _build_nav(self):
        self.nav_frame = tk.Frame(self, bg=BG_PANEL, width=200)
        self.nav_frame.pack(side="left", fill="y")
        self.nav_frame.pack_propagate(False)

        tk.Label(self.nav_frame, text="MENU",
                 font=("Segoe UI", 9, "bold"),
                 fg=FG_MUTED, bg=BG_PANEL).pack(pady=(18, 4))

        self.nav_buttons = {}
        nav_items = [
            ("dashboard",  "  Dashboard"),
            ("add_plant",  "  Add Plant"),
            ("add_obs",    "  Add Observation"),
            ("view_data",  "  View Data"),
            ("stress",     "  Stress Clues"),
            ("compare",    "  Compare Plants"),
        ]
        for key, label in nav_items:
            btn = tk.Button(
                self.nav_frame, text=label,
                font=("Segoe UI", 10), fg=FG_MAIN,
                bg=BG_PANEL, activebackground=BG_CARD,
                activeforeground=FG_ACCENT,
                relief="flat", anchor="w", padx=18, pady=8,
                cursor="hand2",
                command=lambda k=key: self._show_tab(k)
            )
            btn.pack(fill="x")
            self.nav_buttons[key] = btn

        tk.Frame(self.nav_frame, bg=BORDER, height=1).pack(
            fill="x", pady=12, padx=10)
        styled_button(self.nav_frame, "  Quit",
                      self._on_close, color=BTN_RED,
                      width=14).pack(pady=4)

    def _highlight_nav(self, key):
        for k, b in self.nav_buttons.items():
            if k == key:
                b.config(bg=BG_CARD, fg=FG_ACCENT,
                         font=("Segoe UI", 10, "bold"))
            else:
                b.config(bg=BG_PANEL, fg=FG_MAIN,
                         font=("Segoe UI", 10, "normal"))

    # -- content area ----------------------------------------------------------
    def _build_content_area(self):
        self.content = tk.Frame(self, bg=BG_PANEL)
        self.content.pack(side="left", fill="both", expand=True)
        self.frames = {}

    def _show_tab(self, key):
        for f in self.frames.values():
            f.pack_forget()
        if key in self.frames:
            del self.frames[key]

        frame = tk.Frame(self.content, bg=BG_PANEL)
        frame.pack(fill="both", expand=True, padx=16, pady=12)
        self.frames[key] = frame
        self._highlight_nav(key)

        builders = {
            "dashboard":  self._tab_dashboard,
            "add_plant":  self._tab_add_plant,
            "add_obs":    self._tab_add_obs,
            "view_data":  self._tab_view_data,
            "stress":     self._tab_stress,
            "compare":    self._tab_compare,
        }
        builders[key](frame)

    # ==========================================================================
    #  TAB 1 : DASHBOARD
    # ==========================================================================
    def _tab_dashboard(self, f):
        section_header(f, "  Dashboard - Overview").pack(
            fill="x", pady=(0, 14))

        plants = self.db.get_plants()
        obs    = self.db.get_observations()

        # stat cards
        cards_data = [
            ("Total Plants",   str(len(plants)), FG_ACCENT),
            ("Observations",   str(len(obs)),    FG_INFO),
            ("Today",
             datetime.date.today().strftime("%d %b %Y"), FG_WARN),
        ]
        row = tk.Frame(f, bg=BG_PANEL)
        row.pack(fill="x", pady=(0, 16))
        for label, val, color in cards_data:
            c = card_frame(row, padx=20, pady=14)
            c.pack(side="left", padx=8, fill="y")
            tk.Label(c, text=val, font=("Segoe UI", 28, "bold"),
                     fg=color, bg=BG_CARD).pack()
            tk.Label(c, text=label, font=("Segoe UI", 10),
                     fg=FG_MUTED, bg=BG_CARD).pack()

        # quick guide card
        info = card_frame(f, padx=16, pady=14)
        info.pack(fill="x", pady=(0, 10))
        styled_label(info, "Quick Guide", 11, bold=True,
                     color=FG_ACCENT).pack(anchor="w")
        tips = [
            "1.  Go to 'Add Plant' to register your plant groups (A, B, C...).",
            "2.  Use 'Add Observation' to record daily height, leaves & conditions.",
            "3.  'Growth Analysis' draws timeline graphs per plant.",
            "4.  'Stress Clues' highlights possible stress based on your data.",
            "5.  'Compare Plants' shows side-by-side bar charts + overlay.",
            "6.  'What-If Lab' lets you simulate different growing conditions.",
        ]
        for t in tips:
            styled_label(info, t, 10, color=FG_MAIN).pack(anchor="w", pady=2)

        # biology link card
        bio = card_frame(f, padx=16, pady=12)
        bio.pack(fill="x", pady=(0, 10))
        styled_label(bio, "Class 12 Biology Link", 11, bold=True,
                     color=FG_ACCENT).pack(anchor="w")
        concepts = [
            "Photosynthesis & light availability (Chapter: Photosynthesis in Higher Plants)",
            "Water availability & plant physiology (Chapter: Plant Growth & Development)",
            "Environmental factors affecting growth rate",
            "Scientific observation, experimental controls, and data interpretation",
        ]
        for c in concepts:
            styled_label(bio, "  * " + c, 10, color=FG_MUTED).pack(anchor="w")

        # recent plants table
        if plants:
            styled_label(f, "Recently Added Plants", 11, bold=True,
                         color=FG_ACCENT).pack(anchor="w", pady=(10, 4))
            cols = ("ID", "Name", "Species", "Group", "Added")
            tree = ttk.Treeview(f, columns=cols, show="headings", height=5)
            self._style_tree(tree, cols)
            for p in plants[:8]:
                added = p["created_at"]
                if isinstance(added, datetime.datetime):
                    added = added.strftime("%d-%b-%Y")
                tree.insert("", "end", values=(
                    p["plant_id"], p["plant_name"],
                    p["species"], p["grp"], added
                ))
            tree.pack(fill="x")

    # ==========================================================================
    #  TAB 2 : ADD PLANT
    # ==========================================================================
    def _tab_add_plant(self, f):
        section_header(f, "  Add Plant / Experiment Group").pack(
            fill="x", pady=(0, 14))

        left = card_frame(f, padx=24, pady=20)
        left.pack(side="left", fill="y")

        styled_label(left, "Plant Details", 12, bold=True,
                     color=FG_ACCENT).grid(row=0, columnspan=2,
                                           pady=(0, 12), sticky="w")

        self.pname_var  = tk.StringVar()
        self.pspec_var  = tk.StringVar(value="Green Gram (Moong)")
        self.pgroup_var = tk.StringVar(value="Regular Water")

        styled_label(left, "Plant Name / ID:", 10,
                     color=FG_MUTED).grid(row=1, column=0,
                                          sticky="e", padx=(0, 8), pady=5)
        styled_entry(left, textvariable=self.pname_var).grid(
            row=1, column=1, pady=5, sticky="w")

        styled_label(left, "Species:", 10,
                     color=FG_MUTED).grid(row=2, column=0,
                                          sticky="e", padx=(0, 8), pady=5)
        styled_combo(left, self.pspec_var,
                     ["Green Gram (Moong)", "Wheat", "Mustard",
                      "Tomato", "Spinach", "Sunflower",
                      "Pea", "Other"]).grid(
                         row=2, column=1, pady=5, sticky="w")

        styled_label(left, "Experiment Group:", 10,
                     color=FG_MUTED).grid(row=3, column=0,
                                          sticky="e", padx=(0, 8), pady=5)
        styled_combo(left, self.pgroup_var,
                     ["Regular Water", "Less Water",
                      "Excess Water", "Low Light",
                      "High Temperature", "Control"]).grid(
                         row=3, column=1, pady=5, sticky="w")

        styled_button(left, "  Save Plant",
                      self._save_plant).grid(
                          row=4, columnspan=2, pady=16)

        self.plant_status = tk.StringVar()
        tk.Label(left, textvariable=self.plant_status,
                 font=("Segoe UI", 9), fg=FG_WARN,
                 bg=BG_CARD, wraplength=320).grid(
                     row=5, columnspan=2)

        # schema info box
        schema_box = card_frame(left, padx=10, pady=8)
        schema_box.grid(row=6, columnspan=2, pady=(12, 0), sticky="ew")
        styled_label(schema_box, "DB Table: Plants", 9,
                     bold=True, color=FG_INFO).pack(anchor="w")
        for col in ["plant_id (PK, AUTO)", "plant_name VARCHAR(100)",
                    "species VARCHAR(100)", "grp VARCHAR(50)",
                    "created_at DATETIME"]:
            styled_label(schema_box, "  " + col, 9,
                         color=FG_MUTED).pack(anchor="w")

        # right side - plant list
        right = tk.Frame(f, bg=BG_PANEL)
        right.pack(side="left", fill="both", expand=True, padx=(14, 0))

        styled_label(right, "Registered Plants", 12, bold=True,
                     color=FG_ACCENT).pack(anchor="w", pady=(0, 6))

        cols = ("ID", "Name", "Species", "Group")
        self.plant_tree = ttk.Treeview(right, columns=cols,
                                       show="headings", height=14)
        self._style_tree(self.plant_tree, cols)
        self.plant_tree.pack(fill="both", expand=True)

        styled_button(right, "  Delete Selected",
                      self._delete_plant,
                      color=BTN_RED, width=18).pack(pady=8)
        self._refresh_plant_tree()

    def _save_plant(self):
        name  = self.pname_var.get().strip()
        spec  = self.pspec_var.get().strip()
        group = self.pgroup_var.get().strip()
        if not name:
            self.plant_status.set("Plant name cannot be empty."); return
        try:
            self.db.add_plant(name, spec or "Green Gram (Moong)", group)
            self.plant_status.set(f"Plant '{name}' saved successfully.")
            self.pname_var.set("")
            self._refresh_plant_tree()
        except Exception as e:
            self.plant_status.set(f"Error: {e}")

    def _delete_plant(self):
        sel = self.plant_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a plant first.")
            return
        pid = self.plant_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Delete",
                               f"Delete plant ID {pid} and ALL its data?"):
            self.db.delete_plant(pid)
            self._refresh_plant_tree()

    def _refresh_plant_tree(self):
        for row in self.plant_tree.get_children():
            self.plant_tree.delete(row)
        for p in self.db.get_plants():
            self.plant_tree.insert("", "end", values=(
                p["plant_id"], p["plant_name"],
                p["species"], p["grp"]
            ))

    # ==========================================================================
    #  TAB 3 : ADD OBSERVATION
    # ==========================================================================
    def _tab_add_obs(self, f):
        section_header(f, "  Record Observation").pack(
            fill="x", pady=(0, 14))

        # scrollable canvas for small screens
        canvas = tk.Canvas(f, bg=BG_PANEL, highlightthickness=0)
        sb_y   = tk.Scrollbar(f, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb_y.set)
        sb_y.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner  = tk.Frame(canvas, bg=BG_PANEL)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(
                       scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(win_id, width=e.width))

        form = card_frame(inner, padx=28, pady=20)
        form.pack(padx=0, pady=0, anchor="nw")

        styled_label(form, "Enter Observation Data", 12, bold=True,
                     color=FG_ACCENT).grid(
                         row=0, columnspan=2, pady=(0, 12), sticky="w")

        plants = self.db.get_plants()
        if not plants:
            styled_label(form, "No plants found. Add a plant first!",
                         11, color=FG_WARN).grid(row=1, columnspan=2)
            return

        plant_opts = [
            f"{p['plant_id']} - {p['plant_name']} ({p['grp']})"
            for p in plants
        ]

        self.obs_plant_var  = tk.StringVar(value=plant_opts[0])
        self.obs_day_var    = tk.StringVar(value="1")
        self.obs_height_var = tk.StringVar()
        self.obs_leaves_var = tk.StringVar()
        self.obs_temp_var   = tk.StringVar(value="25")
        self.obs_light_var  = tk.StringVar(value="8")
        self.obs_water_var  = tk.StringVar(value="Regular")
        self.obs_soil_var   = tk.StringVar(value="Moist")
        self.obs_notes_var  = tk.StringVar()

        field_defs = [
            ("Select Plant:",        "combo", self.obs_plant_var,  plant_opts),
            ("Observation Day:",     "entry", self.obs_day_var,    None),
            ("Height (cm):",         "entry", self.obs_height_var, None),
            ("Leaf Count:",          "entry", self.obs_leaves_var, None),
            ("Temperature (C):",     "entry", self.obs_temp_var,   None),
            ("Light Hours / Day:",   "entry", self.obs_light_var,  None),
            ("Watering:",            "combo", self.obs_water_var,
             ["Regular", "Less", "Excess"]),
            ("Soil Moisture:",       "combo", self.obs_soil_var,
             ["Dry", "Moist", "Wet"]),
            ("Notes (optional):",    "entry", self.obs_notes_var,  None),
        ]
        for i, (lbl, kind, var, opts) in enumerate(field_defs, 1):
            styled_label(form, lbl, 10,
                         color=FG_MUTED).grid(row=i, column=0,
                                              sticky="e",
                                              padx=(0, 10), pady=5)
            if kind == "combo":
                w = styled_combo(form, var, opts, width=28)
            else:
                w = styled_entry(form, textvariable=var, width=30)
            w.grid(row=i, column=1, pady=5, sticky="w")

        styled_button(form, "  Save Observation",
                      self._save_observation).grid(
                          row=len(field_defs)+1, columnspan=2, pady=16)

        self.obs_status = tk.StringVar()
        tk.Label(form, textvariable=self.obs_status,
                 font=("Segoe UI", 9), fg=FG_WARN,
                 bg=BG_CARD, wraplength=400).grid(
                     row=len(field_defs)+2, columnspan=2)

        # schema info
        schema_box = card_frame(inner, padx=14, pady=10)
        schema_box.pack(padx=0, pady=(12, 0), anchor="nw")
        styled_label(schema_box, "DB Table: Observations", 9,
                     bold=True, color=FG_INFO).pack(anchor="w")
        for col in ["obs_id (PK, AUTO)", "plant_id (FK)",
                    "obs_day INT", "height_cm FLOAT",
                    "leaf_count INT", "temperature FLOAT",
                    "light_hours FLOAT", "watering VARCHAR(20)",
                    "soil_moisture VARCHAR(20)", "notes TEXT"]:
            styled_label(schema_box, "  " + col, 9,
                         color=FG_MUTED).pack(anchor="w")

    def _save_observation(self):
        try:
            raw   = self.obs_plant_var.get()
            pid   = int(raw.split("-")[0].strip())
            day   = int(self.obs_day_var.get().strip())
            ht    = float(self.obs_height_var.get().strip())
            lv    = int(self.obs_leaves_var.get().strip())
            tmp   = float(self.obs_temp_var.get().strip())
            lght  = float(self.obs_light_var.get().strip())
            water = self.obs_water_var.get()
            soil  = self.obs_soil_var.get()
            notes = self.obs_notes_var.get().strip()

            if day < 1:            raise ValueError("Day must be >= 1")
            if ht  < 0:            raise ValueError("Height must be positive")
            if lv  < 0:            raise ValueError("Leaf count must be >= 0")
            if not (0 <= tmp <= 60):   raise ValueError("Temperature: 0-60 C")
            if not (0 <= lght <= 24):  raise ValueError("Light hours: 0-24")

            self.db.add_observation(pid, day, ht, lv, tmp,
                                    lght, water, soil, notes)
            self.obs_status.set(
                f"Observation (Day {day}, {ht} cm) saved successfully.")
            self.obs_height_var.set("")
            self.obs_leaves_var.set("")
        except ValueError as e:
            self.obs_status.set(f"Validation error: {e}")
        except Exception as e:
            self.obs_status.set(f"Error: {e}")

    # ==========================================================================
    #  TAB 4 : VIEW DATA
    # ==========================================================================
    def _tab_view_data(self, f):
        section_header(f, "  View All Observations").pack(
            fill="x", pady=(0, 10))

        obs_list = self.db.get_observations()
        if not obs_list:
            styled_label(f, "No observations found. Add some first!",
                         11, color=FG_WARN).pack(pady=20)
            return

        hdrs = ("ID", "Plant", "Group", "Day", "Height(cm)",
                "Leaves", "Temp(C)", "Light(h)", "Watering", "Soil")

        frame_tree = tk.Frame(f, bg=BG_PANEL)
        frame_tree.pack(fill="both", expand=True)

        sb_y = tk.Scrollbar(frame_tree)
        sb_x = tk.Scrollbar(frame_tree, orient="horizontal")
        tree = ttk.Treeview(frame_tree, columns=hdrs,
                            show="headings", height=18,
                            yscrollcommand=sb_y.set,
                            xscrollcommand=sb_x.set)
        self._style_tree(tree, hdrs,
                         widths=[50, 110, 120, 50, 80, 60, 70, 60, 80, 70])
        sb_y.config(command=tree.yview)
        sb_x.config(command=tree.xview)
        sb_y.pack(side="right", fill="y")
        sb_x.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        for o in obs_list:
            tree.insert("", "end", values=(
                o["obs_id"],    o["plant_name"], o["grp"],
                o["obs_day"],   o["height_cm"],  o["leaf_count"],
                o["temperature"], o["light_hours"],
                o["watering"],  o["soil_moisture"]
            ))

        def delete_obs():
            sel = tree.selection()
            if not sel:
                messagebox.showinfo("Select", "Select a row first.")
                return
            oid = tree.item(sel[0])["values"][0]
            if messagebox.askyesno("Delete",
                                   f"Delete observation ID {oid}?"):
                self.db.delete_observation(oid)
                self._show_tab("view_data")

        styled_button(f, "  Delete Selected Row",
                      delete_obs, color=BTN_RED,
                      width=20).pack(pady=8)

    # ==========================================================================
    #  TAB 6 : STRESS CLUES
    # ==========================================================================
    def _tab_stress(self, f):
        section_header(f,
                       "  Stress Clues - Educational Pattern Analysis").pack(
            fill="x", pady=(0, 10))

        plants = self.db.get_plants()
        if not plants:
            styled_label(f, "No plants found.", 11, color=FG_WARN).pack()
            return

        ctrl = tk.Frame(f, bg=BG_PANEL)
        ctrl.pack(fill="x", pady=(0, 8))
        styled_label(ctrl, "Select Plant:", 10,
                     color=FG_MUTED).pack(side="left", padx=(0, 6))
        opts = [f"{p['plant_id']} - {p['plant_name']}" for p in plants]
        self.stress_plant_var = tk.StringVar(value=opts[0])
        styled_combo(ctrl, self.stress_plant_var,
                     opts, width=32).pack(side="left")
        styled_button(ctrl, "  Analyse Stress",
                      lambda: self._run_stress(result_frame),
                      width=18).pack(side="left", padx=10)

        result_frame = tk.Frame(f, bg=BG_PANEL)
        result_frame.pack(fill="both", expand=True)
        styled_label(result_frame,
                     "Select a plant and click 'Analyse Stress' to begin.",
                     11, color=FG_MUTED).pack(pady=20)

    def _run_stress(self, frame):
        for w in frame.winfo_children(): w.destroy()
        raw = self.stress_plant_var.get()
        pid = int(raw.split("-")[0].strip())
        obs = self.db.get_observations(pid)

        flag, details = AnalysisEngine.detect_stress(obs)
        avg = AnalysisEngine.average_growth(obs)

        flag_color = {
            "None":                        FG_ACCENT,
            "Water Stress":                FG_WARN,
            "Low-Light Stress":            FG_INFO,
            "Heat Stress":                 FG_DANGER,
            "Cold Stress":                 FG_INFO,
            "Excess Water / Waterlogging": FG_WARN,
            "Multiple Stressors":          FG_DANGER,
        }.get(flag, FG_MAIN)

        top = card_frame(frame, padx=18, pady=12)
        top.pack(fill="x", pady=(0, 10))

        pname = obs[0]["plant_name"] if obs else "Unknown"
        styled_label(top, f"Plant: {pname}", 12, bold=True,
                     color=FG_ACCENT).pack(anchor="w")
        styled_label(top,
                     f"Primary Stress Flag:  {flag}",
                     14, bold=True, color=flag_color).pack(
                         anchor="w", pady=4)
        styled_label(top,
                     f"Average Growth Rate: {avg:.4f} cm/day  |  "
                     f"Observations: {len(obs)}",
                     10, color=FG_MUTED).pack(anchor="w")

        # rules used
        rules_box = card_frame(frame, padx=14, pady=8)
        rules_box.pack(fill="x", pady=(0, 6))
        styled_label(rules_box, "Rules Applied (if-then logic):", 10,
                     bold=True, color=FG_INFO).pack(anchor="w")
        rules = [
            "IF watering=Less AND soil=Dry  =>  Water Stress",
            "IF watering=Excess AND soil=Wet =>  Excess Water / Waterlogging",
            "IF light_hours < 4             =>  Low-Light Stress",
            "IF temperature > 38 C          =>  Heat Stress",
            "IF temperature < 10 C          =>  Cold Stress",
            "IF growth_rate < 40% of avg    =>  Investigate conditions",
        ]
        for r in rules:
            styled_label(rules_box, "  " + r, 9,
                         color=FG_MUTED).pack(anchor="w")

        styled_label(frame, "Detailed Clues:", 11, bold=True,
                     color=FG_ACCENT).pack(anchor="w", pady=(6, 2))

        tf, txt = scrollable_text(frame, height=9)
        tf.pack(fill="both", expand=True)
        txt.config(state="normal")
        for d in details:
            txt.insert("end", "  * " + d + "\n")
        txt.insert("end",
                   "\n"
                   "DISCLAIMER: These are educational pattern clues based on\n"
                   "simple if-then rules. Real plant stress diagnosis requires\n"
                   "lab tests and expert observation. This tool is for learning.\n")
        txt.config(state="disabled")

        # save to DB
        summary = "; ".join(details)
        try:
            self.db.save_analysis(pid, 0.0, avg, flag, summary)
        except Exception:
            pass

    # ==========================================================================
    #  TAB 7 : COMPARE PLANTS
    # ==========================================================================
    def _tab_compare(self, f):
        section_header(f, "  Compare Plants - Side-by-Side Analysis").pack(
            fill="x", pady=(0, 10))

        ctrl = tk.Frame(f, bg=BG_PANEL)
        ctrl.pack(fill="x", pady=(0, 8))
        styled_button(ctrl, "  Run Comparison",
                      lambda: self._run_compare(graph_frame),
                      width=20).pack(side="left")

        graph_frame = tk.Frame(f, bg=BG_PANEL)
        graph_frame.pack(fill="both", expand=True)
        self._run_compare(graph_frame)

    def _run_compare(self, frame):
        for w in frame.winfo_children(): w.destroy()

        plants = self.db.get_plants()
        if not plants:
            styled_label(frame, "No plants found.", 11,
                         color=FG_WARN).pack(pady=20)
            return

        plants_data = {}
        for p in plants:
            obs = self.db.get_observations(p["plant_id"])
            if obs:
                plants_data[p["plant_name"]] = obs

        if not plants_data:
            styled_label(frame,
                         "No observations found for any plant.",
                         11, color=FG_WARN).pack(pady=20)
            return

        names  = list(plants_data.keys())
        avgs   = [AnalysisEngine.average_growth(plants_data[n]) for n in names]
        totals = [
            plants_data[n][-1]["height_cm"] - plants_data[n][0]["height_cm"]
            if len(plants_data[n]) >= 2 else 0
            for n in names
        ]

        palette = ["#7EC850","#4FC3F7","#F4A261","#E76F51",
                   "#CE93D8","#80CBC4","#FFF176","#FFAB91"]

        fig = Figure(figsize=(11, 4.2), dpi=90, facecolor=BG_PANEL)

        # chart 1: avg growth rate
        ax1 = fig.add_subplot(131, facecolor=BG_ENTRY)
        bars1 = ax1.bar(names, avgs, color=palette[:len(names)], width=0.5)
        ax1.set_title("Avg Growth Rate\n(cm/day)",
                      color=FG_ACCENT, fontsize=10)
        ax1.set_ylabel("cm/day", color=FG_MUTED)
        ax1.tick_params(colors=FG_MUTED, labelsize=8)
        for bar, val in zip(bars1, avgs):
            ax1.text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.005,
                     f"{val:.3f}", ha="center", va="bottom",
                     fontsize=8, color=FG_MAIN)
        for sp in ax1.spines.values(): sp.set_edgecolor(BORDER)

        # chart 2: total height gain
        ax2 = fig.add_subplot(132, facecolor=BG_ENTRY)
        bars2 = ax2.bar(names, totals, color=palette[:len(names)], width=0.5)
        ax2.set_title("Total Height Gain\n(cm)",
                      color=FG_ACCENT, fontsize=10)
        ax2.set_ylabel("cm", color=FG_MUTED)
        ax2.tick_params(colors=FG_MUTED, labelsize=8)
        for bar, val in zip(bars2, totals):
            ax2.text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.05,
                     f"{val:.1f}", ha="center", va="bottom",
                     fontsize=8, color=FG_MAIN)
        for sp in ax2.spines.values(): sp.set_edgecolor(BORDER)

        # chart 3: height timeline overlay
        ax3 = fig.add_subplot(133, facecolor=BG_ENTRY)
        for i, name in enumerate(names):
            obs = plants_data[name]
            if len(obs) >= 2:
                days = [o["obs_day"]   for o in obs]
                hts  = [o["height_cm"] for o in obs]
                ax3.plot(days, hts, "o-",
                         color=palette[i % len(palette)],
                         label=name, linewidth=1.8, markersize=4)
        ax3.set_title("Height Timeline\nOverlay",
                      color=FG_ACCENT, fontsize=10)
        ax3.set_xlabel("Day", color=FG_MUTED)
        ax3.set_ylabel("Height (cm)", color=FG_MUTED)
        ax3.tick_params(colors=FG_MUTED, labelsize=8)
        ax3.legend(facecolor=BG_CARD, labelcolor=FG_MAIN, fontsize=7)
        for sp in ax3.spines.values(): sp.set_edgecolor(BORDER)

        fig.tight_layout(pad=2)
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        # auto summary
        summary_lines = AnalysisEngine.experiment_summary(plants_data)
        sf, stxt = scrollable_text(frame, height=8)
        sf.pack(fill="x", pady=4)
        stxt.config(state="normal")
        stxt.insert("end", "\n".join(summary_lines))
        stxt.config(state="disabled")

    # -- shared tree styler ----------------------------------------------------
    def _style_tree(self, tree, cols, widths=None):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_ENTRY, foreground=FG_MAIN,
                        rowheight=26, fieldbackground=BG_ENTRY,
                        bordercolor=BORDER,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background=BG_CARD, foreground=FG_ACCENT,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview",
                  background=[("selected", "#2E6B2E")],
                  foreground=[("selected", FG_ACCENT)])
        for i, col in enumerate(cols):
            w = widths[i] if widths and i < len(widths) else 100
            tree.heading(col, text=col)
            tree.column(col, width=w, anchor="center")

    def _on_close(self):
        self.db.disconnect()
        self.destroy()


# -----------------------------------------------------------------------------
#  ENTRY POINT
# -----------------------------------------------------------------------------
def main():
    login = LoginWindow()
    login.mainloop()

    if login.db is None:
        return          # user closed without connecting

    app = PlantStressApp(login.db)
    app.mainloop()


if __name__ == "__main__":
    main()
