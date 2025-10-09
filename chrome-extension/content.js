// Content script for extracting job information from job sites
class JobExtractor {
  constructor() {
    this.currentSite = null;
    this.extractionButton = null;
    
    // Store instance globally for message handling
    window.jobExtractor = this;
    
    this.init();
  }

  detectSite() {
    const hostname = window.location.hostname;
    const pathname = window.location.pathname;
    
    if (hostname.includes('linkedin.com') && pathname.includes('/jobs/view/')) {
      return 'linkedin';
    } else if (hostname.includes('indeed.com') && pathname.includes('viewjob')) {
      return 'indeed';
    } else if (hostname.includes('wellfound.com') || hostname.includes('angel.co')) {
      return 'wellfound';
    }
    return null;
  }

  init() {
    console.log('JobExtractor initializing on:', window.location.href);
    this.currentSite = this.detectSite();
    console.log('Detected site:', this.currentSite);
    
    if (!this.currentSite) {
      console.log('No supported job site detected');
      return;
    }
    
    // Add extraction button to page
    this.addExtractionButton();
    
    // Auto-extract when page loads (with delay for dynamic content)
    setTimeout(() => {
      this.autoExtract();
    }, 2000);
    
    // Listen for URL changes (for SPAs)
    this.observeUrlChanges();
  }

  addExtractionButton() {
    // Remove existing button if present
    const existingBtn = document.getElementById('aria-extract-btn');
    if (existingBtn) existingBtn.remove();

    // Create floating button
    const button = document.createElement('button');
    button.id = 'aria-extract-btn';
    button.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="white">
        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
      </svg>
      Extract for Aria
    `;
    button.className = 'aria-extract-button';
    button.addEventListener('click', () => this.extractAndSend());
    
    document.body.appendChild(button);
  }

  extractJobData() {
    let jobData = {
      site: this.currentSite,
      url: window.location.href,
      timestamp: new Date().toISOString()
    };

    try {
      switch (this.currentSite) {
        case 'linkedin':
          jobData = { ...jobData, ...this.extractLinkedInData() };
          break;
        case 'indeed':
          jobData = { ...jobData, ...this.extractIndeedData() };
          break;
        case 'wellfound':
          jobData = { ...jobData, ...this.extractWellfoundData() };
          break;
      }
    } catch (error) {
      console.error('Error extracting job data:', error);
      jobData.error = error.message;
    }

    return jobData;
  }

  extractLinkedInData() {
    // LinkedIn job page selectors
    const selectors = {
      title: [
        '.top-card-layout__title',
        '.topcard__title', 
        'h1[data-test-id="job-title"]',
        '.job-details-jobs-unified-top-card__job-title h1'
      ],
      company: [
        '.top-card-layout__card .topcard__org-name-link',
        '.topcard__org-name-link',
        '.job-details-jobs-unified-top-card__company-name a',
        '.job-details-jobs-unified-top-card__company-name'
      ],
      description: [
        '.description__text',
        '.jobs-box__html-content',
        '.job-details-jobs-unified-top-card__job-description',
        '[data-test-id="job-description"]'
      ]
    };

    return {
      positionTitle: this.getTextFromSelectors(selectors.title),
      companyName: this.getTextFromSelectors(selectors.company),
      jobDescription: this.getTextFromSelectors(selectors.description)
    };
  }

  extractIndeedData() {
    // Indeed job page selectors
    const selectors = {
      title: [
        '[data-testid="jobsearch-JobInfoHeader-title"]',
        '.jobsearch-JobInfoHeader-title',
        'h1[data-testid="job-title"]'
      ],
      company: [
        '[data-testid="inlineHeader-companyName"]',
        '.jobsearch-InlineCompanyRating-companyHeader',
        'span[data-testid="company-name"]'
      ],
      description: [
        '#jobDescriptionText',
        '.jobsearch-jobDescriptionText',
        '[data-testid="job-description"]'
      ]
    };

    return {
      positionTitle: this.getTextFromSelectors(selectors.title),
      companyName: this.getTextFromSelectors(selectors.company),
      jobDescription: this.getTextFromSelectors(selectors.description)
    };
  }

  extractWellfoundData() {
    // Wellfound (AngelList) job page selectors
    const selectors = {
      title: [
        'h1[data-test="JobHeader-JobTitle"]',
        '.job-header h1',
        '[data-test="job-title"]'
      ],
      company: [
        '[data-test="JobHeader-Company"]',
        '.startup-link',
        '[data-test="company-name"]'
      ],
      description: [
        '[data-test="JobDescription"]',
        '.job-description',
        '.job-details-section'
      ]
    };

    return {
      positionTitle: this.getTextFromSelectors(selectors.title),
      companyName: this.getTextFromSelectors(selectors.company),
      jobDescription: this.getTextFromSelectors(selectors.description)
    };
  }

  getTextFromSelectors(selectors) {
    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) {
        return element.textContent?.trim() || '';
      }
    }
    return '';
  }

  async extractAndSend() {
    const button = document.getElementById('aria-extract-btn');
    if (button) {
      button.textContent = 'Extracting...';
      button.disabled = true;
    }

    try {
      const jobData = this.extractJobData();
      
      // Validate required fields
      if (!jobData.positionTitle || !jobData.companyName || !jobData.jobDescription) {
        throw new Error('Missing required job information. Please check if the page has loaded completely.');
      }

      // Send to background script
      chrome.runtime.sendMessage({
        action: 'extractedJobData',
        data: jobData
      });

      // Show success notification
      this.showNotification('Job data extracted successfully! Opening Aria...', 'success');
      
    } catch (error) {
      console.error('Extraction error:', error);
      this.showNotification(`Error: ${error.message}`, 'error');
    } finally {
      if (button) {
        button.textContent = 'Extract for Aria';
        button.disabled = false;
      }
    }
  }

  async autoExtract() {
    // Check if auto-extract is enabled
    const settings = await chrome.storage.sync.get(['autoExtract']);
    if (!settings.autoExtract) return;

    const jobData = this.extractJobData();
    
    // Only auto-extract if we have all required fields
    if (jobData.positionTitle && jobData.companyName && jobData.jobDescription) {
      chrome.runtime.sendMessage({
        action: 'autoExtractedJobData',
        data: jobData
      });
    }
  }

  showNotification(message, type = 'info') {
    // Remove existing notification
    const existing = document.getElementById('aria-notification');
    if (existing) existing.remove();

    // Create notification
    const notification = document.createElement('div');
    notification.id = 'aria-notification';
    notification.className = `aria-notification aria-notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
      if (notification && notification.parentNode) {
        notification.remove();
      }
    }, 3000);
  }

  observeUrlChanges() {
    let currentUrl = location.href;
    
    new MutationObserver(() => {
      if (location.href !== currentUrl) {
        currentUrl = location.href;
        // Reinitialize if URL changed and still on a job page
        setTimeout(() => {
          if (this.detectSite()) {
            this.addExtractionButton();
          }
        }, 1000);
      }
    }).observe(document, { subtree: true, childList: true });
  }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => new JobExtractor());
} else {
  new JobExtractor();
}

// Store extractor instance for message handling
let extractor;

// Wait for extractor to be ready
setTimeout(() => {
  extractor = window.jobExtractor || new JobExtractor();
  window.jobExtractor = extractor;
}, 100);

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  console.log('Content script received message:', message);
  
  try {
    // Ensure extractor is available
    if (!extractor) {
      console.log('Extractor not ready, creating new instance...');
      extractor = window.jobExtractor || new JobExtractor();
      window.jobExtractor = extractor;
    }
    
    switch (message.action) {
      case 'ping':
        console.log('Ping received, responding...');
        sendResponse({ status: 'ready' });
        break;
        
      case 'getJobData':
        console.log('Getting job data...');
        const jobData = extractor.extractJobData();
        console.log('Extracted job data:', jobData);
        sendResponse({ jobData });
        break;
        
      case 'extractJob':
        console.log('Extracting job...');
        const extractedData = extractor.extractJobData();
        if (extractedData && extractedData.jobDescription) {
          extractor.handleExtraction(extractedData);
          console.log('Job extraction successful');
          sendResponse({ success: true, data: extractedData });
        } else {
          console.log('No job data found');
          sendResponse({ success: false, error: 'No job data found on this page' });
        }
        break;
        
      default:
        console.log('Unknown action:', message.action);
        sendResponse({ error: 'Unknown action' });
    }
  } catch (error) {
    console.error('Content script error:', error);
    sendResponse({ success: false, error: error.message });
  }
  
  return true; // Keep message channel open for async response
});