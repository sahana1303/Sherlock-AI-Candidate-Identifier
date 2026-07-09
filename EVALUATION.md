# Evaluation

## Objective

The Sherlock AI Candidate Identifier identifies the correct interview candidate using participant metadata and AI confidence scoring.

## Evaluation Criteria

- Email Matching
- Candidate Name Matching
- Webcam Status
- Speaking Time
- Confidence Score

## Test Cases

### Test Case 1
Expected Candidate: Sahana Bhairav

Result:
✅ Correctly Identified

Confidence:
94%

---

### Test Case 2
Multiple Participants Present

Result:
✅ Correct Candidate Ranked First

---

### Test Case 3
Incorrect Email

Result:
✅ Confidence Reduced

---

### Test Case 4
Webcam Disabled

Result:
✅ Lower AI Score

## Limitations

- Uses simulated interview data.
- No real-time face recognition in cloud deployment.
- Voice verification is simulated.

## Future Improvements

- Real-time webcam verification
- Voice biometric authentication
- Face embeddings using DeepFace
- LLM-powered transcript analysis
- Multi-camera monitoring

## Conclusion

The proposed solution successfully identifies the interview candidate and provides an explainable confidence score through an interactive Streamlit dashboard.
