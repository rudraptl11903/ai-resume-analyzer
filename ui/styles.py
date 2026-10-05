"""
styles.py
ChatGPT-inspired minimal, clean, professional black-and-white design system.
Semantic color is reserved strictly for meaningful indicators (Green=match/pass, Red=missing/error,
Blue=info, Purple=AI recommendation, Orange=warning).
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Base Reset & Typography */
html, body, [class*="css"], .stMarkdown, .stText, p, span, div, label {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    color: #111827;
}

/* Hide Streamlit default chrome & auto-generated page nav */
#MainMenu, header[data-testid="stHeader"], footer, [data-testid="stSidebarNav"] {
    display: none !important;
}

/* Main Workspace Background */
[data-testid="stAppViewContainer"], .main {
    background-color: #FAFAFA !important;
}

.main .block-container {
    max-width: 1280px !important;
    padding-top: 1.25rem !important;
    padding-bottom: 3.5rem !important;
    padding-left: 2.5rem !important;
    padding-right: 2.5rem !important;
}

/* ==========================================================================
   LEFT SIDEBAR (ChatGPT Deep Black Style)
   ========================================================================== */
[data-testid="stSidebar"] {
    background-color: #0D0D0D !important;
    border-right: 1px solid #222222 !important;
    min-width: 270px !important;
    max-width: 290px !important;
}

[data-testid="stSidebar"] * {
    color: #ECECEC !important;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {
    color: #9CA3AF !important;
}

/* Sidebar Logo / Header */
.sidebar-logo-container {
    padding: 1.2rem 0.5rem 1.4rem 0.5rem;
    border-bottom: 1px solid #222222;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.sidebar-logo-icon {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    background: #1F1F1F;
    border: 1px solid #333333;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
}

.sidebar-logo-text {
    font-size: 1.05rem;
    font-weight: 700;
    color: #FFFFFF !important;
    letter-spacing: -0.01em;
}

.sidebar-logo-sub {
    font-size: 0.72rem;
    color: #71717A !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Sidebar Navigation Items */
.sidebar-nav-title {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #666666 !important;
    padding: 0.5rem 0.6rem 0.3rem 0.6rem;
    font-weight: 600;
}

/* Sidebar Radio Buttons (Menu Items) */
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 3px !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 1px 0 !important;
    transition: all 0.15s ease !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #1A1A1A !important;
    border-color: #2E2E2E !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #212121 !important;
    border-color: #383838 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p,
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}

/* Sidebar Candidate Badge at Bottom */
.sidebar-footer-card {
    background: #171717;
    border: 1px solid #262626;
    border-radius: 10px;
    padding: 12px 14px;
    margin-top: 1.5rem;
}

.sidebar-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #27272A;
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ==========================================================================
   TOP BAR (Minimal, Clean Search, Notifications, Profile)
   ========================================================================== */
.top-nav-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid #E5E7EB;
    margin-bottom: 1.75rem;
    background: transparent;
}

.top-nav-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.top-breadcrumb {
    font-size: 0.92rem;
    color: #6B7280;
    display: flex;
    align-items: center;
    gap: 8px;
}

.top-breadcrumb-active {
    font-weight: 600;
    color: #111827;
}

.top-nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
}

.top-search-mock {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.84rem;
    color: #9CA3AF;
    min-width: 240px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.top-search-kbd {
    background: #F3F4F6;
    border: 1px solid #E5E7EB;
    border-radius: 4px;
    padding: 1px 6px;
    font-size: 0.72rem;
    font-family: monospace;
    color: #6B7280;
    margin-left: auto;
}

.top-icon-btn {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    color: #4B5563;
    font-size: 1rem;
    transition: all 0.15s ease;
}

.top-icon-btn:hover {
    background: #F9FAFB;
    border-color: #D1D5DB;
}

.notification-dot {
    position: absolute;
    top: 6px;
    right: 6px;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10B981;
    border: 1px solid #FFFFFF;
}

.top-profile-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 4px 10px 4px 4px;
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 20px;
    cursor: pointer;
}

.top-profile-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #111827;
    color: #FFFFFF;
    font-size: 0.75rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
}

.top-profile-name {
    font-size: 0.82rem;
    font-weight: 500;
    color: #111827;
}

/* ==========================================================================
   MINIMAL CARD DESIGN (White, Subtle Border, Rounded, Minimal Shadow)
   ========================================================================== */
.clean-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    height: 100%;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.clean-card:hover {
    border-color: #D1D5DB;
    box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.05);
}

.card-heading {
    font-size: 1.05rem;
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.4rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.card-subtext {
    font-size: 0.86rem;
    color: #6B7280;
    line-height: 1.5;
}

/* Hero Section */
.hero-wrapper {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 3.5rem 3rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.hero-title {
    font-size: 2.75rem;
    font-weight: 700;
    color: #111827;
    letter-spacing: -0.03em;
    margin-bottom: 0.75rem;
    line-height: 1.15;
}

.hero-subtitle {
    font-size: 1.25rem;
    font-weight: 500;
    color: #4B5563;
    margin-bottom: 1rem;
    letter-spacing: -0.01em;
}

.hero-description {
    font-size: 1.02rem;
    color: #6B7280;
    max-width: 680px;
    margin: 0 auto 2rem auto;
    line-height: 1.6;
}

.hero-badge-row {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 1.75rem;
    flex-wrap: wrap;
}

.hero-badge {
    background: #F3F4F6;
    border: 1px solid #E5E7EB;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.76rem;
    font-weight: 500;
    color: #4B5563;
}

/* ==========================================================================
   BUTTONS (Minimal Black & White)
   ========================================================================== */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.15s ease !important;
    letter-spacing: -0.01em !important;
}

/* Primary Button: Clean Solid Dark */
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background-color: #111827 !important;
    color: #FFFFFF !important;
    border: 1px solid #111827 !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08) !important;
}

.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="baseButton-primary"]:hover {
    background-color: #1F2937 !important;
    border-color: #1F2937 !important;
    color: #FFFFFF !important;
}

/* Secondary Button: Clean White with Subtle Border */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="baseButton-secondary"] {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
}

.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="baseButton-secondary"]:hover {
    background-color: #F9FAFB !important;
    border-color: #D1D5DB !important;
    color: #111827 !important;
}

/* ==========================================================================
   CIRCULAR PROGRESS INDICATORS (Minimal, Semantic color ring)
   ========================================================================== */
.circular-progress-card {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.25rem 1rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.circular-svg {
    transform: rotate(-90deg);
}

.circular-bg {
    fill: none;
    stroke: #E5E7EB;
    stroke-width: 8;
}

.circular-fg {
    fill: none;
    stroke-width: 8;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.6s ease;
}

.circular-text {
    font-size: 1.35rem;
    font-weight: 700;
    fill: #111827;
    font-family: 'Inter', sans-serif;
}

.circular-label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #374151;
    margin-top: 0.6rem;
    letter-spacing: -0.01em;
}

.circular-sublabel {
    font-size: 0.74rem;
    color: #6B7280;
    margin-top: 2px;
}

/* ==========================================================================
   SEMANTIC BADGES & CHIPS (Strict Color Usage)
   ========================================================================== */
.pill-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 3px 4px 3px 0;
    line-height: 1.3;
}

/* Neutral / Default Badge (Black & White) */
.pill-neutral {
    background: #F3F4F6;
    color: #374151;
    border: 1px solid #E5E7EB;
}

/* Green = Good / Matched / Passed */
.pill-green {
    background: #ECFDF5;
    color: #065F46;
    border: 1px solid #A7F3D0;
}

/* Red = Missing / Problem / Failed */
.pill-red {
    background: #FEF2F2;
    color: #991B1B;
    border: 1px solid #FECACA;
}

/* Blue = Information / Metadata */
.pill-blue {
    background: #EFF6FF;
    color: #1E40AF;
    border: 1px solid #BFDBFE;
}

/* Purple = AI / Recommendation */
.pill-purple {
    background: #F5F3FF;
    color: #5B21B6;
    border: 1px solid #DDD6FE;
}

/* Orange = Warning / Moderate */
.pill-orange {
    background: #FFFBEB;
    color: #92400E;
    border: 1px solid #FDE68A;
}

/* Section Status Boxes */
.status-box {
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    font-size: 0.88rem;
    line-height: 1.5;
}

.status-box-green {
    background: #ECFDF5;
    border: 1px solid #A7F3D0;
    color: #065F46;
}

.status-box-red {
    background: #FEF2F2;
    border: 1px solid #FECACA;
    color: #991B1B;
}

.status-box-blue {
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    color: #1E40AF;
}

.status-box-purple {
    background: #F5F3FF;
    border: 1px solid #DDD6FE;
    color: #5B21B6;
}

.status-box-orange {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    color: #92400E;
}

/* Tables & Dataframes */
.stDataFrame, div[data-testid="stTable"] {
    border: 1px solid #E5E7EB !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* Text Inputs and Text Areas */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    color: #111827 !important;
    font-size: 0.9rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #111827 !important;
    box-shadow: 0 0 0 1px #111827 !important;
}

/* Divider */
hr {
    border: none !important;
    border-top: 1px solid #E5E7EB !important;
    margin: 1.75rem 0 !important;
}

/* Streamlit Expander styling */
.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

[data-testid="stExpander"] {
    border: none !important;
    margin-bottom: 0.6rem !important;
}
</style>
"""
