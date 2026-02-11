# Frontend Documentation

## Overview

The frontend is a beautiful, modern single-page application (SPA) built with vanilla JavaScript, HTML5, and CSS3. It provides an intuitive interface for all AI processing features.

## Features

### 1. Summarize Text
- Input: Long text content
- Output: Concise summary
- Use Case: Quickly understand long articles, documents, or content

### 2. Polish Text
- Input: Text with grammar or style issues
- Output: Improved, professional text
- Use Case: Enhance writing quality, fix grammar, improve clarity

### 3. Generate Image
- Input: Text description of desired image
- Output: AI-generated image
- Use Case: Create visuals from descriptions, generate artwork

## Design Features

### Visual Design
- **Modern Gradient Theme**: Purple to violet gradient (667eea to 764ba2)
- **Card-Based Layout**: Clean, organized content sections
- **Smooth Animations**: Fade-in effects and transitions
- **Responsive Design**: Works on all screen sizes

### User Experience
- **Tab Navigation**: Easy switching between features
- **Real-time Feedback**: Character counters and loading states
- **Copy to Clipboard**: Quick copy functionality for results
- **Toast Notifications**: Non-intrusive success/error messages
- **Keyboard Shortcuts**: Ctrl+Enter to submit

### Technical Features
- **No Dependencies**: Pure vanilla JavaScript
- **Fast Loading**: Minimal assets, optimized CSS
- **Modern CSS**: Flexbox, Grid, CSS Variables
- **Accessible**: Semantic HTML, proper ARIA labels

## File Structure

```
static/
├── index.html      # Main HTML structure
├── styles.css      # All styling and animations
└── script.js       # Application logic and API calls
```

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --bg-color: #f8f9fa;
    --card-bg: #ffffff;
    --text-primary: #2d3748;
    --text-secondary: #718096;
}
```

### Adding New Features
1. Add a new tab button in `index.html`
2. Add corresponding tab content section
3. Create handler function in `script.js`
4. Add API endpoint in `main.py`

## Browser Support

- Chrome/Edge: 90+
- Firefox: 88+
- Safari: 14+
- Opera: 76+

## Performance

- **First Load**: < 100ms
- **API Response**: Depends on external API (typically 2-5s)
- **Image Generation**: 5-15s (depends on complexity)

## Keyboard Shortcuts

- `Ctrl+Enter`: Submit current form
- `Tab`: Navigate between fields
- `Escape`: Close modals (if implemented)

## API Integration

The frontend communicates with the FastAPI backend using fetch API:

```javascript
// Example API call
const response = await fetch('/summarize', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ text: input })
});
```

## Error Handling

- Network errors: User-friendly toast notifications
- API errors: Display error details from backend
- Validation: Client-side validation before API calls

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Save/load history
- [ ] Export results to PDF
- [ ] Batch processing
- [ ] Progress bars for long operations
- [ ] Image editing tools
- [ ] Multi-language support
