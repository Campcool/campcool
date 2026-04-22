// BottomNav.jsx — Campcool 4-tab bottom navigation
const TABS = [
  { id: 'rental',  emoji: '🏕️', label: '租借資訊', color: '#34d399', bg: 'rgba(52,211,153,.18)' },
  { id: 'wiki',    emoji: '📚', label: '知識百科', color: '#a78bfa', bg: 'rgba(167,139,250,.18)' },
  { id: 'booking', emoji: '📋', label: '預約須知', color: '#f87171', bg: 'rgba(248,113,113,.18)' },
  { id: 'fridge',  emoji: '🧊', label: '冰箱租借', color: '#22d3ee', bg: 'rgba(34,211,238,.18)' },
];

const BottomNav = ({ active, onTabChange }) => {
  const s = {
    bar: {
      position: 'fixed', bottom: 0, left: 0, right: 0,
      background: '#0f1f14',
      borderTop: '1px solid rgba(255,255,255,.08)',
      boxShadow: '0 -6px 24px rgba(0,0,0,.4)',
      display: 'flex', padding: '4px 0 6px', zIndex: 200,
    },
  };
  return (
    <div style={s.bar}>
      {TABS.map(tab => {
        const isOn = active === tab.id;
        return (
          <button key={tab.id} onClick={() => onTabChange(tab.id)} style={{
            flex: 1, padding: '10px 4px 12px', border: 'none', background: 'none',
            color: isOn ? tab.color : 'rgba(255,255,255,.45)',
            cursor: 'pointer', display: 'flex', flexDirection: 'column',
            alignItems: 'center', gap: 4,
            borderTop: `3px solid ${isOn ? tab.color : 'transparent'}`,
            fontFamily: 'inherit', fontWeight: 600, transition: 'color .2s',
          }}>
            <div style={{
              width: 38, height: 38, borderRadius: 11,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: '1.35rem',
              background: isOn ? tab.bg : 'rgba(255,255,255,.07)',
              transform: isOn ? 'translateY(-2px)' : 'none',
              transition: 'transform .15s, background .15s',
            }}>{tab.emoji}</div>
            <span style={{ fontSize: '.72rem', letterSpacing: '.3px', lineHeight: 1, whiteSpace: 'nowrap' }}>
              {tab.label}
            </span>
          </button>
        );
      })}
    </div>
  );
};

Object.assign(window, { BottomNav, TABS });
