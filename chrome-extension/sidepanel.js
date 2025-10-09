// Side Panel JavaScript for Aria Job Parser Chrome Extension
class AriaSidePanel {
  constructor() {
    this.currentTab = null;
    this.currentJobData = null;
    this.settings = {};
    this.init();
  }

  async init() {
    // Get current tab
    this.currentTab = await this.getCurrentTab();
    
    // Load settings
    await this.loadSettings();
    
    // Setup event listeners
    this.setupEventListeners();
    
    // Check for job page and extracted data
    await this.checkJobPage();
    
    // Load recent extractions
    this.loadRecentExtractions();
    
    // Setup auto-refresh for dynamic content
    this.setupAutoRefresh();
  }

  async getCurrentTab() {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    return tab;
  }

  setupEventListeners() {
    // Action buttons
    document.getElementById('extractBtn').addEventListener('click', () => this.extractJobData());
    document.getElementById('testConnectionBtn').addEventListener('click', () => this.testConnection());
    document.getElementById('openAriaBtn').addEventListener('click', () => this.openAria());
    document.getElementById('manualExtractBtn').addEventListener('click', () => this.showManualExtractForm());
    
    // Settings
    document.getElementById('autoExtractToggle').addEventListener('change', (e) => {
      this.settings.autoExtract = e.target.checked;
    });
    
    document.getElementById('autoOpenToggle').addEventListener('change', (e) => {
      this.settings.autoOpen = e.target.checked;
    });
    
    document.getElementById('notificationsToggle').addEventListener('change', (e) => {
      this.settings.notifications = e.target.checked;
    });
    
    document.getElementById('ariaUrl').addEventListener('change', (e) => {
      this.settings.ariaUrl = e.target.value;
    });
    
    document.getElementById('apiUrl').addEventListener('change', (e) => {
      this.settings.apiUrl = e.target.value;
    });
    
    document.getElementById('saveSettingsBtn').addEventListener('click', () => this.saveSettings());
    
    // Footer links
    document.getElementById('viewDocsLink').addEventListener('click', () => {
      chrome.tabs.create({ url: 'https://github.com/your-repo/aria-extension' });
    });
    
    document.getElementById('reportIssueLink').addEventListener('click', () => {
      chrome.tabs.create({ url: 'https://github.com/your-repo/aria-extension/issues' });
    });
    
    document.getElementById('refreshBtn').addEventListener('click', () => {
      this.refreshData();
    });
    
    // Tab switching for preview
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        this.switchTab(e.target.dataset.tab);
      });
    });
    
    // Listen for tab changes
    chrome.tabs.onActivated.addListener(() => {
      this.handleTabChange();
    });
    
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete') {
        this.handleTabChange();
      }
    });
  }

  async handleTabChange() {
    this.currentTab = await this.getCurrentTab();
    await this.checkJobPage();
  }

  async loadSettings() {
    try {
      const response = await chrome.runtime.sendMessage({ action: 'getSettings' });
      this.settings = response.settings;
      
      // Update UI
      document.getElementById('autoExtractToggle').checked = this.settings.autoExtract;
      document.getElementById('autoOpenToggle').checked = this.settings.autoOpen;
      document.getElementById('notificationsToggle').checked = this.settings.notifications;
      document.getElementById('ariaUrl').value = this.settings.ariaUrl;
      document.getElementById('apiUrl').value = this.settings.apiUrl;
      
    } catch (error) {
      console.error('Error loading settings:', error);
      this.showError('Failed to load settings');
    }
  }

  async saveSettings() {
    try {
      await chrome.runtime.sendMessage({ 
        action: 'saveSettings', 
        settings: this.settings 
      });
      
      this.showSuccess('Settings saved successfully');
      
    } catch (error) {
      console.error('Error saving settings:', error);
      this.showError('Failed to save settings');
    }
  }

  async checkJobPage() {
    if (!this.currentTab) return;
    
    console.log('Current tab URL:', this.currentTab.url);
    const isJobPage = this.isJobPage(this.currentTab.url);
    console.log('Is job page:', isJobPage);
    
    const statusIndicator = document.getElementById('statusIndicator');
    const jobInfo = document.getElementById('jobInfo');
    const noJobMessage = document.getElementById('noJobMessage');
    const extractBtn = document.getElementById('extractBtn');
    const livePreviewSection = document.getElementById('livePreviewSection');
    
    if (isJobPage) {
      // Update status
      statusIndicator.querySelector('.status-dot').className = 'status-dot active';
      statusIndicator.querySelector('.status-text').textContent = 'Job page detected';
      
      // Enable extract button
      extractBtn.disabled = false;
      
      // Show live preview section
      livePreviewSection.style.display = 'block';
      
      // Check for auto-extracted data
      const stored = await chrome.storage.local.get(['autoExtractedJob']);
      if (stored.autoExtractedJob && this.isRecentExtraction(stored.autoExtractedJob.extractedAt)) {
        this.displayJobInfo(stored.autoExtractedJob);
        jobInfo.style.display = 'block';
        noJobMessage.style.display = 'none';
      } else {
        // Try to extract data from content script
        this.requestJobData();
      }
      
    } else {
      // Update status
      statusIndicator.querySelector('.status-dot').className = 'status-dot';
      statusIndicator.querySelector('.status-text').textContent = 'No job page';
      
      // Disable extract button
      extractBtn.disabled = true;
      
      // Hide live preview section
      livePreviewSection.style.display = 'none';
      
      // Show no job message
      jobInfo.style.display = 'none';
      noJobMessage.style.display = 'block';
    }
  }

  isJobPage(url) {
    if (!url) return false;
    
    const jobPagePatterns = [
      /linkedin\.com\/jobs\/view/,
      /indeed\.com\/viewjob/,
      /wellfound\.com\/jobs/,
      /angel\.co\/jobs/
    ];

    return jobPagePatterns.some(pattern => pattern.test(url));
  }

  isRecentExtraction(timestamp) {
    // Consider extraction recent if within last 5 minutes
    return Date.now() - timestamp < 5 * 60 * 1000;
  }

  async requestJobData() {
    try {
      // First, try to inject the content script if it's not already loaded
      await this.ensureContentScriptLoaded();
      
      const response = await chrome.tabs.sendMessage(this.currentTab.id, {
        action: 'getJobData'
      });
      
      if (response && response.jobData) {
        this.displayJobInfo(response.jobData);
        this.updateLivePreview(response.jobData);
        document.getElementById('jobInfo').style.display = 'block';
        document.getElementById('noJobMessage').style.display = 'none';
      }
      
    } catch (error) {
      console.log('Content script not ready or no job data available:', error);
    }
  }

  async ensureContentScriptLoaded() {
    try {
      // Try to ping the content script first
      const response = await chrome.tabs.sendMessage(this.currentTab.id, { action: 'ping' });
      if (response && response.status === 'ready') {
        return true;
      }
    } catch (error) {
      console.log('Content script not responding, attempting to inject...');
    }

    try {
      // Content script not loaded, inject it manually
      await chrome.scripting.executeScript({
        target: { tabId: this.currentTab.id },
        files: ['content.js']
      });
      
      // Wait a bit for the script to initialize
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Try to ping again
      const response = await chrome.tabs.sendMessage(this.currentTab.id, { action: 'ping' });
      if (response && response.status === 'ready') {
        return true;
      } else {
        throw new Error('Content script failed to initialize');
      }
    } catch (error) {
      console.error('Failed to inject content script:', error);
      throw new Error('Unable to load job extraction script. Please refresh the page and try again.');
    }
  }

  displayJobInfo(jobData) {
    this.currentJobData = jobData;
    
    document.getElementById('jobTitle').textContent = jobData.positionTitle || 'Unknown';
    document.getElementById('jobCompany').textContent = jobData.companyName || 'Unknown';
    document.getElementById('jobSite').textContent = jobData.site || 'Unknown';
    
    // Show job description preview
    const descText = document.getElementById('descriptionText');
    if (jobData.jobDescription) {
      const preview = jobData.jobDescription.substring(0, 200) + '...';
      descText.textContent = preview;
    } else {
      descText.textContent = 'No description available';
    }
  }

  updateLivePreview(jobData) {
    // Update company tab
    document.getElementById('previewCompany').textContent = jobData.companyName || '-';
    document.getElementById('previewPosition').textContent = jobData.positionTitle || '-';
    document.getElementById('previewLocation').textContent = jobData.location || 'Not specified';
    
    // Simple extraction for requirements and skills (you can make this more sophisticated)
    const description = jobData.jobDescription || '';
    
    // Extract requirements
    const requirementsMatch = description.match(/requirements?:?\s*([^.]*(?:\.[^.]*){0,3})/i);
    document.getElementById('previewRequirements').textContent = 
      requirementsMatch ? requirementsMatch[1].trim() : 'No specific requirements mentioned';
    
    // Extract skills
    const skillsKeywords = ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'SQL', 'HTML', 'CSS', 'AWS', 'Docker'];
    const foundSkills = skillsKeywords.filter(skill => 
      description.toLowerCase().includes(skill.toLowerCase())
    );
    document.getElementById('previewSkills').textContent = 
      foundSkills.length > 0 ? foundSkills.join(', ') : 'No specific skills mentioned';
  }

  switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
      content.classList.toggle('active', content.id === `${tabName}Tab`);
    });
  }

  async testConnection() {
    this.setButtonLoading('testConnectionBtn', true);
    
    try {
      console.log('Testing connection to content script...');
      console.log('Current tab:', this.currentTab);
      
      // Try to ensure content script is loaded
      await this.ensureContentScriptLoaded();
      
      // Try to get job data
      const response = await chrome.tabs.sendMessage(this.currentTab.id, {
        action: 'getJobData'
      });
      
      console.log('Content script response:', response);
      
      if (response) {
        this.showSuccess('Connection successful! Content script is working.');
        
        if (response.jobData && response.jobData.jobDescription) {
          this.showSuccess(`Found job: ${response.jobData.positionTitle} at ${response.jobData.companyName}`);
        } else {
          this.showSuccess('Connected, but no job data found on this page.');
        }
      } else {
        this.showError('Connected but received no response');
      }
      
    } catch (error) {
      console.error('Connection test failed:', error);
      this.showError(`Connection failed: ${error.message}`);
    } finally {
      this.setButtonLoading('testConnectionBtn', false);
    }
  }

  async extractJobData() {
    if (!this.currentTab) return;
    
    this.setButtonLoading('extractBtn', true);
    
    try {
      // Ensure content script is loaded
      await this.ensureContentScriptLoaded();
      
      const response = await chrome.tabs.sendMessage(this.currentTab.id, {
        action: 'extractJob'
      });
      
      if (response && response.success) {
        this.showSuccess('Job data extracted successfully!');
        
        // Update recent extractions
        setTimeout(() => this.loadRecentExtractions(), 500);
        
      } else {
        throw new Error(response?.error || 'Extraction failed');
      }
      
    } catch (error) {
      console.error('Error extracting job data:', error);
      
      // More specific error messages
      if (error.message.includes('Could not establish connection')) {
        this.showError('Please refresh the page and try again');
      } else if (error.message.includes('Extension context invalidated')) {
        this.showError('Extension needs to be reloaded');
      } else {
        this.showError('Failed to extract job data');
      }
    } finally {
      this.setButtonLoading('extractBtn', false);
    }
  }

  async openAria() {
    const url = this.settings.ariaUrl || 'http://localhost:3000';
    
    // If we have current job data, include it in URL
    if (this.currentJobData) {
      const params = new URLSearchParams({
        jobDescription: this.currentJobData.jobDescription || '',
        companyName: this.currentJobData.companyName || '',
        positionTitle: this.currentJobData.positionTitle || '',
        source: this.currentJobData.site || '',
        sourceUrl: this.currentTab.url
      });
      
      await chrome.tabs.create({
        url: `${url}?${params.toString()}`,
        index: this.currentTab.index + 1
      });
    } else {
      await chrome.tabs.create({ url });
    }
  }

  showManualExtractForm() {
    // Create a simple prompt for manual extraction
    const jobDescription = prompt('Paste the job description:');
    if (!jobDescription) return;
    
    const companyName = prompt('Company name:');
    const positionTitle = prompt('Position title:');
    
    const manualJobData = {
      jobDescription,
      companyName: companyName || 'Unknown',
      positionTitle: positionTitle || 'Unknown',
      site: 'Manual',
      url: this.currentTab.url,
      isManual: true
    };
    
    // Send to background script
    chrome.runtime.sendMessage({
      action: 'extractedJobData',
      data: manualJobData
    });
    
    this.showSuccess('Manual job data submitted!');
  }

  async loadRecentExtractions() {
    try {
      // Get recent extractions from storage
      const stored = await chrome.storage.local.get(['recentExtractions']);
      const extractions = stored.recentExtractions || [];
      
      const container = document.getElementById('recentExtractions');
      
      if (extractions.length === 0) {
        container.innerHTML = '<div class="empty-state">No recent extractions</div>';
        return;
      }
      
      container.innerHTML = extractions
        .slice(0, 5) // Show only last 5
        .map(extraction => `
          <div class="recent-item" onclick="ariaSidePanel.openAriaWithJob('${extraction.id}')">
            <div class="recent-title">${extraction.positionTitle}</div>
            <div class="recent-company">${extraction.companyName}</div>
            <div class="recent-meta">
              <span class="recent-site">${extraction.site}</span>
              <span class="recent-time">${this.formatTime(extraction.extractedAt)}</span>
            </div>
          </div>
        `).join('');
        
    } catch (error) {
      console.error('Error loading recent extractions:', error);
    }
  }

  setupAutoRefresh() {
    // Auto-refresh data every 10 seconds if on a job page
    setInterval(() => {
      if (this.isJobPage(this.currentTab?.url)) {
        this.requestJobData();
      }
    }, 10000);
  }

  refreshData() {
    this.handleTabChange();
    this.loadRecentExtractions();
    this.showSuccess('Data refreshed');
  }

  formatTime(timestamp) {
    const now = Date.now();
    const diff = now - timestamp;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return `${Math.floor(diff / 86400000)}d ago`;
  }

  setButtonLoading(buttonId, loading) {
    const button = document.getElementById(buttonId);
    const icon = button.querySelector('.btn-icon');
    
    if (loading) {
      button.disabled = true;
      button.originalIcon = icon.textContent;
      icon.textContent = '⏳';
    } else {
      button.disabled = false;
      if (button.originalIcon) {
        icon.textContent = button.originalIcon;
      }
    }
  }

  showSuccess(message) {
    this.showToast(message, 'success');
  }

  showError(message) {
    this.showToast(message, 'error');
  }

  showToast(message, type) {
    // Create toast notification
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Show toast
    setTimeout(() => toast.classList.add('show'), 100);
    
    // Remove toast
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => document.body.removeChild(toast), 300);
    }, 3000);
  }
}

// Global functions for HTML onclick handlers
function toggleSection(sectionId) {
  const section = document.getElementById(sectionId);
  const header = section.previousElementSibling;
  const icon = header.querySelector('.toggle-icon');
  
  section.classList.toggle('collapsed');
  icon.style.transform = section.classList.contains('collapsed') ? 'rotate(-90deg)' : 'rotate(0deg)';
}

// Initialize side panel when DOM is loaded
let ariaSidePanel;
document.addEventListener('DOMContentLoaded', () => {
  ariaSidePanel = new AriaSidePanel();
});