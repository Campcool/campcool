// PricingTable.jsx — Rental pricing display + LINE CTA
const PricingTable = ({ onLineClick }) => (
  <div style={{ background: 'rgba(255,255,255,.95)', borderRadius: 18, overflow: 'hidden', boxShadow: '0 8px 24px rgba(0,0,0,.15)', maxWidth: 480, margin: '0 auto 1.5rem' }}>
    <div style={{ background: '#059669', color: 'white', textAlign: 'center', padding: '13px 16px', fontWeight: 700, fontSize: '1.05rem' }}>
      🏕️ 冷氣租借價目表
    </div>
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ background: '#ecfdf5' }}>
          <th style={{ padding: '9px 14px', textAlign: 'left', color: '#065f46', borderBottom: '1px solid #d1fae5', fontSize: '.85rem' }}>租借天數</th>
          <th style={{ padding: '9px 14px', textAlign: 'center', color: '#065f46', borderBottom: '1px solid #d1fae5', fontSize: '.85rem' }}>費用</th>
          <th style={{ padding: '9px 14px', textAlign: 'left', color: '#065f46', borderBottom: '1px solid #d1fae5', fontSize: '.85rem' }}>說明</th>
        </tr>
      </thead>
      <tbody>
        {[
          { period: '兩天一夜', price: '$1,000', desc: '週末露營首選' },
          { period: '三天兩夜', price: '$1,300', desc: '連假露營優惠 🔥', highlight: true },
          { period: '延長加日', price: '+$300/天', desc: '每多一天加收' },
        ].map((row, i) => (
          <tr key={i} style={{ background: row.highlight ? '#dcfce7' : 'transparent' }}>
            <td style={{ padding: '11px 14px', borderBottom: '1px solid #f0fdf4', color: '#1f2937', fontWeight: 600 }}>{row.period}</td>
            <td style={{ padding: '11px 14px', textAlign: 'center', fontWeight: 800, color: '#059669', fontSize: '1.1rem', borderBottom: '1px solid #f0fdf4' }}>{row.price}</td>
            <td style={{ padding: '11px 14px', color: '#4b5563', fontSize: '.85rem', borderBottom: '1px solid #f0fdf4' }}>{row.desc}</td>
          </tr>
        ))}
      </tbody>
    </table>
    <div style={{ padding: '13px 14px' }}>
      <button onClick={onLineClick} style={{
        width: '100%', background: 'linear-gradient(135deg,#059669,#047857)',
        color: 'white', border: 'none', borderRadius: 12,
        padding: 14, fontSize: '1rem', fontWeight: 700,
        cursor: 'pointer', fontFamily: 'inherit',
      }}>
        💬 立即預約 → 加 LINE 客服
      </button>
    </div>
  </div>
);

// LineBanner.jsx — LINE CTA banner
const LineBanner = ({ onLineClick }) => (
  <div style={{
    background: 'linear-gradient(135deg,#06C755 0%,#00a844 100%)',
    borderRadius: 20, padding: '1rem 1.2rem', color: 'white',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '.8rem',
    margin: '1.1rem 0', boxShadow: '0 6px 16px rgba(6,199,85,.3)',
  }}>
    <strong style={{ fontSize: '.9rem', fontWeight: 700, lineHeight: 1.45 }}>
      💬 有問題就找我們！<br/>LINE 快速回覆・免等待
    </strong>
    <a href="#" onClick={e => { e.preventDefault(); onLineClick?.(); }} style={{
      background: 'white', color: '#06C755',
      padding: '.6rem 1.2rem', borderRadius: 30, textDecoration: 'none',
      fontWeight: 800, fontSize: '.88rem', whiteSpace: 'nowrap',
      boxShadow: '0 3px 8px rgba(0,0,0,.12)', flexShrink: 0,
    }}>
      加入 LINE
    </a>
  </div>
);

Object.assign(window, { PricingTable, LineBanner });
