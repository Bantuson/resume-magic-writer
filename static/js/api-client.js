// API client for backend communication

const API_BASE_URL = '';  // Same origin

async function generateResume(resumeData, jobDescription) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/generate-resume`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_data: resumeData,
                job_description: jobDescription,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate resume');
        }

        return await response.json();
    } catch (error) {
        console.error('Error generating resume:', error);
        throw error;
    }
}

async function regenerateResume(resumeData, jobDescription, variationType) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/regenerate-resume`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                resume_data: resumeData,
                job_description: jobDescription,
                variation_type: variationType,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to regenerate resume');
        }

        return await response.json();
    } catch (error) {
        console.error('Error regenerating resume:', error);
        throw error;
    }
}

async function downloadResumePDF(markdownContent, filename) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/download-pdf`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown_content: markdownContent,
                filename: filename,
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to download PDF');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename || 'resume.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error downloading PDF:', error);
        throw error;
    }
}

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return await response.json();
    } catch (error) {
        console.error('Error checking health:', error);
        throw error;
    }
}
