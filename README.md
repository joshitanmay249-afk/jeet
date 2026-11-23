# PLANT STRESS DETECTIVE
**Class 12 Biology + Computer Science (083) Project Report**

---

## CERTIFICATE

This is to certify that **Jeet Yadav** of standard **XII** of **Airport School Ahmedabad** has successfully completed the project work in **Computer Science (083)** titled **"Plant Stress Detective"** under the guidance of **Mr. Arpit Desai** during the academic year 2026–2027.

The project was carried out as a part of the practical assessment for the subject. The work presented in this report is the original effort of the student, and the application described in it has been designed, coded, tested, and demonstrated by him on the school computer laboratory systems.

<br>

**School Stamp:** `________________________`  
**Teacher’s Signature:** `________________________`  
**Principal’s Signature:** `____________________`  
**Examiner’s Signature:** `____________________`  
**Examiner’s Code:** `________________________`  
**Date:** `________________________`  

---

## ACKNOWLEDGEMENT

I would like to express a special token of gratitude to my Computer Science Teacher, **Mr. Arpit Desai**, for his constant guidance, valuable suggestions, and supervision throughout the development of this project. His insights helped me overcome technical hurdles and complete the project successfully.

I am also deeply thankful to our Principal, **Ms. Shalini Dhanwani**, for providing the necessary facilities, computer laboratory resources, and encouragement to carry out this practical work.

My sincere thanks go to my parents and friends for their continuous support, motivation, and help in finalizing this project within the given timeframe.

Lastly, I thank all my classmates who directly or indirectly contributed with their constructive feedback and suggestions during the testing and demonstration phases of the application.

- **Student Name:** Jeet Yadav
- **Class & Section:** Standard 12 - A
- **Roll Number:** ____________________
- **Subject:** Computer Science (083)
- **Date:** 18/11/2026
- **Signature:** ____________________

---

## INDEX

| Sr. No. | Topic | Page No. |
| :---: | :--- | :---: |
| 1. | About the Project | 5 |
| 2. | List of Functions | 6 |
| 3. | List of Libraries | 7 |
| 4. | Source Code (`main.py`) | 8 – 27 |
| 5. | Output and Database Verification | 28 – 29 |
| 6. | Bibliography | 30 |

*Note: Certificate and Acknowledgement serve as the official introductory preliminaries preceding the indexed topics.*

---

## 1. About The Project

**Plant Stress Detective** is an interdisciplinary desktop software solution engineered using **Python 3**, **MySQL Relational Database**, **Tkinter (GUI)**, and **Matplotlib**. The primary objective of the project is to provide higher secondary students with an interactive, data-driven analytical tool to observe, quantify, and analyze how varying environmental stressors (drought/water scarcity, overwatering, low light, extreme temperature) affect plant physiological growth metrics over time.

### Key Objectives and Educational Link
In standard Class 12 Biology (Units covering *Plant Physiology, Photosynthesis in Higher Plants, and Plant Growth & Development*), controlled experimentation is crucial to understand limiting factors (Blackman's Law of Limiting Factors). Students germinate seeds (such as *Vigna radiata* / Green Gram) under differentiated conditions:
- **Group A (Control / Optimal):** Regular watering schedule, adequate sunlight (8–10 hours/day), ambient temperature (22–28°C).
- **Group B (Water Stress):** Deficit hydration, desiccated soil conditions.
- **Group C (Photoperiod / Light Stress):** Sub-optimal illuminance (< 4 hours/day) leading to reduced photosynthetic assimilation and potential etiolation.
- **Group D (Temperature Stress):** High or freezing temperatures triggering enzymatic inactivation.

### Technical Architecture
The desktop system provides six modular components:
1. **Database & Authentication Manager:** Secure parameter configuration dialog connecting Python to the MySQL daemon with automatic database/schema creation.
2. **Dashboard Overview:** Real-time summary statistics, experiment guidelines, biology syllabus correlation, and recent experimental batches.
3. **Plant Registry Module:** Registration of experimental test subjects, biological taxonomy, and control vs. variable group designations stored in the `Plants` relation.
4. **Observation Logger:** Numerical logging of observational days, stem height (cm), leaf count, diurnal light exposure, thermal conditions, and soil moisture grades.
5. **Rule-Based Stress Detective:** Transparent if-then deduction engine detecting physiological anomalies (e.g., water deficit wilting, root hypoxia from overwatering, photosynthetic deficits, and severe growth decelerations) with educational citations.
6. **Side-by-Side Multi-Plant Comparative Analytics:** Integrated Matplotlib visualization showing comparative average growth rate bar charts (cm/day), total vegetative height gain, overlaid day-by-day growth curves, and automated synthesis rankings.

---

## 2. List of Functions

| Sr. No. | Name of Function | Library / Module | Purpose & Functionality |
| :---: | :--- | :--- | :--- |
| 1. | `mysql.connector.connect()` | `mysql.connector` | Establishes a TCP connection session between Python and MySQL server. |
| 2. | `cursor()` | `mysql.connector` | Creates an active cursor object configured for query dispatch. |
| 3. | `execute()` | `mysql.connector` | Compiles and executes SQL DDL/DML statements (`CREATE`, `INSERT`, `SELECT`, `DELETE`). |
| 4. | `fetchall()` | `mysql.connector` | Retrieves all resultant records from the most recently executed `SELECT` query as dictionary rows. |
| 5. | `commit()` | `mysql.connector` | Permanently saves all transaction modifications executed on the database instance. |
| 6. | `close()` | `mysql.connector` | Gracefully closes active cursor instances and terminates the database connection session. |
| 7. | `DatabaseManager.connect()` | Custom Class | Authenticates with MySQL, creates `plant_stress_db` if not present, and invokes table definitions. |
| 8. | `DatabaseManager._create_tables()` | Custom Class | Generates relational schemas for `Plants`, `Observations`, and `AnalysisResults` with foreign keys. |
| 9. | `DatabaseManager.add_plant()` | Custom Class | Inserts a new experimental specimen record into the `Plants` table. |
| 10. | `DatabaseManager.get_plants()` | Custom Class | Queries and retrieves all registered experimental plants sorted by creation timestamp. |
| 11. | `DatabaseManager.delete_plant()` | Custom Class | Removes a plant record along with all cascading observation logs. |
| 12. | `DatabaseManager.add_observation()` | Custom Class | Validates and appends a single daily biological log into the `Observations` table. |
| 13. | `DatabaseManager.get_observations()` | Custom Class | Fetches observations either globally or filtered by individual `plant_id`. |
| 14. | `DatabaseManager.delete_observation()`| Custom Class | Removes an incorrect or outlier observation record by its primary key (`obs_id`). |
| 15. | `DatabaseManager.save_analysis()` | Custom Class | Stores derived growth rates and diagnosed stress flags into `AnalysisResults`. |
| 16. | `AnalysisEngine.growth_rate()` | Custom Class | Computes incremental growth rate using the slope formula: $\frac{H_2 - H_1}{t_2 - t_1}$. |
| 17. | `AnalysisEngine.all_growth_rates()` | Custom Class | Computes day-by-day incremental differential growth rates over a sequence of observations. |
| 18. | `AnalysisEngine.average_growth()` | Custom Class | Calculates net mean growth velocity across the entire observation period. |
| 19. | `AnalysisEngine.detect_stress()` | Custom Class | Evaluates conditional stress rules based on moisture, temperature, photoperiod, and growth slopes. |
| 20. | `AnalysisEngine.experiment_summary()`| Custom Class | Sorts plants by growth velocity and generates comparative analytical experiment rankings. |
| 21. | `ttk.Style()` | `tkinter.ttk` | Instantiates a GUI widget styler to control fonts, colors, treeview heights, and margins. |
| 22. | `theme_use()` | `tkinter.ttk` | Sets the visual rendering theme (e.g., `'clam'`) across all ttk elements. |
| 23. | `configure()` | `tkinter.ttk` | Overrides styling attributes (background, foreground, font, padding) of custom widgets. |
| 24. | `map()` | `tkinter.ttk` | Assigns dynamic style attributes depending on widget states (e.g., active selection background). |
| 25. | `pack()` | `tkinter` | Places widgets within windows or frames according to side, fill, and padding geometry constraints. |
| 26. | `grid()` | `tkinter` | Positions widgets in structured rows and columns with explicit column-spanning and sticky alignments. |
| 27. | `pack_forget()` | `tkinter` | Unmaps and hides an existing frame to enable dynamic single-window screen transitions. |
| 28. | `winfo_children()` | `tkinter` | Returns a list of all child widget objects contained inside an arbitrary parent frame. |
| 29. | `destroy()` | `tkinter` | Destroys and cleans up a widget or top-level window from memory. |
| 30. | `bind()` | `tkinter` | Connects system GUI events (e.g., `<Enter>`, `<Leave>`, `<Configure>`) to Python callback functions. |
| 31. | `get()` | `tkinter` | Extracts user-entered string values from Entry widgets, Comboboxes, and StringVars. |
| 32. | `set()` | `tkinter` | Modifies or updates the dynamic text content stored inside a `StringVar`. |
| 33. | `insert()` | `tkinter` | Inserts data strings into Text boxes or adds formatted records into `ttk.Treeview` tables. |
| 34. | `selection()` | `tkinter.ttk` | Identifies and returns the active user-selected item ID within a Treeview widget. |
| 35. | `item()` | `tkinter.ttk` | Retrieves attribute maps and cell values of an existing row item in a Treeview. |
| 36. | `heading()` | `tkinter.ttk` | Defines column headers, display names, and sorting anchors in tabular views. |
| 37. | `column()` | `tkinter.ttk` | Customizes column width, minimum sizing, and text alignment properties in Treeviews. |
| 38. | `messagebox.showinfo()` | `tkinter.messagebox` | Renders a standard informational notification dialog window to the user. |
| 39. | `messagebox.showwarning()` | `tkinter.messagebox` | Displays validation failure warnings (e.g., empty fields, range errors). |
| 40. | `messagebox.showerror()` | `tkinter.messagebox` | Launches an error alert modal on unhandled exceptions or database connection failures. |
| 41. | `messagebox.askyesno()` | `tkinter.messagebox` | Launches an affirmative confirmation dialog before executing destructive database deletions. |
| 42. | `Figure()` | `matplotlib.figure` | Constructs the top-level canvas container for rendering 2D scientific plots. |
| 43. | `add_subplot()` | `matplotlib.figure` | Allocates individual subplot coordinate grids (Axes) within a multi-chart figure layout. |
| 44. | `bar()` | `matplotlib.axes` | Generates discrete bar charts for comparative vegetative parameters across test subjects. |
| 45. | `plot()` | `matplotlib.axes` | Draws continuous mathematical linear timeline curves tracking day-by-day height progression. |
| 46. | `FigureCanvasTkAgg()` | `matplotlib.backends` | Bridges native Matplotlib charts directly into the Tkinter window hierarchy as embeddable canvas widgets. |
| 47. | `draw()` | `matplotlib.backends` | Executes vector rasterization to render Matplotlib plots inside the Tkinter application view. |
| 48. | `tight_layout()` | `matplotlib.figure` | Automatically recalculates sub-plot margins, legends, and axis padding to prevent label overlap. |
| 49. | `eval("tk::PlaceWindow . center")` | `tkinter` | Centers application windows symmetrically on the user's primary monitor display. |
| 50. | `after()` | `tkinter` | Registers non-blocking timed asynchronous callbacks to update the real-time header clock. |

---

## 3. List of Libraries

| Sr. No. | Library Name | Module / Import Alias | Purpose in Project |
| :---: | :--- | :--- | :--- |
| 1. | **Tkinter** | `tkinter`, `ttk` | Primary Graphical User Interface (GUI) engine used to build the desktop window, layout navigation panels, input forms, and Treeviews. |
| 2. | **Tkinter Dialogs** | `tkinter.messagebox`, `tkinter.font` | Provides native modal dialogue windows for user notifications, validation warnings, and confirmation popups. |
| 3. | **MySQL Connector** | `mysql.connector`, `mysql.connector.Error` | Database driver enabling standard Python Database API v2.0 communication with the MySQL server, executing relational queries and maintaining transactions. |
| 4. | **Matplotlib** | `matplotlib`, `matplotlib.pyplot` | Standard 2D data visualization library employed to plot comparative vegetative growth rates and overlaid growth trajectories. |
| 5. | **Matplotlib Tk Backend** | `matplotlib.backends.backend_tkagg.FigureCanvasTkAgg` | Bridge module that renders Matplotlib vector figures directly inside standard Tkinter container frames without external popups. |
| 6. | **Datetime** | `datetime` | Standard Python module handling real-time timestamps, calendar logging, and formatting database insertion dates. |
| 7. | **Regular Expressions** | `re` | Provides string parsing and sanitation helpers during data validation. |

---

## 4. Output and Database Verification

The application execution sequence adheres to the following step-by-step graphical workflow:

```
+-----------------------------------------------------------------------+
|  STEP 1: DATABASE AUTHENTICATION DIALOG (LoginWindow)                |
|  - Prompts for MySQL Host, Port, User, Password, Database Name.       |
|  - Automatically creates database 'plant_stress_db' and tables.       |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 2: CENTRAL OVERVIEW DASHBOARD (_tab_dashboard)                  |
|  - Displays live metric cards: Total Plants, Total Observations, Date. |
|  - Summarizes CBSE Class 12 Biology theoretical topics.               |
|  - Lists recently registered experimental plants in a data grid.      |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 3: REGISTER EXPERIMENTAL SPECIMENS (_tab_add_plant)             |
|  - User specifies Plant ID, Botanical/Common Species, Experiment Group|
|    (Control, Less Water, Excess Water, Low Light, High Temp).         |
|  - Direct interactive table with Delete Plant capabilities.           |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 4: LOG OBSERVATIONS (_tab_add_obs)                              |
|  - User inputs Day number, Height (cm), Leaf count, Temperature,       |
|    Photoperiod (hrs/day), Water regime, and Soil moisture condition.  |
|  - Validates numerical limits and updates the 'Observations' table.   |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 5: TABULAR OBSERVATION REVIEW (_tab_view_data)                  |
|  - Full scrollable Treeview showing all recorded observations.        |
|  - Single-click row deletion for outlier / mistake pruning.           |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 6: EDUCATIONAL STRESS CLUES (_tab_stress)                       |
|  - Evaluates rule engine against the selected plant's dataset.        |
|  - Outputs Stress Flags (Water Stress, Low Light, Heat Stress, etc.)   |
|  - Displays mathematical average growth velocity and deduction notes. |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  STEP 7: MULTI-PLANT COMPARATIVE ANALYTICS (_tab_compare)             |
|  - Embeds 3 Matplotlib plots:                                         |
|      1. Bar chart: Average Growth Rate (cm/day) per plant.            |
|      2. Bar chart: Total Vegetative Height Gain (cm).                 |
|      3. Line plot: Overlaid multi-plant day-by-day growth curves.      |
|  - Outputs text ranking from fastest to slowest growth with margins.  |
+-----------------------------------------------------------------------+
```

### Sample Analytical Run Output (Simulated Experiment Data)

```text
=======================================================
   AUTOMATIC EXPERIMENT SUMMARY
=======================================================

Average Growth Rate Ranking (highest to lowest):
   1. Plant A (Regular Water)     =>  0.6857 cm/day
   2. Plant C (Low Light)         =>  0.3143 cm/day
   3. Plant B (Less Water Stress) =>  0.1857 cm/day

Plant A grew fastest; Plant B grew slowest.
Difference in average growth rate: 0.5000 cm/day

Stress Flags per Plant:
   * Plant A: None
   * Plant B: Water Stress
   * Plant C: Low-Light Stress

NOTE: These are educational pattern observations.
Real causation requires controlled experiments.
```

---

## 5. Bibliography

1. **NCERT Biology Class XII Textbook** — Unit IV: Plant Physiology, Photosynthesis in Higher Plants, and Plant Growth & Development.
2. **Computer Science with Python by Sumita Arora (Class XII)** — Dhanpat Rai & Co. (Modules on Tkinter GUI, File Handling, and MySQL Connectivity).
3. **Python Official Documentation (v3.13)** — *https://docs.python.org/3/* (Standard library, `tkinter`, `datetime`).
4. **MySQL Connector/Python Developer Guide** — Oracle Corporation, *https://dev.mysql.com/doc/connector-python/en/*.
5. **Matplotlib: Visualization with Python** — John D. Hunter et al., *https://matplotlib.org/* (Embedding in Tkinter with `FigureCanvasTkAgg`).
6. **Blackman, F.F. (1905)** — *Optima and Limiting Factors*, Annals of Botany (Biological foundation for physiological growth limitations).
