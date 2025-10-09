// Side Panel JavaScript for Aria Job Parser Chrome Extension with React App Integration

class AriaSidePanel {
  constructor() {
    this.currentJob = null;
    this.settings = {
      autoExtract: true,
      reactAppUrl: 'http://localhost:3000'
    };
    this.isSettingsPanelOpen = false;
    this.retryCount = 0;
    this.maxRetries = 3;
    this.toastTimeout = null;
    this.reactAppLoaded = false;

    this.init();
  }

  async init() {
    await this.loadSettings();
    this.setupEventListeners();
    this.loadReactApp();
    this.detectJobOnCurrentPage();
    this.updateUI();
  }

  setupEventListeners() {
    // Settings toggle
    const settingsBtn = document.getElementById('settingsBtn');
    const settingsPanel = document.getElementById('settingsPanel');
    
    if (settingsBtn) {
      settingsBtn.addEventListener('click', () => {
        this.isSettingsPanelOpen = !this.isSettingsPanelOpen;
        settingsPanel.style.display = this.isSettingsPanelOpen ? 'block' : 'none';
        settingsBtn.textContent = this.isSettingsPanelOpen ? '⚙️' : '⚙️';
      });
    }

    // Auto-extract toggle
    const autoExtractToggle = document.getElementById('autoExtract');
    if (autoExtractToggle) {
      autoExtractToggle.checked = this.settings.autoExtract;
      autoExtractToggle.addEventListener('change', (e) => {
        this.settings.autoExtract = e.target.checked;
        this.saveSettings();
      });
    }

    // React app URL input
    const reactUrlInput = document.getElementById('reactAppUrl');
    if (reactUrlInput) {
      reactUrlInput.value = this.settings.reactAppUrl;
      reactUrlInput.addEventListener('blur', (e) => {
        this.settings.reactAppUrl = e.target.value;
        this.saveSettings();
        this.loadReactApp(); // Reload with new URL
      });
    }

    // Use job button
    const useJobBtn = document.getElementById('useJobBtn');
    if (useJobBtn) {
      useJobBtn.addEventListener('click', () => {
        this.sendJobToReactApp();
      });
    }

    // Error overlay retry button
    const retryBtn = document.getElementById('retryBtn');
    if (retryBtn) {
      retryBtn.addEventListener('click', () => {
        this.loadReactApp();
      });
    }

    // External app button
    const externalBtn = document.getElementById('externalBtn');
    if (externalBtn) {
      externalBtn.addEventListener('click', () => {
        chrome.tabs.create({ url: this.settings.reactAppUrl });
      });
    }

    // Chrome message listener for job data
    chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
      if (message.type === 'JOB_DETECTED') {
        this.handleJobDetected(message.jobData);
      } else if (message.type === 'TAB_UPDATED') {
        this.detectJobOnCurrentPage();
      }
    });

    // React app iframe message listener
    window.addEventListener('message', (event) => {
      // Verify origin for security
      if (event.origin !== new URL(this.settings.reactAppUrl).origin) {
        return;
      }

      if (event.data.type === 'REACT_APP_READY') {
        this.reactAppLoaded = true;
        this.hideLoadingOverlay();
        this.sendJobToReactApp(); // Send current job if available
      } else if (event.data.type === 'REQUEST_JOB_DATA') {
        this.sendJobToReactApp();
      }
    });
  }

  loadReactApp() {
    const iframe = document.getElementById('ariaFrame');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const errorOverlay = document.getElementById('errorOverlay');

    // Show loading state
    this.showLoadingOverlay();
    errorOverlay.style.display = 'none';
    this.reactAppLoaded = false;

    if (iframe) {
      // Set up iframe load handlers
      iframe.onload = () => {
        // Give React app time to initialize
        setTimeout(() => {
          if (!this.reactAppLoaded) {
            this.hideLoadingOverlay();
            this.retryCount = 0;
          }
        }, 5000);
      };

      iframe.onerror = () => {
        this.showErrorOverlay();
        this.retryCount++;
      };

      // Load the React app
      iframe.src = this.settings.reactAppUrl;
    }
  }

  showLoadingOverlay() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
      loadingOverlay.style.display = 'flex';
    }
  }

  hideLoadingOverlay() {
    const loadingOverlay = document.getElementById('loadingOverlay');
    if (loadingOverlay) {
      loadingOverlay.style.display = 'none';
    }
  }

  showErrorOverlay() {
    const errorOverlay = document.getElementById('errorOverlay');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    if (errorOverlay) {
      errorOverlay.style.display = 'flex';
    }
    if (loadingOverlay) {
      loadingOverlay.style.display = 'none';
    }
  }

  async detectJobOnCurrentPage() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (tab && this.isJobSite(tab.url)) {
        // Update status indicator
        this.updateStatus(true);
        
        // Extract job data if auto-extract is enabled
        if (this.settings.autoExtract) {
          chrome.tabs.sendMessage(tab.id, { type: 'EXTRACT_JOB' }, (response) => {
            if (response && response.jobData) {
              this.handleJobDetected(response.jobData);
            }
          });
        }
      } else {
        this.updateStatus(false);
        this.currentJob = null;
        this.updateJobBanner();
      }
    } catch (error) {
      console.error('Error detecting job:', error);
      this.updateStatus(false);
    }
  }

  isJobSite(url) {
    if (!url) return false;
    
    const jobSites = [
      'linkedin.com/jobs',
      'indeed.com',
      'glassdoor.com',
      'monster.com',
      'ziprecruiter.com',
      'careerbuilder.com',
      'simplyhired.com',
      'wellfound.com'
    ];

    return jobSites.some(site => url.includes(site));
  }

  handleJobDetected(jobData) {
    this.currentJob = jobData;
    this.updateJobBanner();
    
    // Automatically send to React app if it's loaded
    if (this.reactAppLoaded) {
      this.sendJobToReactApp();
    }
    
    this.showToast('Job detected successfully!', 'success');
  }

  updateJobBanner() {
    const jobBanner = document.getElementById('jobBanner');
    const jobTitle = document.getElementById('jobTitle');
    const jobCompany = document.getElementById('jobCompany');
    const useJobBtn = document.getElementById('useJobBtn');

    if (this.currentJob && jobBanner) {
      jobBanner.style.display = 'flex';
      
      if (jobTitle) {
        jobTitle.textContent = this.currentJob.title || 'Job Title';
      }
      
      if (jobCompany) {
        jobCompany.textContent = this.currentJob.company || 'Company Name';
      }
      
      if (useJobBtn) {
        useJobBtn.disabled = false;
      }
    } else if (jobBanner) {
      jobBanner.style.display = 'none';
    }
  }

  sendJobToReactApp() {
    if (!this.currentJob || !this.reactAppLoaded) {
      return;
    }

    const iframe = document.getElementById('ariaFrame');
    if (iframe && iframe.contentWindow) {
      try {
        iframe.contentWindow.postMessage({
          type: 'JOB_DATA_FROM_EXTENSION',
          jobData: this.currentJob
        }, this.settings.reactAppUrl);
        
        this.showToast('Job data sent to Aria app!', 'success');
      } catch (error) {
        console.error('Error sending job data to React app:', error);
        this.showToast('Failed to send job data', 'error');
      }
    }
  }

  updateStatus(isActive) {
    const statusDot = document.querySelector('.status-dot');
    const statusText = document.getElementById('statusText');

    if (statusDot) {
      statusDot.classList.toggle('active', isActive);
    }

    if (statusText) {
      statusText.textContent = isActive ? 'Job page detected' : 'No job page detected';
    }
  }

  updateUI() {
    // Update any other UI elements based on current state
    this.updateJobBanner();
  }

  showToast(message, type = 'success') {
    // Clear existing toast
    if (this.toastTimeout) {
      clearTimeout(this.toastTimeout);
    }

    // Remove existing toast
    const existingToast = document.querySelector('.toast');
    if (existingToast) {
      existingToast.remove();
    }

    // Create new toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => {
      toast.classList.add('show');
    }, 100);

    // Hide toast after 3 seconds
    this.toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        if (toast.parentNode) {
          toast.remove();
        }
      }, 300);
    }, 3000);
  }

  async loadSettings() {
    try {
      const result = await chrome.storage.local.get(['ariaSidePanelSettings']);
      if (result.ariaSidePanelSettings) {
        this.settings = { ...this.settings, ...result.ariaSidePanelSettings };
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }

  async saveSettings() {
    try {
      await chrome.storage.local.set({ ariaSidePanelSettings: this.settings });
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  }
}

// Initialize the side panel when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  window.ariaSidePanel = new AriaSidePanel();
});

// Handle visibility changes to detect when side panel is opened
document.addEventListener('visibilitychange', () => {
  if (!document.hidden && window.ariaSidePanel) {
    window.ariaSidePanel.detectJobOnCurrentPage();
  }
});