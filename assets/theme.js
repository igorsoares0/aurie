/**
 * Motion helpers. Animations are off when the Animations speed setting is None
 * or the visitor asks their device for reduced motion.
 */
window.Theme.prefersMotion = () =>
  window.Theme.animations !== false && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/** The `behavior` for scrollTo, scrollBy and scrollIntoView calls made from scripts. */
window.Theme.scrollBehavior = () => (window.Theme.prefersMotion() ? 'smooth' : 'auto');

/**
 * Opens a <dialog> when an element with [data-dialog-open="dialog-id"] is clicked,
 * closing any dialog the opener sits in first. Links keep their href as a
 * no-JavaScript fallback. Closes from [data-dialog-close] or a backdrop click.
 */
document.addEventListener('click', (event) => {
  const opener = event.target.closest('[data-dialog-open]');
  if (opener) {
    const dialog = document.getElementById(opener.dataset.dialogOpen);
    if (!dialog) return;
    event.preventDefault();
    opener.closest('dialog[open]')?.close();
    dialog.showModal();
    return;
  }

  const closer = event.target.closest('[data-dialog-close]');
  if (closer) {
    closer.closest('dialog')?.close();
    return;
  }

  if (event.target.matches('dialog.drawer, dialog.search-modal')) event.target.close();
});

/**
 * Adds items to the cart through the Cart API. With the drawer cart, it
 * re-renders the cart drawer, updates every [data-cart-count] and opens the
 * drawer; with the page cart, it goes to the cart page.
 * `body` is FormData from a product form, or `{ items: [{ id, quantity }] }`.
 * Resolves to an error message, or null on success.
 */
window.Theme.addToCart = async (body) => {
  const useDrawer = window.Theme.cartType === 'drawer' && document.getElementById('CartDrawer');
  const isFormData = body instanceof FormData;

  if (useDrawer) {
    if (isFormData) {
      body.append('sections', 'cart-drawer');
      body.append('sections_url', window.location.pathname);
    } else {
      body = { ...body, sections: 'cart-drawer', sections_url: window.location.pathname };
    }
  }

  const response = await fetch(`${window.Shopify.routes.root}cart/add.js`, {
    method: 'POST',
    headers: isFormData
      ? { Accept: 'application/json' }
      : { Accept: 'application/json', 'Content-Type': 'application/json' },
    body: isFormData ? body : JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) return data.description || data.message;

  if (!useDrawer) {
    window.location.href = window.Theme.cartUrl;
    return null;
  }

  const drawer = document.getElementById('CartDrawer');
  const CartItems = customElements.get('cart-items');
  CartItems?.renderSections(data.sections);
  const count = drawer.querySelector('[data-cart-count-value]')?.dataset.cartCountValue;
  if (count) CartItems?.updateCount(count);
  drawer.showModal();
  document.dispatchEvent(new CustomEvent('cart:updated'));
  return null;
};

/** Product forms marked with [data-ajax-add] add to the cart without leaving the page. */
document.addEventListener('submit', async (event) => {
  const form = event.target;
  if (!form.matches?.('form[data-ajax-add]')) return;
  if (window.Theme.cartType !== 'drawer') return;

  event.preventDefault();
  const button = form.querySelector('[type="submit"][name="add"]');
  const error = form.querySelector('[data-add-error]');
  button?.setAttribute('aria-busy', 'true');
  if (button) button.disabled = true;

  try {
    const message = await window.Theme.addToCart(new FormData(form));
    if (error) {
      error.textContent = message || '';
      error.hidden = !message;
    }
  } catch (exception) {
    console.error(exception);
  } finally {
    button?.removeAttribute('aria-busy');
    if (button) button.disabled = false;
  }
});

/** Formats an amount in cents with the shopper's currency. */
window.Theme.formatMoney = (cents) =>
  new Intl.NumberFormat(window.Theme.moneyLocale, {
    style: 'currency',
    currency: window.Shopify?.currency?.active || 'USD',
  }).format(cents / 100);

/**
 * Tabs: a [role="tablist"] of [role="tab"] buttons, each with aria-controls
 * pointing to a [role="tabpanel"]. Arrow keys, Home and End move between tabs.
 */
if (!customElements.get('tab-panels')) {
  customElements.define(
    'tab-panels',
    class TabPanels extends HTMLElement {
      connectedCallback() {
        this.tabs = [...this.querySelectorAll('[role="tab"]')];
        this.tabs.forEach((tab, index) => {
          tab.addEventListener('click', () => this.select(index));
          tab.addEventListener('keydown', (event) => this.onKeydown(event, index));
        });
        this.addEventListener('shopify:block:select', (event) => {
          const index = this.tabs.findIndex((tab) => tab.dataset.blockId === event.detail?.blockId);
          if (index >= 0) this.select(index);
        });
      }

      select(index, focus = false) {
        this.tabs.forEach((tab, i) => {
          const selected = i === index;
          tab.setAttribute('aria-selected', String(selected));
          tab.tabIndex = selected ? 0 : -1;
          const panel = document.getElementById(tab.getAttribute('aria-controls'));
          if (panel) panel.hidden = !selected;
        });
        if (focus) this.tabs[index].focus();
      }

      onKeydown(event, index) {
        const last = this.tabs.length - 1;
        const keys = { ArrowRight: index + 1, ArrowLeft: index - 1, Home: 0, End: last };
        if (!(event.key in keys)) return;
        event.preventDefault();
        let next = keys[event.key];
        if (next > last) next = 0;
        if (next < 0) next = last;
        this.select(next, true);
      }
    }
  );
}

/**
 * Lets a mouse drag horizontal scrollers sideways. Touch and trackpads scroll
 * them natively, so only mouse pointers are handled. A drag of more than a few
 * pixels doesn't count as a click, and rows with scroll snap settle on the
 * nearest item when released.
 */
{
  const DRAG_SCROLLERS = [
    '.scroll-row',
    '.lookbook__list',
    '.product-recommendations__list',
    '.product-media__thumbs',
    '.product-media__list',
    '.slideshow__track',
    '.chip-tabs',
    '.main-blog__tag-list',
  ].join(',');
  const THRESHOLD = 6;

  const scrollerFrom = (target) => {
    const scroller = target instanceof Element ? target.closest(DRAG_SCROLLERS) : null;
    return scroller && scroller.scrollWidth > scroller.clientWidth + 1 ? scroller : null;
  };

  const settle = (scroller) => {
    const done = () => scroller.classList.remove('is-dragging');
    const start = scroller.getBoundingClientRect().left + (parseFloat(getComputedStyle(scroller).scrollPaddingLeft) || 0);
    let offset = 0;
    let best = Infinity;
    for (const item of scroller.children) {
      const distance = item.getBoundingClientRect().left - start;
      if (Math.abs(distance) < best) {
        best = Math.abs(distance);
        offset = distance;
      }
    }
    scroller.scrollBy({ left: offset, behavior: window.Theme.scrollBehavior() });
    const timer = setTimeout(done, 500);
    scroller.addEventListener('scrollend', () => {
      clearTimeout(timer);
      done();
    }, { once: true });
  };

  document.addEventListener('pointerover', (event) => {
    if (event.pointerType !== 'mouse') return;
    const scroller = event.target instanceof Element ? event.target.closest(DRAG_SCROLLERS) : null;
    if (scroller) scroller.classList.toggle('is-draggable', scroller.scrollWidth > scroller.clientWidth + 1);
  });

  document.addEventListener('pointerdown', (event) => {
    if (event.pointerType !== 'mouse' || event.button !== 0) return;
    const scroller = scrollerFrom(event.target);
    if (!scroller) return;
    // Snap is computed before dragging turns it off.
    const snapType = getComputedStyle(scroller).scrollSnapType;
    const startX = event.clientX;
    const startScroll = scroller.scrollLeft;
    let dragging = false;

    const onMove = (move) => {
      const distance = move.clientX - startX;
      if (!dragging) {
        if (Math.abs(distance) < THRESHOLD) return;
        dragging = true;
        scroller.classList.add('is-dragging');
      }
      move.preventDefault();
      scroller.scrollLeft = startScroll - distance;
    };

    const onUp = () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointercancel', onUp);
      if (!dragging) return;
      if (snapType.startsWith('none')) {
        // The class stays on until the click that follows pointerup has passed.
        setTimeout(() => scroller.classList.remove('is-dragging'), 0);
      } else {
        settle(scroller);
      }
    };

    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
    window.addEventListener('pointercancel', onUp);
  });

  // Links and images would otherwise start a native drag-and-drop.
  document.addEventListener('dragstart', (event) => {
    if (scrollerFrom(event.target)) event.preventDefault();
  });
}

/**
 * Cart lines on the cart page and in the cart drawer: quantity changes,
 * removals, the cart note and cart attributes. Defined here rather than in
 * the cart-items snippet because Shopify only loads a snippet's JavaScript on
 * pages that render it, and the drawer starts without lines when the cart is
 * empty.
 */
if (!customElements.get('cart-items')) {
  customElements.define(
    'cart-items',
    class CartItems extends HTMLElement {
      connectedCallback() {
        this.addEventListener('change', (event) => {
          const input = event.target;
          if (input.matches('input[data-line]')) {
            clearTimeout(this.quantityTimer);
            this.quantityTimer = setTimeout(() => this.updateLine(input.dataset.line, input.value, input.id), 300);
          } else if (input.matches('[data-cart-note]')) {
            this.updateCart({ note: input.value });
          } else if (input.matches('[data-cart-attribute]')) {
            const value = input.type === 'checkbox' ? (input.checked ? input.value : '') : input.value;
            this.updateCart({ attributes: { [input.dataset.cartAttribute]: value } });
          }
        });

        this.addEventListener('click', (event) => {
          const remove = event.target.closest('[data-cart-remove]');
          if (!remove) return;
          event.preventDefault();
          this.updateLine(remove.dataset.cartRemove, 0);
        });
      }

      get sectionIds() {
        return (this.dataset.sections || '').split(',').filter(Boolean);
      }

      async updateLine(line, quantity, focusId) {
        this.setAttribute('aria-busy', 'true');
        try {
          const response = await fetch(`${window.Shopify.routes.root}cart/change.js`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({
              line: Number(line),
              quantity: Number(quantity),
              sections: this.sectionIds,
              sections_url: window.location.pathname,
            }),
          });
          const cart = await response.json();

          if (!response.ok) {
            const error = this.querySelector(`[id$="-${line}"].cart-item__error`);
            if (error) {
              error.textContent = cart.description || cart.message;
              error.hidden = false;
            }
            return;
          }

          CartItems.renderSections(cart.sections);
          CartItems.updateCount(cart.item_count);
          if (focusId) document.getElementById(focusId)?.focus();
          document.dispatchEvent(new CustomEvent('cart:updated', { detail: { cart } }));
        } catch (error) {
          console.error(error);
        } finally {
          this.removeAttribute('aria-busy');
        }
      }

      async updateCart(body) {
        try {
          await fetch(`${window.Shopify.routes.root}cart/update.js`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify(body),
          });
        } catch (error) {
          console.error(error);
        }
      }

      static renderSections(sections = {}) {
        Object.entries(sections).forEach(([id, html]) => {
          if (!html) return;
          const next = new DOMParser().parseFromString(html, 'text/html');
          document.querySelectorAll(`#shopify-section-${id} [data-cart-content]`).forEach((current) => {
            const replacement = next.querySelector('[data-cart-content]');
            if (replacement) current.replaceWith(replacement.cloneNode(true));
          });
        });
      }

      static updateCount(count) {
        document.querySelectorAll('[data-cart-count]').forEach((element) => {
          element.textContent = count;
        });
      }
    }
  );
}

/** Plus and minus buttons around a quantity field; loaded globally for the same reason as cart-items. */
if (!customElements.get('quantity-input')) {
  customElements.define(
    'quantity-input',
    class QuantityInput extends HTMLElement {
      connectedCallback() {
        this.input = this.querySelector('input');
        this.querySelectorAll('button').forEach((button) => {
          button.addEventListener('click', () => {
            const previous = this.input.value;
            if (button.name === 'plus') {
              this.input.stepUp();
            } else if (Number(this.input.value) > Number(this.input.min || 0)) {
              this.input.stepDown();
            }
            if (this.input.value !== previous) this.input.dispatchEvent(new Event('change', { bubbles: true }));
          });
        });
      }
    }
  );
}

/**
 * Card swatches swap the card image and link to the chosen variant. Global
 * because cards also arrive after load (product recommendations), on pages
 * where the product-card snippet, and so its JavaScript, was never rendered.
 */
document.addEventListener('click', (event) => {
  const swatch = event.target.closest('[data-card-swatch]');
  if (!swatch) return;

  const card = swatch.closest('.product-card');
  const image = card.querySelector('.product-card__image:not(.product-card__image--secondary):not(svg)');
  if (image && swatch.dataset.src) {
    image.srcset = swatch.dataset.srcset;
    image.src = swatch.dataset.src;
    // Keep the merchant's crop: image_tag set the first image's focal point inline.
    image.style.objectPosition = swatch.dataset.focalPoint || '';
  }

  card.querySelectorAll('[data-card-swatch]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button === swatch));
  });
  card.querySelectorAll('.product-card__link').forEach((link) => {
    link.href = swatch.dataset.variantUrl;
  });

  const label = card.querySelector('.product-card__swatch-label');
  if (label && swatch.dataset.label) label.textContent = swatch.dataset.label;
});

/**
 * Reveals sections as they scroll into view (Animations > Reveal sections on
 * scroll). Only sections that start below the screen are hidden, so the first
 * screen, and with it the largest contentful paint, is never delayed. Skipped
 * in the theme editor, where sections are added and moved all the time.
 */
if (
  window.Theme.revealSections &&
  window.Theme.prefersMotion() &&
  !window.Shopify?.designMode &&
  'IntersectionObserver' in window
) {
  const reveal = (section) => {
    section.classList.add('is-revealed');
    const done = () => section.classList.remove('reveal', 'is-revealed');
    section.addEventListener('transitionend', (event) => event.target === section && done());
    // In case the transition never runs (a tab in the background, for example).
    setTimeout(done, 2000);
  };
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        observer.unobserve(entry.target);
        reveal(entry.target);
      });
    },
    { rootMargin: '0px 0px -8% 0px' }
  );
  document.querySelectorAll('#MainContent > .shopify-section:not(:first-child)').forEach((section) => {
    if (section.getBoundingClientRect().top <= window.innerHeight) return;
    section.classList.add('reveal');
    observer.observe(section);
  });
}
