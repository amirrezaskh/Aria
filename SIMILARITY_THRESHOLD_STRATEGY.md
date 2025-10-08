# Similarity Threshold Selection Strategy

## Threshold Determination Methodology

### 1. **Multi-Tier Threshold System**

```python
class SimilarityThresholds:
    VERY_HIGH = 0.95    # Almost identical jobs (same company, similar role)
    HIGH = 0.85         # Very similar (same role type, similar requirements)
    MEDIUM = 0.75       # Moderately similar (same domain, different specifics)
    LOW = 0.65          # Somewhat similar (transferable skills)
    
    @classmethod
    def get_threshold_label(cls, score: float) -> str:
        if score >= cls.VERY_HIGH:
            return "Nearly Identical"
        elif score >= cls.HIGH:
            return "Very Similar"
        elif score >= cls.MEDIUM:
            return "Similar"
        elif score >= cls.LOW:
            return "Somewhat Similar"
        else:
            return "Different"
    
    @classmethod
    def should_show_match(cls, score: float) -> bool:
        return score >= cls.MEDIUM  # Show matches >= 75%
```

### 2. **Dynamic Threshold Adaptation**

```python
class AdaptiveThresholdManager:
    def __init__(self):
        self.user_feedback_data = {}
        self.default_threshold = 0.75
    
    async def get_personalized_threshold(self, user_id: str) -> float:
        """Get personalized threshold based on user behavior"""
        
        # Get user's historical feedback
        feedback = await self.get_user_feedback_history(user_id)
        
        if not feedback:
            return self.default_threshold
        
        # Analyze patterns
        accepted_scores = [f['similarity_score'] for f in feedback if f['action'] == 'accepted']
        rejected_scores = [f['similarity_score'] for f in feedback if f['action'] == 'rejected']
        
        if len(accepted_scores) >= 5:
            # User tends to accept suggestions at this level
            return min(accepted_scores) - 0.05
        
        return self.default_threshold
    
    async def update_threshold_feedback(self, 
                                      user_id: str, 
                                      similarity_score: float, 
                                      user_action: str):
        """Update threshold based on user feedback"""
        # Store: user accepted/rejected similarity suggestion
        feedback_entry = {
            'user_id': user_id,
            'similarity_score': similarity_score,
            'action': user_action,  # 'accepted', 'rejected', 'modified'
            'timestamp': datetime.now()
        }
        await self.store_feedback(feedback_entry)
```

### 3. **A/B Testing Framework**

```python
class ThresholdExperiment:
    """A/B test different thresholds to optimize user experience"""
    
    EXPERIMENTS = {
        'conservative': 0.85,   # High threshold, fewer but better matches
        'moderate': 0.75,       # Balanced approach
        'liberal': 0.65,        # Lower threshold, more matches
    }
    
    async def assign_user_to_experiment(self, user_id: str) -> float:
        """Assign user to threshold experiment group"""
        # Hash user_id to get consistent assignment
        import hashlib
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        group = hash_val % 3
        
        experiment_names = list(self.EXPERIMENTS.keys())
        selected_experiment = experiment_names[group]
        
        return self.EXPERIMENTS[selected_experiment]
```

## Performance Optimization Strategy

### 1. **Embedding Caching**

```python
class EmbeddingCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.cache_ttl = 3600 * 24 * 7  # 1 week
    
    async def get_cached_embedding(self, text_hash: str) -> Optional[List[float]]:
        """Get cached embedding if available"""
        cached = await self.redis.get(f"embedding:{text_hash}")
        if cached:
            return json.loads(cached)
        return None
    
    async def cache_embedding(self, text_hash: str, embedding: List[float]):
        """Cache embedding for future use"""
        await self.redis.setex(
            f"embedding:{text_hash}", 
            self.cache_ttl, 
            json.dumps(embedding)
        )
    
    def get_text_hash(self, text: str) -> str:
        """Generate hash for text content"""
        import hashlib
        return hashlib.sha256(text.encode()).hexdigest()
```

### 2. **Batch Processing**

```python
class BatchSimilarityProcessor:
    async def process_similarity_batch(self, user_id: str, new_jobs: List[Dict]):
        """Process multiple jobs at once for efficiency"""
        
        # Generate embeddings in batch
        embeddings = await self.generate_embeddings_batch([
            job['combined_text'] for job in new_jobs
        ])
        
        # Store all jobs with embeddings
        job_ids = []
        for job, embedding in zip(new_jobs, embeddings):
            job_id = await self.store_job_with_embedding(user_id, job, embedding)
            job_ids.append(job_id)
        
        # Find similarities for all new jobs
        similarities = await self.find_similarities_batch(user_id, embeddings)
        
        return job_ids, similarities
```

## User Experience Integration

### 1. **Similarity Notification Component**

```typescript
// Frontend component for showing similar jobs
interface SimilarJobMatch {
  jobId: string;
  companyName: string;
  positionTitle: string;
  similarityScore: number;
  applicationStatus: string;
  createdAt: string;
  resumePath?: string;
  coverLetterPath?: string;
}

const SimilarJobNotification: React.FC<{
  matches: SimilarJobMatch[];
  onAcceptMatch: (jobId: string) => void;
  onRejectMatch: (jobId: string) => void;
  onViewDetails: (jobId: string) => void;
}> = ({ matches, onAcceptMatch, onRejectMatch, onViewDetails }) => {
  
  if (matches.length === 0) return null;
  
  return (
    <Alert 
      severity="info" 
      sx={{ mb: 3 }}
      action={
        <Button color="inherit" size="small" onClick={() => setExpanded(!expanded)}>
          {expanded ? 'Hide' : 'Show'} Similar Jobs
        </Button>
      }
    >
      <AlertTitle>🎯 Similar Job Found!</AlertTitle>
      We found {matches.length} similar job{matches.length > 1 ? 's' : ''} you've applied to before.
      
      {expanded && (
        <Box sx={{ mt: 2 }}>
          {matches.map(match => (
            <Card key={match.jobId} sx={{ mb: 1, p: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {match.positionTitle} at {match.companyName}
                  </Typography>
                  <Chip 
                    label={`${Math.round(match.similarityScore * 100)}% similar`}
                    color={match.similarityScore >= 0.9 ? 'success' : 'primary'}
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  <Chip 
                    label={match.applicationStatus}
                    color={getStatusColor(match.applicationStatus)}
                    size="small"
                  />
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1 }}>
                  {match.resumePath && (
                    <Button 
                      size="small" 
                      variant="outlined"
                      onClick={() => onAcceptMatch(match.jobId)}
                    >
                      Use This Resume
                    </Button>
                  )}
                  <Button 
                    size="small" 
                    onClick={() => onViewDetails(match.jobId)}
                  >
                    Details
                  </Button>
                </Box>
              </Box>
            </Card>
          ))}
        </Box>
      )}
    </Alert>
  );
};
```

### 2. **Enhanced Workflow Integration**

```typescript
// Modified useGenerateForm hook
export function useGenerateForm() {
  const [similarJobs, setSimilarJobs] = useState<SimilarJobMatch[]>([]);
  const [showingSimilarJobs, setShowingSimilarJobs] = useState(false);

  const handleStartPersonalization = async () => {
    // Validation...
    
    // Check for similar jobs before proceeding
    const matches = await checkForSimilarJobs({
      company: formData.companyName,
      position: formData.positionTitle,
      description: formData.jobDescription
    });
    
    if (matches.length > 0) {
      setSimilarJobs(matches);
      setShowingSimilarJobs(true);
      // Don't proceed to personalization yet
      return;
    }
    
    // No matches, proceed normally
    setCurrentStep('personalization');
  };

  const handleAcceptSimilarJob = async (jobId: string) => {
    // Use existing resume/cover letter
    const jobData = await getJobApplicationById(jobId);
    setPaths({
      resumePath: jobData.resumePath,
      coverLetterPath: jobData.coverLetterPath
    });
    setCurrentStep('results');
    
    // Track user acceptance for threshold tuning
    await trackSimilarityFeedback(jobId, 'accepted');
  };

  const handleRejectSimilarJob = async () => {
    // User wants to create new documents
    setShowingSimilarJobs(false);
    setCurrentStep('personalization');
    
    // Track rejection for threshold tuning
    for (const job of similarJobs) {
      await trackSimilarityFeedback(job.jobId, 'rejected');
    }
  };
}
```

## Recommended Implementation Plan

### Phase 1: Basic Similarity (Week 1-2)
1. Set up PostgreSQL with pgvector
2. Implement basic embedding generation
3. Simple similarity search with fixed threshold (0.75)
4. Basic UI notification for matches

### Phase 2: Enhanced Matching (Week 3-4)
1. Multi-tier thresholds
2. User feedback collection
3. Performance optimizations (caching, indexing)
4. Detailed similarity explanations

### Phase 3: Intelligent Adaptation (Week 5-6)
1. Adaptive thresholds based on user behavior
2. A/B testing framework
3. Advanced analytics and insights
4. Batch processing for performance

**Recommended starting threshold: 0.75 (75% similarity)**

This provides a good balance between showing relevant matches while avoiding false positives. You can adjust based on user feedback and usage patterns.

Would you like me to start implementing the database schema and similarity search service?