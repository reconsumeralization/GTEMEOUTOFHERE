# TEACHER Week 9: Flask for COSURVIVAL

> *"The jump from static websites to dynamic web applications. Apps take input and produce output, combining Python + HTML + SQL + Jinja to build COSURVIVAL dashboards."*

---

## Module Overview

**Duration:** 10-12 hours  
**Prerequisites:** Week 8 (Web Foundations)  
**Next:** Capstone (Full-Stack COSURVIVAL Application)

This week, learners discover how **Flask enables dynamic COSURVIVAL web applications**. Just as CS50 Week 9 shows Flask connecting Python + SQL + HTML, TEACHER Week 9 shows Flask connecting COSURVIVAL extractors + SQL database + dashboard templates.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Build** Flask applications for COSURVIVAL
2. **Create** routes for TRIBE/TEACHER/RECON endpoints
3. **Use** Jinja templates for dashboard rendering
4. **Handle** GET and POST requests
5. **Integrate** SQL queries with Flask
6. **Implement** sessions for user state
7. **Build** JSON APIs for dashboard data
8. **Deploy** full-stack COSURVIVAL applications

---

## Core Concept: From Static to Dynamic

### CS50's Insight

> "The jump from **static websites** (served by `http-server`) to **dynamic web applications** (served by `flask run`). Apps take input and produce output."

### TEACHER's Insight

> "The jump from **static JSON files** to **dynamic COSURVIVAL dashboards** (served by Flask). Dashboards take queries and produce real-time TRIBE/TEACHER/RECON insights."

---

## Flask Basics: The Smallest COSURVIVAL App

### Project Structure

**COSURVIVAL Flask conventions:**
```
cosurvival_app/
├── app.py                 # Main Flask application
├── templates/             # HTML templates
│   ├── layout.html       # Base template
│   ├── index.html        # Dashboard home
│   ├── tribe.html        # TRIBE visualization
│   ├── teacher.html      # TEACHER visualization
│   └── recon.html        # RECON visualization
├── static/               # CSS/JS/images
│   ├── css/
│   │   └── dashboard.css
│   └── js/
│       └── dashboard.js
├── extractors/           # Python extractors
│   ├── tribe_graph.py
│   ├── teacher_paths.py
│   └── recon_scores.py
├── cosurvival.db         # SQLite database
└── requirements.txt      # Dependencies
```

---

### Minimal COSURVIVAL App

**Hello, COSURVIVAL:**
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "COSURVIVAL Dashboard"

if __name__ == "__main__":
    app.run(debug=True)
```

**Upgrade to HTML:**
```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
```

---

## Routes: COSURVIVAL Endpoints

### TRIBE/TEACHER/RECON Routes

**Dashboard routes:**
```python
@app.route("/")
def index():
    """Dashboard home page."""
    return render_template("index.html")

@app.route("/tribe")
def tribe():
    """TRIBE network visualization."""
    return render_template("tribe.html")

@app.route("/teacher")
def teacher():
    """TEACHER learning pathways."""
    return render_template("teacher.html")

@app.route("/recon")
def recon():
    """RECON provider scores."""
    return render_template("recon.html")
```

**Everything after the domain is a path/route. No 1:1 file mapping needed.**

---

## Query Parameters: GET Requests

### Filtering COSURVIVAL Data

**TRIBE with filters:**
```python
from flask import Flask, render_template, request

@app.route("/tribe")
def tribe():
    """TRIBE network with optional filters."""
    company_id = request.args.get("company_id")
    group_id = request.args.get("group_id")
    
    # Query database with filters
    graph_data = get_tribe_graph(company_id=company_id, group_id=group_id)
    
    return render_template("tribe.html", graph_data=graph_data)
```

**URL examples:**
```
/tribe
/tribe?company_id=org_techcorp
/tribe?company_id=org_techcorp&group_id=team_alpha
```

---

## Templates + Jinja: Dynamic Dashboards

### Variable Interpolation

**Template:**
```html
<!-- tribe.html -->
<h1>TRIBE Network</h1>
<p>Company: {{ company_name }}</p>
<p>Communities: {{ community_count }}</p>
```

**Python:**
```python
@app.route("/tribe")
def tribe():
    company_name = "TechCorp"
    community_count = 5
    return render_template("tribe.html", 
                         company_name=company_name,
                         community_count=community_count)
```

---

### Logic in Templates

**Conditional rendering:**
```html
{% if graph_data %}
    <div id="tribe-graph">
        <!-- Render graph -->
    </div>
{% else %}
    <p>No graph data available.</p>
{% endif %}
```

**Loops:**
```html
<ul>
{% for community in communities %}
    <li>
        Community {{ loop.index }}: {{ community.size }} members
        <ul>
        {% for member in community.members %}
            <li>{{ member }}</li>
        {% endfor %}
        </ul>
    </li>
{% endfor %}
</ul>
```

---

## Forms: User-Friendly Query Interface

### COSURVIVAL Query Form

**HTML form:**
```html
<form action="/query" method="get">
    <label for="user-id">User ID:</label>
    <input type="text" id="user-id" name="user_id" placeholder="Enter user ID">
    
    <label for="lens">Lens:</label>
    <select id="lens" name="lens">
        <option value="tribe">TRIBE</option>
        <option value="teacher">TEACHER</option>
        <option value="recon">RECON</option>
    </select>
    
    <button type="submit">Query</button>
</form>
```

**Flask handler:**
```python
@app.route("/query")
def query():
    user_id = request.args.get("user_id")
    lens = request.args.get("lens", "tribe")
    
    if lens == "tribe":
        data = get_tribe_data(user_id)
        return render_template("tribe.html", data=data)
    elif lens == "teacher":
        data = get_teacher_data(user_id)
        return render_template("teacher.html", data=data)
    elif lens == "recon":
        data = get_recon_data(user_id)
        return render_template("recon.html", data=data)
```

---

## POST for Privacy: Secure Queries

### Sensitive Data Handling

**POST form (data not in URL):**
```html
<form action="/query" method="post">
    <input type="text" name="user_id" placeholder="User ID">
    <input type="text" name="company_id" placeholder="Company ID">
    <button type="submit">Query</button>
</form>
```

**Flask handler:**
```python
from flask import request

@app.route("/query", methods=["POST"])
def query():
    user_id = request.form.get("user_id")
    company_id = request.form.get("company_id")
    
    # Process query (data not visible in URL)
    data = get_cross_lens_data(user_id=user_id, company_id=company_id)
    
    return render_template("results.html", data=data)
```

---

## Consolidating GET + POST

### Single Route Pattern

**Elegant pattern for query pages:**
```python
@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        # Handle form submission
        user_id = request.form.get("user_id")
        lens = request.form.get("lens")
        
        data = get_lens_data(user_id, lens)
        return render_template("results.html", data=data)
    
    # Handle GET (show form)
    return render_template("query.html")
```

---

## Template Inheritance: Avoid Duplication

### Base Template

**layout.html:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}COSURVIVAL{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/dashboard.css') }}">
</head>
<body>
    <header>
        <h1>COSURVIVAL</h1>
        <nav>
            <a href="{{ url_for('index') }}">Home</a>
            <a href="{{ url_for('tribe') }}">TRIBE</a>
            <a href="{{ url_for('teacher') }}">Teacher</a>
            <a href="{{ url_for('recon') }}">RECON</a>
        </nav>
    </header>
    
    <main>
        {% block body %}{% endblock %}
    </main>
    
    <footer>
        <p>Generated at {{ timestamp }}</p>
    </footer>
</body>
</html>
```

**Child template:**
```html
{% extends "layout.html" %}

{% block title %}TRIBE Network - COSURVIVAL{% endblock %}

{% block body %}
    <h2>TRIBE Network Analysis</h2>
    <div id="tribe-graph">
        <!-- Graph visualization -->
    </div>
{% endblock %}
```

---

## Validation: Never Trust Client-Side

### Server-Side Validation

**COSURVIVAL validation:**
```python
# Authoritative list
VALID_LENSES = ["tribe", "teacher", "recon"]

@app.route("/query", methods=["POST"])
def query():
    user_id = request.form.get("user_id")
    lens = request.form.get("lens")
    
    # Server-side validation
    if not user_id:
        return render_template("error.html", 
                             message="User ID is required")
    
    if lens not in VALID_LENSES:
        return render_template("error.html", 
                             message=f"Invalid lens. Must be one of: {', '.join(VALID_LENSES)}")
    
    # Validate user exists
    if not user_exists(user_id):
        return render_template("error.html", 
                             message="User not found")
    
    # Safe to query
    data = get_lens_data(user_id, lens)
    return render_template("results.html", data=data)
```

**Key lesson:**
> "HTML `required` is a UX hint, not security. Always validate server-side."

---

## Redirects: Post-Redirect-Get Pattern

### After Processing POST

**Redirect to avoid resubmission:**
```python
from flask import redirect, url_for

@app.route("/query", methods=["POST"])
def query():
    user_id = request.form.get("user_id")
    lens = request.form.get("lens")
    
    # Process query
    query_id = save_query(user_id, lens)
    
    # Redirect to results page
    return redirect(url_for("results", query_id=query_id))

@app.route("/results/<query_id>")
def results(query_id):
    data = get_query_results(query_id)
    return render_template("results.html", data=data)
```

**Benefits:**
- Avoids resubmission on refresh
- Clean URLs
- Matches real-world patterns

---

## SQL Integration: Persisting COSURVIVAL Data

### Database Queries

**Store queries:**
```python
import sqlite3
from flask import g

def get_db():
    """Get database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect('cosurvival.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route("/query", methods=["POST"])
def query():
    user_id = request.form.get("user_id")
    lens = request.form.get("lens")
    
    db = get_db()
    
    # Store query
    db.execute("""
        INSERT INTO queries (user_id, lens, timestamp)
        VALUES (?, ?, datetime('now'))
    """, (user_id, lens))
    db.commit()
    
    # Get results
    results = get_lens_data(user_id, lens)
    
    return render_template("results.html", results=results)
```

**List queries:**
```python
@app.route("/queries")
def queries():
    db = get_db()
    rows = db.execute("""
        SELECT * FROM queries
        ORDER BY timestamp DESC
        LIMIT 100
    """).fetchall()
    
    return render_template("queries.html", queries=rows)
```

---

## Primary Keys in UI: Delete Operations

### Hidden Fields for IDs

**Delete query form:**
```html
<form action="/delete" method="post">
    <input type="hidden" name="query_id" value="{{ query.id }}">
    <button type="submit">Delete Query</button>
</form>
```

**Flask handler:**
```python
@app.route("/delete", methods=["POST"])
def delete():
    query_id = request.form.get("query_id")
    
    db = get_db()
    db.execute("DELETE FROM queries WHERE id = ?", (query_id,))
    db.commit()
    
    return redirect(url_for("queries"))
```

---

## Sessions: User State Management

### COSURVIVAL User Sessions

**Configure sessions:**
```python
from flask import Flask, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
```

**Store user preferences:**
```python
@app.route("/set-preferences", methods=["POST"])
def set_preferences():
    lens = request.form.get("default_lens", "tribe")
    company_id = request.form.get("company_id")
    
    session["default_lens"] = lens
    session["company_id"] = company_id
    
    return redirect(url_for("index"))

@app.route("/")
def index():
    # Use session preferences
    default_lens = session.get("default_lens", "tribe")
    company_id = session.get("company_id")
    
    return render_template("index.html", 
                         default_lens=default_lens,
                         company_id=company_id)
```

---

## Shopping Cart Pattern: Saved Queries

### Per-User Saved Queries

**Save queries to session:**
```python
@app.route("/save-query", methods=["POST"])
def save_query():
    query_id = request.form.get("query_id")
    
    if "saved_queries" not in session:
        session["saved_queries"] = []
    
    if query_id not in session["saved_queries"]:
        session["saved_queries"].append(query_id)
    
    return redirect(url_for("saved_queries"))

@app.route("/saved-queries")
def saved_queries():
    query_ids = session.get("saved_queries", [])
    
    db = get_db()
    queries = []
    for query_id in query_ids:
        row = db.execute("SELECT * FROM queries WHERE id = ?", 
                        (query_id,)).fetchone()
        if row:
            queries.append(row)
    
    return render_template("saved_queries.html", queries=queries)
```

---

## AJAX + JSON APIs: Modern Dashboard UX

### Autocomplete Search

**JavaScript:**
```javascript
document.getElementById('user-search').addEventListener('input', function(e) {
    const query = e.target.value;
    
    if (query.length >= 2) {
        fetch(`/api/search/users?q=${query}`)
            .then(response => response.json())
            .then(data => {
                const ul = document.getElementById('user-results');
                ul.innerHTML = '';
                
                data.users.forEach(user => {
                    const li = document.createElement('li');
                    li.textContent = user.id;
                    li.addEventListener('click', () => selectUser(user.id));
                    ul.appendChild(li);
                });
            });
    }
});
```

**Flask API endpoint:**
```python
from flask import jsonify

@app.route("/api/search/users")
def search_users():
    query = request.args.get("q", "")
    
    db = get_db()
    rows = db.execute("""
        SELECT id, company_id
        FROM users
        WHERE id LIKE ?
        LIMIT 10
    """, (f"%{query}%",)).fetchall()
    
    users = [{"id": row["id"], "company_id": row["company_id"]} 
             for row in rows]
    
    return jsonify({"users": users})
```

---

## JSON APIs: Clean Data Endpoints

### RESTful COSURVIVAL API

**TRIBE API:**
```python
@app.route("/api/v1/tribe/graph")
def api_tribe_graph():
    company_id = request.args.get("company_id")
    
    graph_data = get_tribe_graph(company_id=company_id)
    
    return jsonify({
        "nodes": graph_data["nodes"],
        "edges": graph_data["edges"],
        "communities": graph_data["communities"]
    })

@app.route("/api/v1/tribe/mentors")
def api_tribe_mentors():
    limit = request.args.get("limit", 10, type=int)
    
    mentors = get_mentor_candidates(limit=limit)
    
    return jsonify({"mentors": mentors})
```

**TEACHER API:**
```python
@app.route("/api/v1/teacher/recommendations")
def api_teacher_recommendations():
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    
    recommendations = get_recommendations(user_id)
    
    return jsonify({"recommendations": recommendations})

@app.route("/api/v1/teacher/progressions")
def api_teacher_progressions():
    user_id = request.args.get("user_id")
    
    progressions = get_progressions(user_id)
    
    return jsonify({"progressions": progressions})
```

**RECON API:**
```python
@app.route("/api/v1/recon/providers")
def api_recon_providers():
    company_id = request.args.get("company_id")
    
    providers = get_provider_scores(company_id=company_id)
    
    return jsonify({"providers": providers})

@app.route("/api/v1/recon/friction-points")
def api_recon_friction():
    friction_points = get_friction_points()
    
    return jsonify({"friction_points": friction_points})
```

---

## The Big Stack: MVC for COSURVIVAL

### Model-View-Controller

**Model = Data (SQL database):**
```python
# models.py or database queries
def get_tribe_graph(company_id=None):
    db = get_db()
    # Query database
    return graph_data
```

**View = Templates (HTML):**
```html
<!-- templates/tribe.html -->
{% extends "layout.html" %}
{% block body %}
    <div id="tribe-graph"></div>
{% endblock %}
```

**Controller = Flask routes (app.py):**
```python
# app.py
@app.route("/tribe")
def tribe():
    graph_data = get_tribe_graph()  # Model
    return render_template("tribe.html", graph_data=graph_data)  # View
```

**Full stack:**
> **HTML + CSS + JS + Flask + SQL + Jinja + JSON**

---

## Complete COSURVIVAL Flask App

### Full Application Structure

**app.py:**
```python
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from extractors.tribe_graph import get_tribe_graph
from extractors.teacher_paths import get_recommendations
from extractors.recon_scores import get_provider_scores

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('cosurvival.db')
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tribe")
def tribe():
    company_id = request.args.get("company_id")
    graph_data = get_tribe_graph(company_id=company_id)
    return render_template("tribe.html", graph_data=graph_data)

@app.route("/teacher")
def teacher():
    user_id = request.args.get("user_id")
    if user_id:
        recommendations = get_recommendations(user_id)
        return render_template("teacher.html", recommendations=recommendations)
    return render_template("teacher.html")

@app.route("/recon")
def recon():
    company_id = request.args.get("company_id")
    providers = get_provider_scores(company_id=company_id)
    return render_template("recon.html", providers=providers)

# API endpoints
@app.route("/api/v1/tribe/graph")
def api_tribe_graph():
    company_id = request.args.get("company_id")
    graph_data = get_tribe_graph(company_id=company_id)
    return jsonify(graph_data)

@app.route("/api/v1/teacher/recommendations")
def api_teacher_recommendations():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    recommendations = get_recommendations(user_id)
    return jsonify({"recommendations": recommendations})

@app.route("/api/v1/recon/providers")
def api_recon_providers():
    company_id = request.args.get("company_id")
    providers = get_provider_scores(company_id=company_id)
    return jsonify({"providers": providers})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Micro-Labs (CS50-Style)

### Lab 1: Build Minimal Flask App

**Task:** Create smallest working COSURVIVAL app

**Requirements:**
1. Flask app with one route
2. Return "COSURVIVAL Dashboard"
3. Run with `flask run`
4. View in browser

---

### Lab 2: Add Templates

**Task:** Render HTML templates

**Requirements:**
1. Create base template
2. Create index.html
3. Use `render_template()`
4. Add navigation

---

### Lab 3: Add Query Forms

**Task:** Build query interface

**Requirements:**
1. Create query form
2. Handle GET requests
3. Display results
4. Add validation

---

### Lab 4: Integrate SQL

**Task:** Connect to COSURVIVAL database

**Requirements:**
1. Query SQL database
2. Display results in template
3. Handle errors
4. Add database connection management

---

### Lab 5: Build JSON APIs

**Task:** Create API endpoints

**Requirements:**
1. TRIBE graph API
2. TEACHER recommendations API
3. RECON providers API
4. Return JSON with `jsonify()`

---

### Lab 6: Add AJAX

**Task:** Make dashboard interactive

**Requirements:**
1. Fetch data with JavaScript
2. Update DOM dynamically
3. Add loading states
4. Handle errors

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 9)

**Question:** "Can you build a dynamic web application?"

**Expected Response:**
- May understand HTML/CSS/JS
- May not know Flask
- May not connect to database

### After Week 9

**Question:** "Can you build a full-stack COSURVIVAL application?"

**Expected Response:**
- Can build Flask apps
- Can create routes and templates
- Can integrate SQL queries
- Can build JSON APIs
- Can handle forms and sessions

---

## Key Takeaways

1. **Flask enables dynamic web apps.** Connect Python + SQL + HTML.

2. **Routes map URLs to functions.** No 1:1 file mapping needed.

3. **Templates render dynamic content.** Jinja enables logic in HTML.

4. **Forms enable user input.** GET for visible, POST for private.

5. **Always validate server-side.** Client-side validation is UX, not security.

6. **SQL persists data.** Move from RAM to database.

7. **Sessions manage user state.** Store preferences and saved queries.

8. **JSON APIs enable modern UX.** AJAX avoids full page reloads.

9. **MVC separates concerns.** Model = data, View = templates, Controller = routes.

10. **Full stack = HTML + CSS + JS + Flask + SQL + Jinja + JSON.**

---

## Next Steps

**Capstone:** Full-Stack COSURVIVAL Application
- Build complete Flask app
- Integrate all three lenses
- Add authentication
- Deploy to production

**For Now:** Practice Flask:
- Build routes
- Create templates
- Integrate SQL
- Build APIs

---

## Resources

- **extractors/:** See Python extractors
- **curriculum/:** See all week modules
- **dashboard.html:** See front-end structure

---

*"The jump from static websites to dynamic web applications. Apps take input and produce output, combining Python + HTML + SQL + Jinja to build COSURVIVAL dashboards."*
