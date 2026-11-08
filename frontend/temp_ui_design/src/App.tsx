import { useEffect, useState, type ReactNode } from "react";

type Portal = "Customer" | "Seller Center" | "Admin";
type IconName =
  | "leaf" | "search" | "bag" | "bell" | "home" | "grid" | "box" | "orders"
  | "chart" | "users" | "sparkles" | "upload" | "check" | "arrow" | "plus"
  | "more" | "shield" | "truck" | "clock" | "camera" | "menu" | "x";

const photos = {
  basket: "https://images.unsplash.com/photo-1624668430039-0175a0fbf006?auto=format&fit=crop&w=1200&q=85",
  tomato: "https://images.unsplash.com/photo-1631021967261-c57ee4dfa9bb?auto=format&fit=crop&w=900&q=85",
  carrots: "https://images.unsplash.com/photo-1609842947419-ba4f04d5d60f?auto=format&fit=crop&w=900&q=85",
  vegetables: "https://images.unsplash.com/photo-1723347101054-c246b0034f11?auto=format&fit=crop&w=900&q=85",
};

function Icon({ name, size = 20 }: { name: IconName; size?: number }) {
  const paths: Record<IconName, ReactNode> = {
    leaf: <><path d="M20 4c-8 0-14 4-14 10 0 3 2 5 5 5 6 0 9-7 9-15Z"/><path d="M4 21c2-6 6-10 12-13"/></>,
    search: <><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></>,
    bag: <><path d="M5 8h14l-1 13H6L5 8Z"/><path d="M9 9V6a3 3 0 0 1 6 0v3"/></>,
    bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/><path d="M10 21h4"/></>,
    home: <><path d="m3 11 9-8 9 8"/><path d="M5 10v11h14V10M9 21v-7h6v7"/></>,
    grid: <><rect x="3" y="3" width="7" height="7" rx="2"/><rect x="14" y="3" width="7" height="7" rx="2"/><rect x="3" y="14" width="7" height="7" rx="2"/><rect x="14" y="14" width="7" height="7" rx="2"/></>,
    box: <><path d="m4 7 8-4 8 4-8 4-8-4Z"/><path d="m4 7v10l8 4 8-4V7M12 11v10"/></>,
    orders: <><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/></>,
    chart: <><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></>,
    users: <><circle cx="9" cy="8" r="4"/><path d="M2 21c0-4 3-7 7-7s7 3 7 7M16 4c3 0 5 2 5 5s-2 5-5 5M18 15c3 1 4 3 4 6"/></>,
    sparkles: <><path d="m12 3 1.2 3.8L17 8l-3.8 1.2L12 13l-1.2-3.8L7 8l3.8-1.2L12 3Z"/><path d="m19 14 .8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8L19 14ZM5 14l.7 1.3L7 16l-1.3.7L5 18l-.7-1.3L3 16l1.3-.7L5 14Z"/></>,
    upload: <><path d="M12 16V4M7 9l5-5 5 5"/><path d="M4 15v5h16v-5"/></>,
    check: <path d="m4 12 5 5L20 6"/>,
    arrow: <path d="m9 18 6-6-6-6"/>,
    plus: <path d="M12 5v14M5 12h14"/>,
    more: <><circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/></>,
    shield: <><path d="M12 3 4 6v6c0 5 3 8 8 10 5-2 8-5 8-10V6l-8-3Z"/><path d="m8 12 3 3 5-6"/></>,
    truck: <><path d="M3 6h11v11H3zM14 10h4l3 3v4h-7z"/><circle cx="7" cy="19" r="2"/><circle cx="18" cy="19" r="2"/></>,
    clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
    camera: <><rect x="3" y="6" width="18" height="14" rx="2"/><path d="m8 6 2-3h4l2 3"/><circle cx="12" cy="13" r="4"/></>,
    menu: <path d="M4 7h16M4 12h16M4 17h16"/>,
    x: <path d="m6 6 12 12M18 6 6 18"/>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">{paths[name]}</svg>;
}

function Button({ children, className = "", onClick, disabled, type = "button" }: {
  children: ReactNode; className?: string; onClick?: () => void; disabled?: boolean; type?: "button" | "submit";
}) {
  return <button type={type} className={`button ${className}`} onClick={onClick} disabled={disabled}>{children}</button>;
}

function Field({ label, placeholder, value, onChange, suffix }: {
  label: string; placeholder?: string; value?: string; onChange?: (value: string) => void; suffix?: string;
}) {
  return <label className="field"><span>{label}</span><div className="field-input"><input value={value} placeholder={placeholder} onChange={(e) => onChange?.(e.target.value)} />{suffix && <b>{suffix}</b>}</div></label>;
}

function SelectField({ label, value, options, onChange }: { label: string; value: string; options: string[]; onChange?: (v: string) => void }) {
  return <label className="field"><span>{label}</span><select value={value} onChange={(e) => onChange?.(e.target.value)}>{options.map(o => <option key={o}>{o}</option>)}</select></label>;
}

function AppHeader({ portal, setPortal, onMenu }: { portal: Portal; setPortal: (p: Portal) => void; onMenu: () => void }) {
  return <header className="topbar">
    <div className="brand"><div className="logo"><Icon name="leaf" size={22}/></div><div><strong>AgriXanh</strong><small>Grow green. Live well.</small></div></div>
    <div className="portal-switch">
      {(["Customer", "Seller Center", "Admin"] as Portal[]).map(item => <Button key={item} className={portal === item ? "active" : ""} onClick={() => setPortal(item)}>{item}</Button>)}
    </div>
    <div className="top-actions">
      <Button className="icon-button mobile-menu" onClick={onMenu}><Icon name="menu"/></Button>
      <Button className="icon-button"><Icon name="search"/></Button>
      <Button className="icon-button notice"><Icon name="bell"/><i/></Button>
      <div className="avatar">AM</div><div className="user-name"><strong>An Minh</strong><small>{portal === "Seller Center" ? "Green Farm" : portal}</small></div>
    </div>
  </header>;
}

const navConfig: Record<Portal, { label: string; icon: IconName }[]> = {
  Customer: [{ label: "Discover", icon: "home" }, { label: "Categories", icon: "grid" }, { label: "My orders", icon: "orders" }],
  "Seller Center": [{ label: "Overview", icon: "chart" }, { label: "Create product", icon: "plus" }, { label: "Products", icon: "box" }, { label: "Orders", icon: "orders" }],
  Admin: [{ label: "Platform overview", icon: "grid" }, { label: "User management", icon: "users" }, { label: "AI operations", icon: "sparkles" }],
};

function Sidebar({ portal, page, setPage, open, close }: { portal: Portal; page: string; setPage: (p: string) => void; open: boolean; close: () => void }) {
  return <aside className={`sidebar ${open ? "open" : ""}`}>
    <div className="sidebar-label">{portal === "Customer" ? "Marketplace" : portal}</div>
    <nav>{navConfig[portal].map(item => <Button key={item.label} className={`nav-item ${page === item.label ? "selected" : ""}`} onClick={() => { setPage(item.label); close(); }}><Icon name={item.icon}/><span>{item.label}</span>{page === item.label && <i/>}</Button>)}</nav>
    {portal === "Seller Center" && <div className="sidebar-card"><div className="mini-ai"><Icon name="sparkles" size={18}/></div><strong>AI scans this month</strong><span>142 / 200 images</span><div className="progress"><i style={{ width: "71%" }}/></div><Button>View usage <Icon name="arrow" size={14}/></Button></div>}
    <div className="sidebar-foot"><div className="avatar small">AM</div><div><strong>An Minh</strong><small>Account settings</small></div><Icon name="more"/></div>
  </aside>;
}

function PageTitle({ eyebrow, title, text, action }: { eyebrow?: string; title: string; text?: string; action?: ReactNode }) {
  return <div className="page-heading"><div>{eyebrow && <div className="eyebrow">{eyebrow}</div>}<div className="title" role="heading" aria-level={1}>{title}</div>{text && <p>{text}</p>}</div>{action}</div>;
}

const products = [
  { name: "Vine-ripened Tomatoes", farm: "Green Valley Farm", price: "$4.80", unit: "/ kg", grade: "Grade 1", image: photos.tomato },
  { name: "Organic Harvest Basket", farm: "Sunny Fields Co.", price: "$12.50", unit: "/ basket", grade: "Grade 1", image: photos.basket },
  { name: "Crunchy Carrots", farm: "Mekong Roots", price: "$3.20", unit: "/ kg", grade: "Grade 2", image: photos.carrots },
  { name: "Seasonal Vegetable Box", farm: "Green Valley Farm", price: "$16.00", unit: "/ box", grade: "Grade 1", image: photos.vegetables },
];

function ProductCard({ product, onOpen }: { product: typeof products[number]; onOpen: () => void }) {
  return <article className="product-card" onClick={onOpen}>
    <div className="product-photo"><img src={product.image} alt={product.name}/><div className="ai-badge"><Icon name="sparkles" size={14}/><span>AI Quality</span><strong>{product.grade}</strong></div><Button className="quick-add" onClick={onOpen}><Icon name="plus" size={18}/></Button></div>
    <div className="product-info"><small>{product.farm}</small><div className="product-name">{product.name}</div><div className="product-bottom"><strong>{product.price}</strong><span>{product.unit}</span><div className="rating">★ 4.9</div></div></div>
  </article>;
}

function CustomerHome({ onProduct }: { onProduct: () => void }) {
  return <div className="content">
    <section className="hero">
      <img src={photos.basket} alt="Fresh organic produce in a harvest basket"/>
      <div className="hero-overlay"/>
      <div className="hero-content"><div className="hero-kicker"><Icon name="shield" size={16}/> AI-verified freshness</div><div className="hero-title">Better food,<br/>grown with care.</div><p>Shop local produce, graded for quality by our intelligent vision technology.</p>
        <div className="hero-search"><Icon name="search"/><input placeholder="Search tomatoes, carrots, farms..."/><Button>Search</Button></div>
      </div>
      <div className="freshness-card"><div className="score-ring">98<span>%</span></div><div><strong>Freshness assured</strong><small>Every listed item is AI inspected</small></div></div>
    </section>
    <div className="section-row"><div><div className="section-title">Shop by category</div><p>Fresh essentials for every kitchen</p></div><Button className="text-button">View all <Icon name="arrow" size={16}/></Button></div>
    <div className="categories">
      <Button className="category active"><span className="category-icon">🍅</span><div><strong>Fresh vegetables</strong><small>128 products</small></div><Icon name="arrow"/></Button>
      <Button className="category"><span className="category-icon">🍊</span><div><strong>Seasonal fruits</strong><small>84 products</small></div><Icon name="arrow"/></Button>
      <div className="category-note"><Icon name="sparkles"/><div><strong>Why AI quality?</strong><small>Consistent grading. Confident shopping.</small></div></div>
    </div>
    <div className="section-row"><div><div className="section-title">Featured this week</div><p>Peak freshness, verified by AgriXanh AI</p></div><div className="filter-chips"><Button className="active">All</Button><Button>Vegetables</Button><Button>Fruits</Button></div></div>
    <div className="product-grid">{products.map(p => <ProductCard key={p.name} product={p} onOpen={onProduct}/>)}</div>
  </div>;
}

function ProductDetail({ onBack }: { onBack: () => void }) {
  return <div className="content">
    <Button className="back" onClick={onBack}>← Back to marketplace</Button>
    <div className="detail-layout">
      <div className="gallery"><div className="main-image"><img src={photos.tomato} alt="Vine-ripened tomatoes"/><div className="ai-badge large"><Icon name="sparkles" size={16}/> AI inspected · March 24</div></div><div className="thumbs"><img src={photos.tomato}/><img src={photos.basket}/><img src={photos.vegetables}/></div></div>
      <div className="detail-info"><div className="eyebrow">Green Valley Farm · Vegetables</div><div className="detail-title">Vine-ripened Tomatoes</div><div className="detail-rating">★ 4.9 <span>126 reviews</span> <i/> <span>312 sold</span></div><div className="detail-price">$4.80 <span>/ kilogram</span></div><p>Sweet, juicy tomatoes grown with regenerative farming methods and picked at peak ripeness.</p>
        <div className="analysis-card"><div className="analysis-head"><div className="ai-orb"><Icon name="sparkles"/></div><div><strong>AI Analysis Results</strong><small>Computer vision quality report</small></div><div className="verified"><Icon name="shield" size={15}/> Verified</div></div>
          <div className="analysis-grade"><div><small>QUALITY CLASS</small><strong>Grade 1</strong><span>Premium quality</span></div><div className="confidence"><div><strong>98.4%</strong><small>CONFIDENCE SCORE</small></div></div></div>
          <div className="condition"><span>Surface condition</span><strong><Icon name="check" size={16}/> Smooth, no visible defects</strong></div>
        </div>
        <div className="quantity"><span>Quantity</span><div><Button>−</Button><strong>1 kg</strong><Button>+</Button></div></div>
        <div className="buy-actions"><Button className="secondary"><Icon name="bag"/> Add to cart</Button><Button className="primary">Buy now <Icon name="arrow"/></Button></div>
      </div>
    </div>
  </div>;
}

function CustomerOrders() {
  const steps = [{ t: "Order confirmed", d: "Mar 22, 09:14", icon: "check" as IconName }, { t: "Quality checked", d: "Mar 22, 11:30", icon: "sparkles" as IconName }, { t: "Shipped", d: "Mar 23, 08:45", icon: "truck" as IconName }, { t: "Out for delivery", d: "Expected today", icon: "clock" as IconName }];
  return <div className="content"><PageTitle eyebrow="MY ORDERS" title="Track your fresh delivery" text="Follow your produce from farm to doorstep."/><div className="order-track-card"><div className="order-summary"><div><span>ORDER #AGX-2048</span><strong>Arriving today, 2–4 PM</strong></div><div className="status-pill">In transit</div></div><div className="ordered-products"><img src={photos.tomato}/><img src={photos.carrots}/><div><strong>3 fresh items</strong><small>Green Valley Farm · $24.60</small></div></div><div className="timeline">{steps.map((s, i) => <div className={`timeline-step ${i < 3 ? "done" : "current"}`} key={s.t}><div className="step-icon"><Icon name={s.icon}/></div>{i < steps.length - 1 && <i/>}<strong>{s.t}</strong><small>{s.d}</small></div>)}</div></div></div>;
}

type AnalyzeState = "empty" | "uploading" | "ready" | "analyzing" | "done";

function CreateProduct() {
  const [state, setState] = useState<AnalyzeState>("empty");
  useEffect(() => {
    if (state === "uploading") { const timer = setTimeout(() => setState("ready"), 1100); return () => clearTimeout(timer); }
    if (state === "analyzing") { const timer = setTimeout(() => setState("done"), 1400); return () => clearTimeout(timer); }
  }, [state]);
  return <div className="content seller-content">
    <PageTitle eyebrow="SELLER CENTER / PRODUCTS" title="Create a new product" text="Add product details and let AgriXanh AI verify its quality." action={<div className="draft-badge">Draft auto-saved</div>}/>
    <div className="steps"><div className="active"><i>1</i><span>Product details</span></div><b/><div className={state === "done" ? "active" : ""}><i>2</i><span>AI quality check</span></div><b/><div><i>3</i><span>Review & publish</span></div></div>
    <div className="create-grid">
      <div className="form-card">
        <div className="card-heading"><div className="number">01</div><div><strong>Product information</strong><small>Tell customers what you're selling</small></div></div>
        <div className="form-grid"><Field label="Product name" value="Vine-ripened Tomatoes"/><SelectField label="Category" value="Vegetables" options={["Vegetables", "Fruits"]}/><Field label="Price" value="4.80" suffix="USD / kg"/><Field label="Available quantity" value="120" suffix="kg"/></div>
        <label className="field"><span>Description</span><textarea defaultValue="Sweet, juicy tomatoes grown with regenerative farming methods and picked at peak ripeness."/><small className="char-count">98 / 500</small></label>
        <div className="field-row"><SelectField label="Farm / Origin" value="Green Valley Farm" options={["Green Valley Farm", "Sunny Fields Co."]}/><SelectField label="Harvest date" value="March 23, 2025" options={["March 23, 2025", "March 22, 2025"]}/></div>
      </div>
      <div className={`ai-panel ${state === "done" ? "complete" : ""}`}>
        <div className="card-heading"><div className="number ai"><Icon name="sparkles" size={18}/></div><div><strong>AI Image Analysis</strong><small>Verify quality before publishing</small></div>{state === "done" && <div className="status-pill green"><Icon name="check" size={14}/> Complete</div>}</div>
        {state === "empty" && <div className="upload-zone" onClick={() => setState("uploading")}><div className="upload-icon"><Icon name="camera" size={29}/></div><strong>Upload produce images</strong><p>Use clear, well-lit images showing the full product surface.</p><Button className="secondary"><Icon name="upload"/> Choose images</Button><small>JPG or PNG · Max 10 MB · Up to 6 images</small></div>}
        {state === "uploading" && <div className="uploading-state"><div className="scan-image"><img src={photos.tomato}/><div className="scan-line"/></div><strong>Uploading image...</strong><div className="upload-progress"><i/></div><span>tomatoes_batch_24.jpg · 3.8 MB</span></div>}
        {state === "ready" && <div className="ready-state"><div className="image-ready"><img src={photos.tomato}/><Button className="remove" onClick={() => setState("empty")}><Icon name="x" size={15}/></Button><div><Icon name="check" size={14}/> Upload complete</div></div><div className="ai-prompt"><Icon name="sparkles"/><div><strong>Ready for quality analysis</strong><small>AI will inspect color, shape and surface condition.</small></div></div><Button className="primary analyze" onClick={() => setState("analyzing")}><Icon name="sparkles"/> Analyze with AI</Button></div>}
        {state === "analyzing" && <div className="analyzing-state"><div className="scan-image large"><img src={photos.tomato}/><div className="scan-line"/><div className="focus-corner c1"/><div className="focus-corner c2"/><div className="focus-corner c3"/><div className="focus-corner c4"/></div><div className="ai-loader"><Icon name="sparkles"/><div><strong>Analyzing produce quality...</strong><small>Inspecting surface condition and color consistency</small></div></div><div className="analysis-progress"><i/></div></div>}
        {state === "done" && <div className="result-state"><div className="result-image"><img src={photos.tomato}/><div className="detected"><Icon name="check" size={14}/> Quality detected</div></div><div className="result-hero"><div><small>AI QUALITY CLASS</small><strong>Grade 1</strong><span>Premium quality</span></div><div className="confidence-ring"><strong>98%</strong><small>confidence</small></div></div><div className="metrics"><div><span>Surface condition</span><strong><Icon name="check" size={15}/> Smooth, no defects</strong></div><div><span>Color consistency</span><strong><Icon name="check" size={15}/> Excellent</strong></div><div><span>Estimated freshness</span><strong>5–7 days</strong></div></div><div className="ai-note"><Icon name="shield"/><p><strong>Quality verified by AgriXanh AI</strong><br/>This badge will appear on your product listing.</p></div><Button className="text-button centered" onClick={() => setState("ready")}>Run analysis again</Button></div>}
        {state === "empty" && <div className="tips"><strong>Photo tips for accurate results</strong><span><Icon name="check" size={14}/> Natural, even lighting</span><span><Icon name="check" size={14}/> Show the full product</span><span><Icon name="check" size={14}/> Avoid filters or edits</span></div>}
      </div>
    </div>
    <div className="publish-bar"><div><Icon name="shield"/><span><strong>AI quality check required</strong><small>Complete the image analysis to publish this product.</small></span></div><div><Button className="secondary">Save as draft</Button><Button className="primary" disabled={state !== "done"}>Review & publish <Icon name="arrow"/></Button></div></div>
  </div>;
}

function SellerOverview() {
  const bars = [35, 48, 42, 66, 52, 76, 88, 70, 92, 74, 82, 96];
  return <div className="content"><PageTitle eyebrow="SELLER CENTER" title="Good morning, An Minh" text="Here's what's happening with Green Valley Farm today." action={<Button className="primary"><Icon name="plus"/> Add product</Button>}/><div className="stat-grid"><Stat title="Total sales" value="$12,840" trend="+18.2%" icon="chart"/><Stat title="Orders" value="368" trend="+8.4%" icon="orders"/><Stat title="Products listed" value="42" trend="6 low stock" icon="box"/><Stat title="AI quality scans" value="1,248" trend="98.2% avg." icon="sparkles"/></div><div className="dashboard-grid"><div className="chart-card"><div className="card-top"><div><strong>Sales performance</strong><small>Last 12 months</small></div><strong>$8,420 <span>+12.5%</span></strong></div><div className="chart"><div className="y-labels"><span>$8k</span><span>$6k</span><span>$4k</span><span>$2k</span><span>$0</span></div><div className="bars">{bars.map((h,i) => <div key={i} className={i === 11 ? "hot" : ""}><i style={{height: `${h}%`}}/><span>{["A","M","J","J","A","S","O","N","D","J","F","M"][i]}</span></div>)}</div></div></div><div className="alerts-card"><div className="card-top"><div><strong>Inventory alerts</strong><small>Products needing attention</small></div><span className="alert-count">3</span></div>{products.slice(0,3).map((p,i)=><div className="alert-item" key={p.name}><img src={p.image}/><div><strong>{p.name}</strong><small>{[4,8,12][i]} kg remaining</small></div><Button><Icon name="arrow"/></Button></div>)}</div></div></div>;
}

function Stat({ title, value, trend, icon }: { title: string; value: string; trend: string; icon: IconName }) {
  return <div className="stat-card"><div className="stat-icon"><Icon name={icon}/></div><span>{title}</span><strong>{value}</strong><small>{trend}</small></div>;
}

const initialOrders = [
  { id: "#AGX-2048", customer: "Linh Nguyen", total: "$42.80", date: "Mar 24", status: "Pending" },
  { id: "#AGX-2047", customer: "Bao Tran", total: "$28.40", date: "Mar 24", status: "Shipped" },
  { id: "#AGX-2046", customer: "Emma Dao", total: "$68.10", date: "Mar 23", status: "Delivered" },
  { id: "#AGX-2045", customer: "Minh Hoang", total: "$31.25", date: "Mar 23", status: "Pending" },
];

function OrdersTable() {
  const [orders, setOrders] = useState(initialOrders);
  return <div className="content"><PageTitle eyebrow="SELLER CENTER" title="Order management" text="Track and update customer orders."/><div className="table-card"><div className="table-tools"><div className="filter-chips"><Button className="active">All orders</Button><Button>Pending</Button><Button>Shipped</Button><Button>Delivered</Button></div><div className="small-search"><Icon name="search"/><input placeholder="Search orders"/></div></div><table><thead><tr><th>Order</th><th>Customer</th><th>Date</th><th>Total</th><th>Status</th><th/></tr></thead><tbody>{orders.map((o,i)=><tr key={o.id}><td><strong>{o.id}</strong></td><td><div className="customer-cell"><div className="avatar tiny">{o.customer.split(" ").map(n=>n[0]).join("")}</div>{o.customer}</div></td><td>{o.date}</td><td><strong>{o.total}</strong></td><td><select className={`order-status ${o.status.toLowerCase()}`} value={o.status} onChange={e=>setOrders(orders.map((x,n)=>n===i?{...x,status:e.target.value}:x))}><option>Pending</option><option>Shipped</option><option>Delivered</option></select></td><td><Button className="icon-button"><Icon name="more"/></Button></td></tr>)}</tbody></table></div></div>;
}

function AdminOverview() {
  return <div className="content"><PageTitle eyebrow="ADMIN CONSOLE" title="Platform overview" text="AgriXanh ecosystem performance at a glance." action={<div className="date-pill">Mar 01 – Mar 24, 2025</div>}/><div className="stat-grid"><Stat title="Total users" value="24,892" trend="+12.8% this month" icon="users"/><Stat title="Active sellers" value="1,248" trend="+48 this month" icon="shield"/><Stat title="Gross revenue" value="$284.6K" trend="+18.2% this month" icon="chart"/><Stat title="Total AI scans" value="86,420" trend="98.1% confidence" icon="sparkles"/></div><div className="admin-hero"><div><div className="eyebrow">AI QUALITY NETWORK</div><div className="admin-title">86,420 scans building<br/>a more trusted food system.</div><p>Every scan helps improve marketplace transparency and gives customers confidence in what they buy.</p><div className="admin-metrics"><div><strong>94.8%</strong><span>Grade accuracy</span></div><div><strong>1.8s</strong><span>Avg. scan time</span></div><div><strong>99.2%</strong><span>System uptime</span></div></div></div><div className="orbit"><div className="orbit-core"><Icon name="sparkles" size={38}/><span>AI</span></div><i className="orbit-one"/><i className="orbit-two"/><b className="dot d1"/><b className="dot d2"/><b className="dot d3"/></div></div></div>;
}

const initialUsers = [
  { name: "Linh Nguyen", email: "linh@example.com", role: "Customer", status: "Active", joined: "Mar 12, 2025" },
  { name: "An Minh", email: "an@greenvalley.farm", role: "Seller", status: "Active", joined: "Feb 24, 2025" },
  { name: "Bao Tran", email: "bao@example.com", role: "Customer", status: "Active", joined: "Jan 08, 2025" },
  { name: "Mai Pham", email: "mai@agrixanh.co", role: "Admin", status: "Active", joined: "Dec 15, 2024" },
];

function UsersPage() {
  const [users,setUsers]=useState(initialUsers);
  return <div className="content"><PageTitle eyebrow="ADMIN CONSOLE" title="User management" text="Manage access, permissions and account status." action={<Button className="primary"><Icon name="plus"/> Invite user</Button>}/><div className="table-card"><div className="table-tools"><div className="small-search wide"><Icon name="search"/><input placeholder="Search by name or email"/></div><div className="filter-chips"><Button className="active">All users</Button><Button>Customers</Button><Button>Sellers</Button><Button>Admins</Button></div></div><table><thead><tr><th>User</th><th>Role</th><th>Status</th><th>Joined</th><th/></tr></thead><tbody>{users.map((u,i)=><tr key={u.email}><td><div className="user-cell"><div className={`avatar tiny role-${u.role.toLowerCase()}`}>{u.name.split(" ").map(n=>n[0]).join("")}</div><div><strong>{u.name}</strong><small>{u.email}</small></div></div></td><td><select className={`role-select ${u.role.toLowerCase()}`} value={u.role} onChange={e=>setUsers(users.map((x,n)=>n===i?{...x,role:e.target.value}:x))}><option>Customer</option><option>Seller</option><option>Admin</option></select></td><td><span className="active-dot"><i/> Active</span></td><td>{u.joined}</td><td><Button className="icon-button"><Icon name="more"/></Button></td></tr>)}</tbody></table></div></div>;
}

export default function App() {
  const [portal, setPortal] = useState<Portal>("Seller Center");
  const [page, setPage] = useState("Create product");
  const [menu, setMenu] = useState(false);
  const switchPortal = (p: Portal) => { setPortal(p); setPage(navConfig[p][0].label); };
  let view: ReactNode;
  if (portal === "Customer") view = page === "My orders" ? <CustomerOrders/> : page === "Product detail" ? <ProductDetail onBack={()=>setPage("Discover")}/> : <CustomerHome onProduct={()=>setPage("Product detail")}/>;
  else if (portal === "Seller Center") view = page === "Create product" ? <CreateProduct/> : page === "Orders" ? <OrdersTable/> : <SellerOverview/>;
  else view = page === "User management" ? <UsersPage/> : <AdminOverview/>;
  return <div className="app"><AppHeader portal={portal} setPortal={switchPortal} onMenu={()=>setMenu(!menu)}/><div className="app-body"><Sidebar portal={portal} page={page} setPage={setPage} open={menu} close={()=>setMenu(false)}/><main>{view}</main></div>{menu && <div className="scrim" onClick={()=>setMenu(false)}/>}</div>;
}
