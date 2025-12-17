# AI Tools Usage Documentation

**Project**: RAG Policy Assistant  
**Date**: December 2025  
**Author**: Adil Naseer Khawaja

---

## Overview

This document describes the AI code generation tools and assistants used in developing this RAG Policy Assistant project, along with reflections on what worked well and what didn't.

---

## AI Tools Used

### 1. **Chat GPT - Primary Development Assistant**

**Version**: ChatGPT Go

**Usage Scope**: ~80-90% of development

**Specific Applications**:

#### **A. Initial Setup & Architecture (Google Colab Phase)**
- Generated complete RAG pipeline structure
- Created document processing modules
- Implemented vector store integration with ChromaDB
- Built initial evaluation framework

**What worked well**:
- ✅ Chat GPT provided well-structured, modular code from the start
- ✅ Excellent at explaining LangChain patterns and best practices
- ✅ Generated comprehensive docstrings and type hints
- ✅ Suggested appropriate chunking strategies (RecursiveCharacterTextSplitter)
- ✅ Helped troubleshoot OpenAI API integration issues

**What didn't work well**:
- ⚠️ Initial suggestions used older LangChain syntax (0.0.x) - had to update to 0.1.x
- ⚠️ Some vector store code needed adaptation for local persistence
- ⚠️ Required iterative refinement for optimal chunk sizes (tried 500, 750, 1000, 1500)

#### **B. Transition to Local Development (Streamlit)**
- Converted Colab notebooks to production Python scripts
- Created Streamlit web interface (app.py)
- Implemented chat interface with message history
- Added source citation display

**What worked well**:
- ✅ Rapid UI prototyping with Streamlit suggestions
- ✅ Good practices for session state management
- ✅ Helpful debugging when encountering "0 chunks" issue
- ✅ Created comprehensive debug script (debug_pipeline.py) that systematically tested each component

**What didn't work well**:
- ⚠️ Initial app structure had `app.py` in root - reorganized to `app/` folder for clarity
- ⚠️ Some CSS styling suggestions didn't render properly in Streamlit - had to simplify

#### **C. Debugging & Troubleshooting**
**Critical Issue Resolved**: Vector store showing "0 chunks"

**Chat GPT's approach**:
1. Created step-by-step debug script testing each pipeline component
2. Identified issue: empty `chroma_db` folder from failed initialization
3. Provided solution: delete folder and re-initialize

**What worked well**:
- ✅ Systematic debugging approach (6-step verification)
- ✅ Clear error messages with color-coded terminal output
- ✅ Root cause analysis that identified the exact problem
- ✅ Verification that pipeline worked end-to-end before assuming data issue

**Impact**: Saved ~2-3 hours of trial-and-error debugging

#### **D. Documentation & Evaluation**
- Co-created design-and-evaluation.md structure
- Suggested evaluation metrics and methodology
- Helped draft README.md with clear setup instructions
- Generated this ai-tooling.md template

**What worked well**:
- ✅ Comprehensive documentation templates
- ✅ Clear explanation of design trade-offs
- ✅ Professional formatting and structure
- ✅ Appropriate level of technical detail

**What didn't work well**:
- ⚠️ Initial evaluation framework was too complex - simplified to focus on required metrics
- ⚠️ Had to add more specific results and numbers manually

#### **E. Dependency Management**
**Critical Issue**: Version conflicts with requirements.txt

**Chat GPT assistance**:
- Recommended using `pip freeze` to capture exact working versions
- Suggested flexible versioning (>=) for better compatibility

**What worked well**:
- ✅ Clear explanation of version pinning trade-offs
- ✅ Practical solution that worked immediately
- ✅ Understanding of dependency resolution issues

---

## Development Workflow

### Typical Interaction Pattern

1. **Describe problem or requirement**
   - Example: "I need to process .md files and create chunks"

2. **Chat GPT suggests solution**
   - Complete code with explanations
   - Multiple options with trade-offs
   - Best practices and warnings

3. **Test and iterate**
   - Run code, identify issues
   - Share error messages
   - Chat GPT debugs and refines

4. **Finalize and document**
   - Clean up code
   - Add comments
   - Update documentation

### Example: Chunking Strategy Development

**Iteration 1**. Chat GPT suggested basic character splitting
```python
# Too simple - broke text at arbitrary points
```

**Iteration 2**: RecursiveCharacterTextSplitter with default settings
```python
# Better but chunk_size=500 was too small
```

**Iteration 3**: Optimized parameters
```python
# Final: chunk_size=1000, overlap=200 - perfect balance
```

**Lesson**: AI suggestions are excellent starting points but require testing and iteration.

---

## Code Generation Statistics (Estimated)

| Component | AI-Generated | Hand-Modified | Ratio |
|-----------|--------------|---------------|-------|
| Document Processing | 90% | 10% | 9:1 |
| Vector Store | 85% | 15% | 5.7:1 |
| RAG Pipeline | 80% | 20% | 4:1 |
| Streamlit App | 75% | 25% | 3:1 |
| Evaluation Scripts | 70% | 30% | 2.3:1 |
| Documentation | 60% | 40% | 1.5:1 |
| **Overall** | **~75%** | **~25%** | **3:1** |

**Notes**:
- "AI-Generated" = initial code structure and logic from Chat GPT
- "Hand-Modified" = debugging, customization, and integration
- Higher modification % for evaluation/docs reflects more manual input needed

---

## Strengths of AI-Assisted Development

### 1. **Rapid Prototyping**
- Generated complete RAG pipeline in hours vs days
- Quick iterations on different approaches
- Immediate feedback on design decisions

### 2. **Best Practices**
- Suggested proper error handling patterns
- Recommended appropriate libraries (LangChain vs manual)
- Enforced clean code structure

### 3. **Debugging Assistance**
- Systematic troubleshooting approaches
- Clear explanations of error messages
- Root cause analysis

### 4. **Documentation**
- Professional documentation templates
- Comprehensive docstrings
- Clear README instructions

### 5. **Learning**
- Explained underlying concepts (RAG, embeddings, vector search)
- Provided context for design decisions
- Suggested resources for deeper understanding

---

## Limitations and Challenges

### 1. **Version Compatibility**
**Issue**: AI training data may reflect older library versions

**Example**: 
- Chat GPT initially suggested LangChain 0.0.x syntax
- Current version 0.1.x has breaking changes
- Required manual updates to imports and method calls

**Solution**: Always verify library versions and check official docs

### 2. **Context Specificity**
**Issue**: Generic suggestions need adaptation to specific use case

**Example**:
- Initial chunk size (500 chars) was too small for our policy documents
- Required testing with actual data to find optimal value (1000 chars)

**Solution**: Treat AI suggestions as starting points, validate with real data

### 3. **Integration Complexity**
**Issue**: AI-generated modules may not integrate perfectly

**Example**:
- Streamlit session state management needed custom handling
- Vector store persistence path required environment-specific configuration

**Solution**: Budget time for integration work and testing

### 4. **Over-Engineering Risk**
**Issue**: AI might suggest more complex solutions than necessary

**Example**:
- Initial evaluation framework had complex metric calculations
- Simplified to focus on required metrics (groundedness, citation, latency)

**Solution**: Start simple, add complexity only when needed

---

## Recommendations for Using AI Tools

### Do's ✅

1. **Start with clear requirements**
   - Describe what you need precisely
   - Provide context and constraints
   - Share relevant code/errors

2. **Iterate and refine**
   - Don't expect perfect code first try
   - Test thoroughly
   - Provide feedback on what works/doesn't

3. **Understand the code**
   - Read and comprehend AI-generated code
   - Don't copy-paste blindly
   - Ask for explanations if unclear

4. **Verify with documentation**
   - Check official library docs
   - Confirm version compatibility
   - Validate best practices

5. **Test systematically**
   - Create debug scripts
   - Test edge cases
   - Measure performance

### Don'ts ❌

1. **Don't trust blindly**
   - AI can hallucinate function names
   - Always test before deploying
   - Verify critical logic manually

2. **Don't skip understanding**
   - Understand why code works
   - Know trade-offs of design decisions
   - Be able to debug independently

3. **Don't ignore warnings**
   - Pay attention to deprecation notices
   - Update outdated patterns
   - Fix security issues

4. **Don't over-rely**
   - Develop your own problem-solving skills
   - Try solutions independently first
   - Use AI as assistant, not replacement

---

## Impact on Development

### Time Savings (Estimated)

| Task | Without AI | With AI | Savings |
|------|-----------|---------|---------|
| Initial setup | 8 hours | 2 hours | 75% |
| RAG pipeline | 12 hours | 3 hours | 75% |
| Streamlit UI | 6 hours | 2 hours | 67% |
| Debugging | 8 hours | 3 hours | 62% |
| Documentation | 6 hours | 3 hours | 50% |
| **Total** | **40 hours** | **13 hours** | **67%** |

**Note**: These are estimates based on typical development time for similar projects

### Quality Improvements

1. **Code Structure**: More modular and maintainable
2. **Error Handling**: Comprehensive try-catch blocks
3. **Documentation**: Better docstrings and comments
4. **Best Practices**: Following industry standards
5. **Testing**: More systematic debugging approach

---

## Lessons Learned

### 1. **AI is a Powerful Accelerator**
- Reduces boilerplate coding time significantly
- Helps explore solutions quickly
- Particularly valuable for well-defined problems (RAG pipelines)

### 2. **Domain Knowledge Still Critical**
- Understanding RAG concepts was essential to guide AI
- Knowing when suggestions were off-track required expertise
- Final decisions on architecture required judgment

### 3. **Iteration is Key**
- First AI-generated solution is rarely perfect
- Testing reveals issues that require refinement
- Conversation-based development works well

### 4. **Balance AI Assistance with Independent Learning**
- Used AI to accelerate but ensured I understood concepts
- Read documentation to verify AI suggestions
- Developed debugging skills through systematic testing

---

## Conclusion

AI tools, particularly Chat GPT, were instrumental in developing this RAG Policy Assistant project efficiently. The combination of rapid code generation, debugging assistance, and comprehensive documentation support reduced development time by an estimated 67% while maintaining high code quality.

**Key Success Factors**:
1. Clear communication of requirements
2. Iterative refinement of solutions
3. Systematic testing and validation
4. Understanding generated code
5. Balancing AI assistance with independent work

**Recommendation**: AI code assistants are highly recommended for RAG application development, particularly for:
- Initial project setup and structure
- Boilerplate code generation
- Debugging and troubleshooting
- Documentation creation

However, human oversight remains critical for:
- Design decisions and trade-offs
- Testing and validation
- Integration and deployment
- Final quality assurance

---

**Document Version**: 1.0  
**Last Updated**: December 15, 2025  
**Author**: Adil Naseer Khawaja