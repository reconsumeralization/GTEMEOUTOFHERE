# TEACHER Week 8: Problem Sets

> *"Web Foundations for COSURVIVAL - From programs to web apps."*

---

## Problem Set 1: HTML Structure

### Problem 1.1: Build COSURVIVAL Dashboard HTML

**Task:** Create HTML structure for dashboard

**Requirements:**
1. DOCTYPE and html tag
2. Head with title and meta tags
3. Header with navigation (TRIBE/TEACHER/RECON)
4. Three main sections (one per lens)
5. Forms for queries
6. Footer with timestamp

**Starter:**
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>COSURVIVAL Dashboard</title>
    <!-- TODO: Add meta tags, CSS link -->
  </head>
  <body>
    <!-- TODO: Add header, main, footer -->
  </body>
</html>
```

---

### Problem 1.2: Add Semantic HTML5

**Task:** Use semantic HTML5 elements

**Requirements:**
1. Replace `div` with semantic tags (`header`, `main`, `section`, `footer`)
2. Add proper headings hierarchy
3. Use `nav` for navigation
4. Use `form` for inputs
5. Add `aria-label` for accessibility

---

## Problem Set 2: CSS Styling

### Problem 2.1: Create COSURVIVAL Color Scheme

**Task:** Define CSS variables for colors

**Requirements:**
1. TRIBE colors (blue)
2. TEACHER colors (green)
3. RECON colors (orange)
4. Neutral colors (background, text)
5. Use CSS variables (`:root`)

---

### Problem 2.2: Style Dashboard Layout

**Task:** Create responsive dashboard layout

**Requirements:**
1. Flexbox or Grid layout
2. Card-based design for sections
3. Responsive (mobile-friendly)
4. Hover effects
5. Consistent spacing

---

## Problem Set 3: JavaScript Basics

### Problem 3.1: Add Event Listeners

**Task:** Make dashboard interactive

**Requirements:**
1. Lens toggle (switch between TRIBE/TEACHER/RECON)
2. Form submission handler
3. Button click handlers
4. Use `addEventListener` (not inline)

---

### Problem 3.2: DOM Manipulation

**Task:** Update dashboard content dynamically

**Requirements:**
1. Create elements with `createElement`
2. Update text with `textContent` or `innerHTML`
3. Add/remove classes
4. Show/hide sections
5. Update timestamp

---

## Problem Set 4: API Integration

### Problem 4.1: Create Python API

**Task:** Build Flask/FastAPI endpoint

**Requirements:**
1. Endpoint: `/v1/tribe/graph`
2. Query SQL database
3. Return JSON
4. Handle errors
5. Add CORS headers

---

### Problem 4.2: Fetch from JavaScript

**Task:** Fetch data from API and display

**Requirements:**
1. Use `fetch()` API
2. Handle promises (`.then()`)
3. Parse JSON response
4. Display in dashboard
5. Handle errors

---

## Problem Set 5: Forms and Validation

### Problem 5.1: Build Query Form

**Task:** Create form for COSURVIVAL queries

**Requirements:**
1. User ID input
2. Lens selection (dropdown)
3. Submit button
4. Client-side validation (UX)
5. Prevent default form submission

---

### Problem 5.2: Server-Side Validation

**Task:** Add validation to Python API

**Requirements:**
1. Validate user_id exists
2. Validate lens is valid (tribe/teacher/recon)
3. Return error messages
4. Use proper HTTP status codes
5. Sanitize input

---

## Problem Set 6: Dynamic Content

### Problem 6.1: Update Graph Dynamically

**Task:** Load and display TRIBE graph

**Requirements:**
1. Fetch graph data from API
2. Create canvas or SVG element
3. Draw graph (use D3.js or similar)
4. Update on button click
5. Show loading state

---

### Problem 6.2: Real-Time Updates

**Task:** Auto-refresh dashboard data

**Requirements:**
1. Use `setInterval()` for periodic updates
2. Update provider scores every 30 seconds
3. Update recommendations on user change
4. Show "last updated" timestamp
5. Handle API errors gracefully

---

## Problem Set 7: Security

### Problem 7.1: Prevent XSS

**Task:** Sanitize user input

**Requirements:**
1. Escape HTML in user input
2. Use `textContent` instead of `innerHTML` where possible
3. Validate input format
4. Use Content Security Policy (CSP)

---

### Problem 7.2: Secure API Calls

**Task:** Add authentication and rate limiting

**Requirements:**
1. Add API key authentication
2. Rate limit requests
3. Validate origin (CORS)
4. Use HTTPS
5. Log suspicious activity

---

## Problem Set 8: Complete Dashboard

### Problem 8.1: Build TRIBE Section

**Task:** Complete TRIBE visualization

**Requirements:**
1. Fetch graph data
2. Display network graph
3. Show communities
4. List mentor candidates
5. Add filters (company, group)

---

### Problem 8.2: Build TEACHER Section

**Task:** Complete TEACHER visualization

**Requirements:**
1. Fetch recommendations
2. Display skill pathways
3. Show progressions
4. List org skill gaps
5. Add user search

---

### Problem 8.3: Build RECON Section

**Task:** Complete RECON visualization

**Requirements:**
1. Fetch provider scores
2. Display reliability table
3. Show friction points
4. List value flows
5. Add filters (company, grade)

---

### Problem 8.4: Integrate All Three

**Task:** Build complete COSURVIVAL dashboard

**Requirements:**
1. All three sections working
2. Navigation between sections
3. Shared query interface
4. Consistent styling
5. Responsive design

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working HTML/CSS/JS
2. **Tests:** Test in browser
3. **Documentation:** Comments explaining code
4. **Security:** Input validation, XSS prevention

### Self-Assessment

After completing all problem sets, answer:

1. Can you build HTML structure for dashboards?
2. Can you style with CSS?
3. Can you add JavaScript interactivity?
4. Can you connect to Python API?
5. Can you prevent security issues?

**Remember:** Growth over position. Compare to your Week 7 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week8_solutions/` for instructors.

**Key Learning Points:**
- HTML provides structure
- CSS provides style
- JavaScript provides interactivity
- Client-side validation = UX, not security
- Always validate server-side
- Connect front-end to back-end

---

*"This week is the front-end + protocol foundation. Next week you'll connect Python + SQL + HTML + CSS + JS into full web apps."*

