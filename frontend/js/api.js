/* ============================================
   SkinSense AI — API Bağlantı Servisi
   ============================================ */
const API_BASE = 'http://localhost:5000/api';
// Token yönetimi
const Auth = {
  getToken: () => localStorage.getItem('skinsense_token'),
  setToken: (t) => localStorage.setItem('skinsense_token', t),
  clearToken: () => localStorage.removeItem('skinsense_token'),
  getUser: () => JSON.parse(localStorage.getItem('skinsense_user') || 'null'),
  setUser: (u) => localStorage.setItem('skinsense_user', JSON.stringify(u)),
  clearUser: () => localStorage.removeItem('skinsense_user'),
  isLoggedIn: () => !!localStorage.getItem('skinsense_token'),
  
  logout: () => {
    localStorage.removeItem('skinsense_token');
    localStorage.removeItem('skinsense_user');
    localStorage.removeItem('skinsense_analysis');
    window.location.href = 'index.html';
  }
};
// CSRF Token Yönetimi
let globalCsrfToken = '';

async function initCSRF() {
  try {
    const res = await fetch(`${API_BASE}/csrf-token`);
    const data = await res.json();
    globalCsrfToken = data.csrf_token;
    
    // Sayfadaki tüm CSRF gizli inputlarına değeri yaz
    document.querySelectorAll('.csrf-input').forEach(input => {
      input.value = globalCsrfToken;
    });
  } catch(e) {
    console.warn('CSRF Token alinamadi', e);
  }
}

// HTTP isteği yardımcısı
async function apiRequest(endpoint, options = {}) {
  const token = Auth.getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...(globalCsrfToken ? { 'X-CSRFToken': globalCsrfToken } : {}),
    ...options.headers
  };
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });
    const data = await response.json();
    if (!response.ok) {
      throw { status: response.status, message: data.error || data.message || 'Bir hata oluştu.' };
    }
    return data;
  } catch (err) {
    if (err.status === 401) {
      Auth.logout();
    }
    throw err;
  }
}
// ── Auth API ──────────────────────────────────
const AuthAPI = {
  register: (data) => apiRequest('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => apiRequest('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  forgotPassword: (email) => apiRequest('/auth/forgot-password', { method: 'POST', body: JSON.stringify({ email }) }),
  verifyOTP: (email, otp) => apiRequest('/auth/verify-otp', { method: 'POST', body: JSON.stringify({ email, otp }) }),
  me: () => apiRequest('/auth/me'),
  updateProfile: (data) => apiRequest('/auth/update-profile', { method: 'PUT', body: JSON.stringify(data) }),
};
// ── Analysis API ─────────────────────────────
const AnalysisAPI = {
  analyzePhoto: (photoBase64) => apiRequest('/analysis/photo', {
    method: 'POST',
    body: JSON.stringify({ photo_base64: photoBase64 })
  }),
  analyzeQuestionnaire: (answers) => apiRequest('/analysis/questionnaire', {
    method: 'POST',
    body: JSON.stringify({ answers })
  }),
  getHistory: () => apiRequest('/analysis/history'),
  getLatest: () => apiRequest('/analysis/latest'),
  getById: (id) => apiRequest(`/analysis/${id}`),
  getPhoto: (id) => apiRequest(`/analysis/photo/${id}`),
};
// ── Products API ─────────────────────────────
const ProductsAPI = {
  recommend: (skinType, concerns = [], category = '') => {
    const params = new URLSearchParams();
    if (skinType) params.set('skin_type', skinType);
    if (concerns.length) params.set('concerns', concerns.join(','));
    if (category) params.set('category', category);
    return apiRequest(`/products/recommend?${params}`);
  },
  search: (q) => apiRequest(`/products/search?q=${encodeURIComponent(q)}`),
  getCategories: () => apiRequest('/products/categories'),
};
// ── Ingredients API ──────────────────────────
const IngredientsAPI = {
  analyze: (productName, ingredients) => apiRequest('/ingredients/analyze', {
    method: 'POST',
    body: JSON.stringify({ product_name: productName, ingredients })
  }),
  checkIngredient: (ingredient) => apiRequest('/ingredients/check-ingredient', {
    method: 'POST',
    body: JSON.stringify({ ingredient })
  }),
};
// ── Toast Bildirimleri ───────────────────────
function showToast(message, type = 'info', duration = 4000) {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${icons[type]}</span>
    <span class="toast-text">${message}</span>
    <button class="toast-close" onclick="this.parentElement.remove()">✕</button>
  `;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(20px)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
// ── Dil Sistemi ──────────────────────────────
const i18n = {
  current: localStorage.getItem('skinsense_lang') || 'tr',
  
  strings: {
    tr: {
      // Nav
      'nav.home': 'Ana Sayfa',
      'nav.analysis': 'Cilt Analizi',
      'nav.products': 'Ürünler',
      'nav.history': 'Geçmiş',
      'nav.ingredients': 'İçerik Kontrolü',
      'nav.login': 'Giriş Yap',
      'nav.register': 'Kayıt Ol',
      'nav.dashboard': 'Panelim',
      'nav.logout': 'Çıkış Yap',
      // Auth
      'auth.login': 'Giriş Yap',
      'auth.register': 'Kayıt Ol',
      'auth.email': 'Email Adresi',
      'auth.password': 'Şifre',
      'auth.name': 'Adınız',
      'auth.forgot': 'Şifremi Unuttum',
      'auth.otp_sent': 'OTP kodunuz email adresinize gönderildi.',
      'auth.welcome_back': 'Tekrar hoş geldiniz!',
      // Analysis
      'analysis.photo': 'Fotoğraf ile Analiz',
      'analysis.questionnaire': 'Anket ile Analiz',
      'analysis.upload': 'Selfie Yükle',
      'analysis.camera': 'Kamera ile Çek',
      'analysis.analyzing': 'AI cildinizi analiz ediyor...',
      // Results
      'result.skin_type': 'Cilt Tipi',
      'result.moisture': 'Nem Oranı',
      'result.acne': 'Akne Seviyesi',
      'result.sensitivity': 'Hassasiyet',
      // Routine
      'routine.morning': 'Sabah Rutini',
      'routine.evening': 'Akşam Rutini',
      // Common
      'common.loading': 'Yükleniyor...',
      'common.error': 'Bir hata oluştu.',
      'common.save': 'Kaydet',
      'common.cancel': 'İptal',
      'common.back': 'Geri',
      'common.next': 'İleri',
    },
    en: {
      'nav.home': 'Home',
      'nav.analysis': 'Skin Analysis',
      'nav.products': 'Products',
      'nav.history': 'History',
      'nav.ingredients': 'Ingredient Check',
      'nav.login': 'Login',
      'nav.register': 'Sign Up',
      'nav.dashboard': 'Dashboard',
      'nav.logout': 'Log Out',
      'auth.login': 'Login',
      'auth.register': 'Sign Up',
      'auth.email': 'Email Address',
      'auth.password': 'Password',
      'auth.name': 'Your Name',
      'auth.forgot': 'Forgot Password',
      'auth.otp_sent': 'OTP code sent to your email.',
      'auth.welcome_back': 'Welcome back!',
      'analysis.photo': 'Photo Analysis',
      'analysis.questionnaire': 'Quiz Analysis',
      'analysis.upload': 'Upload Selfie',
      'analysis.camera': 'Use Camera',
      'analysis.analyzing': 'AI is analyzing your skin...',
      'result.skin_type': 'Skin Type',
      'result.moisture': 'Moisture Level',
      'result.acne': 'Acne Level',
      'result.sensitivity': 'Sensitivity',
      'routine.morning': 'Morning Routine',
      'routine.evening': 'Evening Routine',
      'common.loading': 'Loading...',
      'common.error': 'An error occurred.',
      'common.save': 'Save',
      'common.cancel': 'Cancel',
      'common.back': 'Back',
      'common.next': 'Next',
    }
  },
  
  t(key) {
    return this.strings[this.current]?.[key] || this.strings['tr'][key] || key;
  },
  
  setLang(lang) {
    this.current = lang;
    localStorage.setItem('skinsense_lang', lang);
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      el.textContent = this.t(key);
      el.textContent = this.t(key);
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      el.placeholder = this.t(key);
    });
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.lang === lang);
    });
  },
  
  init() {
    this.setLang(this.current);
    document.querySelectorAll('.lang-btn').forEach(btn => {
      btn.addEventListener('click', () => this.setLang(btn.dataset.lang));
    });
  }
};
// ── Navbar Yardımcıları ───────────────────────
function initNavbar() {
  // Scroll efekti
  window.addEventListener('scroll', () => {
    document.querySelector('.navbar')?.classList.toggle('scrolled', window.scrollY > 20);
  });
  // Avatar menü
  const avatarBtn = document.querySelector('.avatar-btn');
  const dropdown = document.querySelector('.avatar-dropdown');
  if (avatarBtn && dropdown) {
    avatarBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      dropdown.classList.toggle('open');
    });
    document.addEventListener('click', () => dropdown.classList.remove('open'));
  }
  // Kullanıcı bilgisi
  const user = Auth.getUser();
  if (user) {
    const avatarBtnEl = document.querySelector('.avatar-btn');
    if (avatarBtnEl) {
      avatarBtnEl.textContent = user.name?.charAt(0).toUpperCase() || '?';
    }
    document.querySelectorAll('.user-name').forEach(el => el.textContent = user.name);
  }
  // Auth durumuna göre nav göster/gizle
  const isLoggedIn = Auth.isLoggedIn();
  document.querySelectorAll('.auth-only').forEach(el => {
    el.style.display = isLoggedIn ? '' : 'none';
  });
  document.querySelectorAll('.guest-only').forEach(el => {
    el.style.display = isLoggedIn ? 'none' : '';
  });
}
// ── Genel Yardımcılar ────────────────────────
function formatDate(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });
}
function getLevelBadgeClass(level) {
  const map = {
    'Yok': 'badge-good', 'Düşük': 'badge-good', 'Az': 'badge-good', 'Küçük': 'badge-good',
    'Kuru': 'badge-medium', 'Normal': 'badge-good', 'Eşit': 'badge-good',
    'Hafif': 'badge-medium', 'Orta': 'badge-medium', 'Hafif Yağlı': 'badge-medium',
    'Yüksek': 'badge-concern', 'Yağlı': 'badge-concern', 'Çok': 'badge-concern', 'Büyük': 'badge-concern',
    'Belirgin': 'badge-concern', 'Eşitsiz': 'badge-concern',
  };
  return map[level] || 'badge-pink';
}
// Sayfa yüklenince
document.addEventListener('DOMContentLoaded', () => {
  i18n.init();
  initNavbar();
  initCSRF(); // CSRF tokenini al ve formlara ekle
});
