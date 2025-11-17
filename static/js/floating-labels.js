/**
 * Floating Labels Handler
 * Manages Material Design-style floating labels for form inputs
 */

(function() {
    'use strict';

    /**
     * Initialize floating labels on page load
     */
    function initFloatingLabels() {
        // Handle select elements specially
        const selects = document.querySelectorAll('.form-field select');
        selects.forEach(select => {
            // Float label if select has a value
            updateSelectLabel(select);

            // Update on change
            select.addEventListener('change', function() {
                updateSelectLabel(this);
            });
        });

        // Handle dynamic form fields
        observeDynamicFields();
    }

    /**
     * Update label position for select elements
     */
    function updateSelectLabel(select) {
        const label = select.nextElementSibling;
        if (label && label.tagName === 'LABEL') {
            if (select.value !== '') {
                label.classList.add('floated');
            } else {
                label.classList.remove('floated');
            }
        }
    }

    /**
     * Observe DOM for dynamically added form fields
     */
    function observeDynamicFields() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === 1) { // Element node
                        // Check if the node or its descendants contain form fields
                        const selects = node.querySelectorAll ? node.querySelectorAll('.form-field select') : [];
                        selects.forEach(select => {
                            updateSelectLabel(select);
                            select.addEventListener('change', function() {
                                updateSelectLabel(this);
                            });
                        });
                    }
                });
            });
        });

        // Observe the form container
        const formContainer = document.getElementById('resumeForm');
        if (formContainer) {
            observer.observe(formContainer, {
                childList: true,
                subtree: true
            });
        }
    }

    /**
     * Add validation feedback animations
     */
    function initValidationFeedback() {
        const form = document.getElementById('resumeForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const invalidInputs = form.querySelectorAll('input:invalid, textarea:invalid, select:invalid');

            invalidInputs.forEach(input => {
                input.classList.add('attempted');

                // Remove class after animation
                setTimeout(() => {
                    input.classList.remove('attempted');
                }, 400);
            });
        });
    }

    /**
     * Initialize loading state for generate button
     */
    function initButtonLoadingStates() {
        const generateBtn = document.getElementById('generateBtn');
        if (!generateBtn) return;

        const form = document.getElementById('resumeForm');
        if (!form) return;

        form.addEventListener('submit', function(e) {
            // Add loading class
            generateBtn.classList.add('loading');
            generateBtn.disabled = true;

            // Note: The actual form submission will be handled by the existing app.js
            // This just adds the visual loading state
        });

        // Remove loading state on error or completion (handled by app.js)
        window.addEventListener('resume-generated', function() {
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        });

        window.addEventListener('resume-error', function() {
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        });
    }

    /**
     * Add slide-in animation to new entry cards
     */
    function enhanceEntryAnimations() {
        // This is handled by CSS, but we can add additional JS enhancements if needed
        // For now, the CSS animation is sufficient
    }

    /**
     * Initialize all enhancements
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                initFloatingLabels();
                initValidationFeedback();
                initButtonLoadingStates();
                enhanceEntryAnimations();
            });
        } else {
            initFloatingLabels();
            initValidationFeedback();
            initButtonLoadingStates();
            enhanceEntryAnimations();
        }
    }

    // Initialize
    init();

})();
