# Aria Job Parser Chrome Extension

A Chrome extension that runs as a **side panel** next to LinkedIn, Indeed, and Wellfound job pages, automatically extracting job information and seamlessly integrating with your Aria resume generator.

## ✨ New Side Panel Experience

Instead of a traditional popup, this extension opens as a **side panel** that stays open alongside job sites, providing:
- **Persistent interface** while browsing job sites
- **Live job data extraction** as you navigate between postings
- **Real-time preview** of extracted information
- **Seamless workflow** without interrupting your job search

## Features

- 🔍 **Auto-Detection**: Automatically detects job postings on supported sites
- 📋 **Smart Extraction**: Extracts job title, company, description, and requirements
- 👀 **Live Preview**: Real-time preview of extracted data with tabbed interface
- 🚀 **Aria Integration**: Directly opens Aria with pre-filled job data
- ⚙️ **Customizable**: Configure auto-extraction, URLs, and notifications
- 📱 **Side Panel UI**: Modern, collapsible interface optimized for narrow panels
- 🔄 **Auto-Refresh**: Continuously updates as you browse different job postings

## Supported Job Sites

- **LinkedIn** (`linkedin.com/jobs/view/*`)
- **Indeed** (`indeed.com/viewjob*`)
- **Wellfound** (`wellfound.com/jobs/*`)

## Installation

### Method 1: Load Unpacked Extension (Development)

1. **Prepare Icons** (Required):
   ```bash
   # Create icon files in the icons/ directory:
   # - icon16.png (16x16)
   # - icon32.png (32x32) 
   # - icon48.png (48x48)
   # - icon128.png (128x128)
   ```

2. **Open Chrome Extensions**:
   - Navigate to `chrome://extensions/`
   - Enable "Developer mode" (top-right toggle)

3. **Load Extension**:
   - Click "Load unpacked"
   - Select the `chrome-extension` folder
   - Extension should appear in your extensions list

4. **Pin Extension**:
   - Click the puzzle piece icon in Chrome toolbar
   - Pin "Aria Job Parser" for easy access

### Method 2: Package for Chrome Web Store

1. **Complete Setup**:
   ```bash
   # Ensure all files are present:
   # - manifest.json
   # - content.js
   # - background.js
   # - popup.html
   # - popup.js
   # - popup.css
   # - icons/ (with all 4 icon sizes)
   ```

2. **Package Extension**:
   ```bash
   # Zip the entire chrome-extension folder
   cd chrome-extension
   zip -r aria-job-parser.zip .
   ```

3. **Upload to Chrome Web Store**:
   - Visit [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Upload the zip file
   - Fill in store listing details
   - Submit for review

## Configuration

### First-Time Setup

1. **Click Extension Icon**: Access the popup interface
2. **Configure URLs**:
   - **Aria Frontend URL**: `http://localhost:3000` (or your deployment URL)
   - **Aria API URL**: `http://localhost:8080` (or your API URL)
3. **Choose Settings**:
   - ✅ **Auto-extract on page load**: Automatically extract when visiting job pages
   - ✅ **Auto-open Aria**: Automatically open Aria after extraction
   - ✅ **Show notifications**: Display success/error notifications
4. **Save Settings**: Click "Save Settings" to persist configuration

## How to Use

### Opening the Side Panel

1. **Navigate to a job page** on LinkedIn, Indeed, or Wellfound
2. **Click the Aria extension icon** in your Chrome toolbar
3. **Side panel opens** next to the job page automatically
4. **Start extracting** job data immediately

### Side Panel Interface

The side panel features several sections:

- **🔍 Current Page**: Shows detected job information with live preview
- **⚡ Quick Actions**: Extract, test connection, open Aria, manual entry
- **👀 Live Preview**: Tabbed interface showing company info, requirements, and skills
- **⚙️ Settings**: Collapsible section for configuration options
- **📚 Recent Extractions**: Quick access to previously extracted jobs

### Workflow

1. **Browse job sites** normally in the main browser window
2. **Side panel updates automatically** as you visit different job postings
3. **Extract data** with one click when you find an interesting job
4. **Aria opens** in a new tab with pre-filled information
5. **Continue browsing** while keeping the side panel open

## API Integration

The extension integrates with your Aria backend through these endpoints:

### Job Data Storage (Optional)
```http
POST /api/jobs/save
Content-Type: application/json

{
  "company_name": "Example Corp",
  "position_title": "Software Engineer",
  "job_description": "Full job description...",
  "source": "linkedin",
  "source_url": "https://linkedin.com/jobs/view/123456",
  "auto_extracted": true
}
```

### URL Parameters for Frontend
```
http://localhost:3000?jobDescription=...&companyName=...&positionTitle=...
```

## File Structure

```
chrome-extension/
├── manifest.json          # Extension configuration with Side Panel API
├── content.js             # Job extraction logic
├── background.js          # Service worker with side panel handling
├── sidepanel.html         # Side panel interface (NEW)
├── sidepanel.js           # Side panel functionality (NEW)
├── sidepanel.css          # Side panel styling (NEW)
├── popup.html             # Fallback popup interface
├── popup.js               # Popup functionality (fallback)
├── popup.css              # Popup styling (fallback)
├── icons/                 # Extension icons
│   ├── icon16.png
│   ├── icon32.png
│   ├── icon48.png
│   └── icon128.png
└── README.md              # This file
```

## Troubleshooting

### Extension Not Opening Side Panel
- Ensure you're using Chrome 114+ (Side Panel API requirement)
- Check that you clicked the extension icon while on a supported job site
- If side panel doesn't work, the extension will fallback to popup mode
- Try refreshing the page and clicking the extension icon again

### Side Panel Not Updating
- The side panel auto-refreshes every 10 seconds
- Click the "🔄 Refresh" button in the footer to manually update
- Ensure you're on a supported job site URL pattern
- Check browser console for JavaScript errors

### Job Data Not Extracting
- Use the "🔧 Test Connection" button to diagnose issues
- Verify you're on a supported job site
- Check browser console for JavaScript errors
- Ensure content script permissions are granted
- Try refreshing the page and testing again

### Aria Not Opening
- Verify Aria Frontend URL in extension settings
- Ensure Aria is running on the configured URL
- Check popup console for connection errors
- Test URL accessibility in a new tab

### API Integration Issues
- Verify Aria API URL in extension settings
- Check CORS configuration on your Aria backend
- Ensure API endpoints exist and are accessible
- Review network tab for failed requests

## Development

### Testing Content Script
```javascript
// In browser console on job pages:
const extractor = new JobExtractor();
const data = extractor.extractJobData();
console.log(data);
```

### Debugging Background Script
1. Go to `chrome://extensions/`
2. Click "Service worker" link under your extension
3. Use console to debug background script issues

### Local Development Workflow
1. Make changes to extension files
2. Go to `chrome://extensions/`
3. Click refresh icon under your extension
4. Test changes on job sites

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on all supported job sites
5. Submit a pull request

## Privacy & Permissions

The extension requests these permissions:
- **activeTab**: To read job page content
- **storage**: To save settings and recent extractions
- **notifications**: To show extraction status
- **Host permissions**: Access to LinkedIn, Indeed, and Wellfound

**Data Handling**:
- Job data is only extracted when explicitly requested
- No personal information is collected
- Data is sent directly to your configured Aria instance
- No data is stored on external servers

## License

This extension is part of the Aria project. See main project for licensing information.

## Support

For issues and feature requests:
1. Check this README for troubleshooting tips
2. Review browser console for error messages
3. Create an issue in the main Aria repository
4. Include extension version, browser version, and job site details