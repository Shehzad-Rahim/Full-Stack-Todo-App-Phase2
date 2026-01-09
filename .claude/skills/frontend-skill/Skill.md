---
name: frontend-pages-components
description: Build responsive frontend pages, reusable components, and layouts with modern styling techniques. Use for web application and website UI development.
---

# Frontend Pages, Components, and Layouts

## Instructions

1. **Page structure**
   - Semantic HTML5 layout
   - Clear hierarchy (header, main, footer)
   - Accessibility-first markup

2. **Components**
   - Reusable UI components (buttons, cards, forms)
   - Component-based structure
   - Consistent spacing and typography

3. **Layouts**
   - Responsive grid or flexbox layouts
   - Mobile-first design
   - Adaptive breakpoints for tablet and desktop

4. **Styling**
   - Modern CSS (Flexbox, Grid)
   - Design tokens for colors and spacing
   - Scalable class naming (BEM or utility-based)

## Best Practices
- Prioritize readability and accessibility
- Keep components small and reusable
- Use consistent spacing and font scales
- Test layouts across multiple screen sizes
- Avoid inline styles; prefer reusable classes

## Example Structure
```html
<main class="page">
  <header class="page-header">
    <h1 class="page-title">Page Title</h1>
  </header>

  <section class="content-grid">
    <article class="card">
      <h2 class="card-title">Component Title</h2>
      <p class="card-text">Component description text.</p>
      <button class="btn-primary">Action</button>
    </article>
  </section>
</main>
