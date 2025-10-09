// Background service worker for Chrome extension
class AriaBackgroundService {
  constructor() {
    this.ariaBaseUrl = 'http://localhost:3000'; // Your Aria frontend URL
    this.ariaApiUrl = 'http://localhost:8080';  // Your Aria backend URL
    this.init();
  }

  init() {
    // Listen for messages from content script and side panel
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      this.handleMessage(message, sender, sendResponse);
      return true; // Keep message channel open for async response
    });

    // Listen for extension installation
    chrome.runtime.onInstalled.addListener(() => {
      this.onInstalled();
    });

    // Listen for tab updates (for auto-detection)
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      this.onTabUpdated(tabId, changeInfo, tab);
    });

    // Handle action button click to open side panel
    chrome.action.onClicked.addListener((tab) => {
      this.openSidePanel(tab);
    });
  }

  async openSidePanel(tab) {
    try {
      // Check if this is a job page
      const isJobPage = this.isJobPage(tab.url);
      
      if (isJobPage) {
        // Open side panel for the current tab
        await chrome.sidePanel.open({ tabId: tab.id });
        
        // Clear any existing badge
        await chrome.action.setBadgeText({ text: '', tabId: tab.id });
      } else {
        // Open side panel anyway, but show a message
        await chrome.sidePanel.open({ tabId: tab.id });
      }
    } catch (error) {
      console.error('Error opening side panel:', error);
      
      // Fallback to old popup behavior if side panel is not supported
      chrome.action.setPopup({ popup: 'popup.html' });
    }
  }

  async handleMessage(message, sender, sendResponse) {
    try {
      switch (message.action) {
        case 'extractedJobData':
          await this.handleExtractedData(message.data, sender.tab);
          sendResponse({ success: true });
          break;
          
        case 'autoExtractedJobData':
          await this.handleAutoExtractedData(message.data, sender.tab);
          sendResponse({ success: true });
          break;
          
        case 'getSettings':
          const settings = await this.getSettings();
          sendResponse({ settings });
          break;
          
        case 'saveSettings':
          await this.saveSettings(message.settings);
          sendResponse({ success: true });
          break;
          
        default:
          sendResponse({ error: 'Unknown action' });
      }
    } catch (error) {
      console.error('Background script error:', error);
      sendResponse({ error: error.message });
    }
  }

  async handleExtractedData(jobData, sourceTab) {
    console.log('Job data extracted:', jobData);
    
    try {
      // Store the job data temporarily
      await chrome.storage.local.set({
        'lastExtractedJob': {
          ...jobData,
          extractedAt: Date.now()
        }
      });

      // Open Aria with pre-filled data
      await this.openAriaWithJobData(jobData, sourceTab);
      
      // Optional: Send to Aria API to pre-populate
      await this.sendToAriaAPI(jobData);
      
    } catch (error) {
      console.error('Error handling extracted data:', error);
      this.showNotification('Error processing job data', 'error');
    }
  }

  async handleAutoExtractedData(jobData, sourceTab) {
    // Store for popup access
    await chrome.storage.local.set({
      'autoExtractedJob': {
        ...jobData,
        extractedAt: Date.now()
      }
    });

    // Show badge with notification
    await chrome.action.setBadgeText({
      text: '1',
      tabId: sourceTab.id
    });
    
    await chrome.action.setBadgeBackgroundColor({
      color: '#4CAF50'
    });
  }

  async openAriaWithJobData(jobData, sourceTab) {
    // Encode job data for URL parameters
    const params = new URLSearchParams({
      jobDescription: jobData.jobDescription,
      companyName: jobData.companyName,
      positionTitle: jobData.positionTitle,
      source: jobData.site,
      sourceUrl: jobData.url
    });

    const ariaUrl = `${this.ariaBaseUrl}?${params.toString()}`;
    
    // Open in new tab
    await chrome.tabs.create({
      url: ariaUrl,
      index: sourceTab.index + 1
    });
  }

  async sendToAriaAPI(jobData) {
    try {
      // Optional: Pre-save job data to your backend
      const response = await fetch(`${this.ariaApiUrl}/api/jobs/save`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          company_name: jobData.companyName,
          position_title: jobData.positionTitle,
          job_description: jobData.jobDescription,
          source: jobData.site,
          source_url: jobData.url,
          auto_extracted: true
        })
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const result = await response.json();
      console.log('Job data saved to API:', result);
      
    } catch (error) {
      console.warn('Could not save to API (this is optional):', error);
    }
  }

  async getSettings() {
    const defaultSettings = {
      autoExtract: false,
      ariaUrl: 'http://localhost:3000',
      apiUrl: 'http://localhost:8080',
      autoOpen: true,
      notifications: true
    };

    const stored = await chrome.storage.sync.get(defaultSettings);
    return stored;
  }

  async saveSettings(settings) {
    await chrome.storage.sync.set(settings);
    
    // Update instance URLs
    this.ariaBaseUrl = settings.ariaUrl;
    this.ariaApiUrl = settings.apiUrl;
  }

  onInstalled() {
    console.log('Aria extension installed');
    
    // Set default settings
    this.saveSettings({
      autoExtract: false,
      ariaUrl: 'http://localhost:3000',
      apiUrl: 'http://localhost:8080',
      autoOpen: true,
      notifications: true
    });
  }

  onTabUpdated(tabId, changeInfo, tab) {
    // Clear badge when navigating away from job pages
    if (changeInfo.status === 'complete' && tab.url) {
      const isJobPage = this.isJobPage(tab.url);
      if (!isJobPage) {
        chrome.action.setBadgeText({ text: '', tabId: tabId });
      }
    }
  }

  isJobPage(url) {
    const jobPagePatterns = [
      /linkedin\.com\/jobs\/view/,
      /indeed\.com\/viewjob/,
      /wellfound\.com\/jobs/,
      /angel\.co\/jobs/
    ];

    return jobPagePatterns.some(pattern => pattern.test(url));
  }

  async showNotification(message, type = 'info') {
    // Create Chrome notification
    await chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: 'Aria',
      message: message
    });
  }
}

// Initialize the background service
new AriaBackgroundService();