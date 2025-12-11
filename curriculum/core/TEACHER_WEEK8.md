# TEACHER Week 8: Web Foundations for COSURVIVAL

> *"We're moving from 'programs that run on your machine' to 'software built on top of the internet.' This week is the front-end + protocol foundation for COSURVIVAL dashboards."*

---

## Module Overview

**Duration:** 8-10 hours  
**Prerequisites:** Week 7 (SQL for COSURVIVAL)  
**Next:** Capstone (Full-Stack COSURVIVAL Application)

This week, learners discover how **web technologies power COSURVIVAL dashboards**. Just as CS50 Week 8 introduces HTML/CSS/JS for web apps, TEACHER Week 8 introduces web foundations for building interactive TRIBE/TEACHER/RECON visualizations.

---

## Learning Outcomes

By the end of this week, learners will be able to:

1. **Explain** how internet protocols enable COSURVIVAL dashboards
2. **Build** HTML structure for COSURVIVAL visualizations
3. **Style** dashboards with CSS
4. **Add interactivity** with JavaScript
5. **Connect** front-end to back-end (Python + SQL)
6. **Build** interactive queries and filters
7. **Create** responsive, accessible dashboards

---

## Core Concept: From Programs to Web Apps

### CS50's Insight

> "We're moving from 'programs that run on your machine' to **software built on top of the internet**."

### TEACHER's Insight

> "We're moving from 'Python scripts that process CSV' to **interactive dashboards that query SQL and visualize TRIBE/TEACHER/RECON in real-time**."

---

## The Internet: COSURVIVAL Data Flow

### Routers → Data Routing

**CS50's model:** Routers route data from A to B

**TEACHER's model:** Data flows from CSV → SQL → API → Dashboard

```
CSV File (Brian's data)
    ↓
SQL Database (normalized, indexed)
    ↓
Python API (FastAPI/Flask)
    ↓
HTTP/HTTPS
    ↓
Dashboard (HTML/CSS/JS)
    ↓
User (sees TRIBE/TEACHER/RECON insights)
```

**Key insight:**
> "Multiple paths exist for the same data. The system can route around failure."

---

### TCP/IP → COSURVIVAL Protocol

**IP Addresses:**
- Source: Where data comes from (user's browser)
- Destination: Where data goes (COSURVIVAL server)

**TCP Ports:**
- **80** = HTTP (dashboard access)
- **443** = HTTPS (secure dashboard)
- **5000** = Development API (local testing)

**COSURVIVAL flow:**
```
User Browser (IP: 192.168.1.100)
    ↓ HTTP request
COSURVIVAL Server (IP: 10.0.0.5, Port: 443)
    ↓ SQL query
Database (IP: 10.0.0.6, Port: 5432)
    ↓ JSON response
User Browser (sees dashboard)
```

---

### DNS → COSURVIVAL Domains

**Domain mapping:**
- `cosurvival.local` → Development server
- `dashboard.cosurvival.io` → Production dashboard
- `api.cosurvival.io` → API endpoint

**Hierarchical lookup:**
```
User types: dashboard.cosurvival.io
    ↓
Local DNS cache
    ↓
COSURVIVAL DNS server
    ↓
IP address: 203.0.113.42
```

---

## HTTP/HTTPS: COSURVIVAL API Protocol

### Protocol = Agreed Behavior

**Client ↔ Server:**
- Client requests: "Show me TRIBE network graph"
- Server responds: JSON with graph data

### URLs for COSURVIVAL

**Dashboard URLs:**
```
https://dashboard.cosurvival.io/
https://dashboard.cosurvival.io/tribe
https://dashboard.cosurvival.io/teacher
https://dashboard.cosurvival.io/recon
```

**API URLs:**
```
https://api.cosurvival.io/v1/tribe/graph
https://api.cosurvival.io/v1/teacher/recommendations?user_id=user_123
https://api.cosurvival.io/v1/recon/providers?company_id=org_abc
```

**URL Anatomy:**
- **Scheme:** `https://`
- **Host:** `api.cosurvival.io`
- **Path:** `/v1/tribe/graph`
- **Query:** `?user_id=user_123&limit=10`

---

### GET vs POST

**GET - Retrieving data:**
```javascript
// Get TRIBE graph
fetch('https://api.cosurvival.io/v1/tribe/graph')
    .then(response => response.json())
    .then(data => displayGraph(data));
```

**POST - Sending data:**
```javascript
// Submit query
fetch('https://api.cosurvival.io/v1/teacher/recommendations', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({user_id: 'user_123'})
})
    .then(response => response.json())
    .then(data => displayRecommendations(data));
```

---

### HTTP Status Codes for COSURVIVAL

| Code | Meaning | COSURVIVAL Example |
|------|---------|-------------------|
| **200** | OK | Graph data retrieved successfully |
| **301** | Moved | API endpoint changed location |
| **404** | Not Found | User ID doesn't exist |
| **500** | Server Error | SQL query failed |
| **418** | I'm a Teapot | Easter egg in API |

---

## HTML: COSURVIVAL Dashboard Structure

### Skeleton

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <title>COSURVIVAL Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <header>
      <h1>COSURVIVAL</h1>
      <nav>
        <a href="#tribe">TRIBE</a>
        <a href="#teacher">TEACHER</a>
        <a href="#recon">RECON</a>
      </nav>
    </header>
    
    <main>
      <section id="tribe">
        <h2>TRIBE Network</h2>
        <div id="tribe-graph"></div>
      </section>
      
      <section id="teacher">
        <h2>TEACHER Pathways</h2>
        <div id="teacher-recommendations"></div>
      </section>
      
      <section id="recon">
        <h2>RECON Scores</h2>
        <div id="recon-providers"></div>
      </section>
    </main>
    
    <footer>
      <p>Generated at <span id="timestamp"></span></p>
    </footer>
    
    <script src="dashboard.js"></script>
  </body>
</html>
```

---

### Core Tags for COSURVIVAL

**Structure:**
```html
<!-- Headings -->
<h1>COSURVIVAL Dashboard</h1>
<h2>TRIBE Network Analysis</h2>

<!-- Paragraphs -->
<p>This dashboard shows collaboration networks, learning pathways, and provider scores.</p>

<!-- Lists -->
<ul>
  <li>TRIBE: Social network analysis</li>
  <li>TEACHER: Learning pathway recommendations</li>
  <li>RECON: Provider reliability scores</li>
</ul>

<!-- Tables -->
<table>
  <tr>
    <th>Provider</th>
    <th>Reliability</th>
    <th>Grade</th>
  </tr>
  <tr>
    <td>provider_aws</td>
    <td>0.998</td>
    <td>A</td>
  </tr>
</table>

<!-- Links -->
<a href="https://api.cosurvival.io/v1/tribe/graph">View Graph Data</a>

<!-- Images -->
<img src="tribe-network.png" alt="TRIBE collaboration network visualization">

<!-- Forms -->
<form id="query-form">
  <input type="text" name="user_id" placeholder="Enter user ID">
  <button type="submit">Query</button>
</form>
```

---

### Forms + Query Strings

**COSURVIVAL query form:**
```html
<form id="user-query">
  <label for="user-id">User ID:</label>
  <input type="text" id="user-id" name="user_id" required>
  
  <label for="lens">Lens:</label>
  <select id="lens" name="lens">
    <option value="tribe">TRIBE</option>
    <option value="teacher">TEACHER</option>
    <option value="recon">RECON</option>
  </select>
  
  <button type="submit">Query</button>
</form>
```

**Query string generation:**
```javascript
// User submits form
// Generates: ?user_id=user_123&lens=tribe
// API call: /v1/tribe/user?user_id=user_123
```

---

## CSS: COSURVIVAL Dashboard Styling

### Where CSS Lives

**1. Inline (quick tests):**
```html
<div style="background-color: #f0f0f0; padding: 20px;">
  TRIBE Network
</div>
```

**2. `<style>` tag (small dashboards):**
```html
<style>
  .tribe-section {
    background-color: #e3f2fd;
    padding: 20px;
    border-radius: 8px;
  }
</style>
```

**3. External file (production):**
```html
<link rel="stylesheet" href="cosurvival-dashboard.css">
```

---

### Selectors for COSURVIVAL

**Tag selector:**
```css
h1 {
  color: #1976d2;
  font-family: 'Roboto', sans-serif;
}
```

**Class selector:**
```css
.tribe-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
}
```

**ID selector:**
```css
#tribe-graph {
  width: 100%;
  height: 600px;
  border: 1px solid #ccc;
}
```

**Pseudo-class:**
```css
a:hover {
  color: #1976d2;
  text-decoration: underline;
}

.tribe-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
```

---

### COSURVIVAL Color Scheme

```css
:root {
  /* TRIBE colors (blue) */
  --tribe-primary: #1976d2;
  --tribe-light: #e3f2fd;
  
  /* TEACHER colors (green) */
  --teacher-primary: #388e3c;
  --teacher-light: #e8f5e9;
  
  /* RECON colors (orange) */
  --recon-primary: #f57c00;
  --recon-light: #fff3e0;
  
  /* Neutral */
  --background: #f5f5f5;
  --text: #212121;
}
```

---

### Better Semantics (HTML5)

**Instead of `div` everywhere:**
```html
<!-- Old way -->
<div class="header">...</div>
<div class="main">...</div>
<div class="footer">...</div>

<!-- Better way -->
<header>...</header>
<main>...</main>
<footer>...</footer>
```

**Benefits:**
- Accessibility (screen readers)
- SEO (search engines)
- Clarity (code readability)

---

## JavaScript: COSURVIVAL Dashboard Interactivity

### Key Idea

JavaScript can:
- Respond to user events (clicks, form submissions)
- Change HTML dynamically (update graph, show recommendations)
- Change CSS dynamically (highlight active lens, show/hide sections)
- Fetch data from API (load TRIBE/TEACHER/RECON data)

---

### Event Handling

**1. Inline handler (quick tests):**
```html
<button onclick="loadTribeGraph()">Load TRIBE Graph</button>
```

**2. Cleaner (addEventListener):**
```javascript
document.getElementById('tribe-button').addEventListener('click', loadTribeGraph);
```

**3. Even cleaner (DOMContentLoaded):**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    // All DOM elements are ready
    document.getElementById('tribe-button').addEventListener('click', loadTribeGraph);
    document.getElementById('query-form').addEventListener('submit', handleQuery);
});
```

---

### DOM Manipulation

**The web page is a tree in memory. JS edits that tree.**

**Example: Update TRIBE graph:**
```javascript
function displayTribeGraph(data) {
    const graphContainer = document.getElementById('tribe-graph');
    
    // Clear existing content
    graphContainer.innerHTML = '';
    
    // Create new elements
    const canvas = document.createElement('canvas');
    canvas.width = 800;
    canvas.height = 600;
    graphContainer.appendChild(canvas);
    
    // Draw graph (using D3.js or similar)
    drawGraph(canvas, data);
}
```

---

### COSURVIVAL Dashboard Demos

**1. Lens Toggle:**
```javascript
function switchLens(lens) {
    // Hide all sections
    document.querySelectorAll('section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show selected lens
    document.getElementById(lens).style.display = 'block';
    
    // Update active nav link
    document.querySelectorAll('nav a').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`nav a[href="#${lens}"]`).classList.add('active');
    
    // Load data for lens
    loadLensData(lens);
}
```

**2. Dynamic Recommendations:**
```javascript
function displayRecommendations(recommendations) {
    const container = document.getElementById('teacher-recommendations');
    container.innerHTML = '';
    
    recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.innerHTML = `
            <h3>${rec.skill}</h3>
            <p>${rec.reason}</p>
            <span class="priority">${rec.priority}</span>
        `;
        container.appendChild(card);
    });
}
```

**3. Real-time Provider Scores:**
```javascript
function updateProviderScores() {
    fetch('https://api.cosurvival.io/v1/recon/providers')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById('provider-table');
            table.innerHTML = '';
            
            data.providers.forEach(provider => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${provider.name}</td>
                    <td>${provider.reliability.toFixed(3)}</td>
                    <td class="grade-${provider.grade.toLowerCase()}">${provider.grade}</td>
                `;
                table.appendChild(row);
            });
        });
}

// Update every 30 seconds
setInterval(updateProviderScores, 30000);
```

---

## Connecting Front-End to Back-End

### Python API (Flask/FastAPI)

**Simple Flask API:**
```python
from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/v1/tribe/graph')
def get_tribe_graph():
    """Get TRIBE network graph data."""
    db = sqlite3.connect('cosurvival.db')
    db.row_factory = sqlite3.Row
    
    # Query graph data
    rows = db.execute("""
        SELECT 
            u1.id AS user_a,
            u2.id AS user_b,
            COUNT(*) AS collaboration_count
        FROM activities a1
        JOIN activities a2 ON a1.user_id = a2.target_user_id
        WHERE a1.user_id < a1.target_user_id
        GROUP BY a1.user_id, a1.target_user_id
        HAVING collaboration_count >= 5
    """).fetchall()
    
    graph_data = {
        "nodes": get_all_users(),
        "edges": [dict(row) for row in rows]
    }
    
    return jsonify(graph_data)

if __name__ == '__main__':
    app.run(port=5000)
```

**JavaScript fetch:**
```javascript
fetch('http://localhost:5000/v1/tribe/graph')
    .then(response => response.json())
    .then(data => {
        console.log('Graph data:', data);
        displayTribeGraph(data);
    });
```

---

## Security: Client-Side vs Server-Side

### The Danger

**Client-side validation is not security.**

**Why:**
- Users can edit HTML in dev tools
- Users can bypass JavaScript validation
- Malicious users can send direct API requests

**Example:**
```html
<!-- Client-side validation -->
<input type="email" pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$" required>
```

**Problem:** User can remove `required` attribute or change `pattern` in dev tools.

### The Solution

**Always validate server-side:**
```python
@app.route('/v1/teacher/recommendations', methods=['POST'])
def get_recommendations():
    data = request.json
    user_id = data.get('user_id')
    
    # Server-side validation
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    if not is_valid_user_id(user_id):
        return jsonify({'error': 'invalid user_id'}), 400
    
    # Safe to query
    recommendations = get_recommendations(user_id)
    return jsonify(recommendations)
```

**Rule:**
> "Client-side validation = friendly UX. Server-side validation = security."

---

## Micro-Labs (CS50-Style)

### Lab 1: Build COSURVIVAL Dashboard HTML

**Task:** Create HTML structure for dashboard

**Requirements:**
1. Header with navigation (TRIBE/TEACHER/RECON)
2. Three main sections (one per lens)
3. Forms for queries
4. Footer with timestamp

---

### Lab 2: Style with CSS

**Task:** Add CSS styling to dashboard

**Requirements:**
1. Color scheme (TRIBE=blue, TEACHER=green, RECON=orange)
2. Responsive layout (mobile-friendly)
3. Hover effects
4. Card-based design

---

### Lab 3: Add JavaScript Interactivity

**Task:** Make dashboard interactive

**Requirements:**
1. Lens toggle (switch between TRIBE/TEACHER/RECON)
2. Form submission handler
3. Dynamic content updates
4. Loading states

---

### Lab 4: Connect to API

**Task:** Fetch data from Python API

**Requirements:**
1. Create Flask/FastAPI endpoint
2. Return JSON data
3. Fetch from JavaScript
4. Display in dashboard

---

### Lab 5: Build Query Interface

**Task:** Create query form with validation

**Requirements:**
1. User ID input
2. Lens selection
3. Client-side validation (UX)
4. Server-side validation (security)
5. Display results

---

## Assessment: Self-Relative Growth

### Baseline (Before Week 8)

**Question:** "Can you build a web interface for COSURVIVAL?"

**Expected Response:**
- May not understand HTML/CSS/JS
- May not know how to connect to API
- May not understand security

### After Week 8

**Question:** "Can you build an interactive COSURVIVAL dashboard?"

**Expected Response:**
- Can build HTML structure
- Can style with CSS
- Can add JavaScript interactivity
- Can connect to Python API
- Can validate input securely

---

## Key Takeaways

1. **Internet protocols enable web apps.** HTTP/HTTPS connects front-end to back-end.

2. **HTML provides structure.** Semantic HTML improves accessibility and SEO.

3. **CSS provides style.** Consistent styling creates professional dashboards.

4. **JavaScript provides interactivity.** Dynamic updates create engaging experiences.

5. **Client-side validation = UX, not security.** Always validate server-side.

6. **Connect front-end to back-end.** Python API + SQL + JavaScript = full-stack app.

7. **Different tools for different jobs.** HTML for structure, CSS for style, JS for behavior.

---

## Next Steps

**Capstone:** Full-Stack COSURVIVAL Application
- Build complete dashboard
- Connect to SQL database
- Add authentication
- Deploy to production

**For Now:** Practice web foundations:
- Build HTML structure
- Style with CSS
- Add JavaScript interactivity
- Connect to API

---

## Resources

- **dashboard.html:** See dashboard structure
- **extractors/rapid_pipeline.py:** See Python API
- **curriculum/:** See all week modules

---

*"This week is the front-end + protocol foundation. Next week you'll connect Python + SQL + HTML + CSS + JS into full web apps."*
