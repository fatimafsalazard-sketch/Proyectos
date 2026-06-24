/* =====================================================
   TECHSTORE — JavaScript compartido
   Usado por index.html y producto.html
   Cada bloque verifica que sus elementos existan,
   así el mismo archivo sirve para ambas páginas.
   ===================================================== */

document.addEventListener('DOMContentLoaded', () => {

  /* ===== Año en footer ===== */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ===== Navbar al hacer scroll ===== */
  const navbar = document.getElementById('navbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 30);
    });
  }

  /* ===== Menú móvil ===== */
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navToggle.classList.toggle('open');
      navLinks.classList.toggle('open');
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navToggle.classList.remove('open');
        navLinks.classList.remove('open');
      });
    });
  }

  /* ===== Revelado al hacer scroll ===== */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(el => revealObserver.observe(el));
  }

  /* ===== Contadores animados (stats del home) ===== */
  const statNums = document.querySelectorAll('.stat-num');
  if (statNums.length) {
    const statObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateCount(entry.target);
          statObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.4 });
    statNums.forEach(el => statObserver.observe(el));
  }

  function animateCount(el) {
    const target = parseFloat(el.dataset.target);
    const divide = parseFloat(el.dataset.divide || 1);
    const decimals = parseInt(el.dataset.decimals || 0);
    const suffix = el.dataset.suffix || '';
    const finalValue = target / divide;
    const duration = 1400;
    const start = performance.now();

    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = finalValue * eased;
      el.textContent = current.toLocaleString('es-MX', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
      }) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ===== Tilt 3D del iPhone con el mouse (solo home) ===== */
  const phoneStage = document.querySelector('.phone-stage');
  const phoneTilt = document.getElementById('phoneTilt');
  const finePointer = window.matchMedia('(pointer: fine)').matches;

  if (finePointer && phoneStage && phoneTilt) {
    phoneStage.addEventListener('mousemove', (e) => {
      const rect = phoneStage.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      phoneTilt.style.animation = 'none';
      phoneTilt.style.transform = `rotateY(${x * 22 - 8}deg) rotateX(${-y * 18 + 4}deg)`;
    });
    phoneStage.addEventListener('mouseleave', () => {
      phoneTilt.style.transform = '';
      phoneTilt.style.animation = '';
    });
  }

  /* ===== Carrito compartido (localStorage entre páginas) ===== */
  const cartBadge = document.getElementById('cartBadge');

  function getCart() {
    return parseInt(localStorage.getItem('techstore_cart') || '0', 10);
  }
  function setCart(n) {
    localStorage.setItem('techstore_cart', String(n));
    updateCartBadge();
  }
  function updateCartBadge() {
    if (!cartBadge) return;
    cartBadge.textContent = getCart();
  }
  function bumpBadge() {
    if (!cartBadge) return;
    cartBadge.classList.add('bump');
    setTimeout(() => cartBadge.classList.remove('bump'), 350);
  }
  updateCartBadge();

  /* Botones "Añadir" de tarjetas de accesorios (en ambas páginas) */
  document.querySelectorAll('.add-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      setCart(getCart() + 1);
      bumpBadge();
      const original = btn.textContent;
      btn.textContent = 'Añadido ✓';
      setTimeout(() => { btn.textContent = original; }, 1200);
    });
  });

  /* ===== Newsletter (demo, sin backend) ===== */
  const newsletterForm = document.getElementById('newsletterForm');
  const formMsg = document.getElementById('formMsg');
  if (newsletterForm && formMsg) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = newsletterForm.querySelector('input').value;
      formMsg.textContent = `Listo, avisaremos a ${email} de nuevas llegadas.`;
      newsletterForm.reset();
    });
  }

  /* =====================================================
     PÁGINA DE DETALLE DE PRODUCTO
     ===================================================== */

  const galleryInner = document.getElementById('galleryInner');
  if (galleryInner) {

    /* --- Voltear entre frente / atrás --- */
    const viewBtns = document.querySelectorAll('.gallery-controls button');
    viewBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        viewBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        galleryInner.classList.toggle('flipped', btn.dataset.view === 'back');
      });
    });

    /* --- Selección de color --- */
    const colorDots = document.querySelectorAll('.color-dot');
    const colorLabel = document.getElementById('colorLabel');
    const galleryFlip = document.querySelector('.gallery-flip');

    colorDots.forEach(dot => {
      dot.addEventListener('click', () => {
        colorDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        if (colorLabel) colorLabel.textContent = dot.dataset.name;
        if (galleryFlip) galleryFlip.style.setProperty('--device-color', dot.dataset.color);
      });
    });

    /* --- Selección de almacenamiento (actualiza precio) --- */
    const storagePills = document.querySelectorAll('.storage-pill');
    const priceNow = document.getElementById('priceNow');
    const priceNote = document.getElementById('priceNote');

    function formatMXN(value) {
      return value.toLocaleString('es-MX', { style: 'currency', currency: 'MXN', maximumFractionDigits: 0 });
    }

    storagePills.forEach(pill => {
      pill.addEventListener('click', () => {
        storagePills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const price = parseInt(pill.dataset.price, 10);
        if (priceNow) priceNow.textContent = formatMXN(price);
        if (priceNote) priceNote.textContent = `o desde ${formatMXN(Math.round(price / 18))}/mes a 18 meses sin intereses`;
      });
    });

    /* --- Contador de cantidad --- */
    const qtyVal = document.getElementById('qtyVal');
    const qtyDec = document.getElementById('qtyDec');
    const qtyInc = document.getElementById('qtyInc');
    let qty = 1;

    if (qtyDec && qtyInc && qtyVal) {
      qtyDec.addEventListener('click', () => {
        qty = Math.max(1, qty - 1);
        qtyVal.textContent = qty;
      });
      qtyInc.addEventListener('click', () => {
        qty = Math.min(5, qty + 1);
        qtyVal.textContent = qty;
      });
    }

    /* --- Agregar al carrito / Comprar ahora --- */
    const addToCartBtn = document.getElementById('addToCartBtn');
    const buyNowBtn = document.getElementById('buyNowBtn');
    const productMsg = document.getElementById('productMsg');

    if (addToCartBtn) {
      addToCartBtn.addEventListener('click', () => {
        setCart(getCart() + qty);
        bumpBadge();
        if (productMsg) productMsg.textContent = `Se ${qty > 1 ? 'agregaron' : 'agregó'} ${qty} ${qty > 1 ? 'unidades' : 'unidad'} al carrito.`;
      });
    }
    if (buyNowBtn) {
      buyNowBtn.addEventListener('click', () => {
        setCart(getCart() + qty);
        bumpBadge();
        if (productMsg) productMsg.textContent = 'Redirigiendo al pago seguro... (demo, sin backend conectado)';
      });
    }
  }

});
