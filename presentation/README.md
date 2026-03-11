# AI Agents Presentations

Two reveal.js presentations — pick the one that fits your audience.

## Files

| File | Audience | Slides | Focus |
|------|----------|--------|-------|
| `index.html` | Technical deep-dive | ~20 | Full system: teams, providers, setup, CI/CD |
| `article.html` | Blog / talk intro | 14 | Article walk-through: why, what, payoff |

## Quick Start

### Option 1: Open in Browser (Recommended)
```bash
# Article presentation (blog-style, shorter)
open presentation/article.html

# Technical deep-dive
open presentation/index.html

# Or serve locally
python3 -m http.server 8000
# Then visit: http://localhost:8000/presentation/article.html
```

### Option 2: View Online
Both presentations use CDN-hosted reveal.js — internet connection required.

## Keyboard Controls

| Key | Action |
|-----|--------|
| `→` / `Space` | Next slide |
| `←` | Previous slide |
| `↑` / `↓` | Navigate vertical slides |
| `ESC` | Slide overview |
| `F` | Fullscreen |
| `S` | Speaker notes |
| `B` | Pause (black screen) |
| `?` | Help |

## Presentation Structure

1. **Introduction** - The multi-agent approach
2. **The Problem** - Why single agents fail
3. **The Solution** - Architecture & components
4. **20 Specialized Skills** - Team breakdown
5. **Critic Loop** - Self-correction mechanism
6. **Memory System** - Persistent context
7. **CLI Interface** - How to use it
8. **Model Selection** - Right tool per task
9. **Example Workflow** - REST API case study
10. **Best Practices** - DO's and DON'Ts
11. **When to Use** - Comparisons
12. **Key Takeaways** - Summary
13. **Call to Action** - Getting started

## Sections with Vertical Navigation

The following sections have sub-slides (press ↓ to navigate):

- The Problem (2 sub-slides)
- The Solution (2 sub-slides)
- 20 Specialized Skills (1 sub-slide)
- Critic Loop (3 sub-slides)
- Memory System (3 sub-slides)
- CLI Interface (5 sub-slides)
- Model Selection (1 large table)
- Example Workflow (3 sub-slides)
- Best Practices (2 sub-slides)

## Customization

To modify the presentation:

1. **Colors**: Edit the CSS `<style>` section
2. **Themes**: Change `black.min.css` to other themes:
   - `white.min.css`
   - `league.min.css`
   - `sky.min.css`
   - `beige.min.css`
   - `simple.min.css`
   - `serif.min.css`
   - `blood.min.css`
   - `night.min.css`
   - `moon.min.css`
   - `solarized.min.css`

3. **Content**: Edit the HTML in the `<section>` tags

## Presenter View

Press `S` during presentation to open speaker notes (if available).

## Export to PDF

Via reveal.js:
1. Add `?print-pdf` to URL: `index.html?print-pdf`
2. Print to PDF from browser (Cmd+P / Ctrl+P)

Example:
```bash
# Open in browser with ?print-pdf
open "index.html?print-pdf"
# Then print to PDF
```

## Tips for Presenting

1. **Practice timing**: Allow 1-2 min per main section
2. **Use ESC**: For slide overview before jumping to specific slide
3. **Pause with B**: Black screen to refocus audience
4. **Resize for comfort**: Most browsers support zoom (Cmd+/Ctrl+)
5. **Full screen**: Press F for distraction-free mode

## Slide Timing

- Intro → Problem: 2 min
- Problem → Solution: 3 min
- Architecture & Skills: 3 min
- Critic Loop & Memory: 3 min
- CLI & Usage: 3 min
- Models & Example: 2 min
- Best Practices & Takeaways: 2 min
- **Total: ~20 minutes** (comfortable for Q&A)

## Adding Speaker Notes

To add speaker notes, add this inside any `<section>`:

```html
<aside class="notes">
  Speaker notes here
</aside>
```

Then press `S` during presentation to see notes in speaker view.

## Troubleshooting

**Slides not loading?**
- Check internet connection (reveal.js loads from CDN)
- Or download reveal.js locally and update script src

**Fonts look wrong?**
- Ensure browser zoom is at 100%
- Try different browser (Chrome/Safari/Firefox)

**Navigation stuck?**
- Press ESC to reset
- Reload page (F5)

## Next Steps

1. Open in browser with `open index.html`
2. Navigate with arrow keys or space
3. Practice presenting!
4. Share with the team

---

**Built with**: [reveal.js](https://revealjs.com/)  
**Format**: HTML5 + CSS + JavaScript  
**No dependencies**: Works offline after first load
