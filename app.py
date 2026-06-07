import streamlit as st
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fashion Cosmetics",
    page_icon="💄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #fff5f7; }
    .stApp { background-color: #fff5f7; }
    h1 { color: #c2185b; font-family: 'Georgia', serif; }
    h2, h3 { color: #880e4f; }
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(194,24,91,0.1);
        border: 1px solid #f8bbd0;
    }
    .badge-new {
        background: #e91e63; color: white;
        padding: 2px 8px; border-radius: 20px;
        font-size: 12px; font-weight: bold;
    }
    .badge-discount {
        background: #ff5722; color: white;
        padding: 2px 8px; border-radius: 20px;
        font-size: 12px; font-weight: bold;
    }
    .price-main { color: #c2185b; font-size: 20px; font-weight: bold; }
    .price-old { color: #999; text-decoration: line-through; font-size: 14px; }
    .rating-stars { color: #ffc107; }
    .brand-chip {
        display: inline-block;
        background: #fce4ec;
        color: #880e4f;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin: 2px;
    }
    .hero-banner {
        background: linear-gradient(135deg, #880e4f, #e91e63, #f48fb1);
        color: white;
        padding: 40px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
    }
    .stat-box {
        background: white;
        border: 2px solid #f48fb1;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    div[data-testid="stSidebarContent"] { background-color: #fce4ec; }
</style>
""", unsafe_allow_html=True)

# ─── Product Data ───────────────────────────────────────────────────────────────
products = [
    {"id": "dc-001", "name": "Dermacos Day Cream SPF 30", "brand": "Dermacos", "category": "skincare", "price": 1850, "originalPrice": 2200, "description": "A luxurious day cream with SPF 30 protection that hydrates, brightens, and shields your skin from harmful UV rays.", "rating": 4.7, "reviewCount": 128, "isNew": False, "isFeatured": True, "discount": 16, "weight": "50ml", "inStock": True, "stockCount": 45, "tags": ["spf", "hydrating", "brightening"]},
    {"id": "dc-002", "name": "Dermacos Night Repair Cream", "brand": "Dermacos", "category": "skincare", "price": 1950, "originalPrice": 2400, "description": "An intensive night repair cream that works overnight to restore, rejuvenate, and deeply nourish your skin.", "rating": 4.8, "reviewCount": 95, "isNew": False, "isFeatured": True, "discount": 19, "weight": "50ml", "inStock": True, "stockCount": 32, "tags": ["night cream", "anti-aging"]},
    {"id": "dc-003", "name": "Dermacos Whitening Face Wash", "brand": "Dermacos", "category": "skincare", "price": 750, "originalPrice": 900, "description": "A gentle foaming face wash that effectively cleanses, brightens, and evens out skin tone.", "rating": 4.5, "reviewCount": 210, "isNew": False, "isFeatured": False, "discount": 17, "weight": "100ml", "inStock": True, "stockCount": 60, "tags": ["face wash", "whitening"]},
    {"id": "dc-004", "name": "Dermacos Anti-Acne Serum", "brand": "Dermacos", "category": "skincare", "price": 1650, "originalPrice": 1900, "description": "A powerful anti-acne serum with salicylic acid and tea tree oil that targets breakouts.", "rating": 4.6, "reviewCount": 87, "isNew": True, "isFeatured": False, "discount": 13, "weight": "30ml", "inStock": True, "stockCount": 28, "tags": ["acne", "serum"]},
    {"id": "ds-001", "name": "Dermashine Brightening Serum", "brand": "Dermashine", "category": "skincare", "price": 2200, "originalPrice": 2800, "description": "A premium brightening serum with 15% Vitamin C, niacinamide, and alpha arbutin.", "rating": 4.9, "reviewCount": 156, "isNew": True, "isFeatured": True, "discount": 21, "weight": "30ml", "inStock": True, "stockCount": 35, "tags": ["vitamin c", "brightening", "serum"]},
    {"id": "ds-002", "name": "Dermashine Hydra Boost Moisturizer", "brand": "Dermashine", "category": "skincare", "price": 1550, "originalPrice": 1800, "description": "A lightweight, fast-absorbing moisturizer with triple hyaluronic acid.", "rating": 4.7, "reviewCount": 134, "isNew": False, "isFeatured": True, "discount": 14, "weight": "60ml", "inStock": True, "stockCount": 42, "tags": ["hydration", "moisturizer"]},
    {"id": "ds-003", "name": "Dermashine Under Eye Cream", "brand": "Dermashine", "category": "skincare", "price": 1350, "originalPrice": 1600, "description": "A targeted under eye cream with caffeine and peptides.", "rating": 4.5, "reviewCount": 72, "isNew": False, "isFeatured": False, "discount": 16, "weight": "15ml", "inStock": True, "stockCount": 25, "tags": ["eye cream", "dark circles"]},
    {"id": "ds-004", "name": "Dermashine Sunscreen SPF 50+", "brand": "Dermashine", "category": "skincare", "price": 1200, "originalPrice": 1450, "description": "A broad-spectrum SPF 50+ sunscreen with PA++++ rating.", "rating": 4.8, "reviewCount": 198, "isNew": True, "isFeatured": False, "discount": 17, "weight": "50ml", "inStock": True, "stockCount": 50, "tags": ["sunscreen", "spf 50"]},
    {"id": "mk-001", "name": "Dermacos Matte Foundation", "brand": "Dermacos", "category": "makeup", "price": 1750, "originalPrice": 2000, "description": "A full-coverage matte foundation with 24-hour wear formula.", "rating": 4.6, "reviewCount": 112, "isNew": False, "isFeatured": True, "discount": 13, "weight": "30ml", "inStock": True, "stockCount": 38, "tags": ["foundation", "matte"]},
    {"id": "mk-002", "name": "Dermashine Liquid Lipstick", "brand": "Dermashine", "category": "makeup", "price": 950, "originalPrice": 1200, "description": "A highly pigmented liquid lipstick with a velvet matte finish that lasts up to 16 hours.", "rating": 4.8, "reviewCount": 243, "isNew": True, "isFeatured": True, "discount": 21, "weight": "5ml", "inStock": True, "stockCount": 65, "tags": ["lipstick", "matte"]},
    {"id": "mk-003", "name": "Dermacos HD Loose Powder", "brand": "Dermacos", "category": "makeup", "price": 1100, "originalPrice": 1350, "description": "An ultra-fine HD loose setting powder that sets makeup and controls shine.", "rating": 4.5, "reviewCount": 89, "isNew": False, "isFeatured": False, "discount": 19, "weight": "20g", "inStock": True, "stockCount": 30, "tags": ["setting powder", "HD"]},
    {"id": "mk-004", "name": "Dermashine 18-Color Eyeshadow Palette", "brand": "Dermashine", "category": "makeup", "price": 2500, "originalPrice": 3200, "description": "A stunning 18-shade eyeshadow palette featuring mattes, shimmers, and glitters.", "rating": 4.9, "reviewCount": 167, "isNew": True, "isFeatured": True, "discount": 22, "weight": "18g", "inStock": True, "stockCount": 22, "tags": ["eyeshadow", "palette"]},
    {"id": "mk-005", "name": "Dermacos Waterproof Eyeliner", "brand": "Dermacos", "category": "makeup", "price": 650, "originalPrice": 800, "description": "A precision waterproof eyeliner with a fine tip for intense, jet-black color.", "rating": 4.6, "reviewCount": 198, "isNew": False, "isFeatured": False, "discount": 19, "weight": "1.2g", "inStock": True, "stockCount": 75, "tags": ["eyeliner", "waterproof"]},
    {"id": "jj-001", "name": "Johnson's Baby Shampoo", "brand": "Johnson & Johnson", "category": "haircare", "price": 550, "originalPrice": 650, "description": "Johnson's No More Tears baby shampoo — as gentle to eyes as pure water.", "rating": 4.8, "reviewCount": 312, "isNew": False, "isFeatured": True, "discount": 15, "weight": "200ml", "inStock": True, "stockCount": 80, "tags": ["baby shampoo", "gentle"]},
    {"id": "jj-002", "name": "Johnson's Baby Lotion", "brand": "Johnson & Johnson", "category": "beauty", "price": 480, "originalPrice": 580, "description": "Johnson's Baby Lotion with COTTONTOUCH formula that softens baby's delicate skin.", "rating": 4.9, "reviewCount": 425, "isNew": False, "isFeatured": True, "discount": 17, "weight": "200ml", "inStock": True, "stockCount": 95, "tags": ["baby lotion", "gentle"]},
    {"id": "jj-003", "name": "Johnson's Vita-Rich Body Lotion", "brand": "Johnson & Johnson", "category": "beauty", "price": 650, "originalPrice": 780, "description": "Johnson's Vita-Rich body lotion with nourishing oils — 24-hour moisturization.", "rating": 4.7, "reviewCount": 189, "isNew": False, "isFeatured": False, "discount": 17, "weight": "300ml", "inStock": True, "stockCount": 55, "tags": ["body lotion", "vitamin e"]},
    {"id": "sg-001", "name": "Saeed Ghani Herbal Shampoo", "brand": "Saeed Ghani", "category": "haircare", "price": 420, "originalPrice": 500, "description": "A natural herbal shampoo with bhringraj, amla, and shikakai that strengthens hair.", "rating": 4.6, "reviewCount": 267, "isNew": False, "isFeatured": True, "discount": 16, "weight": "200ml", "inStock": True, "stockCount": 70, "tags": ["herbal shampoo", "hair fall"]},
    {"id": "sg-002", "name": "Saeed Ghani Rose Water", "brand": "Saeed Ghani", "category": "skincare", "price": 280, "originalPrice": 350, "description": "Pure 100% natural rose water distilled from fresh Damask roses.", "rating": 4.8, "reviewCount": 498, "isNew": False, "isFeatured": True, "discount": 20, "weight": "120ml", "inStock": True, "stockCount": 120, "tags": ["rose water", "toner"]},
    {"id": "sg-003", "name": "Saeed Ghani Aloe Vera Gel", "brand": "Saeed Ghani", "category": "skincare", "price": 350, "originalPrice": 450, "description": "Pure, cold-pressed aloe vera gel that soothes sunburn, moisturizes and reduces redness.", "rating": 4.7, "reviewCount": 334, "isNew": False, "isFeatured": False, "discount": 22, "weight": "150g", "inStock": True, "stockCount": 85, "tags": ["aloe vera", "soothing"]},
    {"id": "sg-004", "name": "Saeed Ghani Black Seed Oil", "brand": "Saeed Ghani", "category": "beauty", "price": 650, "originalPrice": 800, "description": "Cold-pressed pure black seed (kalonji) oil for hair growth, skin healing.", "rating": 4.9, "reviewCount": 187, "isNew": True, "isFeatured": False, "discount": 19, "weight": "60ml", "inStock": True, "stockCount": 40, "tags": ["black seed oil", "kalonji"]},
    {"id": "sg-005", "name": "Saeed Ghani Anti-Dandruff Shampoo", "brand": "Saeed Ghani", "category": "haircare", "price": 380, "originalPrice": 480, "description": "An effective anti-dandruff shampoo with neem and tea tree oil.", "rating": 4.5, "reviewCount": 143, "isNew": False, "isFeatured": False, "discount": 21, "weight": "200ml", "inStock": True, "stockCount": 55, "tags": ["anti-dandruff", "neem"]},
    {"id": "sg-006", "name": "Saeed Ghani Multani Mitti Face Pack", "brand": "Saeed Ghani", "category": "skincare", "price": 220, "originalPrice": 280, "description": "Traditional Multani Mitti face pack enriched with rose water and sandalwood powder.", "rating": 4.6, "reviewCount": 289, "isNew": False, "isFeatured": False, "discount": 21, "weight": "100g", "inStock": True, "stockCount": 100, "tags": ["multani mitti", "face pack"]},
]

# ─── Session State (Cart & Wishlist) ───────────────────────────────────────────
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "wishlist" not in st.session_state:
    st.session_state.wishlist = set()
if "page" not in st.session_state:
    st.session_state.page = "home"

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💄 Fashion Cosmetics")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home", "🛍️ Products", "🛒 Cart", "❤️ Wishlist", "📞 Contact"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🔍 Filter Products")

    category_filter = st.selectbox(
        "Category",
        ["All", "Skincare", "Makeup", "Haircare", "Beauty"]
    )

    brand_filter = st.selectbox(
        "Brand",
        ["All", "Dermacos", "Dermashine", "Johnson & Johnson", "Saeed Ghani"]
    )

    price_range = st.slider("Price Range (PKR)", 0, 3500, (0, 3500), step=50)

    search_query = st.text_input("🔎 Search products...", "")

    st.markdown("---")
    cart_count = sum(st.session_state.cart.values())
    st.markdown(f"🛒 **Cart:** {cart_count} items")
    st.markdown(f"❤️ **Wishlist:** {len(st.session_state.wishlist)} items")

    st.markdown("---")
    st.markdown("📍 **Lahore, Pakistan**")
    st.markdown("📞 0300-1234567")
    st.markdown("🕐 Mon–Sat: 10am–9pm")

# ─── Helper Functions ──────────────────────────────────────────────────────────
def add_to_cart(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1
    else:
        st.session_state.cart[product_id] = 1

def toggle_wishlist(product_id):
    if product_id in st.session_state.wishlist:
        st.session_state.wishlist.discard(product_id)
    else:
        st.session_state.wishlist.add(product_id)

def render_stars(rating):
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "⭐" * full + ("✨" if half else "") + "☆" * empty

def get_product_by_id(pid):
    return next((p for p in products if p["id"] == pid), None)

def filter_products(prods):
    filtered = prods
    if category_filter != "All":
        filtered = [p for p in filtered if p["category"] == category_filter.lower()]
    if brand_filter != "All":
        filtered = [p for p in filtered if p["brand"] == brand_filter]
    filtered = [p for p in filtered if price_range[0] <= p["price"] <= price_range[1]]
    if search_query:
        q = search_query.lower()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["brand"].lower() or any(q in t for t in p["tags"])]
    return filtered

def render_product_card(p, cols_per_row=3):
    heart = "❤️" if p["id"] in st.session_state.wishlist else "🤍"
    in_cart = st.session_state.cart.get(p["id"], 0)

    st.markdown(f"""
    <div class="product-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <span class="brand-chip">{p['brand']}</span>
            <div>
                {"<span class='badge-new'>NEW</span> " if p['isNew'] else ""}
                {"<span class='badge-discount'>-" + str(p['discount']) + "%</span>" if p['discount'] else ""}
            </div>
        </div>
        <h4 style="margin:8px 0; color:#880e4f;">{p['name']}</h4>
        <p style="font-size:13px; color:#666; margin:5px 0;">{p['description'][:90]}...</p>
        <div style="margin:5px 0;">
            <span class="rating-stars">{render_stars(p['rating'])}</span>
            <span style="color:#999; font-size:12px;"> {p['rating']} ({p['reviewCount']} reviews)</span>
        </div>
        <div>
            <span class="price-main">PKR {p['price']:,}</span>
            <span class="price-old"> PKR {p['originalPrice']:,}</span>
        </div>
        <div style="font-size:12px; color:#888; margin-top:4px;">
            📦 {p['weight']} &nbsp;|&nbsp; 
            {'✅ In Stock (' + str(p['stockCount']) + ')' if p['inStock'] else '❌ Out of Stock'}
        </div>
        {f"<div style='margin-top:6px; background:#fce4ec; border-radius:8px; padding:4px 8px; display:inline-block; font-size:12px; color:#c2185b;'>🛒 In cart: {in_cart}</div>" if in_cart > 0 else ""}
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button(f"🛒 Add to Cart", key=f"cart_{p['id']}"):
            add_to_cart(p["id"])
            st.rerun()
    with c2:
        if st.button(f"{heart} Wishlist", key=f"wish_{p['id']}"):
            toggle_wishlist(p["id"])
            st.rerun()

# ─── PAGE: HOME ────────────────────────────────────────────────────────────────
if "Home" in page:
    st.markdown("""
    <div class="hero-banner">
        <h1 style="color:white; font-size:2.5rem; margin:0;">💄 Fashion Cosmetics</h1>
        <p style="font-size:1.2rem; margin:10px 0;">Pakistan's Trusted Beauty Store — Lahore</p>
        <p style="font-size:1rem; opacity:0.9;">✨ Authentic Products • Free Delivery • Best Prices</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="stat-box"><h2 style="color:#e91e63;">30+</h2><p>Products</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><h2 style="color:#e91e63;">4</h2><p>Brands</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box"><h2 style="color:#e91e63;">500+</h2><p>Happy Customers</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="stat-box"><h2 style="color:#e91e63;">4.7⭐</h2><p>Avg Rating</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Categories
    st.markdown("## 🗂️ Shop by Category")
    c1, c2, c3, c4 = st.columns(4)
    cats = [("🧴", "Skincare", "skincare"), ("💋", "Makeup", "makeup"), ("💆", "Haircare", "haircare"), ("✨", "Beauty", "beauty")]
    for col, (icon, name, cid) in zip([c1, c2, c3, c4], cats):
        count = len([p for p in products if p["category"] == cid])
        with col:
            st.markdown(f"""
            <div class="product-card" style="text-align:center;">
                <div style="font-size:2.5rem;">{icon}</div>
                <h3 style="margin:5px 0;">{name}</h3>
                <p style="color:#999; font-size:13px;">{count} products</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Featured Products
    st.markdown("## ⭐ Featured Products")
    featured = [p for p in products if p.get("isFeatured")][:6]
    cols = st.columns(3)
    for i, p in enumerate(featured):
        with cols[i % 3]:
            render_product_card(p)

    st.markdown("---")

    # Brands
    st.markdown("## 🏷️ Our Brands")
    b1, b2, b3, b4 = st.columns(4)
    brands_info = [
        ("💊", "Dermacos", "#E8B4B8", "Dermatologist-tested skincare"),
        ("✨", "Dermashine", "#D4AF37", "Radiance & glow solutions"),
        ("🌸", "Johnson & Johnson", "#FFD700", "Trusted gentle care"),
        ("🌿", "Saeed Ghani", "#90EE90", "Natural herbal beauty"),
    ]
    for col, (icon, name, color, desc) in zip([b1, b2, b3, b4], brands_info):
        with col:
            st.markdown(f"""
            <div class="product-card" style="text-align:center; border-top: 4px solid {color};">
                <div style="font-size:2rem;">{icon}</div>
                <b>{name}</b>
                <p style="font-size:12px; color:#888;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Testimonials
    st.markdown("## 💬 Customer Reviews")
    testimonials = [
        ("Ayesha Malik", "Lahore", 5, "Fashion Cosmetics is my go-to place! Quality is amazing and prices are very reasonable."),
        ("Sana Fatima", "Lahore", 5, "Ordered online and received products in 2 days! Dermashine serum has transformed my skin!"),
        ("Zara Ahmed", "Township, Lahore", 5, "بہترین کاسمیٹکس! سارے products authentic ہیں اور قیمتیں بھی مناسب ہیں۔"),
    ]
    tc1, tc2, tc3 = st.columns(3)
    for col, (name, loc, rating, comment) in zip([tc1, tc2, tc3], testimonials):
        with col:
            st.markdown(f"""
            <div class="product-card">
                <div style="font-size:1.5rem; background:#fce4ec; width:45px; height:45px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; color:#880e4f;">
                    {name[0]}
                </div>
                <b>{name}</b> <span style="color:#999; font-size:12px;">📍 {loc}</span><br>
                <span style="color:#ffc107;">{"⭐"*rating}</span><br>
                <p style="font-size:13px; color:#555; margin-top:5px;">{comment}</p>
            </div>
            """, unsafe_allow_html=True)

# ─── PAGE: PRODUCTS ────────────────────────────────────────────────────────────
elif "Products" in page:
    st.markdown("## 🛍️ All Products")

    filtered = filter_products(products)
    st.markdown(f"<p style='color:#888;'>Showing <b>{len(filtered)}</b> products</p>", unsafe_allow_html=True)

    if not filtered:
        st.warning("No products found. Try adjusting filters.")
    else:
        cols = st.columns(3)
        for i, p in enumerate(filtered):
            with cols[i % 3]:
                render_product_card(p)

# ─── PAGE: CART ────────────────────────────────────────────────────────────────
elif "Cart" in page:
    st.markdown("## 🛒 Your Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Go shop! 🛍️")
    else:
        total = 0
        for pid, qty in list(st.session_state.cart.items()):
            p = get_product_by_id(pid)
            if not p:
                continue
            subtotal = p["price"] * qty
            total += subtotal

            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                st.markdown(f"**{p['name']}** — {p['brand']}")
                st.caption(f"PKR {p['price']:,} each")
            with col2:
                st.markdown(f"x **{qty}**")
            with col3:
                st.markdown(f"**PKR {subtotal:,}**")
            with col4:
                if st.button("🗑️", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()

        st.markdown("---")
        shipping = 150 if total < 2000 else 0
        st.markdown(f"**Subtotal:** PKR {total:,}")
        st.markdown(f"**Shipping:** {'PKR 150' if shipping else '🎉 FREE'}")
        st.markdown(f"### Total: PKR {total + shipping:,}")

        if st.button("✅ Place Order", type="primary"):
            st.success("🎉 Order placed successfully! You'll receive a confirmation SMS.")
            st.session_state.cart = {}
            st.balloons()

# ─── PAGE: WISHLIST ────────────────────────────────────────────────────────────
elif "Wishlist" in page:
    st.markdown("## ❤️ Your Wishlist")

    if not st.session_state.wishlist:
        st.info("Your wishlist is empty. Heart products you love! 🤍")
    else:
        cols = st.columns(3)
        for i, pid in enumerate(st.session_state.wishlist):
            p = get_product_by_id(pid)
            if p:
                with cols[i % 3]:
                    render_product_card(p)

# ─── PAGE: CONTACT ─────────────────────────────────────────────────────────────
elif "Contact" in page:
    st.markdown("## 📞 Contact Us")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="product-card">
            <h3>📍 Store Location</h3>
            <p>Main Boulevard, Gulberg<br>Lahore, Punjab, Pakistan</p>
            <h3>📞 Phone</h3>
            <p>0300-1234567<br>042-35761234</p>
            <h3>🕐 Hours</h3>
            <p>Monday – Saturday: 10:00 AM – 9:00 PM<br>Sunday: 12:00 PM – 7:00 PM</p>
            <h3>📧 Email</h3>
            <p>info@fashioncosmetics.pk</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### 💬 Send a Message")
        name = st.text_input("Your Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        message = st.text_area("Message")
        if st.button("Send Message 📨", type="primary"):
            if name and message:
                st.success(f"Thank you {name}! We'll get back to you soon. ✅")
            else:
                st.warning("Please fill in your name and message.")

    st.markdown("---")
    st.markdown("### 🗺️ Find Us")
    st.map(data={"lat": [31.5204], "lon": [74.3587]}, zoom=13)
