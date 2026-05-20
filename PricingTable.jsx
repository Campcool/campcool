// PricingTable.jsx — Rental pricing display + LINE CTA
const PricingTable = ({ onLineClick }) => (
  <div style={{ background: 'rgba(255,255,255,.97)', borderRadius: 18, overflow: 'hidden', boxShadow: '0 8px 28px rgba(0,0,0,.13)', maxWidth: 480, margin: '0 auto 1.5rem' }}>

    {/* 標題列 */}
    <div style={{ background: 'linear-gradient(135deg,#059669,#047857)', color: 'white', textAlign: 'center', padding: '13px 16px' }}>
      <div style={{ fontWeight: 800, fontSize: '1.05rem' }}>❄️ 冷氣租借價目表</div>
      <div style={{ fontSize: '.75rem', opacity: .88, marginTop: 3 }}>艾比酷 JUZ-400・山水 SAC688 均適用</div>
    </div>

    {/* 社會證明 */}
    <div style={{ background: '#f0fdf4', borderBottom: '1px solid #d1fae5', padding: '7px 14px', display: 'flex', alignItems: 'center', gap: 6, fontSize: '.78rem', color: '#065f46', fontWeight: 700 }}>
      <span>⭐</span>
      <span>已服務 800+ 組露友・好評不斷・連假必備</span>
    </div>

    {/* 價目表 */}
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
        <tr style={{ background: '#f9fafb' }}>
          <th style={{ padding: '9px 14px', textAlign: 'left', color: '#6b7280', borderBottom: '1px solid #e5e7eb', fontSize: '.8rem', fontWeight: 600 }}>租借方案</th>
          <th style={{ padding: '9px 14px', textAlign: 'center', color: '#6b7280', borderBottom: '1px solid #e5e7eb', fontSize: '.8rem', fontWeight: 600 }}>費用</th>
          <th style={{ padding: '9px 14px', textAlign: 'left', color: '#6b7280', borderBottom: '1px solid #e5e7eb', fontSize: '.8rem', fontWeight: 600 }}>備註</th>
        </tr>
      </thead>
      <tbody>
        {[
          { period: '兩天一夜', price: '$1,000', desc: '週末首選', highlight: false },
          { period: '三天兩夜', price: '$1,300', desc: '連假最划算 🔥', highlight: true, tag: '熱門' },
          { period: '每延長一天', price: '+$300', desc: '彈性加購', highlight: false },
        ].map((row, i) => (
          <tr key={i} style={{ background: row.highlight ? '#dcfce7' : 'white' }}>
            <td style={{ padding: '12px 14px', borderBottom: '1px solid #f0fdf4', color: '#1f2937', fontWeight: 700, fontSize: '.92rem' }}>
              {row.tag && <span style={{ background: '#059669', color: 'white', fontSize: '.65rem', fontWeight: 800, borderRadius: 6, padding: '2px 6px', marginRight: 6 }}>{row.tag}</span>}
              {row.period}
            </td>
            <td style={{ padding: '12px 14px', textAlign: 'center', fontWeight: 800, color: row.highlight ? '#047857' : '#059669', fontSize: '1.1rem', borderBottom: '1px solid #f0fdf4' }}>{row.price}</td>
            <td style={{ padding: '12px 14px', color: '#6b7280', fontSize: '.83rem', borderBottom: '1px solid #f0fdf4' }}>{row.desc}</td>
          </tr>
        ))}
      </tbody>
    </table>

    {/* CTA 區 */}
    <div style={{ padding: '14px 14px 12px' }}>
      <button onClick={() => { logLineClick('pricing_table'); onLineClick?.(); }} style={{
        width: '100%',
        background: 'linear-gradient(135deg,#06C755,#00a844)',
        color: 'white', border: 'none', borderRadius: 14,
        padding: '14px 16px', fontSize: '1rem', fontWeight: 800,
        cursor: 'pointer', fontFamily: 'inherit',
        boxShadow: '0 4px 16px rgba(6,199,85,.35)',
        letterSpacing: '.01em',
      }}>
        💬 加 LINE 查詢檔期・免費諮詢
      </button>
      {/* 緊迫感提示 */}
      <div style={{ textAlign: 'center', marginTop: 8, fontSize: '.75rem', color: '#dc2626', fontWeight: 700 }}>
        ⚡ 連假熱門時段有限，建議提前 2 週預約
      </div>
      <div style={{ textAlign: 'center', marginTop: 4, fontSize: '.72rem', color: '#9ca3af' }}>
        無隱藏費用・透明定價・LINE 30 分鐘內回覆
      </div>
    </div>
  </div>
);

// LineBanner.jsx — LINE CTA banner
const LineBanner = ({ onLineClick }) => (
  <div style={{
    background: 'linear-gradient(135deg,#06C755 0%,#00a844 100%)',
    borderRadius: 20, padding: '1rem 1.2rem', color: 'white',
    display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '.8rem',
    margin: '1.1rem 0', boxShadow: '0 6px 20px rgba(6,199,85,.35)',
  }}>
    <div>
      <div style={{ fontSize: '.92rem', fontWeight: 800, lineHeight: 1.4 }}>
        💬 現在詢問，今晚確認檔期
      </div>
      <div style={{ fontSize: '.75rem', opacity: .88, marginTop: 3, fontWeight: 600 }}>
        平均 30 分鐘回覆・問完沒有強迫預約
      </div>
    </div>
    <a href="https://lin.ee/8maotVi" target="_blank" rel="noopener"
       onClick={() => logLineClick('linebanner')}
       style={{
         background: 'white', color: '#059669',
         padding: '.65rem 1.2rem', borderRadius: 30, textDecoration: 'none',
         fontWeight: 800, fontSize: '.88rem', whiteSpace: 'nowrap',
         boxShadow: '0 3px 10px rgba(0,0,0,.15)', flexShrink: 0,
       }}>
      馬上加 LINE
    </a>
  </div>
);

Object.assign(window, { PricingTable, LineBanner });
