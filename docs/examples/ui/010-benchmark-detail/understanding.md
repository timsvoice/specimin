# UI Understanding Document - Benchmark Detail View Redesign

## Overview
**Feature**: Benchmark Detail View with Visual Stats Dashboard
**Type**: Page Enhancement
**Complexity**: Moderate
**Existing Implementation**: `/lib/chapter_ai_web/live/benchmark_live/show.html.heex`

## Layout Structure
**Container**: `max-w-6xl` centered container (existing pattern)
**Sections**:
- Header: Benchmark name with version/domain subtitle, Edit & Add Prompt buttons
- Description section: Gray card with benchmark description (if present)
- **Stats dashboard (REDESIGN TARGET)**: Visual charts replacing current text lists
- Prompts table: Existing table structure (keep as-is)

**Layout Pattern**: Vertical stack, stats dashboard uses 3-column grid on desktop

## Components Identified

### Navigation (Existing - Keep)
- **Type**: App-level navbar (not shown in sketch, assumed from existing app)
- **Elements**: "CHAPTER" branding, navigation items

### Header Section (Existing - Keep)
- Benchmark name (H1)
- Subtitle: Version + Domain
- Edit button → navigates to `/benchmarks/:id/edit`
- Add Prompt button → navigates to `/benchmarks/:id/prompts/new`

### Description Section (Existing - Keep)
- Gray card (`bg-gray-50 rounded-lg p-6`)
- Conditional display (only if description exists)

### Stats Dashboard (REDESIGN TARGET)

**Current Implementation** (lines 25-65):
- 3-column grid layout
- Text-based lists showing counts
- Data: `@benchmark.difficulty_counts`, `@benchmark.category_counts`, `@benchmark.split_counts`

**New Design Requirements**:
- Replace text lists with **ApexCharts horizontal bar charts**
- Three chart groups side-by-side:

1. **DIFFICULTY Distribution**
   - Data source: `@benchmark.difficulty_counts` (easy, medium, hard, very_hard)
   - Chart type: Horizontal bar chart
   - Display: Bar length proportional to count
   - Static display (not interactive)

2. **CATEGORY Distribution** (TYPE in sketch)
   - Data source: `@benchmark.category_counts` (open_ended, summarization, hypothetical)
   - Chart type: Horizontal bar chart
   - Display: Bar length proportional to count
   - Static display (not interactive)

3. **SPLIT Distribution**
   - Data source: `@benchmark.split_counts` (public, eval, test)
   - Chart type: Horizontal bar chart
   - Display: Bar length proportional to count
   - Static display (not interactive)

### Prompts Table (Existing - Keep)

**Columns**:
- **Text**: Prompt text truncated to 100 chars, link to `/prompts/:id` (lines 81-89)
- **Difficulty**: `prompt.difficulty_level` (line 90)
- **Category**: `prompt.category` (line 91)
- **Split**: `prompt.split_type` (line 92)
- **Reviews**: Shows review count with stats (lines 93-107)
  - Review count (e.g., "3 reviews")
  - Difficulty agreement percentage
  - Average quality score (x/5)
  - "No reviews" if count = 0

**Empty State**: Shows centered message with "Add First Prompt" button (lines 71-78)

## Visual Style

### Colors (Existing Tailwind)
- **Primary**: Blue for links (`text-blue-600 hover:text-blue-800`)
- **Neutrals**: Gray-50 backgrounds, Gray-700/900 for text
- **Charts**: Will need color palette for bars (suggest using brand colors)

### Typography (Existing)
- **H2**: Section headings (`text-lg font-semibold text-gray-900`)
- **H3**: Subsection headings (`text-sm font-medium text-gray-700`)
- **Body**: `text-gray-700`, `text-gray-600` for secondary text
- **Stats**: `text-2xl font-bold` for counts

### Spacing & Layout (Existing)
- **Section gaps**: `space-y-8` between major sections
- **Card padding**: `p-6` on gray cards
- **Grid**: `grid-cols-1 md:grid-cols-3 gap-6` for stats

### Visual Effects (Existing)
- **Border Radius**: `rounded-lg` on cards
- **Shadows**: None currently, standard Flowbite patterns
- **Borders**: Table borders via `.table` component

## Responsive Behavior

### Breakpoints
- **Desktop (md+)**: 3-column grid for stats
- **Mobile**: Single column stack

### Stats Dashboard Responsive
- Charts: 3 columns → 1 column stack on mobile
- Horizontal scroll on chart content if needed
- Table: Horizontal scroll (existing behavior)

## Interaction Patterns

### User Actions
- **Edit button**: Navigate to edit page (existing)
- **Add Prompt button**: Navigate to new prompt page (existing)
- **Table row links**: Click prompt text to view details (existing)
- **Charts**: Static display only (no click interactions)

### State Changes
- **Empty state**: Table shows when `total_prompts == 0` (existing, line 71)
- **Loading**: Will need for initial chart render
- **No description**: Description section hidden if null (existing, line 17)

## Accessibility Considerations

**Existing**:
- Semantic HTML structure
- Link text describes destination
- Button labels clear

**Chart Requirements**:
- Provide text alternative for chart data (keep existing text as fallback or add aria-label)
- Ensure color is not the only indicator (add value labels on bars)
- Keyboard navigation not needed (static display)

## Ambiguities & Questions

**Resolved**:
- Q1: Chart interactivity → **Static displays only**
- Q2: Stats data source → **Calculated as currently done** (aggregated in LiveView assigns)
- Q3: Edit behavior → **Navigate to edit page** (existing `/benchmarks/:id/edit`)
- Q4: Table text → **Truncated to 100 chars, no expand on click**
- Q5: Reviews column → **Shows count with stats** (review_count, agreement %, quality score)
- Q6: Chart type → **Horizontal bar charts** (ApexCharts)
- Q7: Mobile table → **Horizontal scroll** (existing behavior)

**Remaining**: None

## Design System Mapping

**Standard Components** (Flowbite/existing):
- `.header` component with actions (existing)
- `.button` component (existing)
- `.link` component (existing)
- `.table` component (existing)
- Gray card pattern (`bg-gray-50 rounded-lg p-6`)

**New Components**:
- ApexCharts horizontal bar chart wrapper (to be implemented)
- Chart container component (reusable for all three charts)

## Implementation Notes

**Framework**: Phoenix LiveView with HEEx templates
**Chart Library**: ApexCharts (https://apexcharts.com)
**Data Flow**:
- Stats already calculated in LiveView mount/handle_params
- Assigns: `@benchmark.difficulty_counts`, `@benchmark.category_counts`, `@benchmark.split_counts`
- Pass to chart component via assigns

**Chart Configuration**:
- Horizontal bar chart (`type: 'bar'` with `plotOptions.bar.horizontal: true`)
- X-axis: Count values
- Y-axis: Category labels (Easy, Medium, Hard, Very Hard, etc.)
- Colors: Define color palette for bars
- Responsive: `responsive: true` for mobile scaling

**Performance**:
- Client-side chart rendering (ApexCharts JS loaded once)
- Static data (no real-time updates)
- Lazy load chart library if not already in bundle

## Technical Specifications

**Data Structure Expected**:
```elixir
# From assigns (existing)
@benchmark.difficulty_counts = %{
  easy: 10,
  medium: 25,
  hard: 8,
  very_hard: 2
}

@benchmark.category_counts = %{
  open_ended: 30,
  summarization: 10,
  hypothetical: 5
}

@benchmark.split_counts = %{
  public: 20,
  eval: 15,
  test: 10
}
```

**ApexCharts Configuration** (reference):
```javascript
{
  chart: { type: 'bar', height: 200 },
  plotOptions: { bar: { horizontal: true } },
  series: [{ data: [10, 25, 8, 2] }],
  xaxis: { categories: ['Easy', 'Medium', 'Hard', 'Very Hard'] }
}
```

## Scope of Changes

**Files to Modify**:
1. `/lib/chapter_ai_web/live/benchmark_live/show.html.heex` (lines 24-65)
   - Replace text-based stats with chart components

**Files to Create**:
1. Chart component for ApexCharts horizontal bar
2. JavaScript hook for ApexCharts integration (Phoenix LiveView hook)

**Files Unchanged**:
- Header section (lines 2-13)
- Description section (lines 16-22)
- Prompts table section (lines 67-111)
- LiveView module (data preparation already exists)

## Next Steps

After this understanding is approved:
1. Run `specimin:ui-structure` to define chart component hierarchy
2. Map to Flowbite design system for consistent styling
3. Create ApexCharts integration pattern for Phoenix LiveView
4. Generate implementation tasks
