// HeroSection.jsx — Page hero banner
const HERO_THEMES = {
  rental: {
    gradient: 'linear-gradient(135deg,#064e3b,#059669)',
    badge: '🏕️ 夏季熱門出租中',
    emoji: '❄️',
    title: '睡覺不悶熱，露營才好玩',
    sub: '兩天一夜 $1,000・新竹・台北・台中・24H 取還',
    stat: '✅ 已服務 800+ 組露友',
  },
  wiki: {
    gradient: 'linear-gradient(135deg,#3b0764,#7c3aed)',
    badge: '📖 選購前必讀',
    emoji: '📊',
    title: '選冷氣前，先看這篇',
    sub: 'BTU、跳電、免排水⋯⋯露營冷氣所有問題一次解答',
    stat: null,
  },
  booking: {
    gradient: 'linear-gradient(135deg,#7f1d1d,#dc2626)',
    badge: '💬 LINE 30 分鐘內回覆',
    emoji: '📋',
    title: '預約簡單，3 步驟搞定',
    sub: 'LINE 詢問 → 確認檔期 → 付款完成，不用等',
    stat: null,
  },
  fridge: {
    gradient: 'linear-gradient(135deg,#155e75,#0891b2)',
    badge: '🧊 統一 $800 / 次',
    emoji: '🧊',
    title: '食材新鮮，露營更美味',
    sub: '20L～60L 多款冰箱，冷藏冷凍都行，搭冷氣一起租更划算',
    stat: null,
  },
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
      {/* 背景暗化層 */}
      <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,.12)', pointerEvents: 'none' }} />

      {/* Badge */}
      {theme.badge && (
        <div style={{
          display: 'inline-block',
          background: 'rgba(255,255,255,.22)',
          backdropFilter: 'blur(4px)',
          borderRadius: 20, padding: '4px 14px',
          fontSize: '.75rem', fontWeight: 700,
          marginBottom: 10, position: 'relative', zIndex: 1,
          letterSpacing: '.02em',
        }}>
          {theme.badge}
        </div>
      )}

      {/* 主標題 */}
      <h1 style={{
        fontSize: 'clamp(1.45rem,4.5vw,2.1rem)',
        fontWeight: 800, marginBottom: '.35rem',
        lineHeight: 1.2,
        textShadow: '0 2px 10px rgba(0,0,0,.25)',
        position: 'relative', zIndex: 1,
      }}>
        {theme.emoji} {theme.title}
      </h1>

      {/* 副標題 */}
      <p style={{
        fontSize: '.88rem', opacity: .92,
        maxWidth: 400, margin: '0 auto',
        lineHeight: 1.6, position: 'relative', zIndex: 1,
      }}>
        {theme.sub}
      </p>

      {/* 社會證明（僅 rental tab） */}
      {theme.stat && (
        <div style={{
          marginTop: 10, position: 'relative', zIndex: 1,
          fontSize: '.75rem', opacity: .88, fontWeight: 600,
          background: 'rgba(255,255,255,.15)',
          display: 'inline-block', borderRadius: 20,
          padding: '3px 12px',
        }}>
          {theme.stat}
        </div>
      )}
    </div>
  );
};

Object.assign(window, { HeroSection, HERO_THEMES });
