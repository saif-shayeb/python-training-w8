// Global Flash Message System
window.showFlash = function(message, type = 'success') {
    const container = document.getElementById('flash-container');
    if (!container) return;
    
    const flash = document.createElement('div');
    flash.className = `flash-msg flash-${type}`;
    flash.innerHTML = `<span>${message}</span> <button style="background:none;border:none;color:inherit;font-weight:bold;cursor:pointer;margin-left:15px;font-size:1.2rem;" onclick="this.parentElement.classList.add('fade-out'); setTimeout(() => this.parentElement.remove(), 300)">×</button>`;
    
    container.appendChild(flash);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if(flash.parentElement) {
            flash.classList.add('fade-out');
            setTimeout(() => flash.remove(), 300);
        }
    }, 5000);
}

// API Utility Wrapper
async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('jwt_token');
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;
    
    const response = await fetch('/api' + endpoint, {
        ...options,
        headers
    });
    
    if (!response.ok) {
        let msg = "API Error";
        try { const data = await response.json(); msg = data.description || data.error || msg; } catch(e){}
        throw new Error(msg);
    }
    return await response.json();
}

// Global UI state
function updateNavigation() {
    const token = localStorage.getItem('jwt_token');
    const role = localStorage.getItem('user_role');
    const nav = document.getElementById('nav-menu');
    if (!nav) return;

    if (!token) {
        nav.innerHTML = `<li><a href="/login">Login</a></li><li><a href="/register">Register</a></li>`;
        return;
    }

    let links = '';
    if (role === 'admin') {
        links += `<li><a href="/admin">Admin Panel</a></li>`;
    } else if (role === 'student') {
        links += `<li><a href="/student">My Dashboard</a></li>`;
    }
    links += `<li><a href="#" onclick="logout()">Logout</a></li>`;
    nav.innerHTML = links;
}

function logout() {
    localStorage.clear();
    window.location.href = '/';
}

// Auth Handlers
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const data = await apiFetch('/auth/login', {
                method: 'POST',
                body: JSON.stringify({
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                })
            });
            localStorage.setItem('jwt_token', data.access_token);
            localStorage.setItem('user_role', data.user.role);
            if (data.student) localStorage.setItem('student_id', data.student.id);
            
            showFlash("Login successful!");
            window.location.href = data.user.role === 'admin' ? '/admin' : '/student';
        } catch (err) {
            showFlash(err.message, 'error');
        }
    });
}

const regForm = document.getElementById('registerForm');
if (regForm) {
    regForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            username: document.getElementById('reg-username').value,
            password: document.getElementById('reg-password').value,
            email: document.getElementById('reg-email').value,
            role: document.getElementById('reg-role').value
        };
        if (payload.role === 'student') {
            payload.name = document.getElementById('reg-name').value;
            payload.gpa = parseFloat(document.getElementById('reg-gpa').value);
        }
        
        try {
            await apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(payload) });
            showFlash("Registration successful! Please login.");
            window.location.href = '/login';
        } catch (err) {
            showFlash(err.message, 'error');
        }
    });
}

// Admin Dashboard Logic
if (window.location.pathname === '/admin') {
    async function loadAdminData() {
        try {
            // Load Courses
            const courses = await apiFetch('/courses');
            document.getElementById('admin-courses-list').innerHTML = courses.map(c => `
                <li class="data-item">
                    <span><a href="/course/${c.id}" style="color:var(--accent)"><strong>${c.name}</strong></a> (${c.credits}cr)</span>
                    <button onclick="deleteCourse(${c.id})" class="btn danger sm">Delete</button>
                </li>
            `).join('');

            const cSelect = document.getElementById('enroll-course-id');
            if (cSelect) {
                cSelect.innerHTML = '<option value="">-- Select Course --</option>' + courses.map(c => `<option value="${c.id}">${c.name}</option>`).join('');
            }

            // Load Students
            const students = await apiFetch('/students');
            document.getElementById('admin-students-list').innerHTML = students.map(s => `
                <li class="data-item">
                    <div>
                        <strong>${s.name}</strong> (GPA: ${s.gpa}) <br>
                        <small class="text-muted">Enrolled in: ${s.courses.map(cs => cs.name).join(', ') || 'None'}</small>
                    </div>
                    <div style="flex-direction:row; display:flex; gap:10px;">
                        <button onclick="openUpdateStudent(${s.id}, '${s.name}', ${s.gpa})" class="btn warning sm">Edit</button>
                        <button onclick="deleteStudent(${s.id})" class="btn danger sm">Delete</button>
                    </div>
                </li>
            `).join('');
            
            const sSelect = document.getElementById('enroll-student-id');
            if (sSelect) {
                sSelect.innerHTML = '<option value="">-- Select Student --</option>' + students.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
            }
        } catch (err) {
            showFlash(err.message, 'error');
        }
    }
    
    document.getElementById('enrollmentForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiFetch('/enrollments', {
                method: 'POST',
                body: JSON.stringify({
                    student_id: parseInt(document.getElementById('enroll-student-id').value),
                    course_id: parseInt(document.getElementById('enroll-course-id').value)
                })
            });
            showFlash('Student successfully enrolled!', 'success');
            loadAdminData();
        } catch (err) { showFlash(err.message, 'error'); }
    });

    document.getElementById('createCourseForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            await apiFetch('/courses', {
                method: 'POST',
                body: JSON.stringify({
                    name: document.getElementById('new-c-name').value,
                    credits: parseInt(document.getElementById('new-c-credits').value)
                })
            });
            e.target.reset(); // Empties the input fields automatically
            showFlash('Course successfully created!', 'success');
            loadAdminData();
        } catch (err) { showFlash(err.message, 'error'); }
    });

    window.deleteCourse = async (id) => {
        if(confirm('Delete course?')) {
            try {
                await apiFetch(`/courses/${id}`, { method: 'DELETE' });
                showFlash('Course deleted!', 'success');
                loadAdminData();
            } catch(e) { showFlash(e.message, 'error'); }
        }
    };
    window.deleteStudent = async (id) => {
        if(confirm('Delete student?')) {
            try {
                await apiFetch(`/students/${id}`, { method: 'DELETE' });
                showFlash('Student deleted!', 'success');
                loadAdminData();
            } catch(e) { showFlash(e.message, 'error'); }
        }
    };
    
    // Update Modal Flow
    window.openUpdateStudent = (id, _name, _gpa) => {
        document.getElementById('u-student-id').innerText = id;
        document.getElementById('u-student-name').value = _name;
        document.getElementById('u-student-gpa').value = _gpa;
        document.getElementById('updateStudentModal').style.display = 'flex';
    };
    
    window.submitStudentUpdate = async () => {
        const id = document.getElementById('u-student-id').innerText;
        try {
            await apiFetch(`/students/${id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    name: document.getElementById('u-student-name').value,
                    gpa: parseFloat(document.getElementById('u-student-gpa').value)
                })
            });
            document.getElementById('updateStudentModal').style.display = 'none';
            showFlash('Student updated!', 'success');
            loadAdminData();
        } catch(err) { showFlash(err.message, 'error'); }
    };

    document.addEventListener('DOMContentLoaded', loadAdminData);
}

// Student Dashboard Logic
if (window.location.pathname === '/student') {
    async function loadStudentData() {
        try {
            // Load their specific profile
            const me = await apiFetch('/students/me');
            document.getElementById('student-name-display').innerText = me.name;
            document.getElementById('my-gpa').innerText = me.gpa;
            document.getElementById('my-courses-count').innerText = me.courses.length;
            
            document.getElementById('my-schedule-list').innerHTML = me.courses.map(c => `
                <li class="data-item"><a href="/course/${c.id}" style="color:var(--accent)"><strong>${c.name}</strong></a></li>
            `).join('');
            
            // Load globally available courses to simulate enrollment capability
            const allCourses = await apiFetch('/courses');
            document.getElementById('available-courses-list').innerHTML = allCourses.map(c => {
                const enrolled = me.courses.some(mc => mc.id === c.id);
                return `
                <li class="data-item ${enrolled ? 'enrolled' : ''}">
                    <a href="/course/${c.id}" style="color:white; text-decoration:none;"><strong>${c.name}</strong> (${c.credits}cr)</a>
                    ${enrolled ? '<span class="badge success">Enrolled</span>' : '<span class="badge">Available</span>'}
                </li>
            `}).join('');
        } catch (err) {
            showFlash(err.message, 'error');
        }
    }
    document.addEventListener('DOMContentLoaded', loadStudentData);
}

// Specific Course Details Logic
if (window.location.pathname.startsWith('/course/')) {
    async function loadCourseDetails() {
        try {
            const parts = window.location.pathname.split('/');
            const courseId = parts[parts.length - 1];
            
            const course = await apiFetch(`/courses/${courseId}`);
            document.getElementById('c-name').innerText = course.name;
            document.getElementById('c-credits').innerText = course.credits + " Credits";
            
            const list = document.getElementById('c-students-list');
            document.getElementById('c-student-count').innerText = course.students.length;
            
            list.innerHTML = course.students.map(s => `
                <li class="data-item">
                    <span class="icon">👤</span> <strong>${s.name}</strong>
                </li>
            `).join('') || '<li class="empty-state">No students are enrolled in this course yet.</li>';
            
        } catch (err) { showFlash(err.message, 'error'); }
    }
    document.addEventListener('DOMContentLoaded', loadCourseDetails);
}
