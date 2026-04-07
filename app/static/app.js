// Global Utilities
const Api = {
    async fetch(endpoint, options = {}) {
        const token = localStorage.getItem('jwt_token');
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        try {
            const response = await fetch('/api' + endpoint, { ...options, headers });
            const data = await response.json();
            
            if (!response.ok) {
                // If token expired, clear and redirect
                if (response.status === 401 && endpoint !== '/auth/login') {
                    Auth.logout();
                }
                throw new Error(data.description || data.error || 'Server Error');
            }
            return data;
        } catch (e) {
            throw e;
        }
    }
};

const UI = {
    toast(message, type = 'success') {
        let container = document.getElementById('flash-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'flash-container';
            container.className = 'flash-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span class="toast-body">${message}</span>
            <button class="btn" style="border:none;background:none;padding:0;font-size:18px" onclick="this.parentElement.remove()">&times;</button>
        `;
        container.appendChild(toast);
        setTimeout(() => { if (toast.parentElement) toast.remove(); }, 4000);
    },
    
    pagination(containerId, totalPages, currentPage, callbackName) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        if (totalPages <= 1) {
            container.innerHTML = '';
            return;
        }
        
        let html = '<div class="pagination">';
        html += `<button class="page-item" ${currentPage === 1 ? 'disabled' : ''} onclick="${callbackName}(${currentPage - 1})">&lt;</button>`;
        
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
                html += `<button class="page-item ${i === currentPage ? 'active' : ''}" onclick="${callbackName}(${i})">${i}</button>`;
            } else if (i === currentPage - 2 || i === currentPage + 2) {
                html += `<span style="padding: 0 4px">...</span>`;
            }
        }
        
        html += `<button class="page-item" ${currentPage === totalPages ? 'disabled' : ''} onclick="${callbackName}(${currentPage + 1})">&gt;</button>`;
        html += '</div>';
        
        container.innerHTML = html;
    },

    modal: {
        open(modalId) {
            const overlay = document.getElementById(modalId);
            if (overlay) overlay.classList.add('active');
        },
        close(modalId) {
            const overlay = document.getElementById(modalId);
            if (overlay) overlay.classList.remove('active');
        }
    },

    debounce(func, timeout = 300) {
        let timer;
        return (...args) => {
            clearTimeout(timer);
            timer = setTimeout(() => { func.apply(this, args); }, timeout);
        };
    }
};

const Auth = {
    guard(allowedRoles = []) {
        const token = localStorage.getItem('jwt_token');
        const role = localStorage.getItem('user_role');

        if (!token) {
            window.location.href = '/login';
            return false;
        }

        if (allowedRoles.length > 0 && !allowedRoles.includes(role)) {
            window.location.href = `/${role}/dashboard`;
            return false;
        }
        return true;
    },

    logout() {
        localStorage.clear();
        window.location.href = '/login';
    },

    updateAvatarUI(url) {
        const topImg = document.getElementById('topbar-avatar-img');
        const topIcon = document.getElementById('topbar-avatar-icon');
        const modalImg = document.getElementById('modal-avatar-preview');
        const modalIcon = document.getElementById('modal-avatar-icon');

        if (url) {
            localStorage.setItem('profile_pic_url', url);
            if (topImg) { topImg.src = url; topImg.style.display = 'block'; }
            if (topIcon) topIcon.style.display = 'none';
            if (modalImg) { modalImg.src = url; modalImg.style.display = 'block'; }
            if (modalIcon) modalIcon.style.display = 'none';
        } else {
            if (topImg) topImg.style.display = 'none';
            if (topIcon) topIcon.style.display = 'block';
            if (modalImg) modalImg.style.display = 'none';
            if (modalIcon) modalIcon.style.display = 'block';
        }
    },

    initSidebar() {
        const role = localStorage.getItem('user_role');
        const sidebarNav = document.getElementById('sidebar-nav');
        if (!sidebarNav) return;

        const path = window.location.pathname;
        let links = '';

        if (role === 'admin') {
            links = `
                <a href="/admin/dashboard" class="nav-item ${path.includes('dashboard') ? 'active' : ''}"><i class="fas fa-home"></i> Home</a>
                <a href="/admin/students" class="nav-item ${path.includes('students') ? 'active' : ''}"><i class="fas fa-user-graduate"></i> Students</a>
                <a href="/admin/instructors" class="nav-item ${path.includes('instructors') ? 'active' : ''}"><i class="fas fa-chalkboard-teacher"></i> Instructors</a>
                <a href="/admin/courses" class="nav-item ${path.includes('courses') ? 'active' : ''}"><i class="fas fa-book"></i> Courses</a>
            `;
        } else if (role === 'instructor') {
            links = `
                <a href="/instructor/dashboard" class="nav-item ${path.includes('dashboard') ? 'active' : ''}"><i class="fas fa-home"></i> Home</a>
                <a href="/instructor/courses" class="nav-item ${path.includes('courses') ? 'active' : ''}"><i class="fas fa-book"></i> My Courses</a>
            `;
        } else if (role === 'student') {
            links = `
                <a href="/student/dashboard" class="nav-item ${path.includes('dashboard') ? 'active' : ''}"><i class="fas fa-home"></i> Home</a>
                <a href="/student/my-courses" class="nav-item ${path.includes('my-courses') ? 'active' : ''}"><i class="fas fa-book-open"></i> My Courses</a>
                <a href="/student/catalog" class="nav-item ${path.includes('catalog') ? 'active' : ''}"><i class="fas fa-search"></i> Course Catalog</a>
            `;
        }

        sidebarNav.innerHTML = links;

        // Populate topbar username
        const topUser = document.getElementById('topbar-user-name');
        if (topUser) topUser.innerText = localStorage.getItem('username') || role.toUpperCase();

        // Initial avatar load
        this.updateAvatarUI(localStorage.getItem('profile_pic_url'));
    }
};

// Profile Picture Handlers
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;

    document.getElementById('selected-file-name').innerText = file.name;
    document.getElementById('upload-pic-btn').disabled = false;

    // Preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const modalImg = document.getElementById('modal-avatar-preview');
        const modalIcon = document.getElementById('modal-avatar-icon');
        modalImg.src = e.target.result;
        modalImg.style.display = 'block';
        modalIcon.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

async function uploadProfilePic() {
    const input = document.getElementById('profile-pic-input');
    const file = input.files[0];
    if (!file) return;

    const btn = document.getElementById('upload-pic-btn');
    btn.disabled = true;
    btn.innerText = 'Uploading...';

    const formData = new FormData();
    formData.append('file', file);

    const token = localStorage.getItem('jwt_token');

    try {
        const response = await fetch('/api/users/profile_pic', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` },
            body: formData
        });

        const data = await response.json();
        if (!response.ok) throw new Error(data.description || 'Upload failed');

        Auth.updateAvatarUI(data.profile_pic_url);
        UI.toast('Profile picture updated!');
        UI.modal.close('profilePicModal');
    } catch (e) {
        UI.toast(e.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerText = 'Upload New Picture';
    }
}

// Page Initializers
document.addEventListener('DOMContentLoaded', () => {
    // Topbar logout bindings
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) logoutBtn.addEventListener('click', Auth.logout);

    // If we're on a public page, don't execute app logic
    if (window.location.pathname === '/login' || window.location.pathname === '/register' || window.location.pathname === '/') {
        return;
    }

    // Build sidebar
    Auth.initSidebar();
});
