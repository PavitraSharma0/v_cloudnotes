class Dashboard {
  constructor() {
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.loadUserData();
    this.animateOnLoad();
  }

  setupEventListeners() {
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', this.handleNavigation.bind(this));
    });

    // Post cards
    document.querySelectorAll('.post-card').forEach(card => {
      card.addEventListener('click', this.handlePostClick.bind(this));
    });

    // Upload items
    document.querySelectorAll('.upload-item').forEach(item => {
      item.addEventListener('click', this.handleUploadClick.bind(this));
    });

    // Action buttons
    document.querySelectorAll('.action-button').forEach(button => {
      button.addEventListener('click', this.handleActionClick.bind(this));
    });

    // AI Assistant button
    const aiButton = document.querySelector('.ai-button');
    if (aiButton) aiButton.addEventListener('click', this.openAIAssistant.bind(this));

    // Notification bell
    const notifBell = document.querySelector('.notification-bell');
    if (notifBell) notifBell.addEventListener('click', this.toggleNotifications.bind(this));

    // User avatar
    const userAvatar = document.querySelector('.user-avatar');
    if (userAvatar) userAvatar.addEventListener('click', this.openUserMenu.bind(this));
  }

  handleNavigation(event) {
    event.preventDefault();
    const link = event.currentTarget;

    // Remove active class from all links
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));

    // Add active class to clicked link
    link.classList.add('active');

    // Here you would typically handle routing
    console.log('Navigating to:', link.textContent.trim());
  }

  handlePostClick(event) {
    // Allow clicks on inner controls not to trigger open
    const postCard = event.currentTarget;
    const postTitleEl = postCard.querySelector('.post-title');
    const postTitle = postTitleEl ? postTitleEl.textContent.trim() : 'Untitled';

    // Add click animation
    postCard.style.transform = 'scale(0.98)';
    setTimeout(() => {
      postCard.style.transform = '';
    }, 150);

    console.log('Opening post:', postTitle);
    // Here you would open the post detail view
  }

  handleUploadClick(event) {
    const uploadItem = event.currentTarget;
    const uploadTitleEl = uploadItem.querySelector('.upload-title');
    const uploadTitle = uploadTitleEl ? uploadTitleEl.textContent.trim() : 'Upload';

    console.log('Managing upload:', uploadTitle);
    // Here you would open the upload management view
  }

  handleActionClick(event) {
    event.stopPropagation();
    const button = event.currentTarget;
    // Attempt to read a data-action first for more reliable detection
    const actionData = button.dataset.action;
    const actionText = actionData || (button.querySelector('span') ? button.querySelector('span').textContent.trim() : button.textContent.trim());

    // Add click animation
    button.style.transform = 'scale(0.95)';
    setTimeout(() => {
      button.style.transform = '';
    }, 150);

    switch (actionText) {
      case 'Upload Notes':
      case 'upload-notes':
        this.openUploadDialog();
        break;
      case 'Create Study Set':
      case 'create-study-set':
        this.openStudySetCreator();
        break;
      case 'Search Materials':
      case 'search-materials':
        this.openSearchDialog();
        break;
      case 'AI Assistant':
      case 'ai-assistant':
        this.openAIAssistant();
        break;
      default:
        console.log('Unhandled action:', actionText);
    }
  }

  openUploadDialog() {
    console.log('Opening upload dialog...');
    // Here you would open the upload modal/page
    this.showToast('Open upload dialog (stub)', 'info');
  }

  openStudySetCreator() {
    console.log('Opening study set creator...');
    // Here you would open the study set creation tool
    this.showToast('Open study set creator (stub)', 'info');
  }

  openSearchDialog() {
    console.log('Opening search dialog...');
    // Here you would open the search interface
    this.showToast('Open search dialog (stub)', 'info');
  }

  openAIAssistant() {
    console.log('Opening AI Assistant...');
    // Here you would open the AI chat interface
    this.showAIAssistantModal();
  }

  showAIAssistantModal() {
    // Create a simple modal for demonstration
    const modal = document.createElement('div');
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
      box-sizing: border-box;
    `;

    const surfaceColor = getComputedStyle(document.documentElement).getPropertyValue('--surface-color') || '#fff';
    const borderColor = getComputedStyle(document.documentElement).getPropertyValue('--border-color') || '#e5e7eb';
    const textPrimary = getComputedStyle(document.documentElement).getPropertyValue('--text-primary') || '#111827';
    const textSecondary = getComputedStyle(document.documentElement).getPropertyValue('--text-secondary') || '#6b7280';
    const secondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color') || '#6366f1';

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
      background: ${surfaceColor};
      padding: 28px;
      border-radius: 12px;
      border: 1px solid ${borderColor};
      max-width: 560px;
      width: 100%;
      text-align: center;
      box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    `;

    modalContent.innerHTML = `
      <h3 style="color: ${textPrimary}; margin-bottom: 12px;">AI Study Assistant</h3>
      <p style="color: ${textSecondary}; margin-bottom: 18px;">
        Ask me anything about your study materials, get explanations, or create summaries!
      </p>
      <div style="display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">
        <button id="aiCloseBtn" style="
          background: ${secondaryColor};
          color: white;
          border: none;
          padding: 10px 18px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
        ">Got it!</button>
        <button id="aiOpenChat" style="
          background: transparent;
          color: ${textPrimary};
          border: 1px solid ${borderColor};
          padding: 10px 18px;
          border-radius: 8px;
          cursor: pointer;
          font-weight: 600;
        ">Open Chat</button>
      </div>
    `;

    modal.appendChild(modalContent);
    document.body.appendChild(modal);

    // Close modal
    modal.querySelector('#aiCloseBtn').addEventListener('click', () => {
      document.body.removeChild(modal);
    });

    modal.querySelector('#aiOpenChat').addEventListener('click', () => {
      document.body.removeChild(modal);
      // Hook to open the full AI assistant page/modal if available
      this.showToast('Opening full AI assistant (stub)', 'success');
    });

    // Click outside to close
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        document.body.removeChild(modal);
      }
    });
  }

  toggleNotifications() {
    console.log('Toggling notifications...');
    // Here you would show/hide the notifications dropdown
    this.showToast('Toggled notifications (stub)', 'info');
  }

  openUserMenu() {
    console.log('Opening user menu...');
    // Here you would show the user profile menu
    this.showToast('Open user menu (stub)', 'info');
  }

  loadUserData() {
    // Simulate loading user data
    console.log('Loading user dashboard data...');

    // You would typically fetch this from an API
    const userData = {
      name: 'Alex',
      savedPosts: 127,
      uploads: 23,
      followers: 89,
      following: 156
    };

    // Update the welcome message
    const welcomeTitle = document.querySelector('.welcome-title');
    if (welcomeTitle) {
      welcomeTitle.textContent = `Welcome back, ${userData.name}`;
    }

    // Update stat cards if present
    const statMap = {
      saved: userData.savedPosts,
      uploads: userData.uploads,
      followers: userData.followers,
      following: userData.following
    };

    Object.keys(statMap).forEach(key => {
      const el = document.querySelector(`.stat-${key} .stat-number`);
      if (el) el.textContent = statMap[key];
    });
  }

  animateOnLoad() {
    // Add entrance animations
    const elements = document.querySelectorAll('.stat-card, .post-card, .upload-item, .notification-item');

    elements.forEach((element, index) => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(20px)';

      setTimeout(() => {
        element.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      }, index * 100);
    });
  }

  // Utility method to show toast notifications
  showToast(message, type = 'info') {
    const successColor = getComputedStyle(document.documentElement).getPropertyValue('--success-color') || '#10b981';
    const secondaryColor = getComputedStyle(document.documentElement).getPropertyValue('--secondary-color') || '#6366f1';
    const bg = type === 'success' ? successColor : secondaryColor;

    const toast = document.createElement('div');
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: ${bg};
      color: white;
      padding: 12px 18px;
      border-radius: 8px;
      z-index: 1000;
      box-shadow: 0 8px 30px rgba(0,0,0,0.15);
      animation: slideIn 0.3s ease-out;
      font-weight: 600;
      max-width: 320px;
    `;

    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease-in';
      setTimeout(() => {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 3000);
  }
}

/* Toast animation keyframes */
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to   { transform: translateX(0); opacity: 1; }
  }
  @keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to   { transform: translateX(100%); opacity: 0; }
  }
  @keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.12); }
    100% { transform: scale(1); }
  }
`;
document.head.appendChild(style);

/* Initialize dashboard and demo interactions once DOM is ready */
document.addEventListener('DOMContentLoaded', () => {
  // Initialize core Dashboard
  const dashboard = new Dashboard();

  // Simulate real-time notifications demo
  setTimeout(() => {
    const notificationCount = document.querySelector('.notification-count');
    if (notificationCount) {
      let count = parseInt(notificationCount.textContent || '0', 10);
      setInterval(() => {
        if (Math.random() > 0.7) { // ~30% chance every 10s
          count++;
          notificationCount.textContent = count;
          notificationCount.style.animation = 'pulse 0.5s ease-in-out';
          setTimeout(() => {
            notificationCount.style.animation = '';
          }, 500);
        }
      }, 10000);
    }
  }, 5000);

  // Example: auto-open AI assistant if ?ai=true in URL (handy for testing)
  try {
    const url = new URL(window.location.href);
    if (url.searchParams.get('ai') === 'true') {
      dashboard.openAIAssistant();
    }
  } catch (e) {
    // ignore URL parse errors (e.g., in weird environments)
  }
});