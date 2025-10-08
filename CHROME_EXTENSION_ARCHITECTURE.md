# Aria Chrome Extension Architecture

## 🎯 Vision
Transform Aria into a Chrome extension that automatically detects job postings, generates tailored resumes/cover letters, and predicts job success probability - all with one click while browsing job sites.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHROME EXTENSION                             │
├─────────────────────────────────────────────────────────────────┤
│  Content Scripts    │  Background Service  │  Popup Interface   │
│  • Job Detection    │  • API Communication │  • Quick Actions   │
│  • Page Parsing     │  • Data Processing   │  • Success Meter   │
│  • DOM Injection    │  • State Management  │  • One-Click Gen   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     CLOUD API SERVER                           │
├─────────────────────────────────────────────────────────────────┤
│  Job Analysis API   │  Document Generator  │  Success Predictor │
│  • Content Extract  │  • Resume Generator  │  • ML Model API    │
│  • Requirements AI  │  • Cover Letter Gen  │  • Probability     │
│  • Company Research │  • PDF Generation    │  • Match Score     │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                   DATA & ML PIPELINE                           │
├─────────────────────────────────────────────────────────────────┤
│   Vector Database   │   ML Models         │   Analytics Engine │
│   • Job Embeddings  │   • Success Predictor│   • Usage Tracking │
│   • Resume Cache    │   • Content Ranker   │   • Success Rates  │
│   • Company Data    │   • Similarity Search│   • Optimization   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔧 Chrome Extension Components

### 1. Content Scripts
**Purpose**: Detect and extract job posting data from various job sites

```javascript
// content-script.js
class JobDetector {
  constructor() {
    this.supportedSites = {
      'linkedin.com': new LinkedInParser(),
      'indeed.com': new IndeedParser(),
      'glassdoor.com': new GlassdoorParser(),
      'monster.com': new MonsterParser(),
      'ziprecruiter.com': new ZipRecruiterParser()
    };
  }

  detectJobPosting() {
    const hostname = window.location.hostname;
    const parser = this.getSiteParser(hostname);
    
    if (parser && parser.isJobPage()) {
      return {
        jobTitle: parser.getJobTitle(),
        company: parser.getCompanyName(),
        description: parser.getJobDescription(),
        requirements: parser.getRequirements(),
        location: parser.getLocation(),
        salary: parser.getSalary(),
        url: window.location.href,
        source: hostname
      };
    }
    return null;
  }

  injectAriaButton() {
    if (this.detectJobPosting()) {
      const button = this.createAriaButton();
      this.insertButton(button);
    }
  }
}
```

### 2. Site-Specific Parsers
```javascript
class LinkedInParser {
  isJobPage() {
    return window.location.pathname.includes('/jobs/view/');
  }

  getJobTitle() {
    return document.querySelector('.top-card-layout__title')?.textContent?.trim();
  }

  getCompanyName() {
    return document.querySelector('.topcard__flavor-row .topcard__flavor--black-link')?.textContent?.trim();
  }

  getJobDescription() {
    return document.querySelector('.description__text')?.innerHTML;
  }

  getRequirements() {
    // Extract requirements section
    const description = this.getJobDescription();
    return this.extractRequirements(description);
  }
}

class IndeedParser {
  // Similar implementation for Indeed
}
```

### 3. Background Service Worker
```javascript
// background.js
class AriaBackgroundService {
  constructor() {
    this.apiBaseUrl = 'https://api.aria-ai.com';
    this.setupMessageHandlers();
  }

  async generateDocuments(jobData) {
    try {
      // Send to cloud API
      const response = await fetch(`${this.apiBaseUrl}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await this.getAuthToken()}`
        },
        body: JSON.stringify(jobData)
      });

      return await response.json();
    } catch (error) {
      console.error('Document generation failed:', error);
      throw error;
    }
  }

  async predictJobSuccess(jobData, userProfile) {
    const response = await fetch(`${this.apiBaseUrl}/api/predict-success`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${await this.getAuthToken()}`
      },
      body: JSON.stringify({ jobData, userProfile })
    });

    return await response.json();
  }
}
```

### 4. Popup Interface
```typescript
// popup.tsx
interface JobSuccessMetrics {
  overallScore: number;
  skillsMatch: number;
  experienceMatch: number;
  locationFit: number;
  salaryExpectation: number;
  companyFit: number;
}

const AriaPopup: React.FC = () => {
  const [currentJob, setCurrentJob] = useState<JobData | null>(null);
  const [successMetrics, setSuccessMetrics] = useState<JobSuccessMetrics | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  return (
    <div className="aria-popup">
      <Header />
      
      {currentJob && (
        <>
          <JobSummaryCard job={currentJob} />
          <SuccessProbabilityMeter metrics={successMetrics} />
          
          <ActionButtons>
            <GenerateButton 
              onClick={handleGenerate} 
              loading={isGenerating}
              disabled={successMetrics?.overallScore < 30}
            />
            <ViewDetailsButton onClick={handleViewDetails} />
          </ActionButtons>
          
          <RecommendationsPanel metrics={successMetrics} />
        </>
      )}
    </div>
  );
};
```

## 🤖 ML Success Prediction Model

### 1. Training Data Collection
```python
# ml/data_collector.py
class JobSuccessDataCollector:
    """Collect training data for success prediction model"""
    
    def collect_training_data(self):
        return {
            'job_features': self.extract_job_features(),
            'user_features': self.extract_user_features(),
            'application_outcome': self.get_outcome(),  # hired/rejected/no_response
            'time_to_response': self.get_response_time(),
            'interview_stages': self.get_interview_data()
        }
    
    def extract_job_features(self, job_data):
        return {
            'title_embedding': self.embed_text(job_data['title']),
            'description_embedding': self.embed_text(job_data['description']),
            'required_skills': self.extract_skills(job_data['requirements']),
            'experience_level': self.classify_seniority(job_data),
            'company_size': self.get_company_data(job_data['company']),
            'industry': self.classify_industry(job_data['company']),
            'location_competitiveness': self.get_market_data(job_data['location']),
            'salary_range': self.extract_salary(job_data),
            'posting_age': self.calculate_posting_age(job_data['posted_date'])
        }
```

### 2. Success Prediction Model
```python
# ml/success_predictor.py
class JobSuccessPredictorModel:
    def __init__(self):
        self.skill_matcher = SkillMatchingModel()
        self.experience_matcher = ExperienceMatchingModel()
        self.company_culture_matcher = CultureFitModel()
        self.market_analyzer = JobMarketAnalyzer()
        
    def predict_success_probability(self, job_data, user_profile):
        features = self.extract_features(job_data, user_profile)
        
        predictions = {
            'skills_match': self.skill_matcher.predict(features['skills']),
            'experience_match': self.experience_matcher.predict(features['experience']),
            'culture_fit': self.company_culture_matcher.predict(features['culture']),
            'market_competition': self.market_analyzer.predict(features['market']),
            'location_preference': self.location_matcher.predict(features['location'])
        }
        
        # Weighted ensemble prediction
        overall_score = self.calculate_weighted_score(predictions)
        
        return {
            'overall_probability': overall_score,
            'breakdown': predictions,
            'confidence': self.calculate_confidence(features),
            'recommendations': self.generate_recommendations(predictions)
        }
```

### 3. Feature Engineering
```python
class FeatureEngineer:
    def extract_comprehensive_features(self, job_data, user_profile):
        return {
            # Text embeddings
            'job_description_embedding': self.embed_job_description(job_data),
            'user_resume_embedding': self.embed_user_profile(user_profile),
            
            # Skill matching
            'skill_overlap_score': self.calculate_skill_overlap(job_data, user_profile),
            'missing_critical_skills': self.identify_missing_skills(job_data, user_profile),
            'skill_level_match': self.compare_skill_levels(job_data, user_profile),
            
            # Experience matching
            'years_experience_gap': self.calculate_experience_gap(job_data, user_profile),
            'domain_experience_match': self.match_domain_experience(job_data, user_profile),
            'role_progression_fit': self.analyze_career_progression(job_data, user_profile),
            
            # Market factors
            'application_competition': self.estimate_competition(job_data),
            'salary_expectation_match': self.compare_salary_expectations(job_data, user_profile),
            'location_desirability': self.analyze_location_fit(job_data, user_profile),
            
            # Company factors
            'company_culture_fit': self.predict_culture_fit(job_data, user_profile),
            'company_growth_stage': self.analyze_company_stage(job_data['company']),
            'hiring_velocity': self.analyze_hiring_patterns(job_data['company'])
        }
```

## 🌐 Cloud API Architecture

### 1. Enhanced API Endpoints
```python
# api/routes.py
@app.route('/api/analyze-job', methods=['POST'])
async def analyze_job():
    """Analyze job posting and return structured data"""
    job_data = request.json
    
    analysis = await JobAnalyzer.analyze(job_data)
    success_prediction = await SuccessPredictor.predict(job_data, current_user.profile)
    
    return {
        'job_analysis': analysis,
        'success_prediction': success_prediction,
        'recommendations': generate_recommendations(analysis, success_prediction)
    }

@app.route('/api/generate-documents', methods=['POST'])
async def generate_documents():
    """Generate resume and cover letter with success optimization"""
    job_data = request.json
    
    # Only generate if success probability > threshold
    if job_data['success_probability'] < 0.3:
        return {'error': 'Low success probability. Consider improving profile first.'}
    
    documents = await DocumentGenerator.generate(job_data, current_user.profile)
    
    # Track generation for learning
    await Analytics.track_generation(job_data, documents, current_user.id)
    
    return documents

@app.route('/api/predict-success', methods=['POST'])
async def predict_success():
    """Predict job application success probability"""
    data = request.json
    
    prediction = await SuccessPredictor.predict(
        data['job_data'], 
        data['user_profile']
    )
    
    return prediction
```

### 2. Real-time Job Market Data
```python
class JobMarketAnalyzer:
    def __init__(self):
        self.market_data_sources = [
            'glassdoor_api',
            'linkedin_api', 
            'indeed_api',
            'bls_data',  # Bureau of Labor Statistics
            'github_jobs'
        ]
    
    async def analyze_market_competition(self, job_data):
        """Analyze how competitive this specific job posting is"""
        similar_jobs = await self.find_similar_postings(job_data)
        
        return {
            'competition_level': self.calculate_competition(similar_jobs),
            'average_applications': self.estimate_application_volume(job_data),
            'salary_competitiveness': self.compare_salary_market(job_data),
            'skill_demand': self.analyze_skill_demand(job_data['requirements']),
            'location_market': self.analyze_location_market(job_data['location'])
        }
```

## 📱 Enhanced User Experience

### 1. Smart Notifications
```javascript
class SmartNotificationSystem {
  async analyzePageAndNotify() {
    const jobData = await this.detectJob();
    
    if (jobData) {
      const prediction = await this.predictSuccess(jobData);
      
      if (prediction.overall_probability > 0.7) {
        this.showHighPotentialNotification(jobData, prediction);
      } else if (prediction.overall_probability < 0.3) {
        this.showLowPotentialWarning(jobData, prediction);
      } else {
        this.showStandardNotification(jobData, prediction);
      }
    }
  }
  
  showHighPotentialNotification(jobData, prediction) {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/aria-success.png',
      title: '🎯 High Success Probability!',
      message: `${Math.round(prediction.overall_probability * 100)}% match for ${jobData.title} at ${jobData.company}. Generate documents?`
    });
  }
}
```

### 2. Success Probability Visualization
```typescript
const SuccessProbabilityMeter: React.FC<{metrics: JobSuccessMetrics}> = ({metrics}) => {
  const getColorByScore = (score: number) => {
    if (score >= 70) return '#4CAF50'; // Green
    if (score >= 50) return '#FF9800'; // Orange  
    return '#f44336'; // Red
  };

  return (
    <div className="success-meter">
      <div className="overall-score">
        <CircularProgress 
          value={metrics.overallScore} 
          color={getColorByScore(metrics.overallScore)}
        />
        <span className="score-label">
          {metrics.overallScore}% Success Probability
        </span>
      </div>
      
      <div className="breakdown">
        <MetricBar label="Skills Match" value={metrics.skillsMatch} />
        <MetricBar label="Experience" value={metrics.experienceMatch} />
        <MetricBar label="Location Fit" value={metrics.locationFit} />
        <MetricBar label="Company Culture" value={metrics.companyFit} />
      </div>
      
      <RecommendationsList metrics={metrics} />
    </div>
  );
};
```

## 🚀 Deployment Strategy

### 1. Chrome Extension Deployment
```json
{
  "manifest_version": 3,
  "name": "Aria - Smart Job Application Assistant",
  "version": "1.0.0",
  "description": "AI-powered resume generation and job success prediction",
  
  "permissions": [
    "activeTab",
    "storage",
    "notifications",
    "identity"
  ],
  
  "host_permissions": [
    "https://*.linkedin.com/*",
    "https://*.indeed.com/*",
    "https://*.glassdoor.com/*",
    "https://api.aria-ai.com/*"
  ],
  
  "content_scripts": [
    {
      "matches": ["https://*.linkedin.com/*", "https://*.indeed.com/*"],
      "js": ["content-script.js"],
      "css": ["aria-overlay.css"]
    }
  ],
  
  "background": {
    "service_worker": "background.js"
  },
  
  "action": {
    "default_popup": "popup.html",
    "default_title": "Aria Job Assistant"
  }
}
```

### 2. Cloud Infrastructure
```yaml
# docker-compose.yml
services:
  api-server:
    build: ./api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=${REDIS_URL}
    
  ml-service:
    build: ./ml-service
    ports:
      - "8081:8081"
    volumes:
      - ./models:/app/models
    
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      - POSTGRES_DB=aria
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    
  redis:
    image: redis:alpine
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## 📊 Analytics & Learning

### 1. Success Tracking
```python
class SuccessTracker:
    def track_application_outcome(self, user_id, job_id, outcome):
        """Track actual job application outcomes to improve model"""
        
        # Store outcome
        self.db.applications.insert({
            'user_id': user_id,
            'job_id': job_id,
            'predicted_success': self.get_prediction(user_id, job_id),
            'actual_outcome': outcome,  # 'hired', 'rejected', 'no_response'
            'timestamp': datetime.now()
        })
        
        # Trigger model retraining if enough new data
        if self.should_retrain():
            self.schedule_model_retraining()
    
    def calculate_model_accuracy(self):
        """Calculate prediction accuracy for model improvement"""
        predictions = self.db.applications.find({'actual_outcome': {'$exists': True}})
        
        correct_predictions = 0
        total_predictions = 0
        
        for pred in predictions:
            predicted_success = pred['predicted_success'] > 0.5
            actual_success = pred['actual_outcome'] == 'hired'
            
            if predicted_success == actual_success:
                correct_predictions += 1
            total_predictions += 1
        
        return correct_predictions / total_predictions if total_predictions > 0 else 0
```

## 🎯 Implementation Timeline

### **Phase 1: MVP Chrome Extension (3-4 weeks)**
- [ ] Basic job detection for LinkedIn/Indeed
- [ ] Simple popup interface
- [ ] API integration with existing Aria backend
- [ ] Basic success prediction (rule-based)

### **Phase 2: ML Success Prediction (4-5 weeks)**
- [ ] Training data collection system
- [ ] ML model development and training
- [ ] Enhanced prediction API
- [ ] Success probability visualization

### **Phase 3: Advanced Features (3-4 weeks)**
- [ ] Multi-site support (Glassdoor, Monster, etc.)
- [ ] Real-time market analysis
- [ ] Smart notifications
- [ ] Analytics dashboard

### **Phase 4: Production & Optimization (2-3 weeks)**
- [ ] Chrome Web Store deployment
- [ ] Cloud infrastructure setup
- [ ] Performance optimization
- [ ] User testing and feedback

## **Total Estimated Timeline: 12-16 weeks**

This transforms Aria from a standalone app into a powerful browser-integrated career assistant that proactively helps you make smart application decisions!

Would you like me to start with the Chrome extension MVP, focusing on the job detection and basic API integration?