// Main application logic

let currentResumeData = null;
let currentJobDescription = null;
let currentMarkdownContent = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('resumeForm');
    form.addEventListener('submit', handleGenerateResume);

    // Check backend health on load
    checkHealth().then(() => {
        console.log('Backend is healthy');
    }).catch(() => {
        console.warn('Backend health check failed - some features may not work');
    });
});

async function handleGenerateResume(event) {
    event.preventDefault();

    const resumeData = collectFormData();
    const jobDescription = {
        job_title: document.getElementById('jobTitle').value,
        company_name: document.getElementById('companyName').value,
        full_description: document.getElementById('jobDescription').value,
    };

    // Validate required fields
    if (!resumeData.contact_info.full_name || !resumeData.contact_info.email) {
        alert('Please fill in required contact information');
        return;
    }

    if (!jobDescription.job_title || !jobDescription.full_description) {
        alert('Please fill in job description');
        return;
    }

    // Store for regeneration
    currentResumeData = resumeData;
    currentJobDescription = jobDescription;

    // Show loading state in modal
    if (window.previewModal) {
        window.previewModal.showLoading();
    }

    try {
        const result = await generateResume(resumeData, jobDescription);
        displayResumePreview(result);
    } catch (error) {
        showError('Failed to generate resume. Please try again.');
        console.error(error);
    }
}

function displayResumePreview(result) {
    // Render markdown to HTML
    const htmlContent = marked.parse(result.markdown_content);

    // Store current markdown for PDF download
    currentMarkdownContent = result.markdown_content;

    // Display in modal
    if (window.previewModal) {
        window.previewModal.displayPreview(htmlContent, {
            match_score: result.match_score.toFixed(1)
        });
    }

    // Save to localStorage
    const generatedResume = {
        markdown: result.markdown_content,
        matchScore: result.match_score,
        timestamp: result.timestamp,
        keywords: result.keywords_used,
    };
    localStorage.setItem('lastGeneratedResume', JSON.stringify(generatedResume));
}

async function downloadPDF() {
    if (!currentMarkdownContent) {
        alert('Please generate a resume first');
        return;
    }

    const contactInfo = currentResumeData?.contact_info;
    const filename = contactInfo?.full_name
        ? `${contactInfo.full_name.replace(/\s+/g, '_')}_Resume.pdf`
        : 'resume.pdf';

    try {
        await downloadResumePDF(currentMarkdownContent, filename);
    } catch (error) {
        showError('Failed to download PDF. Please try again.');
        console.error(error);
    }
}

function showRegenerateOptions() {
    document.getElementById('regenerateModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('regenerateModal').style.display = 'none';
}

async function handleRegenerateResume(variationType) {
    if (!currentResumeData || !currentJobDescription) {
        alert('Please generate a resume first');
        return;
    }

    closeModal();

    // Show loading in preview modal
    if (window.previewModal) {
        window.previewModal.showLoading();
    }

    try {
        const result = await regenerateResume(
            currentResumeData,
            currentJobDescription,
            variationType
        );
        displayResumePreview(result);
    } catch (error) {
        showError('Failed to regenerate resume. Please try again.');
        console.error(error);
    }
}

// Expose globally for onclick handlers in HTML
window.regenerateResume = handleRegenerateResume;

function showError(message) {
    if (window.previewModal) {
        window.previewModal.showError(message);
    } else {
        alert(message);
    }
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    const modal = document.getElementById('regenerateModal');
    if (event.target === modal) {
        closeModal();
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + S to save progress
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        saveProgress();
    }

    // Ctrl/Cmd + G to generate
    if ((event.ctrlKey || event.metaKey) && event.key === 'g') {
        event.preventDefault();
        document.getElementById('generateBtn').click();
    }

    // Escape to close modal
    if (event.key === 'Escape') {
        closeModal();
    }
});
