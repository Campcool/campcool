// Header.jsx — Campcool sticky site header
const Header = ({ onLogoClick }) => {
  const s = {
    header: {
      position: 'sticky', top: 0, zIndex: 100,
      background: 'rgba(255,255,255,0.96)',
      backdropFilter: 'blur(8px)',
      borderBottom: '1px solid #d1fae5',
      boxShadow: '0 1px 8px rgba(0,0,0,0.06)',
      padding: '10px 16px',
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    },
    logo: { display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', userSelect: 'none' },
    logoImg: { width: 44, height: 44, borderRadius: 10, objectFit: 'cover', flexShrink: 0 },
    logoText: { display: 'flex', flexDirection: 'column' },
    logoMain: { fontSize: 15, fontWeight: 800, color: '#064e3b', lineHeight: 1.15 },
    logoSub: { fontSize: 10, color: '#059669', fontWeight: 600, letterSpacing: '0.04em' },    lineBtn: {
      background: '#06C755', color: 'white', border: 'none',
      borderRadius: 20, padding: '7px 14px', fontSize: 12,
      fontWeight: 700, cursor: 'pointer', fontFamily: 'inherit',
      display: 'flex', alignItems: 'center', gap: 5,
      boxShadow: '0 2px 8px rgba(6,199,85,.3)',
    },
  };
  return (
    <header style={s.header}>
      <div style={s.logo} onClick={onLogoClick}>
        <img src="../../assets/logo.jpg" alt="露涼社 CampCool Logo" style={s.logoImg} />
        <div style={s.logoText}>
          <span style={s.logoMain}>露涼社</span>
          <span style={s.logoSub}>@CampCool</span>
        </div>
      </div>
      <button style={s.lineBtn} onClick={() => window.open('https://lin.ee/8maotVi','_blank')}>
        <span>💬</span> LINE 諮詢
      </button>
    </header>
  );
};

Object.assign(window, { Header });
