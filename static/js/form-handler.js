// Form handling and localStorage management

let workExperienceCount = 0;
let educationCount = 0;
let certificationCount = 0;
let projectCount = 0;

// Initialize form with one entry for each dynamic section
window.addEventListener('DOMContentLoaded', () => {
    addWorkExperience();
    addEducation();
    loadFromLocalStorage();
    setupAutoSave();
});

function addWorkExperience() {
    const container = document.getElementById('workExperienceContainer');
    const id = workExperienceCount++;

    const entry = document.createElement('div');
    entry.className = 'work-experience-entry';
    entry.id = `work-exp-${id}`;
    entry.innerHTML = `
        <div class="entry-header">
            <h4>Experience ${id + 1}</h4>
            <button type="button" class="btn-remove" onclick="removeEntry('work-exp-${id}')">Remove</button>
        </div>
        <input type="text" name="jobTitle-${id}" placeholder="Job Title" required>
        <input type="text" name="company-${id}" placeholder="Company Name" required>
        <input type="text" name="location-${id}" placeholder="Location (City, State)" required>
        <div class="form-grid">
            <input type="text" name="startDate-${id}" placeholder="Start Date (MM/YYYY)" required>
            <input type="text" name="endDate-${id}" placeholder="End Date (MM/YYYY or Present)" required>
        </div>
        <textarea name="responsibilities-${id}" rows="3" placeholder="Responsibilities (one per line)"></textarea>
        <textarea name="achievements-${id}" rows="3" placeholder="Achievements (one per line)"></textarea>
        <textarea name="technologies-${id}" rows="2" placeholder="Technologies Used (comma-separated)"></textarea>
    `;
    container.appendChild(entry);
}

function addEducation() {
    const container = document.getElementById('educationContainer');
    const id = educationCount++;

    const entry = document.createElement('div');
    entry.className = 'education-entry';
    entry.id = `education-${id}`;
    entry.innerHTML = `
        <div class="entry-header">
            <h4>Education ${id + 1}</h4>
            <button type="button" class="btn-remove" onclick="removeEntry('education-${id}')">Remove</button>
        </div>
        <div class="form-grid">
            <input type="text" name="degreeType-${id}" placeholder="Degree Type (BS, MS, etc.)" required>
            <input type="text" name="fieldOfStudy-${id}" placeholder="Field of Study" required>
        </div>
        <input type="text" name="institution-${id}" placeholder="Institution Name" required>
        <div class="form-grid">
            <input type="text" name="eduLocation-${id}" placeholder="Location (City, State)" required>
            <input type="text" name="graduationDate-${id}" placeholder="Graduation Date (MM/YYYY)" required>
        </div>
        <input type="number" name="gpa-${id}" placeholder="GPA (optional)" step="0.01" min="0" max="4">
        <textarea name="honors-${id}" rows="2" placeholder="Honors (comma-separated, optional)"></textarea>
    `;
    container.appendChild(entry);
}

function addCertification() {
    const container = document.getElementById('certificationsContainer');
    const id = certificationCount++;

    const entry = document.createElement('div');
    entry.className = 'certification-entry';
    entry.id = `cert-${id}`;
    entry.innerHTML = `
        <div class="entry-header">
            <h4>Certification ${id + 1}</h4>
            <button type="button" class="btn-remove" onclick="removeEntry('cert-${id}')">Remove</button>
        </div>
        <input type="text" name="certName-${id}" placeholder="Certification Name" required>
        <input type="text" name="certOrg-${id}" placeholder="Issuing Organization" required>
        <div class="form-grid">
            <input type="text" name="certIssueDate-${id}" placeholder="Issue Date (MM/YYYY)" required>
            <input type="text" name="certExpDate-${id}" placeholder="Expiration Date (optional)">
        </div>
    `;
    container.appendChild(entry);
}

function addProject() {
    const container = document.getElementById('projectsContainer');
    const id = projectCount++;

    const entry = document.createElement('div');
    entry.className = 'project-entry';
    entry.id = `project-${id}`;
    entry.innerHTML = `
        <div class="entry-header">
            <h4>Project ${id + 1}</h4>
            <button type="button" class="btn-remove" onclick="removeEntry('project-${id}')">Remove</button>
        </div>
        <input type="text" name="projectName-${id}" placeholder="Project Name" required>
        <input type="text" name="projectRole-${id}" placeholder="Your Role" required>
        <input type="text" name="projectDuration-${id}" placeholder="Duration" required>
        <textarea name="projectDesc-${id}" rows="3" placeholder="Project Description" required></textarea>
        <textarea name="projectTech-${id}" rows="2" placeholder="Technologies (comma-separated)"></textarea>
        <input type="url" name="projectUrl-${id}" placeholder="Project URL (optional)">
    `;
    container.appendChild(entry);
}

function removeEntry(entryId) {
    const entry = document.getElementById(entryId);
    if (entry) {
        entry.remove();
    }
}

function clearForm() {
    if (confirm('Are you sure you want to clear all form data?')) {
        document.getElementById('resumeForm').reset();
        document.getElementById('workExperienceContainer').innerHTML = '';
        document.getElementById('educationContainer').innerHTML = '';
        document.getElementById('certificationsContainer').innerHTML = '';
        document.getElementById('projectsContainer').innerHTML = '';

        workExperienceCount = 0;
        educationCount = 0;
        certificationCount = 0;
        projectCount = 0;

        addWorkExperience();
        addEducation();

        localStorage.removeItem('resumeFormData');
    }
}

function saveProgress() {
    const formData = collectFormData();
    localStorage.setItem('resumeFormData', JSON.stringify(formData));
    localStorage.setItem('resumeFormTimestamp', new Date().toISOString());
    alert('Progress saved!');
}

function loadFromLocalStorage() {
    const savedData = localStorage.getItem('resumeFormData');
    if (savedData) {
        try {
            const data = JSON.parse(savedData);
            populateForm(data);
        } catch (e) {
            console.error('Error loading saved data:', e);
        }
    }
}

function populateForm(data) {
    // Populate contact info
    if (data.contact_info) {
        document.getElementById('fullName').value = data.contact_info.full_name || '';
        document.getElementById('email').value = data.contact_info.email || '';
        document.getElementById('phone').value = data.contact_info.phone || '';
        document.getElementById('city').value = data.contact_info.city || '';
        document.getElementById('state').value = data.contact_info.state || '';
        document.getElementById('linkedinUrl').value = data.contact_info.linkedin_url || '';
        document.getElementById('portfolioUrl').value = data.contact_info.portfolio_url || '';
        document.getElementById('githubUrl').value = data.contact_info.github_url || '';
    }

    // Populate summary
    if (data.professional_summary) {
        document.getElementById('professionalSummary').value = data.professional_summary;
    }

    // Populate skills
    if (data.skills) {
        document.getElementById('technicalSkills').value = (data.skills.technical_skills || []).join(', ');
        document.getElementById('softSkills').value = (data.skills.soft_skills || []).join(', ');
        document.getElementById('toolsAndTech').value = (data.skills.tools_and_technologies || []).join(', ');
    }

    // Populate job description
    if (data.job_description) {
        document.getElementById('jobTitle').value = data.job_description.job_title || '';
        document.getElementById('companyName').value = data.job_description.company_name || '';
        document.getElementById('jobDescription').value = data.job_description.full_description || '';
    }
}

function setupAutoSave() {
    let autoSaveTimer;
    const form = document.getElementById('resumeForm');

    form.addEventListener('input', () => {
        clearTimeout(autoSaveTimer);
        autoSaveTimer = setTimeout(() => {
            const formData = collectFormData();
            localStorage.setItem('resumeFormData', JSON.stringify(formData));
            localStorage.setItem('resumeFormTimestamp', new Date().toISOString());
        }, 30000); // Auto-save every 30 seconds after last input
    });
}

function collectFormData() {
    const formData = {
        contact_info: {
            full_name: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            city: document.getElementById('city').value,
            state: document.getElementById('state').value,
            linkedin_url: document.getElementById('linkedinUrl').value,
            portfolio_url: document.getElementById('portfolioUrl').value,
            github_url: document.getElementById('githubUrl').value,
        },
        professional_summary: document.getElementById('professionalSummary').value,
        work_experience: collectWorkExperience(),
        education: collectEducation(),
        skills: {
            technical_skills: document.getElementById('technicalSkills').value.split(',').map(s => s.trim()).filter(s => s),
            soft_skills: document.getElementById('softSkills').value.split(',').map(s => s.trim()).filter(s => s),
            tools_and_technologies: document.getElementById('toolsAndTech').value.split(',').map(s => s.trim()).filter(s => s),
            languages: {},
        },
        certifications: collectCertifications(),
        projects: collectProjects(),
    };

    return formData;
}

function collectWorkExperience() {
    const experiences = [];
    const container = document.getElementById('workExperienceContainer');
    const entries = container.querySelectorAll('.work-experience-entry');

    entries.forEach((entry, index) => {
        const jobTitle = entry.querySelector(`[name^="jobTitle"]`)?.value;
        if (jobTitle) {
            experiences.push({
                job_title: jobTitle,
                company_name: entry.querySelector(`[name^="company"]`)?.value || '',
                location: entry.querySelector(`[name^="location"]`)?.value || '',
                start_date: entry.querySelector(`[name^="startDate"]`)?.value || '',
                end_date: entry.querySelector(`[name^="endDate"]`)?.value || '',
                responsibilities: (entry.querySelector(`[name^="responsibilities"]`)?.value || '').split('\n').filter(s => s.trim()),
                achievements: (entry.querySelector(`[name^="achievements"]`)?.value || '').split('\n').filter(s => s.trim()),
                technologies_used: (entry.querySelector(`[name^="technologies"]`)?.value || '').split(',').map(s => s.trim()).filter(s => s),
            });
        }
    });

    return experiences;
}

function collectEducation() {
    const education = [];
    const container = document.getElementById('educationContainer');
    const entries = container.querySelectorAll('.education-entry');

    entries.forEach(entry => {
        const degreeType = entry.querySelector(`[name^="degreeType"]`)?.value;
        if (degreeType) {
            const gpaValue = entry.querySelector(`[name^="gpa"]`)?.value;
            education.push({
                degree_type: degreeType,
                field_of_study: entry.querySelector(`[name^="fieldOfStudy"]`)?.value || '',
                institution_name: entry.querySelector(`[name^="institution"]`)?.value || '',
                location: entry.querySelector(`[name^="eduLocation"]`)?.value || '',
                graduation_date: entry.querySelector(`[name^="graduationDate"]`)?.value || '',
                gpa: gpaValue ? parseFloat(gpaValue) : null,
                honors: (entry.querySelector(`[name^="honors"]`)?.value || '').split(',').map(s => s.trim()).filter(s => s),
            });
        }
    });

    return education;
}

function collectCertifications() {
    const certifications = [];
    const container = document.getElementById('certificationsContainer');
    const entries = container.querySelectorAll('.certification-entry');

    entries.forEach(entry => {
        const certName = entry.querySelector(`[name^="certName"]`)?.value;
        if (certName) {
            certifications.push({
                name: certName,
                issuing_organization: entry.querySelector(`[name^="certOrg"]`)?.value || '',
                issue_date: entry.querySelector(`[name^="certIssueDate"]`)?.value || '',
                expiration_date: entry.querySelector(`[name^="certExpDate"]`)?.value || null,
            });
        }
    });

    return certifications;
}

function collectProjects() {
    const projects = [];
    const container = document.getElementById('projectsContainer');
    const entries = container.querySelectorAll('.project-entry');

    entries.forEach(entry => {
        const projectName = entry.querySelector(`[name^="projectName"]`)?.value;
        if (projectName) {
            projects.push({
                name: projectName,
                role: entry.querySelector(`[name^="projectRole"]`)?.value || '',
                duration: entry.querySelector(`[name^="projectDuration"]`)?.value || '',
                description: entry.querySelector(`[name^="projectDesc"]`)?.value || '',
                technologies: (entry.querySelector(`[name^="projectTech"]`)?.value || '').split(',').map(s => s.trim()).filter(s => s),
                url: entry.querySelector(`[name^="projectUrl"]`)?.value || null,
            });
        }
    });

    return projects;
}
