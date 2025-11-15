# UI Structure Document

## Overview
**Feature**: Benchmark Detail View with Visual Stats Dashboard
**Framework**: Phoenix LiveView 1.0.x
**Styling**: Tailwind CSS 3.x
**Complexity**: Moderate

## Framework Context

**Detected**:
- Framework: Phoenix LiveView 1.0+ (from mix.exs)
- Language: Elixir 1.14
- Build Tool: Mix with esbuild
- Tailwind Version: 3.x with @tailwindcss/forms plugin
- Icons: Heroicons integrated via Tailwind plugin

**Patterns**:
- Component syntax: HEEx function components (`<.component>`)
- State management: LiveView assigns (`@benchmark`)
- Event handling: `phx-click`, `phx-change`, `phx-hook`
- Styling approach: Utility-first Tailwind
- No JavaScript hooks directory yet (needs creation)

## Design System Mapping

### Loaded Patterns
**Files Found**:
- `card.json` → Card component patterns (use for chart containers)
- `table.json` → Table component patterns (used in prompts table, keep as-is)
- `navbar.json` → Navigation patterns (not relevant for this feature)

**Chart Library**:
- ApexCharts via CDN (not npm) - loaded in root layout

### Component Mapping

**Chart Cards** (Standard - NEW)
- **Design System**: `card.json` → `patterns.card_container`
- **Variant**: Base card without button
- **Patterns Used**:
  - Container: `max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm`
  - Title: `mb-2 text-2xl font-bold tracking-tight text-gray-900` (adapted for H3 as chart title)
  - Chart container: Custom div for ApexCharts render target
- **Interactive**: `phx-hook="ApexChart"` for client-side rendering
- **Composition**: H3 heading + chart div inside card_container

**Outer Stats Container** (Existing - KEEP)
- **Design System**: Existing pattern from line 25: `bg-gray-50 rounded-lg p-6`
- **Variant**: Gray background section container
- **Usage**: Wraps entire stats dashboard with section heading

**Header Section** (Existing - KEEP)
- **Design System**: Phoenix CoreComponents `.header` with actions
- **Location**: Lines 2-13
- **No changes needed**

**Table Component** (Existing - KEEP)
- **Design System**: `table.json` patterns via Phoenix CoreComponents `.table`
- **Location**: Lines 80-108
- **No changes needed**

## Component Hierarchy

### Stats Dashboard Section (REDESIGN TARGET - Lines 24-65)

**Semantic Structure**:
```
div.bg-gray-50.rounded-lg.p-6 > (
  h2.text-lg.font-semibold.text-gray-900.mb-6 +
  div.grid.grid-cols-1.md:grid-cols-3.gap-6 > (
    div.max-w-sm.p-6.bg-white.border.border-gray-200.rounded-lg.shadow-sm > (
      h3.mb-2.text-sm.font-bold.tracking-tight.text-gray-900.uppercase +
      div[phx-hook="ApexChart"][data-chart-id="difficulty-chart"][data-chart-config="{...}"]
    ) +
    div.max-w-sm.p-6.bg-white.border.border-gray-200.rounded-lg.shadow-sm > (
      h3.mb-2.text-sm.font-bold.tracking-tight.text-gray-900.uppercase +
      div[phx-hook="ApexChart"][data-chart-id="category-chart"][data-chart-config="{...}"]
    ) +
    div.max-w-sm.p-6.bg-white.border.border-gray-200.rounded-lg.shadow-sm > (
      h3.mb-2.text-sm.font-bold.tracking-tight.text-gray-900.uppercase +
      div[phx-hook="ApexChart"][data-chart-id="split-chart"][data-chart-config="{...}"]
    )
  )
)
```

**Breakdown**:
- **Outer Container**: Gray card (`bg-gray-50 rounded-lg p-6`) matching existing description section
- **Section Heading**: "Prompt Statistics" H2 (keep existing styling)
- **Grid Layout**: 3-column on desktop (`md:grid-cols-3`), single column stack on mobile
- **Chart Cards**: Use `card_container` pattern from card.json
  - `max-w-sm` removed in grid context (let grid control width)
  - White background with border and shadow
  - Consistent padding (`p-6`)
- **Chart Headings**: "DIFFICULTY", "CATEGORY", "SPLIT"
  - Adapted card_title pattern to H3 with smaller font (`text-sm` instead of `text-2xl`)
  - Uppercase styling added
- **Chart Containers**: Divs with `phx-hook="ApexChart"` for client-side rendering
  - `data-chart-id`: Unique identifier for chart instance
  - `data-chart-config`: JSON-encoded chart configuration with data

**Data Flow**:
```elixir
# In HEEx template, encode chart config as JSON
data-chart-config={Jason.encode!(%{
  data: Enum.map(@benchmark.difficulty_counts, fn {k, v} ->
    %{x: humanize_difficulty(k), y: v}
  end),
  horizontal: true
})}
```

**Responsive Behavior**:
- Mobile (< 768px): Charts stack vertically, `max-w-sm` allows cards to center
- Desktop (768px+): 3-column grid, cards expand to fill grid cells
- Chart height: Fixed 200px for visual consistency across all three charts

### Header Section (UNCHANGED - Lines 2-13)
**Keep existing**: `.header` component with Edit and Add Prompt buttons

### Description Section (UNCHANGED - Lines 17-22)
**Keep existing**: Conditional gray card with description text

### Prompts Table Section (UNCHANGED - Lines 67-111)
**Keep existing**: `.table` component with reviews column

## Responsive Strategy

### Breakpoints (Tailwind defaults)
- **Mobile (< 768px)**: Single column stack, cards with `max-w-sm` center naturally
- **Desktop (768px+)**: 3-column grid layout, cards expand to fill

### Mobile-First Approach
Base styles target mobile, desktop enhances:
```
grid grid-cols-1      → Stack by default
md:grid-cols-3        → 3 columns on medium+
gap-6                 → Consistent spacing
```

**Chart Responsiveness**:
- ApexCharts `responsive: [{breakpoint: 768, options: {...}}]` for mobile adjustments
- Fixed height: 200px across all breakpoints for consistency
- Horizontal bars scale better on mobile than vertical

## Interactivity Specifications

### State Requirements

**Charts** (Static Display):
- **State**: None (charts render once on mount, no interactive state)
- **Data Source**:
  - `@benchmark.difficulty_counts` → `%{easy: int, medium: int, hard: int, very_hard: int}`
  - `@benchmark.category_counts` → `%{open_ended: int, summarization: int, hypothetical: int}`
  - `@benchmark.split_counts` → `%{public: int, eval: int, test: int}`
- **Updates**: Only on page navigation (mount/handle_params)
- **No real-time updates**: Charts are snapshot of current data

**Framework Pattern**:
```javascript
// Phoenix LiveView Hook: assets/js/hooks/apex_chart.js
export const ApexChart = {
  mounted() {
    const config = JSON.parse(this.el.dataset.chartConfig)
    const chartOptions = {
      chart: {
        type: 'bar',
        height: 200,
        toolbar: { show: false }
      },
      plotOptions: {
        bar: {
          horizontal: true,
          distributed: true
        }
      },
      dataLabels: { enabled: true },
      series: [{
        name: 'Count',
        data: config.data
      }],
      colors: config.colors || ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
      xaxis: {
        title: { text: 'Number of Prompts' }
      },
      legend: { show: false }
    }

    this.chart = new ApexCharts(this.el, chartOptions)
    this.chart.render()
  },
  destroyed() {
    this.chart && this.chart.destroy()
  }
}
```

### Data Requirements

**Static from Assigns**:
- All chart data passed via LiveView assigns (already calculated in mount/handle_params)
- No API calls needed
- Data structure already exists in LiveView

**Chart Configuration Structure**:
```javascript
// Passed via data-chart-config attribute
{
  data: [
    { x: 'Easy', y: 10 },
    { x: 'Medium', y: 25 },
    { x: 'Hard', y: 8 },
    { x: 'Very Hard', y: 2 }
  ],
  colors: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
}
```

## Accessibility Specifications

### Semantic HTML
- Use `<div>` for chart containers (no semantic alternative for data visualizations)
- Maintain heading hierarchy: H2 for "Prompt Statistics", H3 for chart types
- Keep existing page structure (landmarks unchanged)

### ARIA Patterns

**Chart Containers**:
```html
<div
  phx-hook="ApexChart"
  data-chart-id="difficulty-chart"
  data-chart-config="{...}"
  role="img"
  aria-label="Bar chart showing difficulty distribution: 10 easy, 25 medium, 8 hard, 2 very hard prompts">
</div>
```

**Text Alternatives**:
- Include descriptive `aria-label` on each chart container
- Label format: "Bar chart showing [dimension] distribution: [data summary]"
- Example: "Bar chart showing category distribution: 30 open-ended, 10 summarization, 5 hypothetical prompts"

### Keyboard Navigation
- Not required (charts are static visualizations, not interactive)
- Existing navigation (Edit/Add buttons, table links) remains keyboard accessible

## Context for Generation

### Design System Patterns to Use

**From card.json**:
```json
{
  "card_container": "max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow-sm",
  "card_title": "mb-2 text-2xl font-bold tracking-tight text-gray-900"
}
```

**Adapted for Chart Cards**:
- Container: Remove `max-w-sm` in grid context (grid controls width)
- Title: Use `text-sm` instead of `text-2xl`, add `uppercase`
- Full pattern: `p-6 bg-white border border-gray-200 rounded-lg shadow-sm`

**From Existing Code**:
```json
{
  "gray_section": "bg-gray-50 rounded-lg p-6",
  "section_heading": "text-lg font-semibold text-gray-900 mb-6",
  "grid_layout": "grid grid-cols-1 md:grid-cols-3 gap-6"
}
```

**Color Palette for Charts**:
- Blue: `#3b82f6` (Tailwind blue-500)
- Green: `#10b981` (Tailwind green-500)
- Amber: `#f59e0b` (Tailwind amber-500)
- Red: `#ef4444` (Tailwind red-500)

## Framework-Specific Constraints

### Phoenix LiveView

**Template Syntax**:
- HEEx: `<%= %>` for expressions, `<% %>` for control flow
- Function components: Use existing CoreComponents
- Pass data via assigns: `@benchmark.difficulty_counts`
- JavaScript hooks: `phx-hook="ApexChart"` on chart containers
- Data attributes: Use `data-*` for passing config to hooks
- JSON encoding: Use `Jason.encode!/1` for complex data structures

**HEEx Template Pattern**:
```heex
<div
  phx-hook="ApexChart"
  data-chart-id="difficulty-chart"
  data-chart-config={Jason.encode!(%{
    data: Enum.map(@benchmark.difficulty_counts, fn {k, v} ->
      %{x: humanize_difficulty(k), y: v}
    end),
    colors: ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]
  })}
  role="img"
  aria-label={"Bar chart showing difficulty distribution: #{format_counts(@benchmark.difficulty_counts)}"}>
</div>
```

### ApexCharts Integration (CDN)

**Load in Root Layout** (`lib/chapter_ai_web/components/layouts/root.html.heex`):
```html
<script src="https://cdn.jsdelivr.net/npm/apexcharts@3.45.0/dist/apexcharts.min.js"></script>
```

**Hook Registration** (`assets/js/app.js`):
```javascript
// Import hooks
import { ApexChart } from "./hooks/apex_chart"

let Hooks = { ApexChart }

let liveSocket = new LiveSocket("/live", Socket, {
  longPollFallbackMs: 2500,
  params: {_csrf_token: csrfToken},
  hooks: Hooks  // Add hooks here
})
```

**Hook Implementation** (`assets/js/hooks/apex_chart.js`):
```javascript
export const ApexChart = {
  mounted() {
    // ApexCharts loaded from CDN, available globally
    const config = JSON.parse(this.el.dataset.chartConfig)

    const chartOptions = {
      chart: {
        type: 'bar',
        height: 200,
        toolbar: { show: false }
      },
      plotOptions: {
        bar: {
          horizontal: true,
          distributed: true
        }
      },
      dataLabels: { enabled: true },
      series: [{
        name: 'Count',
        data: config.data
      }],
      colors: config.colors || ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
      xaxis: {
        title: { text: 'Number of Prompts' }
      },
      legend: { show: false }
    }

    this.chart = new ApexCharts(this.el, chartOptions)
    this.chart.render()
  },

  destroyed() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
```

## Generation Instructions

**For ui-generate agent**:

1. **Add ApexCharts CDN to root layout** (`lib/chapter_ai_web/components/layouts/root.html.heex`)
   - Add `<script>` tag in `<head>` before closing tag
   - CDN URL: `https://cdn.jsdelivr.net/npm/apexcharts@3.45.0/dist/apexcharts.min.js`

2. **Replace lines 24-65** in `lib/chapter_ai_web/live/benchmark_live/show.html.heex`
   - Use card.json patterns for chart containers
   - Apply `phx-hook="ApexChart"` with data attributes
   - Include accessibility attributes (`role="img"`, `aria-label`)

3. **Create Phoenix LiveView hook**: `assets/js/hooks/apex_chart.js`
   - Export `ApexChart` object with `mounted()` and `destroyed()` lifecycle hooks
   - Read config from `data-chart-config` attribute
   - Initialize ApexCharts (available globally from CDN)

4. **Update app.js**: `assets/js/app.js`
   - Import hook: `import { ApexChart } from "./hooks/apex_chart"`
   - Create Hooks object: `let Hooks = { ApexChart }`
   - Register with LiveSocket: `hooks: Hooks` in options

5. **Use existing assigns**: No changes to LiveView module needed
   - Data already available: `@benchmark.difficulty_counts`, etc.

6. **Helper functions needed** (add to LiveView module or template):
   - `humanize_difficulty/1`, `humanize_category/1`, `humanize_split/1`
   - `format_counts/1` for aria-label descriptions

7. **Maintain styling consistency**:
   - Use card.json `card_container` pattern
   - Match existing gray section container
   - Keep existing header, description, table sections unchanged

**Validation Criteria**:
- Template compiles without errors
- ApexCharts loads from CDN (check browser console)
- Charts render with real data from assigns
- Responsive grid works (3 columns → 1 column)
- Accessibility attributes present
- No console errors
- Existing sections (header, description, table) unchanged

## Implementation Notes

**Files to Modify**:
1. `lib/chapter_ai_web/components/layouts/root.html.heex` (add ApexCharts CDN script)
2. `lib/chapter_ai_web/live/benchmark_live/show.html.heex` (lines 24-65)
3. `assets/js/app.js` (import and register hook)

**Files to Create**:
1. `assets/js/hooks/apex_chart.js` (Phoenix LiveView hook)
2. (Optional) `assets/js/hooks/index.js` (central exports for all hooks)

**Helper Functions Needed** (in LiveView module):
```elixir
defp humanize_difficulty(:easy), do: "Easy"
defp humanize_difficulty(:medium), do: "Medium"
defp humanize_difficulty(:hard), do: "Hard"
defp humanize_difficulty(:very_hard), do: "Very Hard"

defp humanize_category(:open_ended), do: "Open Ended"
defp humanize_category(:summarization), do: "Summarization"
defp humanize_category(:hypothetical), do: "Hypothetical"

defp humanize_split(:public), do: "Public"
defp humanize_split(:eval), do: "Eval"
defp humanize_split(:test), do: "Test"

defp format_counts(counts) when is_map(counts) do
  counts
  |> Enum.map(fn {k, v} -> "#{v} #{k}" end)
  |> Enum.join(", ")
end
```

**Dependencies**:
- **ApexCharts via CDN**: No npm install needed
- **CDN URL**: `https://cdn.jsdelivr.net/npm/apexcharts@3.45.0/dist/apexcharts.min.js`
- **Size**: ~140KB minified (loaded once for entire app)
- **Availability**: Global `ApexCharts` constructor

**Performance Considerations**:
- ApexCharts loaded from CDN on first page load
- Charts render client-side on mount (~50-100ms per chart)
- Static data (no polling or live updates)
- Fixed height prevents layout shifts during render
- CDN cached by browser for subsequent visits

**Chart Configuration Best Practices**:
- Disable toolbar (`toolbar: { show: false }`) - not needed for static display
- Enable data labels (`dataLabels: { enabled: true }`) - shows counts on bars
- Distributed colors (`distributed: true`) - different color per bar
- Hide legend (`legend: { show: false }`) - redundant with x-axis labels
- Horizontal bars - better for label readability and mobile display

## Next Steps

After this structure is saved:
1. Run `specimin:ui-generate` to create implementation code
2. Agent will generate:
   - ApexCharts CDN script tag in root layout
   - Updated HEEx template with card.json-based chart grid
   - Phoenix hook for ApexCharts integration
   - app.js modifications for hook registration
   - Helper functions for humanizing labels
3. Manual verification:
   - Test charts render correctly with real data
   - Verify responsive behavior (3 columns → 1 column)
   - Validate accessibility with screen reader
   - Check browser console for errors
