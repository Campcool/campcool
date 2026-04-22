// HeroSection.jsx — Page hero banner
const HERO_THEMES = {
  rental:  { gradient: 'linear-gradient(135deg,#064e3b,#059669)', emoji: '🏕️', title: '租借資訊', sub: '冷氣方案・服務據點・透明租金，一頁搞定' },
  wiki:    { gradient: 'linear-gradient(135deg,#3b0764,#7c3aed)', emoji: '📚', title: '知識百科', sub: '設備規格・使用指南・冷氣冰箱知識，全在這裡' },
  booking: { gradient: 'linear-gradient(135deg,#7f1d1d,#dc2626)', emoji: '📋', title: '預約須知', sub: '退費規則・取消政策，安心預約無後顧之憂' },
  fridge:  { gradient: 'linear-gradient(135deg,#155e75,#0891b2)', emoji: '🧊', title: '移動冰箱租借', sub: '搭配露營冷氣一起租，夏日清涼食材全保鮮' },
};

const HeroSection = ({ tab }) => {
  const theme = HERO_THEMES[tab] || HERO_THEMES.rental;
  return (
    <div style={{
      background: theme.gradient,
      color: 'white', textAlign: 'center',
      padding: '28px 20px 24px',
      position: 'relative', overflow: 'hidden',
    }}>
      <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,.1)', pointerEvents: 'none' }} />
      <h1 style={{ fontSize: '1.7rem', fontWeight: 800, marginBottom: '.3rem', lineHeight: 1.2, textShadow: '0 2px 8px rgba(0,0,0,.2)', position: 'relative', zIndex: 1 }}>
        {theme.emoji} {theme.title}
      </h1>
      <p style={{ fontSize: '.88rem', opacity: .9, maxWidth: 400, margin: '0 auto', lineHeight: 1.55, position: 'relative', zIndex: 1 }}>
        {theme.sub}
      </p>
    </div>
  );
};

Object.assign(window, { HeroSection, HERO_THEMES });
