# Chief Of Flow App — UI Style Guide

> **Technical Implementation Guide**  
> This document provides the exact technical specifications for implementing the UI design vision outlined in `Front_End_Details.md`. It includes color codes, Tailwind classes, typography scales, and ready-to-use code snippets for developers.

---

## 1. Fonts & Typography

**Font Family:**  
`Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;`

### Font Sizes & Weights

| Element                  | Tailwind Class            | Size/Weight   |
| ------------------------ | ------------------------- | ------------- |
| Header ("CHIEF OF FLOW") | `text-3xl font-bold`      | 30px / Bold   |
| Section Title ("To Do")  | `text-xl font-semibold`   | 20px / Semi   |
| Block Heading            | `text-base font-semibold` | 16px / Semi   |
| Task Items               | `text-base font-normal`   | 16px / Normal |
| Input Placeholder        | `text-sm font-normal`     | 14px / Normal |
| Bottom Nav (active)      | `text-sm font-semibold`   | 14px / Semi   |
| Bottom Nav (inactive)    | `text-sm font-normal`     | 14px / Normal |

---

## 2. Color Palette & Project Mapping

### Core Colors

| Color Name          | Tailwind Class        | Hex       | Usage                          |
| ------------------- | --------------------- | --------- | ------------------------------ |
| Orange Heading      | `bg-orange-heading`   | `#FFECB5` | Project block headers          |
| Orange Background   | `bg-orange-light`     | `#FFF5E1` | Project block backgrounds      |
| Blue Heading        | `bg-blue-heading`     | `#D2EAFD` | Project block headers          |
| Blue Background     | `bg-blue-light`       | `#EBF6FE` | Project block backgrounds      |
| Lavender Heading    | `bg-lavender-heading` | `#E6D9FA` | Project block headers          |
| Lavender Background | `bg-lavender-light`   | `#F5EEFD` | Project block backgrounds      |
| Text (dark gray)    | `text-text-dark`      | `#1F2937` | Primary text                   |
| Light Gray Text     | `text-light-gray`     | `#6B7280` | Placeholders, inactive states  |
| Nav Active          | `text-nav-active`     | `#111827` | Active navigation items        |
| Accent Blue         | `text-accent-blue`    | `#3B82F6` | Mic icon, interactive elements |
| Borders             | `border-border-light` | `#E5E7EB` | Card borders, dividers         |

### Project Color-Coding System

The orange/blue/lavender color scheme implements the "color-coded by project" vision from Front_End_Details.md:

- **Orange**: Work/Professional projects
- **Blue**: Personal/Lifestyle projects  
- **Lavender**: Creative/Learning projects

*Note: Users can configure project color assignments in their `Memory/Instructions.md` preferences.*

---

## 3. Spacing & Layout Standards

### Padding & Margins

| Element Type        | Tailwind Class | Pixels | Usage                        |
| ------------------- | -------------- | ------ | ---------------------------- |
| Screen Container    | `px-4`         | 16px   | Main horizontal padding      |
| Header Top Margin   | `mt-6`         | 24px   | Top spacing for main header  |
| Section Spacing     | `mt-4`         | 16px   | Between sections             |
| Card Spacing        | `mt-2`         | 8px    | Between cards in same section|
| Card Internal       | `px-3 py-3`    | 12px   | Inside card content          |
| Card Header         | `px-3 py-2`    | 12px/8px | Card header padding        |
| Task Item Height    | `h-10`         | 40px   | Consistent task row height   |
| Task Item Spacing   | `space-y-2`    | 8px    | Between task items           |
| Input Field         | `px-4 py-2`    | 16px/8px | Ask field padding          |
| Bottom Nav          | `py-3`         | 12px   | Navigation bar padding       |

---

## 4. Interactive States

### Button & Interactive Element States

```css
/* Hover States */
.task-checkbox:hover {
  @apply border-accent-blue;
}

.nav-button:hover {
  @apply text-nav-active;
}

.card-block:hover {
  @apply shadow-lg transition-shadow duration-200;
}

/* Active States */
.nav-button-active {
  @apply text-nav-active font-semibold;
}

.nav-button-inactive {
  @apply text-light-gray font-normal hover:text-nav-active transition-colors duration-200;
}

/* Focus States */
.input-field:focus {
  @apply outline-none ring-2 ring-accent-blue ring-opacity-50;
}
```

### Task Completion Animation

```css
.task-completed {
  @apply opacity-50 line-through transition-all duration-300;
}
```

---

## 5. Tailwind Config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        "orange-light":     "#FFF5E1",
        "orange-heading":   "#FFECB5",
        "blue-light":       "#EBF6FE",
        "blue-heading":     "#D2EAFD",
        "lavender-light":   "#F5EEFD",
        "lavender-heading": "#E6D9FA",
        "text-dark":        "#1F2937",
        "text-light-gray":  "#6B7280",
        "nav-active":       "#111827",
        "border-light":     "#E5E7EB",
        "accent-blue":      "#3B82F6",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "sans-serif"],
      },
      fontSize: {
        "3xl": "1.875rem", // 30px
        "xl": "1.25rem",   // 20px
        "base": "1rem",    // 16px
        "sm": "0.875rem",  // 14px
      },
      boxShadow: {
        "card": "0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)",
        "askfield": "0 4px 8px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06)",
      },
      borderRadius: {
        lg: "0.5rem",
        full: "9999px",
      },
      transitionDuration: {
        '200': '200ms',
        '300': '300ms',
      }
    },
  },
  plugins: [],
};
```

---

## 6. Component Code Examples

### Screen Container
```html
<div class="min-h-screen bg-white px-4">
  <!-- Content -->
</div>
```

### Main Header
```html
<h1 class="mt-6 text-3xl font-bold text-text-dark font-sans">
  CHIEF OF FLOW
</h1>
```

### Section Title
```html
<h2 class="mt-4 text-xl font-semibold text-text-dark">
  To Do
</h2>
```

### Project Block Card (Orange Example)
```html
<div class="mt-2 bg-orange-light rounded-lg shadow-card hover:shadow-lg transition-shadow duration-200">
  <div class="bg-orange-heading rounded-t-lg px-3 py-2">
    <span class="text-base font-semibold text-text-dark">
      Morning Routine
    </span>
  </div>
  <div class="px-3 py-3 space-y-2">
    <div class="flex items-center h-10">
      <div class="w-5 h-5 border-2 border-gray-400 rounded-sm hover:border-accent-blue transition-colors duration-200 cursor-pointer"></div>
      <span class="ml-3 text-base font-normal text-text-dark">Coffee</span>
    </div>
    <!-- Repeat for each task -->
  </div>
</div>
```

### "Ask me stuff…" Input Field
```html
<div class="mt-6 w-full bg-white rounded-full shadow-askfield px-4 py-2 flex items-center">
  <input
    type="text"
    placeholder="Ask me stuff…"
    class="flex-1 bg-transparent text-sm font-normal text-light-gray focus:outline-none focus:ring-2 focus:ring-accent-blue focus:ring-opacity-50"
  />
  <svg
    xmlns="http://www.w3.org/2000/svg"
    class="w-6 h-6 text-accent-blue hover:text-blue-600 transition-colors duration-200 cursor-pointer"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
  >
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
      d="M12 1.75a3 3 0 00-3 3v6a3 3 0 006 0v-6a3 3 0 00-3-3zM19.5 10a.75.75 0 01.75.75v1.5a7.5 7.5 0 01-15 0v-1.5a.75.75 0 011.5 0v1.5a6 6 0 0012 0v-1.5a.75.75 0 01.75-.75z" />
  </svg>
</div>
```

### Bottom Navigation
```html
<div class="mt-6 border-t border-border-light bg-white">
  <div class="flex justify-around py-3">
    <button class="nav-button nav-button-active">ToDo</button>
    <button class="nav-button nav-button-inactive">Schedule</button>
    <button class="nav-button nav-button-inactive">Life</button>
  </div>
</div>
```

### Task Item with Completion State
```html
<div class="flex items-center h-10 group">
  <div class="w-5 h-5 border-2 border-gray-400 rounded-sm hover:border-accent-blue transition-colors duration-200 cursor-pointer"></div>
  <span class="ml-3 text-base font-normal text-text-dark group-hover:text-accent-blue transition-colors duration-200">
    Task name
  </span>
</div>
```

---

## 7. Responsive Considerations

### Breakpoints
- **Mobile-first approach**: Base styles for mobile (320px+)
- **Tablet**: Use `md:` prefix for 768px+
- **Desktop**: Use `lg:` prefix for 1024px+

### Key Responsive Adjustments
```html
<!-- Responsive padding -->
<div class="px-4 md:px-6 lg:px-8">

<!-- Responsive text sizes -->
<h1 class="text-2xl md:text-3xl font-bold">

<!-- Responsive spacing -->
<div class="mt-4 md:mt-6">
```

---

## 8. Accessibility Standards

### Color Contrast
- All text meets WCAG AA standards (4.5:1 contrast ratio)
- Interactive elements have clear focus states
- Color is never the only way to convey information

### Keyboard Navigation
```css
.focusable:focus {
  @apply outline-none ring-2 ring-accent-blue ring-opacity-50;
}
```

### Screen Reader Support
```html
<!-- Always include appropriate ARIA labels -->
<button aria-label="Mark task as complete">
  <div class="w-5 h-5 border-2 border-gray-400 rounded-sm"></div>
</button>
```

---

*This style guide implements the design vision from `Front_End_Details.md` with pixel-perfect precision, ensuring a consistent, accessible, and delightful user experience across all devices.* 