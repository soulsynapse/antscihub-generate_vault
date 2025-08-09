/**
 * AntSciHub Knowledge Vault - Publish JavaScript
 * Custom functionality for published knowledge vault content
 */

(function() {
    'use strict';

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    function init() {
        console.log('AntSciHub Vault - Initializing publish enhancements...');
        
        // Initialize all features
        initializeCallouts();
        initializeWikiLinks();
        initializeMetadata();
        initializeSearch();
        initializeThemeToggle();
        initializeBackToTop();
        
        console.log('AntSciHub Vault - Publish enhancements loaded successfully!');
    }

    /**
     * Initialize collapsible callouts
     */
    function initializeCallouts() {
        const callouts = document.querySelectorAll('.callout');
        
        callouts.forEach(callout => {
            const title = callout.querySelector('.callout-title');
            if (title && title.textContent.includes('+')) {
                title.style.cursor = 'pointer';
                title.addEventListener('click', () => {
                    const content = callout.querySelector('.callout-content') || 
                                   callout.querySelector('p, ul, ol, div:not(.callout-title)');
                    
                    if (content) {
                        const isCollapsed = content.style.display === 'none';
                        content.style.display = isCollapsed ? '' : 'none';
                        
                        // Update title indicator
                        const indicator = title.textContent.includes('▶') ? '▼' : '▶';
                        title.textContent = title.textContent.replace(/[▶▼]/, indicator);
                    }
                });
                
                // Add initial indicator
                if (!title.textContent.includes('▶') && !title.textContent.includes('▼')) {
                    title.textContent = '▼ ' + title.textContent.replace('+', '').trim();
                }
            }
        });
    }

    /**
     * Enhance wiki-style links
     */
    function initializeWikiLinks() {
        // Find all links that look like wiki links
        const wikiLinks = document.querySelectorAll('a[href*="[["], a[data-href*="[["]');
        
        wikiLinks.forEach(link => {
            // Add tooltip on hover
            link.addEventListener('mouseenter', function(e) {
                const tooltip = createTooltip(this.textContent || this.getAttribute('data-href'));
                document.body.appendChild(tooltip);
                positionTooltip(tooltip, e);
            });

            link.addEventListener('mouseleave', function() {
                const tooltip = document.querySelector('.wiki-tooltip');
                if (tooltip) {
                    tooltip.remove();
                }
            });

            link.addEventListener('mousemove', function(e) {
                const tooltip = document.querySelector('.wiki-tooltip');
                if (tooltip) {
                    positionTooltip(tooltip, e);
                }
            });
        });
    }

    /**
     * Create tooltip element
     */
    function createTooltip(text) {
        const tooltip = document.createElement('div');
        tooltip.className = 'wiki-tooltip';
        tooltip.textContent = `Link to: ${text.replace(/[\[\]]/g, '')}`;
        tooltip.style.cssText = `
            position: fixed;
            background: var(--surface-color, #f8fafc);
            border: 1px solid var(--border-color, #e2e8f0);
            border-radius: 0.25rem;
            padding: 0.5rem;
            font-size: 0.875rem;
            z-index: 1000;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            max-width: 200px;
            pointer-events: none;
        `;
        return tooltip;
    }

    /**
     * Position tooltip near cursor
     */
    function positionTooltip(tooltip, event) {
        const padding = 10;
        let x = event.clientX + padding;
        let y = event.clientY + padding;

        // Keep tooltip within viewport
        const rect = tooltip.getBoundingClientRect();
        if (x + rect.width > window.innerWidth) {
            x = event.clientX - rect.width - padding;
        }
        if (y + rect.height > window.innerHeight) {
            y = event.clientY - rect.height - padding;
        }

        tooltip.style.left = x + 'px';
        tooltip.style.top = y + 'px';
    }

    /**
     * Initialize metadata display enhancements
     */
    function initializeMetadata() {
        // Look for YAML frontmatter or metadata sections
        const metadataSections = document.querySelectorAll('.metadata, .frontmatter');
        
        metadataSections.forEach(section => {
            // Add collapse/expand functionality for large metadata
            if (section.children.length > 5) {
                const toggle = document.createElement('button');
                toggle.textContent = 'Show metadata ▼';
                toggle.className = 'metadata-toggle';
                toggle.style.cssText = `
                    background: none;
                    border: 1px solid var(--border-color);
                    border-radius: 0.25rem;
                    padding: 0.25rem 0.5rem;
                    cursor: pointer;
                    margin-bottom: 0.5rem;
                `;
                
                toggle.addEventListener('click', () => {
                    const isHidden = section.style.display === 'none';
                    section.style.display = isHidden ? '' : 'none';
                    toggle.textContent = isHidden ? 'Hide metadata ▲' : 'Show metadata ▼';
                });
                
                section.parentNode.insertBefore(toggle, section);
                section.style.display = 'none';
            }
        });
    }

    /**
     * Initialize simple search functionality
     */
    function initializeSearch() {
        // Create search box
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        `;

        const searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = 'Search...';
        searchInput.className = 'search-input';
        searchInput.style.cssText = `
            padding: 0.5rem;
            border: 1px solid var(--border-color);
            border-radius: 0.25rem;
            background: var(--background-color);
            color: var(--text-color);
            font-size: 0.875rem;
            width: 200px;
        `;

        searchContainer.appendChild(searchInput);
        document.body.appendChild(searchContainer);

        // Simple search functionality
        let searchTimeout;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(e.target.value);
            }, 300);
        });
    }

    /**
     * Perform simple text search and highlight results
     */
    function performSearch(query) {
        // Remove previous highlights
        removeHighlights();

        if (!query || query.length < 2) return;

        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );

        const textNodes = [];
        let node;
        while (node = walker.nextNode()) {
            if (node.parentNode.className !== 'search-input' && 
                node.textContent.toLowerCase().includes(query.toLowerCase())) {
                textNodes.push(node);
            }
        }

        textNodes.forEach(textNode => {
            const parent = textNode.parentNode;
            const text = textNode.textContent;
            const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
            const highlightedText = text.replace(regex, '<mark class="search-highlight">$1</mark>');
            
            if (highlightedText !== text) {
                const span = document.createElement('span');
                span.innerHTML = highlightedText;
                parent.replaceChild(span, textNode);
            }
        });
    }

    /**
     * Remove search highlights
     */
    function removeHighlights() {
        const highlights = document.querySelectorAll('.search-highlight');
        highlights.forEach(highlight => {
            const parent = highlight.parentNode;
            parent.replaceChild(document.createTextNode(highlight.textContent), highlight);
            parent.normalize();
        });
    }

    /**
     * Escape special regex characters
     */
    function escapeRegExp(string) {
        return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    /**
     * Initialize theme toggle (dark/light mode)
     */
    function initializeThemeToggle() {
        const themeToggle = document.createElement('button');
        themeToggle.textContent = '🌙';
        themeToggle.title = 'Toggle dark mode';
        themeToggle.className = 'theme-toggle';
        themeToggle.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            font-size: 1.2rem;
            z-index: 1000;
            transition: all 0.2s ease;
        `;

        themeToggle.addEventListener('click', () => {
            const isDark = document.documentElement.hasAttribute('data-theme');
            
            if (isDark) {
                document.documentElement.removeAttribute('data-theme');
                themeToggle.textContent = '🌙';
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                themeToggle.textContent = '☀️';
                localStorage.setItem('theme', 'dark');
            }
        });

        // Apply saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeToggle.textContent = '☀️';
        }

        document.body.appendChild(themeToggle);
    }

    /**
     * Initialize back to top button
     */
    function initializeBackToTop() {
        const backToTop = document.createElement('button');
        backToTop.textContent = '↑';
        backToTop.title = 'Back to top';
        backToTop.className = 'back-to-top';
        backToTop.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            cursor: pointer;
            font-size: 1.2rem;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1000;
        `;

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Show/hide based on scroll position
        window.addEventListener('scroll', () => {
            backToTop.style.opacity = window.scrollY > 300 ? '1' : '0';
        });

        document.body.appendChild(backToTop);
    }

    // Add CSS for dynamic elements
    const style = document.createElement('style');
    style.textContent = `
        .search-highlight {
            background-color: var(--accent-color, #f59e0b);
            color: black;
            padding: 0.1rem;
            border-radius: 0.2rem;
        }

        .theme-toggle:hover,
        .back-to-top:hover {
            transform: scale(1.1);
        }

        @media (max-width: 768px) {
            .search-container {
                top: 10px;
                right: 10px;
            }
            
            .search-input {
                width: 150px;
            }
            
            .theme-toggle {
                top: 10px;
                left: 10px;
            }
            
            .back-to-top {
                bottom: 10px;
                right: 10px;
            }
        }
    `;
    document.head.appendChild(style);

})();
