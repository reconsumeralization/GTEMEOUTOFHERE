# TEACHER Week 9: Problem Sets

> *"Flask for COSURVIVAL - From static to dynamic web applications."*

---

## Problem Set 1: Flask Basics

### Problem 1.1: Build Minimal COSURVIVAL App

**Task:** Create smallest working Flask app

**Requirements:**
1. Flask app with one route (`/`)
2. Return "COSURVIVAL Dashboard"
3. Run with `flask run`
4. View in browser

**Starter:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    # TODO: Return dashboard message
    pass

if __name__ == "__main__":
    app.run(debug=True)
```

---

### Problem 1.2: Add Project Structure

**Task:** Set up proper Flask project structure

**Requirements:**
1. Create `templates/` directory
2. Create `static/` directory
3. Create `requirements.txt`
4. Add Flask to requirements

---

## Problem Set 2: Routes and Templates

### Problem 2.1: Create Dashboard Routes

**Task:** Add routes for TRIBE/TEACHER/RECON

**Requirements:**
1. Route: `/` → index
2. Route: `/tribe` → TRIBE visualization
3. Route: `/teacher` → TEACHER visualization
4. Route: `/recon` → RECON visualization
5. Each renders appropriate template

---

### Problem 2.2: Build Base Template

**Task:** Create template inheritance

**Requirements:**
1. Create `layout.html` base template
2. Add navigation (TRIBE/TEACHER/RECON)
3. Create child templates
4. Use `{% extends %}` and `{% block %}`

---

## Problem Set 3: Forms and Query Parameters

### Problem 3.1: Build Query Form

**Task:** Create form for COSURVIVAL queries

**Requirements:**
1. User ID input
2. Lens selection (dropdown)
3. Submit button
4. Handle GET request
5. Display results

---

### Problem 3.2: Add POST Support

**Task:** Handle POST requests

**Requirements:**
1. Change form to POST
2. Handle `request.form`
3. Validate input
4. Redirect after POST

---

## Problem Set 4: SQL Integration

### Problem 4.1: Connect to Database

**Task:** Integrate SQL queries

**Requirements:**
1. Create database connection function
2. Query TRIBE data
3. Query TEACHER data
4. Query RECON data
5. Display in templates

---

### Problem 4.2: Store Queries

**Task:** Persist user queries

**Requirements:**
1. Create queries table
2. Store query on submission
3. List recent queries
4. Add delete functionality

---

## Problem Set 5: Validation

### Problem 5.1: Server-Side Validation

**Task:** Add validation to all forms

**Requirements:**
1. Validate user_id exists
2. Validate lens is valid
3. Validate company_id (if provided)
4. Return error messages
5. Use proper HTTP status codes

---

### Problem 5.2: Whitelist Validation

**Task:** Use authoritative lists

**Requirements:**
1. Define `VALID_LENSES` constant
2. Use for form generation
3. Use for validation
4. Single source of truth

---

## Problem Set 6: Sessions

### Problem 6.1: Store User Preferences

**Task:** Use sessions for preferences

**Requirements:**
1. Store default lens
2. Store company filter
3. Remember on next visit
4. Add preferences form

---

### Problem 6.2: Saved Queries

**Task:** Implement saved queries

**Requirements:**
1. Save queries to session
2. List saved queries
3. Remove from saved
4. Clear all saved

---

## Problem Set 7: JSON APIs

### Problem 7.1: Build TRIBE API

**Task:** Create JSON endpoints

**Requirements:**
1. `/api/v1/tribe/graph` → graph data
2. `/api/v1/tribe/mentors` → mentor candidates
3. `/api/v1/tribe/communities` → communities
4. Return JSON with `jsonify()`

---

### Problem 7.2: Build TEACHER API

**Task:** Create TEACHER JSON endpoints

**Requirements:**
1. `/api/v1/teacher/recommendations` → recommendations
2. `/api/v1/teacher/progressions` → progressions
3. `/api/v1/teacher/skills` → skill matrix
4. Handle query parameters

---

### Problem 7.3: Build RECON API

**Task:** Create RECON JSON endpoints

**Requirements:**
1. `/api/v1/recon/providers` → provider scores
2. `/api/v1/recon/friction-points` → friction points
3. `/api/v1/recon/value-flows` → value flows
4. Add error handling

---

## Problem Set 8: AJAX Integration

### Problem 8.1: Autocomplete Search

**Task:** Add autocomplete to user search

**Requirements:**
1. Listen to input changes
2. Fetch from API
3. Update dropdown dynamically
4. Handle errors

---

### Problem 8.2: Dynamic Dashboard Updates

**Task:** Update dashboard without reload

**Requirements:**
1. Fetch data with JavaScript
2. Update graph visualization
3. Update recommendations
4. Update provider scores
5. Add loading states

---

## Problem Set 9: Complete Application

### Problem 9.1: Full-Stack COSURVIVAL App

**Task:** Build complete Flask application

**Requirements:**
1. All three lens routes
2. Query forms with validation
3. SQL integration
4. JSON APIs
5. AJAX updates
6. Sessions for preferences
7. Error handling
8. Responsive design

---

## Submission Guidelines

### For Each Problem Set

1. **Code:** Working Flask application
2. **Tests:** Test all routes
3. **Documentation:** Comments explaining code
4. **Security:** Server-side validation

### Self-Assessment

After completing all problem sets, answer:

1. Can you build Flask applications?
2. Can you create routes and templates?
3. Can you integrate SQL queries?
4. Can you build JSON APIs?
5. Can you handle forms and sessions?

**Remember:** Growth over position. Compare to your Week 8 baseline.

---

## Solutions (For Instructors)

Solutions are available in `week9_solutions/` for instructors.

**Key Learning Points:**
- Flask enables dynamic web apps
- Routes map URLs to functions
- Templates render dynamic content
- Always validate server-side
- SQL persists data
- Sessions manage user state
- JSON APIs enable modern UX
- Full stack = HTML + CSS + JS + Flask + SQL + Jinja + JSON

---

*"The jump from static websites to dynamic web applications. Apps take input and produce output, combining Python + HTML + SQL + Jinja to build COSURVIVAL dashboards."*

