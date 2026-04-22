// ProductCard.jsx — AC/Fridge product spec card
const ProductCard = ({ brand, brandColor = '#0891b2', headerGradient, name, tagline, specs = [] }) => (
  <div style={{
    background: 'white', border: '1px solid #d1fae5',
    borderRadius: '1rem', overflow: 'hidden',
    boxShadow: '0 6px 18px rgba(0,0,0,.06)',
    marginBottom: '.85rem',
  }}>
    <div style={{
      padding: '.8rem 1rem .7rem',
      background: headerGradient || 'linear-gradient(135deg,rgba(6,182,212,.08),rgba(59,130,246,.04))',
      borderBottom: '1px solid #d1fae5',
    }}>
      <div style={{ fontSize: '.7rem', fontWeight: 700, letterSpacing: '.07em', textTransform: 'uppercase', color: brandColor, marginBottom: '.1rem' }}>{brand}</div>
      <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a' }}>{name}</div>
      {tagline && <div style={{ fontSize: '.78rem', color: '#6b7280', marginTop: '.1rem' }}>{tagline}</div>}
    </div>
    <div style={{ padding: '.75rem 1rem' }}>
      {specs.map((spec, i) => (
        <div key={i} style={{
          display: 'flex', justifyContent: 'space-between', alignItems: 'center',
          padding: '.32rem 0', borderBottom: i < specs.length - 1 ? '1px solid #f3f4f6' : 'none',
          fontSize: '.9rem',
        }}>
          <span style={{ color: '#6b7280', fontSize: '.85rem' }}>{spec.label}</span>
          <span style={{ color: '#1f2937', fontWeight: 700, fontSize: '.9rem' }}>{spec.value}</span>
        </div>
      ))}
    </div>
  </div>
);

// NoticeCard.jsx — Color-coded notice card
const NOTICE_COLORS = { c: '#0891b2', w: '#d97706', r: '#dc2626', g: '#059669' };

const NoticeCard = ({ type = 'c', icon, title, items = [] }) => (
  <div style={{
    background: 'white', borderRadius: '.875rem',
    padding: '.85rem 1rem', border: '1px solid #e5e7eb',
    borderLeft: `3px solid ${NOTICE_COLORS[type]}`,
    boxShadow: '0 1px 4px rgba(0,0,0,.05)',
  }}>
    <h4 style={{ fontSize: '.88rem', fontWeight: 800, marginBottom: '.28rem', color: '#1f2937', display: 'flex', alignItems: 'center', gap: '.3rem' }}>
      {icon} {title}
    </h4>
    <ul style={{ paddingLeft: '.9rem', margin: 0 }}>
      {items.map((item, i) => (
        <li key={i} style={{ fontSize: '.83rem', color: '#4b5563', lineHeight: 1.65 }} dangerouslySetInnerHTML={{ __html: item }} />
      ))}
    </ul>
  </div>
);

// AlertBanner.jsx — Info/warning/danger inline banners
const ALERT_STYLES = {
  g: { bg: '#ecfdf5', border: '#6ee7b7', text: '#065f46' },
  y: { bg: '#fffbeb', border: '#fcd34d', text: '#92400e' },
  r: { bg: '#fef2f2', border: '#fca5a5', text: '#991b1b' },
  c: { bg: '#ecfeff', border: '#67e8f9', text: '#155e75' },
};

const AlertBanner = ({ type = 'g', icon, children }) => {
  const st = ALERT_STYLES[type];
  return (
    <div style={{
      borderRadius: '1rem', padding: '.9rem 1.1rem', margin: '.8rem 0',
      display: 'flex', gap: '.7rem', fontSize: '.9rem', lineHeight: 1.62,
      border: `1px solid ${st.border}`, background: st.bg, color: st.text,
    }}>
      <span style={{ fontSize: '1.05rem', flexShrink: 0, marginTop: 2 }}>{icon}</span>
      <div>{children}</div>
    </div>
  );
};

Object.assign(window, { ProductCard, NoticeCard, AlertBanner });
