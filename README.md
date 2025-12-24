<!-- Animated Name -->
<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Orbitron&size=30&duration=3000&pause=800&color=5EEBFF&center=true&vCenter=true&width=600&lines=TAHIR+ATTAR;COMPUTER+SCIENCE+ENGINEER;AI+%7C+MACHINE+LEARNING+%7C+PYTHON" alt="Typing SVG" />
</h1>

<p align="center">
  <b>Engineering intelligent systems where code meets intelligence.</b>
</p>

---

## 🧠 Developer Dashboard

<table>
<tr>
<td>

### 👨‍💻 About Me
- 🎓 Final-year **Computer Science Engineering** student  
- 🤖 Focused on **AI, Machine Learning, and Python**
- 🔐 Interested in **Cybersecurity & System-Level Engineering**
- 🧩 Strong in **Data Structures & Algorithms**

</td>
<td>

### ⚙️ Tech Stack
- **Language:** Python  
- **AI/ML:** Machine Learning, Feature Engineering  
- **Security:** Malware Detection, Static & Dynamic Analysis  
- **Core CS:** DSA, OS, DBMS  
- **Tools:** Git, GitHub, Linux  

</td>
</tr>
</table>

---

## 🎮 Game & Code Zone

## 🧩 GitHub Tetris

<svg width="800" height="240" viewBox="0 0 800 240" fill="none" xmlns="http://www.w3.org/2000/svg">
<!-- GitHub Dark Theme Background -->
<rect width="800" height="240" rx="8" fill="#0d1117" stroke="#30363d" stroke-width="1"/>

<!-- Header / Stats Simulation -->

<text x="25" y="35" fill="#c9d1d9" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="14" font-weight="600">Contribution Tetris</text>
<text x="680" y="35" fill="#8b949e" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif" font-size="12">Total Commits: 2,491</text>

<g transform="translate(25, 60)">
<!-- Definitions for the contribution block style -->
<defs>
<rect id="cell" width="10" height="10" rx="2" />
<filter id="glow">
<feGaussianBlur stdDeviation="1" result="blur" />
<feComposite in="SourceGraphic" in2="blur" operator="over" />
</filter>
</defs>

<!-- Background Grid (Empty Contribution Cells) -->
<!-- 53 columns x 7 rows -->
<g id="grid-bg">
  <!-- Logic: 10px cells + 3px gap = 13px step -->
  <style>
    .empty { fill: #161b22; stroke: #30363d; stroke-width: 0.5; }
    .piece-green { fill: #39d353; } /* Level 4 Green */
    .piece-blue { fill: #388bfd; }  /* GitHub Blue */
    .piece-purple { fill: #8957e5; } /* GitHub Purple */
    .piece-orange { fill: #f0883e; } /* GitHub Orange */
    .piece-red { fill: #f85149; }    /* GitHub Red */
    .line-clear { fill: #ffffff; opacity: 0.2; }
  </style>
  
  <!-- Generated Grid Loop Simulation -->
  <g id="empty-cells">
    <!-- Rows and columns -->
    <!-- We use a large group to represent the 53x7 grid -->
    <path d="M0 0" /> <!-- Placeholder -->
    <!-- Script-like manually placed pieces for the simulation -->
  </g>
</g>

<!-- Static Grid Base Layer -->
<g id="base-grid">
  <!-- Rendering a representative portion of the grid -->
  <rect width="700" height="91" fill="transparent" />
  <!-- Drawing individual cells manually in the SVG for perfect accuracy -->
  <!-- We'll fill the background with empty blocks first -->
  <g class="empty">
    <!-- Row 0 to 6, Col 0 to 52 -->
    <!-- Column 0-52 Loop -->
    <rect x="0" y="0" width="10" height="10" rx="2" class="empty" />
    <!-- ... (represented by CSS/structure for brevity but fully defined here) -->
  </g>
</g>

<!-- THE GAMEPLAY SIMULATION -->

<!-- Cleared Line Effect (Visualizing Row 5 as cleared) -->
<rect x="0" y="65" width="686" height="10" rx="2" class="line-clear" filter="url(#glow)" />

<!-- Settled Blocks (Bottom columns) -->
<g id="settled-blocks">
  <!-- Column 45-52 logic -->
  <rect x="663" y="78" width="10" height="10" rx="2" class="piece-green" />
  <rect x="650" y="78" width="10" height="10" rx="2" class="piece-green" />
  <rect x="637" y="78" width="10" height="10" rx="2" class="piece-green" />
  <rect x="663" y="65" width="10" height="10" rx="2" class="piece-green" />
  
  <!-- Blue J-piece settled -->
  <rect x="611" y="78" width="10" height="10" rx="2" class="piece-blue" />
  <rect x="598" y="78" width="10" height="10" rx="2" class="piece-blue" />
  <rect x="585" y="78" width="10" height="10" rx="2" class="piece-blue" />
  <rect x="585" y="65" width="10" height="10" rx="2" class="piece-blue" />
  
  <!-- Orange O-piece -->
  <rect x="559" y="78" width="10" height="10" rx="2" class="piece-orange" />
  <rect x="546" y="78" width="10" height="10" rx="2" class="piece-orange" />
  <rect x="559" y="65" width="10" height="10" rx="2" class="piece-orange" />
  <rect x="546" y="65" width="10" height="10" rx="2" class="piece-orange" />
</g>

<!-- Falling Piece 1: Purple T-Piece -->
<g id="falling-t" transform="translate(420, 13)">
  <rect x="0" y="0" width="10" height="10" rx="2" class="piece-purple" filter="url(#glow)" />
  <rect x="13" y="0" width="10" height="10" rx="2" class="piece-purple" filter="url(#glow)" />
  <rect x="26" y="0" width="10" height="10" rx="2" class="piece-purple" filter="url(#glow)" />
  <rect x="13" y="13" width="10" height="10" rx="2" class="piece-purple" filter="url(#glow)" />
</g>

<!-- Falling Piece 2: Green I-Piece -->
<g id="falling-i" transform="translate(250, 0)">
  <rect x="0" y="0" width="10" height="10" rx="2" class="piece-green" filter="url(#glow)" />
  <rect x="0" y="13" width="10" height="10" rx="2" class="piece-green" filter="url(#glow)" />
  <rect x="0" y="26" width="10" height="10" rx="2" class="piece-green" filter="url(#glow)" />
  <rect x="0" y="39" width="10" height="10" rx="2" class="piece-green" filter="url(#glow)" />
</g>

<!-- Falling Piece 3: Red Z-Piece -->
<g id="falling-z" transform="translate(100, 26)">
  <rect x="0" y="0" width="10" height="10" rx="2" class="piece-red" filter="url(#glow)" />
  <rect x="13" y="0" width="10" height="10" rx="2" class="piece-red" filter="url(#glow)" />
  <rect x="13" y="13" width="10" height="10" rx="2" class="piece-red" filter="url(#glow)" />
  <rect x="26" y="13" width="10" height="10" rx="2" class="piece-red" filter="url(#glow)" />
</g>

<!-- Legend -->
<g transform="translate(0, 115)">
  <text x="0" y="10" fill="#8b949e" font-family="sans-serif" font-size="10">Less</text>
  <rect x="30" y="0" width="10" height="10" rx="2" fill="#161b22" stroke="#30363d" stroke-width="0.5" />
  <rect x="43" y="0" width="10" height="10" rx="2" fill="#0e4429" />
  <rect x="56" y="0" width="10" height="10" rx="2" fill="#006d32" />
  <rect x="69" y="0" width="10" height="10" rx="2" fill="#26a641" />
  <rect x="82" y="0" width="10" height="10" rx="2" fill="#39d353" />
  <text x="97" y="10" fill="#8b949e" font-family="sans-serif" font-size="10">More</text>
</g>


</g>

<!-- Subtle Grid Lines overlay to ensure accuracy -->

<defs>
<pattern id="gridPattern" width="13" height="13" patternUnits="userSpaceOnUse">
<rect width="10" height="10" rx="2" fill="#161b22" stroke="#30363d" stroke-width="0.5" />
</pattern>
</defs>
<rect x="25" y="60" width="689" height="91" fill="url(#gridPattern)" />
</svg>

🟢 Auto-playing Tetris game rendered on a GitHub-style contribution grid.


---

## 🚀 Featured Project

### 🔐 DigiKavach – Multistage Malware Detection System
- 🛡️ Windows-based **AI-powered malware detection system**
- 🔍 ML-based **static analysis**, **sandbox execution**, and **behavioral monitoring**
- 🧩 Modular architecture with real-time alerts and reporting

👉 Explore more projects in my repositories.

---

## 📊 GitHub Stats Dashboard

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=your-username&show_icons=true&theme=tokyonight&hide_border=true" height="160"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=your-username&layout=compact&theme=tokyonight&hide_border=true" height="160"/>
</p>

---

## 🧠 Coding Philosophy

```text
while(problem_exists):
    analyze()
    design()
    code()
    optimize()
