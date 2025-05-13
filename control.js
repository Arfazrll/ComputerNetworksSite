// Updated control.js to remove binary numbers and related functions

const teamMembers = [
    {
        name: "Arief",
        nim: "1030",
        class: "IT-47-04",
        role: " --- ",
        email: "",
        phone: "",
        location: "Bandung, Indonesia",
        image: '',
        about: "Hii.",
        education: "Telkom University",
        networkRole: "Information Technology",
        socials: {
            instagram: "https://instagram.com/ariefrhk",
            linkedin: "https://linkedin.com/in/ariefrhk",
            github: "https://github.com/ariefrhk",
            twitter: "https://twitter.com/ariefrhk"
        }
    },
    {
        name: "Syahril Arfian Almazril",
        nim: "103032300013",
        class: "IT-47-04",
        role: "Backend & Server Management",
        email: "azril4974@gmail.com",
        phone: "+62-81511463282",
        location: "Bandung, Indonesia",
        image: 'WhatsApp Image 2025-01-23 at 14.26.39_643ee427.jpg',
        about: "Hii.",
        education: "Telkom University",
        networkRole: "Information Technology",
        socials: {
            instagram: "https://www.instagram.com/arfazrl09_/?utm_source=ig_web_button_share_sheet",
            linkedin: "https://www.linkedin.com/in/syahril-arfian-almazril-215a12231",
            github: "https://github.com/Arfazrll",
            twitter: "-"
        }
    },
    {
        name: "Nopal",
        nim: "1030",
        class: "IT-47-04",
        role: " --- ",
        email: "---",
        phone: "---",
        location: "Bandung, Indonesia",
        image: '',
        about: "Hiii",
        education: "Telkom University",
        networkRole: "Information Technology",
        socials: {
            instagram: "https://instagram.com/mnfirdaus",
            linkedin: "https://linkedin.com/in/mnfirdaus",
            github: "https://github.com/mnfirdaus",
            twitter: "https://twitter.com/mnfirdaus"
        }
    }
];

let loadingScreen;
let modal;
let modalBackdrop;
let closeBtn;
let backToTopBtn;
let themeToggle;
let themeLabel;
let toast;
let toastMessage;
let toastCloseBtn;
let conclusionCard;
let conclusionHeader;

document.addEventListener('DOMContentLoaded', () => {
    loadingScreen = document.getElementById('loading-screen');
    modal = document.getElementById('detailModal');
    modalBackdrop = document.querySelector('.modal-backdrop');
    closeBtn = document.querySelector('.close-btn');
    backToTopBtn = document.getElementById('back-to-top');
    themeToggle = document.getElementById('theme-toggle');
    themeLabel = document.querySelector('.theme-label');
    toast = document.getElementById('toast');
    toastMessage = document.getElementById('toast-message');
    toastCloseBtn = document.getElementById('toast-close');
    conclusionCard = document.getElementById('conclusion-card');
    conclusionHeader = document.getElementById('conclusion-header');
    
    setTimeout(() => {
        loadingScreen.style.opacity = '0';
        setTimeout(() => {
            loadingScreen.style.display = 'none';
        }, 500);
    }, 1500);
    
    createParticles();
    createNetworkGrid();
    createTeamCards();
    initEventListeners();
    initCardEffects();
    loadThemePreference();
    initNetworkCanvas();
    
    // Modified: Removed call to initDataStream() function
    // The data stream element is still in the HTML but hidden via CSS
    
    setTimeout(() => {
        showToast('Jika anda telah berhasil sampai kesini bearti server berhasil dijalankan!');
    }, 2000);
});

function createTeamCards() {
    const container = document.querySelector('.cards-container');
    
    teamMembers.forEach((member, index) => {
        const card = document.createElement('div');
        card.className = 'card';
        card.dataset.memberId = index;
        
        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <div class="card-decoration">
                        <div class="decoration-circle"></div>
                        <div class="decoration-line"></div>
                    </div>
                    <div class="profile-image-container">
                        <div class="profile-image">
                            <img src="${member.image}" alt="${member.name}" loading="lazy">
                        </div>
                    </div>
                    <div class="profile-info">
                        <h2 class="member-name">${member.name}</h2>
                        <div class="member-details">
                            <p class="nim">NIM: ${member.nim}</p>
                            <p class="class">Kelas: ${member.class}</p>
                        </div>
                    </div>
                    <button class="detail-btn" aria-label="View details for ${member.name}">
                        <span class="btn-text">Lihat Detail</span>
                        <span class="btn-icon"><i class="fas fa-arrow-right"></i></span>
                    </button>
                </div>
            </div>
            <div class="card-reflection"></div>
        `;
        
        container.appendChild(card);
    });
}

function initEventListeners() {
    document.addEventListener('click', (e) => {
        if (e.target.closest('.detail-btn')) {
            const card = e.target.closest('.card');
            const memberId = card.dataset.memberId;
            openModal(e, memberId);
        }
    });
    
    closeBtn.addEventListener('click', closeModal);
    modalBackdrop.addEventListener('click', closeModal);
    window.addEventListener('scroll', toggleBackToTopButton);
    backToTopBtn.addEventListener('click', scrollToTop);
    themeToggle.addEventListener('click', toggleTheme);
    toastCloseBtn.addEventListener('click', hideToast);
    
    // Conclusion card toggle
    conclusionHeader.addEventListener('click', toggleConclusion);
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

function toggleConclusion() {
    conclusionCard.classList.toggle('expanded');
}

function initCardEffects() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach((card, index) => {
        card.addEventListener('mousemove', (e) => {
            if (window.innerWidth <= 768) return;
            
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`;
            
            // Add glow effect at cursor position
            const glowX = (x / rect.width) * 100;
            const glowY = (y / rect.height) * 100;
            card.style.background = `radial-gradient(circle at ${glowX}% ${glowY}%, rgba(0, 212, 255, 0.1), transparent)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
            card.style.background = '';
        });
        
        card.style.animation = `cardFloat 6s ease-in-out ${index * 0.5}s infinite`;
    });
}

// New network canvas visualization
function initNetworkCanvas() {
    const canvas = document.getElementById('network-canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    const nodes = [];
    const connections = [];
    
    // Create nodes
    for (let i = 0; i < 20; i++) {
        nodes.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 3 + 1,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5
        });
    }
    
    // Create connections
    for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
            if (Math.random() < 0.1) {
                connections.push([i, j]);
            }
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Update nodes
        nodes.forEach(node => {
            node.x += node.vx;
            node.y += node.vy;
            
            if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
        });
        
        // Draw connections
        ctx.strokeStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary');
        ctx.lineWidth = 0.5;
        ctx.globalAlpha = 0.3;
        
        connections.forEach(([i, j]) => {
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
        });
        
        // Draw nodes
        ctx.globalAlpha = 1;
        nodes.forEach(node => {
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--accent-primary');
            ctx.fill();
        });
        
        requestAnimationFrame(animate);
    }
    
    animate();
    
    // Resize canvas on window resize
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
}

// REMOVED: initDataStream function is completely removed to eliminate binary numbers

function openModal(e, memberId) {
    const member = teamMembers[memberId];
    
    document.getElementById('modalImage').src = member.image;
    document.getElementById('modalName').textContent = member.name;
    document.getElementById('modalRole').textContent = member.role;
    document.getElementById('modalNim').textContent = `NIM: ${member.nim}`;
    document.getElementById('modalEmail').textContent = member.email;
    document.getElementById('modalPhone').textContent = member.phone;
    document.getElementById('modalLocation').textContent = member.location;
    document.getElementById('modalAbout').textContent = member.about;
    document.getElementById('modalEducation').textContent = member.education;
    document.getElementById('modalNetworkRole').textContent = member.networkRole;
    
    document.getElementById('socialInstagram').href = member.socials.instagram;
    document.getElementById('socialLinkedin').href = member.socials.linkedin;
    document.getElementById('socialGithub').href = member.socials.github;
    document.getElementById('socialTwitter').href = member.socials.twitter;
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden'; 
    
    setTimeout(() => {
        modal.classList.add('active');
    }, 10);
}

function closeModal() {
    modal.classList.remove('active');
    setTimeout(() => {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }, 300);
}

function toggleBackToTopButton() {
    if (window.pageYOffset > 300) {
        backToTopBtn.classList.add('visible');
    } else {
        backToTopBtn.classList.remove('visible');
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

function toggleTheme() {
    const body = document.body;
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeLabel.textContent = 'Light Mode';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeLabel.textContent = 'Dark Mode';
        localStorage.setItem('theme', 'dark');
    }
    
    const mode = body.classList.contains('dark-theme') ? 'Dark' : 'Light';
    showToast(`${mode} mode aktif!`);
}

function loadThemePreference() {
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        themeLabel.textContent = 'Light Mode';
    } else {
        document.body.classList.add('dark-theme');
        document.body.classList.remove('light-theme');
        themeLabel.textContent = 'Dark Mode';
    }
}

function showToast(message) {
    toastMessage.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        hideToast();
    }, 5000);
}

function hideToast() {
    toast.classList.remove('show');
}

function createParticles() {
    const container = document.getElementById('particles');
    const particlesCount = 50;
    
    for (let i = 0; i < particlesCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        const size = Math.random() * 5 + 1;
        const opacity = Math.random() * 0.5 + 0.1;
        const duration = Math.random() * 20 + 10;
        const delay = Math.random() * 5;

        particle.style.cssText = `
            top: ${posY}%;
            left: ${posX}%;
            width: ${size}px;
            height: ${size}px;
            opacity: ${opacity};
            animation: particleFloat ${duration}s linear ${delay}s infinite;
        `;
        
        container.appendChild(particle);
    }
}

function createNetworkGrid() {
    const container = document.getElementById('network-grid');
    const gridSize = 20;
    const dotCount = 50;
    
    for (let i = 0; i < dotCount; i++) {
        const dot = document.createElement('div');
        dot.className = 'grid-dot';
        
        const posX = Math.random() * 100;
        const posY = Math.random() * 100;
        
        dot.style.left = `${posX}%`;
        dot.style.top = `${posY}%`;
        
        // Add pulsing animation to some dots
        if (Math.random() > 0.7) {
            dot.style.animation = `pulse-dot 3s ease-in-out ${Math.random() * 3}s infinite`;
        }
        
        container.appendChild(dot);
    }
    
    // Create more dynamic network lines
    for (let i = 0; i < gridSize; i++) {
        if (Math.random() > 0.7) {
            const hLine = document.createElement('div');
            hLine.className = 'grid-line';
            
            const posY = (i / gridSize) * 100;
            const width = Math.random() * 20 + 10;
            const posX = Math.random() * (100 - width);
            
            hLine.style.cssText = `
                top: ${posY}%;
                left: ${posX}%;
                width: ${width}%;
                height: 1px;
                animation: line-flow ${Math.random() * 5 + 5}s linear infinite;
            `;
            
            container.appendChild(hLine);
        }
        
        if (Math.random() > 0.7) {
            const vLine = document.createElement('div');
            vLine.className = 'grid-line';
            
            const posX = (i / gridSize) * 100;
            const height = Math.random() * 20 + 10;
            const posY = Math.random() * (100 - height);
            
            vLine.style.cssText = `
                left: ${posX}%;
                top: ${posY}%;
                height: ${height}%;
                width: 1px;
                animation: line-flow-vertical ${Math.random() * 5 + 5}s linear infinite;
            `;
            
            container.appendChild(vLine);
        }
    }
}

function animateOnScroll() {
    const elements = document.querySelectorAll('.card, .section-header, .conclusion-card');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementBottom = element.getBoundingClientRect().bottom;
        const windowHeight = window.innerHeight;
        
        if (elementTop < windowHeight * 0.8 && elementBottom > 0) {
            element.classList.add('animate');
        }
    });
}

document.addEventListener('scroll', animateOnScroll);
window.addEventListener('load', animateOnScroll);

function debounce(func, wait = 20, immediate = true) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

window.addEventListener('scroll', debounce(toggleBackToTopButton));
window.addEventListener('scroll', debounce(animateOnScroll));

document.addEventListener('dragstart', (e) => {
    if (e.target.tagName === 'IMG') {
        e.preventDefault();
    }
});

if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src || img.src;
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });
    
    const imgs = document.querySelectorAll('img');
    imgs.forEach(img => imageObserver.observe(img));
}