# Sprint-1 Bhargavi Kale

## What project work have you achieved since last class last week?
- Implemented grid system to arrange input form, map, and summary sections on the UI  
- Made layout responsive across devices  
- Laptop: all three sections in one row (Three-column layout)  
- Tablet: input form and summary side by side (Two-column), map at bottom  
- Mobile: all sections stacked vertically (One-column)  
- Updated changes in `style.css`  

## What challenges, setbacks, or blockers have you encountered?
- Layout works well on laptop and mobile but medium-sized screens were challenging because one-row layout felt too congested and fully vertical layout wasted space, making it difficult to find a balanced arrangement  

## What is your actionable and feasible plan for this week’s sprint?
- Test different edge cases of the application  
- Work on dashboard development  

## How much time are you allocated for this sprint? When?
- Sunday and Tuesday (4–5 hours)  

## What specific activities/tasks will you do in the allocated time?
- Test application in different scenarios and fix issues  
- Start working on dashboard implementation  

## What tangible work products will evidence your work?
- New dashboard HTML file  
- Updates in existing `main.py` file and HTML files  

# Sprint 1 Stand-Up Report
**Date:** April 15, 2026  
**Project:** Carbon Commute Calculator  
**Student:** Isabella Velazquez-Abelardo

---

## What project work have you achieved since last class last week?

This week my primary contribution focused on understanding and attempting UI layout adjustments rather than implementing major new features.

- Reviewed my teammate’s grid layout implementation for the input form, map, and summary panels  
- Attempted to make panels visually consistent in size  
- Worked on aligning the map height with the form and calculation sections  
- Experimented with CSS changes to determine whether layout problems should be solved by:
  - modifying panel containers, or  
  - modifying elements inside each panel  
- Tested styling updates locally and observed how CSS Grid and Flexbox settings affected layout behavior  

Most of my work involved learning how the layout system functions and identifying where styling changes should occur.

---

## What challenges, setbacks, or blockers have you encountered?

- Difficulty determining whether layout issues were caused by panel containers or internal elements such as forms and result boxes  
- Limited experience with responsive CSS layouts made debugging slower  
- Some attempted styling fixes created new spacing or alignment issues  

This sprint was mainly exploratory and helped me better understand how the UI structure works.

---

## What is your actionable and feasible plan for this week’s sprint?

- Ensure visual consistency across the interface  
- Verify all panels align correctly and resize properly  
- Check color contrast and readability for accessibility  

---

## How much time are you allocated for this sprint? When?

- Monday evening — 2 hours  
- Tuesday evening — 2 hours  

**Total planned time:** 4 hours

---

## What specific activities/tasks will you do in the allocated time?

- Debug UI alignment issues across screen sizes  
- Review teammate’s dashboard progress and assist where needed  
- Continue refining layout styling and visual consistency  

---

## What tangible work products will evidence your work?

- Updates to `style.css`  
- Changes to `home.html`  
- Updates to `main.py`  
- Adjustments to calculation result display  
- Git commits reflecting layout experimentation and fixes  




# Sprint-2 Bhargavi Kale, Isabella Velazquez Abelardo

## What project work have you achieved since last class last week?
- Worked on documentation and updated the README.md file  

## What challenges, setbacks, or blockers have you encountered?
- No major challenges.

## What is your actionable and feasible plan for this week’s sprint?
- Test different edge cases of the application.
- Work on deployment

## How much time are you allocated for this sprint? When?
- Sunday and Tuesday (4–5 hours)  

## What specific activities/tasks will you do in the allocated time?
- Test the application in different scenarios and fix issues
- Prepare presentation
- Deploy the application

## What tangible work products will evidence your work?
- Updates in existing main.py file and HTML files
- Updates in docs folder with presentation file

---

## What project work have you achieved since last class last week?

This week my primary contribution focused on implementing and integrating the **Dashboard feature** into the Carbon Commute Calculator.

- Created a new **Dashboard page** (`dashboard.html`) to display commute history
- Implemented the `/dashboard` Flask route to retrieve commute records from the database
- Added logic to calculate:
 - Total distance traveled
 - Total CO₂ emissions across all commutes
- Modified the `/calculate` route so each commute is saved to the database as a `Commute` object
- Designed summary cards displaying overall environmental impact statistics
- Built a trip history table showing vehicle, fuel type, locations, distance, and emissions
- Connected navigation between the calculator page and the dashboard

Evidence of this work exists in:
- `dashboard.html`
- `main.py`
- `style.css`
- Database model usage and stored commute entries

---

## What challenges, setbacks, or blockers have you encountered?

The largest challenge was **page formatting and layout restructuring**.

The application was originally designed using a **three-panel layout** (form, map, and results). The dashboard required a completely different layout — a full-width, centered page — which conflicted with the existing global container styling.

Specific challenges included:

- Dashboard content appearing left-aligned instead of centered
- CSS Grid rules from the calculator layout affecting the dashboard unintentionally
- Difficulty separating page-specific layouts while still using a shared base template
- Multiple iterations of CSS adjustments before identifying that the main container wrapper was forcing the layout behavior

Transitioning from a three-panel interface to a single dashboard view required restructuring how templates and CSS were organized.

---

## What is your actionable and feasible plan for this week’s sprint?

- Finalize dashboard formatting and responsiveness
- Improve visual consistency between calculator and dashboard pages
- Test database persistence and data accuracy
- Clean up unused CSS and redundant layout rules
- Prepare project documentation for final submission

---

## How much time are you allocated for this sprint? When?

- Tuesday evening — 2 hours 
- Wednesday evening — 2 hours 
- Friday afternoon — 2–3 hours 

**Total planned time:** approximately 6–7 hours

---

## What specific activities/tasks will you do in the allocated time?

- Test dashboard rendering across screen sizes
- Verify commute data saves correctly after calculations
- Refine summary card styling and spacing
- Perform UI polishing and layout cleanup
- Update README and documentation files
- Review GitHub repository organization

---

## What tangible work products will evidence your work?

- `dashboard.html` implementation
- Updates to `style.css`
- Modified `/calculate` and `/dashboard` routes in `main.py`
- Database entries demonstrating saved commutes
- Git commits showing dashboard development and layout fixes
