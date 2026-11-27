/* Progressive visitor guidance. Only public model codes travel between pages. */
(function () {
  'use strict';
  var byId = function (id) { return document.getElementById(id); };
  var money = function (amount) { return 'NT$' + amount.toLocaleString('en-US'); };
  var recommended = '不限／請推薦';
  function updatePicker() {
    var tent = byId('quickTent').value;
    var people = byId('quickPeople').value;
    var power = byId('quickPower').value;
    var title, text, button;
    recommended = '不限／請推薦';
    if (power === 'no' || tent === 'open') {
      title = power === 'no' ? '先確認營區規定，不建議直接租用。' : '開放式空間，先討論使用方式。';
      text = '移動冷氣不適合替開放式天幕或客廳帳整體降溫；營區不允許時請勿自行使用。可先與我們討論需求。';
      button = '先討論使用情境';
    } else if (tent === 'large' || people === 'large') {
      recommended = '山水 SAC688';
      title = '可以先比較 SAC-688。';
      text = '大帳或5人以上，優先評估較強冷房力。仍需確認實際帳篷、隔熱、排熱及排水安排。';
      button = '帶入 SAC-688 詢問';
    } else if (tent === 'small' && people === 'small') {
      recommended = '艾比酷 JUZ-400';
      title = '可以先比較 JUZ-400。';
      text = '3×3以下睡帳、1–4人，可先看輕量免排水機型。實際適用仍需核對帳篷及使用條件。';
      button = '帶入 JUZ-400 詢問';
    } else {
      title = '不知道尺寸也沒關係。';
      text = '提供帳篷型號或空間照片，讓我們協助比較兩款機型。你也可以先保留「不限／請推薦」。';
      button = '請協助推薦機型';
    }
    if (power === 'unknown') text += ' 營區用電尚待確認，可先詢問。';
    byId('quickResultTitle').textContent = title;
    byId('quickResultText').textContent = text;
    byId('quickApply').textContent = button;
  }
  function updateSummary() {
    var plan = byId('planSel').value;
    var qty = Number(byId('acQty').textContent);
    var fridge = Number(byId('fridgeQty').textContent);
    var days = plan === '兩天一夜' ? 2 : plan === '三天兩夜' ? 3 : plan === '其他' ? Number(byId('rentDays').textContent) : null;
    var rent = days === null ? null : (1000 + Math.max(0, days - 2) * 300) * qty;
    byId('bkSummaryRent').textContent = rent === null && qty ? '方案待確認' : money(rent || 0);
    byId('bkSummaryDeposit').textContent = money(3000 * qty);
    byId('bkSummaryFridgeRow').hidden = !fridge;
    byId('bkSummaryFridge').textContent = money(800 * fridge);
    var date = byId('bkDate').value;
    var end = '依日期與方案確認';
    if (date && days) {
      var d = date.split('-').map(Number);
      var dt = new Date(Date.UTC(d[0], d[1] - 1, d[2] + days - 1));
      end = dt.toISOString().slice(0,10) + '（取還時間另約）';
    }
    byId('bkSummaryReturn').textContent = end;
    if (date && date >= byId('bkDate').min) {
      byId('bkDate').removeAttribute('aria-invalid');
      byId('bkDate').setAttribute('aria-describedby','bkDateHint');
    }
  }
  window.ccUpdateJourneySummary = updateSummary;
  window.ccEditBooking = function () {
    var result = byId('bkRes');
    result.textContent = '';
    result.classList.remove('show');
    byId('bkComposeStatus').textContent = '請在上方修改需求，再重新整理訊息。原本填寫的內容已保留。';
    var target = document.querySelector('input[name="ccBookingModel"]:checked') || byId('bkDate');
    byId('bookingForm').scrollIntoView({behavior:ccScrollBehavior(),block:'start'});
    target.focus({preventScroll:true});
  };
  if (byId('quickTent')) {
    byId('quickPickerControls').hidden = false;
    ['quickTent','quickPeople','quickPower'].forEach(function (id) { byId(id).addEventListener('change',updatePicker); });
    byId('quickApply').addEventListener('click',function () {
      goBookingWithModel(recommended,'quick_picker');
    });
    updatePicker();
  }
  var anchors = {quickPicker:'rental',rentalModels:'rental',rentalPricing:'rental',pickupLocations:'rental'};
  function revealAnchor(id, push) {
    if (!anchors[id]) return;
    setTab(anchors[id],{noScroll:true});
    try { history[push ? 'pushState' : 'replaceState'](null,'','#' + id); } catch (_) {}
    window.requestAnimationFrame(function () {
      var target = byId(id);
      if (target) {
        target.setAttribute('tabindex','-1');
        target.focus({preventScroll:true});
        target.scrollIntoView({behavior:ccScrollBehavior(),block:'start'});
      }
    });
  }
  document.querySelectorAll('[data-journey-anchor]').forEach(function (link) {
    link.addEventListener('click',function (event) {
      var id = link.getAttribute('href').slice(1);
      if (!anchors[id]) return;
      event.preventDefault();
      revealAnchor(id,true);
    });
  });
  window.addEventListener('hashchange',function () { revealAnchor(location.hash.slice(1),false); });
  // initTab may normalize an unknown anchor. The original requested anchor is retained below.
  var initialAnchor = window.CC_INITIAL_JOURNEY_ANCHOR;
  if (initialAnchor && anchors[initialAnchor]) revealAnchor(initialAnchor,false);
  var model = new URLSearchParams(location.search).get('model');
  var modelMap = {juz400:'艾比酷 JUZ-400',sac688:'山水 SAC688'};
  if (Object.prototype.hasOwnProperty.call(modelMap,model)) goBookingWithModel(modelMap[model],'comparison_model');
  refreshBookingPreview();
})();
