// Chatbot Arsip - Mobile Specific JavaScript
// Version: 1.0.0

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const mobileDocSelectorToggle = document.getElementById('mobile-doc-selector-toggle');
    const mobileDocSelectorContent = document.getElementById('mobile-doc-selector-content');
    const mobileChatDocumentList = document.getElementById('mobile-chat-document-list');
    const mobileDocumentSearch = document.getElementById('mobile-document-search');
    const selectedDocName = document.getElementById('selected-doc-name');
    const mobileChatFab = document.getElementById('mobile-chat-fab');
    
    // Check if we're on a mobile device
    const isMobile = window.innerWidth <= 767;
    
    // Only show mobile elements on mobile devices
    if (isMobile) {
        // Show mobile document selector toggle
        if (mobileDocSelectorToggle) {
            mobileDocSelectorToggle.style.display = 'flex';
        }
        
        // Show mobile FAB
        if (mobileChatFab) {
            mobileChatFab.style.display = 'flex';
        }
        
        // Toggle mobile document selector
        if (mobileDocSelectorToggle && mobileDocSelectorContent) {
            mobileDocSelectorToggle.addEventListener('click', function() {
                const isExpanded = mobileDocSelectorToggle.getAttribute('aria-expanded') === 'true';
                mobileDocSelectorToggle.setAttribute('aria-expanded', !isExpanded);
                mobileDocSelectorToggle.classList.toggle('active');
                mobileDocSelectorContent.classList.toggle('active');
            });
        }
        
        // Handle mobile document search
        if (mobileDocumentSearch) {
            mobileDocumentSearch.addEventListener('input', function(e) {
                // Use the same function as desktop but with mobile elements
                filterChatDocuments(e.target.value, mobileChatDocumentList);
            });
        }
        
        // Handle mobile FAB click
        if (mobileChatFab) {
            mobileChatFab.addEventListener('click', function() {
                // Navigate to chat section
                navigateToSection('chat');
                
                // Focus on chat input if a document is selected
                if (selectedChatDocumentId) {
                    setTimeout(() => {
                        const chatInput = document.getElementById('chat-input');
                        if (chatInput && !chatInput.disabled) {
                            chatInput.focus();
                        }
                    }, 300);
                }
            });
        }
        
        // Sync document selection between desktop and mobile
        function syncDocumentSelection() {
            // Clone desktop document list to mobile
            const desktopDocList = document.getElementById('chat-document-list');
            if (desktopDocList && mobileChatDocumentList) {
                mobileChatDocumentList.innerHTML = desktopDocList.innerHTML;
                
                // Add event listeners to mobile document items
                const mobileDocItems = mobileChatDocumentList.querySelectorAll('.chat-document-item');
                mobileDocItems.forEach(item => {
                    item.addEventListener('click', function() {
                        const docId = this.dataset.docId;
                        const docFilename = this.dataset.docFilename;
                        
                        // Use the same function as desktop
                        activateChatWithDocument(docId, docFilename);
                        
                        // Update selected document name in toggle
                        if (selectedDocName) {
                            selectedDocName.textContent = docFilename || 'Pilih Dokumen';
                        }
                        
                        // Close the document selector
                        mobileDocSelectorToggle.setAttribute('aria-expanded', 'false');
                        mobileDocSelectorToggle.classList.remove('active');
                        mobileDocSelectorContent.classList.remove('active');
                    });
                });
            }
        }
        
        // Override the original renderChatDocumentSelectionList function to sync with mobile
        const originalRenderChatDocumentSelectionList = window.renderChatDocumentSelectionList;
        if (typeof originalRenderChatDocumentSelectionList === 'function') {
            window.renderChatDocumentSelectionList = function(documents) {
                // Call the original function
                originalRenderChatDocumentSelectionList(documents);
                
                // Sync with mobile
                syncDocumentSelection();
            };
        }
        
        // Override activateChatWithDocument to update mobile UI
        const originalActivateChatWithDocument = window.activateChatWithDocument;
        if (typeof originalActivateChatWithDocument === 'function') {
            window.activateChatWithDocument = function(docId, docFilename) {
                // Call the original function
                originalActivateChatWithDocument(docId, docFilename);
                
                // Update mobile UI
                if (selectedDocName) {
                    selectedDocName.textContent = docFilename || 'Pilih Dokumen';
                }
            };
        }
        
        // Initial sync
        setTimeout(syncDocumentSelection, 1000);
    }
    
    // Handle orientation change
    window.addEventListener('orientationchange', function() {
        // Adjust UI based on new orientation
        setTimeout(function() {
            const newIsMobile = window.innerWidth <= 767;
            
            // Show/hide mobile elements based on new width
            if (mobileDocSelectorToggle) {
                mobileDocSelectorToggle.style.display = newIsMobile ? 'flex' : 'none';
            }
            
            if (mobileChatFab) {
                mobileChatFab.style.display = newIsMobile ? 'flex' : 'none';
            }
            
            // Re-sync document selection if needed
            if (newIsMobile) {
                setTimeout(syncDocumentSelection, 500);
            }
        }, 300);
    });
    
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            const newIsMobile = window.innerWidth <= 767;
            
            // Show/hide mobile elements based on new width
            if (mobileDocSelectorToggle) {
                mobileDocSelectorToggle.style.display = newIsMobile ? 'flex' : 'none';
            }
            
            if (mobileChatFab) {
                mobileChatFab.style.display = newIsMobile ? 'flex' : 'none';
            }
            
            // Re-sync document selection if needed
            if (newIsMobile) {
                setTimeout(syncDocumentSelection, 500);
            }
        }, 300);
    });
});