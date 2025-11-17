/**
 * Preview Modal Controller
 * Handles full-screen modal display for resume preview
 */

(function() {
    'use strict';

    let modal = null;
    let modalOverlay = null;
    let modalClose = null;
    let focusedElementBeforeModal = null;
    let focusableElements = [];
    let firstFocusableElement = null;
    let lastFocusableElement = null;

    /**
     * Initialize modal functionality
     */
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', setup);
        } else {
            setup();
        }
    }

    /**
     * Setup modal elements and event listeners
     */
    function setup() {
        modal = document.getElementById('previewModal');
        if (!modal) {
            console.warn('Preview modal element not found');
            return;
        }

        modalOverlay = modal.querySelector('.preview-modal-overlay');
        modalClose = modal.querySelector('.preview-modal-close');

        // Event listeners
        if (modalClose) {
            modalClose.addEventListener('click', closeModal);
        }

        if (modalOverlay) {
            modalOverlay.addEventListener('click', closeModal);
        }

        // Keyboard support
        document.addEventListener('keydown', handleKeyDown);

        // Listen for custom events to open modal
        window.addEventListener('show-resume-preview', handleShowPreview);
    }

    /**
     * Open the modal
     */
    function openModal() {
        if (!modal) return;

        // Store currently focused element
        focusedElementBeforeModal = document.activeElement;

        // Show modal
        modal.classList.add('active');
        modal.setAttribute('aria-hidden', 'false');

        // Lock body scroll
        document.body.style.overflow = 'hidden';

        // Setup focus trap
        setupFocusTrap();

        // Focus first element or close button
        if (firstFocusableElement) {
            firstFocusableElement.focus();
        } else if (modalClose) {
            modalClose.focus();
        }

        // Dispatch event
        window.dispatchEvent(new CustomEvent('modal-opened'));
    }

    /**
     * Close the modal
     */
    function closeModal() {
        if (!modal) return;

        // Hide modal
        modal.classList.remove('active');
        modal.setAttribute('aria-hidden', 'true');

        // Unlock body scroll
        document.body.style.overflow = '';

        // Restore focus
        if (focusedElementBeforeModal && focusedElementBeforeModal.focus) {
            focusedElementBeforeModal.focus();
        }

        // Dispatch event
        window.dispatchEvent(new CustomEvent('modal-closed'));
    }

    /**
     * Setup focus trap within modal
     */
    function setupFocusTrap() {
        if (!modal) return;

        const focusableSelectors = [
            'button:not([disabled])',
            'a[href]',
            'input:not([disabled])',
            'select:not([disabled])',
            'textarea:not([disabled])',
            '[tabindex]:not([tabindex="-1"])'
        ].join(', ');

        focusableElements = Array.from(modal.querySelectorAll(focusableSelectors));
        firstFocusableElement = focusableElements[0];
        lastFocusableElement = focusableElements[focusableElements.length - 1];
    }

    /**
     * Handle keyboard events
     */
    function handleKeyDown(e) {
        if (!modal || !modal.classList.contains('active')) return;

        // Escape key closes modal
        if (e.key === 'Escape' || e.keyCode === 27) {
            e.preventDefault();
            closeModal();
            return;
        }

        // Tab key - implement focus trap
        if (e.key === 'Tab' || e.keyCode === 9) {
            if (focusableElements.length === 0) return;

            if (e.shiftKey) {
                // Shift + Tab
                if (document.activeElement === firstFocusableElement) {
                    e.preventDefault();
                    lastFocusableElement.focus();
                }
            } else {
                // Tab
                if (document.activeElement === lastFocusableElement) {
                    e.preventDefault();
                    firstFocusableElement.focus();
                }
            }
        }
    }

    /**
     * Handle show preview custom event
     */
    function handleShowPreview(event) {
        if (event.detail && event.detail.content) {
            displayPreview(event.detail.content, event.detail.data);
        }
        openModal();
    }

    /**
     * Display resume content in modal
     */
    function displayPreview(content, data) {
        const previewContainer = modal.querySelector('.resume-preview-modal');
        if (!previewContainer) return;

        // Set resume content
        previewContainer.innerHTML = content;

        // Update match score if provided
        if (data && data.match_score) {
            const scoreValue = modal.querySelector('.score-value');
            if (scoreValue) {
                scoreValue.textContent = data.match_score + '%';
            }
        }
    }

    /**
     * Show loading state in modal
     */
    function showLoading() {
        const previewContainer = modal.querySelector('.resume-preview-modal');
        if (!previewContainer) return;

        previewContainer.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Generating your optimized resume...</p>
            </div>
        `;
        openModal();
    }

    /**
     * Show error state in modal
     */
    function showError(message) {
        const previewContainer = modal.querySelector('.resume-preview-modal');
        if (!previewContainer) return;

        previewContainer.innerHTML = `
            <div class="loading-state">
                <p style="color: var(--color-danger);">Error: ${message}</p>
                <button onclick="window.previewModal.close()" class="btn-secondary" style="margin-top: 1rem;">
                    Close
                </button>
            </div>
        `;
        openModal();
    }

    // Public API
    window.previewModal = {
        open: openModal,
        close: closeModal,
        showLoading: showLoading,
        showError: showError,
        displayPreview: displayPreview
    };

    // Initialize
    init();

})();
