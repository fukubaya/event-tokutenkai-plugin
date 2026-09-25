# Event & Tokutenkai Component Patterns Reference
（イベント＆特典会 デザインコンポーネント・パターン集）

本ドキュメントは、フライヤーおよびカルーセル制作時に使用する **HTML/CSSコンポーネントの標準パターン集** です。
プラグイン利用時やAIエージェントによる生成時は、**過去のイベント生成物（`events/` 等）を一切参照せず**、本リファレンスおよび `templates/` のボイラープレートから直接パーツを選択・適用してください。

---

## 1. 事前予約（前金）4ステップフロー（スマホ注文・店頭受取/配送）
タワーレコードやHMV、イベント会場特設レジで広く採用されている「スマホでの事前QR注文 ➔ レジ会計」のフローです。

```html
<!-- 事前予約4ステップ案内ブロック -->
<div class="reservation-steps-card" style="background: var(--color-bg-sub, #f1f5f9); border: 0.8pt solid var(--color-border, #cbd5e1); border-radius: 2mm; padding: 2mm 3mm; margin-bottom: 2mm;">
  <div style="font-size: 8.5pt; font-weight: 800; color: var(--color-text-main, #1e293b); margin-bottom: 1.5mm; display: flex; align-items: center; justify-content: space-between;">
    <span>📱 対象商品：事前予約（前金）ご注文の流れ</span>
    <span style="font-size: 7.2pt; color: var(--color-text-sub, #475569); font-weight: 600;">※店頭受取 または 配送受取 を選択可能</span>
  </div>
  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5mm;">
    <!-- STEP 1 -->
    <div style="background: #ffffff; border: 0.6pt solid var(--color-border, #cbd5e1); border-radius: 1.5mm; padding: 1.5mm; text-align: center;">
      <div style="font-size: 7pt; font-weight: 800; color: var(--color-primary-dark, #1557b0); margin-bottom: 0.5mm;">STEP 1</div>
      <div style="font-size: 7.8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">告知QR読み取り</div>
      <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569); margin-top: 0.5mm;">専用予約サイトへアクセス</div>
    </div>
    <!-- STEP 2 -->
    <div style="background: #ffffff; border: 0.6pt solid var(--color-border, #cbd5e1); border-radius: 1.5mm; padding: 1.5mm; text-align: center;">
      <div style="font-size: 7pt; font-weight: 800; color: var(--color-primary-dark, #1557b0); margin-bottom: 0.5mm;">STEP 2</div>
      <div style="font-size: 7.8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">希望商品・枚数選択</div>
      <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569); margin-top: 0.5mm;">カートに入れて注文番号取得</div>
    </div>
    <!-- STEP 3 -->
    <div style="background: #ffffff; border: 0.6pt solid var(--color-border, #cbd5e1); border-radius: 1.5mm; padding: 1.5mm; text-align: center;">
      <div style="font-size: 7pt; font-weight: 800; color: var(--color-primary-dark, #1557b0); margin-bottom: 0.5mm;">STEP 3</div>
      <div style="font-size: 7.8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">受取方法の指定</div>
      <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569); margin-top: 0.5mm;">指定店舗受取 または 自宅配送</div>
    </div>
    <!-- STEP 4 -->
    <div style="background: #ffffff; border: 0.6pt solid var(--color-border, #cbd5e1); border-radius: 1.5mm; padding: 1.5mm; text-align: center;">
      <div style="font-size: 7pt; font-weight: 800; color: var(--color-primary-dark, #1557b0); margin-bottom: 0.5mm;">STEP 4</div>
      <div style="font-size: 7.8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">特設レジにて会計</div>
      <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569); margin-top: 0.5mm;">特典券＆優先入場券を受領</div>
    </div>
  </div>
</div>
```

---

## 2. 2部制（1部 / 2部）ダブルタイムライン
1日2回公演のイベントにおいて、各部のスケジュールをコンパクトに比較表示するパターンです。

```html
<!-- 2部制タイムライン表示 -->
<div class="session-split-container" style="display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; margin-bottom: 2mm;">
  <!-- 第1部 -->
  <div class="session-card" style="background: #ffffff; border: 1pt solid var(--color-border-bold, #94a3b8); border-radius: 2mm; padding: 2mm 2.5mm;">
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 0.8pt solid var(--color-border, #cbd5e1); padding-bottom: 1mm; margin-bottom: 1.5mm;">
      <span style="background: var(--color-primary-dark, #1557b0); color: #ffffff; font-size: 7.8pt; font-weight: 800; padding: 0.3mm 2mm; border-radius: 1mm;">第1部</span>
      <span style="font-size: 8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">13:00 開演（12:30 優先開場）</span>
    </div>
    <div style="font-size: 7.2pt; line-height: 1.4; color: var(--color-text-sub, #475569);">
      <div>・10:30〜 対象商品 販売・予約受付開始</div>
      <div>・12:15 優先入場集合 ➔ 12:30 優先エリア開場</div>
      <div>・<strong>13:00〜13:30 ミニライブ本編 ＆ 撮可TIME</strong></div>
      <div>・13:45〜 第1部 特典会（個別お話し・2shot）</div>
    </div>
  </div>

  <!-- 第2部 -->
  <div class="session-card" style="background: #ffffff; border: 1pt solid var(--color-border-bold, #94a3b8); border-radius: 2mm; padding: 2mm 2.5mm;">
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 0.8pt solid var(--color-border, #cbd5e1); padding-bottom: 1mm; margin-bottom: 1.5mm;">
      <span style="background: #be185d; color: #ffffff; font-size: 7.8pt; font-weight: 800; padding: 0.3mm 2mm; border-radius: 1mm;">第2部</span>
      <span style="font-size: 8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">16:00 開演（15:30 優先開場）</span>
    </div>
    <div style="font-size: 7.2pt; line-height: 1.4; color: var(--color-text-sub, #475569);">
      <div>・15:15 優先入場集合 ➔ 15:30 優先エリア開場</div>
      <div>・<strong>16:00〜16:30 ミニライブ本編 ＆ 撮可TIME</strong></div>
      <div>・16:45〜 第2部 特典会（個別お話し・グループshot）</div>
    </div>
  </div>
</div>
```

---

## 3. 撮影ルールの条件付き表現（全面禁止断定の禁止）
「メンバー・スタッフからの指定がない場合での写真・動画撮影は禁止」という公式アナウンスに対し、撮可タイムの可能性を担保した表記パターンです。

```html
<!-- 条件付き撮可ルール案内 -->
<div class="camera-rule-box" style="background: #fffbeb; border: 0.8pt solid #fde68a; border-radius: 1.5mm; padding: 1.5mm 2.5mm; display: flex; align-items: center; justify-content: space-between; font-size: 7.5pt;">
  <div style="display: flex; align-items: center; gap: 2mm;">
    <img src="assets/icons/camera.svg" style="width: 4mm; height: 4mm;" alt="">
    <span style="font-weight: 800; color: #92400e;">撮影ルール：</span>
    <span style="color: #78350f;"><strong>指定時以外の写真・動画撮影・録音は禁止</strong>（メンバー・スタッフからのアナウンス時のみ撮影可）</span>
  </div>
  <span style="font-size: 6.8pt; background: #fef3c7; color: #b45309; padding: 0.3mm 1.5mm; border-radius: 0.8mm; font-weight: 700; white-space: nowrap;">
    指示・指定時を除く
  </span>
</div>
```

---

## 4. 特典会内部のメンバー名カラーチップ表示
文字で「ひかる(白)・結菜(青)」と書かず、直感的なインラインカラーチップ（`.member-chip`）で配置します。

```html
<!-- メンバーチップ（1行折り返し防止・十分な列幅） -->
<span class="member-chip" style="background: #dbeafe; color: #1e3a8a; border: 0.5pt solid #3b82f6; white-space: nowrap;">
  禾本 珠彩
</span>
<span class="member-chip" style="background: #fce7f3; color: #9d174d; border: 0.5pt solid #ec4899; white-space: nowrap;">
  橘 花怜
</span>
<span class="member-chip" style="background: #fef9c3; color: #854d0e; border: 0.5pt solid #eab308; white-space: nowrap;">
  律月 ひかる
</span>
```

---

## 5. 特典会マナー・禁止事項ピクトグラムストリップ
文字を長々と読ませず、直感的に0.1秒でルールを伝えるピクトグラムストリップです。

```html
<!-- 特典会共通マナーストリップ -->
<div style="background: var(--color-bg-sub, #f8fafc); border: 0.6pt solid var(--color-border, #cbd5e1); border-radius: 1.5mm; padding: 1.2mm 2.5mm; display: flex; align-items: center; justify-content: space-around; font-size: 7.2pt; color: var(--color-text-main, #1e293b);">
  <span style="display: flex; align-items: center; gap: 1mm;">
    <img src="assets/icons/bag-basket.svg" style="width: 3.8mm; height: 3.8mm;" alt="">
    <strong>荷物カゴ：</strong>手荷物はカゴへ
  </span>
  <span style="display: flex; align-items: center; gap: 1mm;">
    <img src="assets/icons/no-touch.svg" style="width: 3.8mm; height: 3.8mm;" alt="">
    <strong>接触禁止：</strong>握手・ハイタッチNG
  </span>
  <span style="display: flex; align-items: center; gap: 1mm;">
    <img src="assets/icons/no-prop.svg" style="width: 3.8mm; height: 3.8mm;" alt="">
    <strong>小道具：</strong>持たせ・着用NG
  </span>
  <span style="display: flex; align-items: center; gap: 1mm;">
    <img src="assets/icons/no-screen-record.svg" style="width: 3.8mm; height: 3.8mm;" alt="">
    <strong>画面録画・LivePhoto禁止</strong>
  </span>
</div>
```

---

## 6. 特典会イラストグリッド（均等3〜4カラム）
テキストのみの殺風景な表組みを避け、案内イラスト（2shot、個別お話し、グループshot）を均等配置してスペースを余すことなく埋めるパターンです。

```html
<!-- 特典会イラストグリッド -->
<div class="summary-illust-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm; margin-top: 1.5mm;">
  <!-- アイテム 1 -->
  <div style="background: #ffffff; border: 0.8pt solid var(--color-border, #cbd5e1); border-radius: 2mm; padding: 1.5mm; text-align: center;">
    <div style="height: 24mm; background: #ffffff; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 1mm;">
      <img src="assets/illustrations/talk.jpg" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="個別お話し会">
    </div>
    <div style="font-size: 8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">① 個別お話し会</div>
    <div style="font-size: 7.2pt; font-weight: 800; color: var(--color-primary-dark, #1557b0); margin: 0.5mm 0;">特典券 1枚</div>
    <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569);">メンバー指名制・1対1トーク</div>
  </div>
  <!-- アイテム 2 -->
  <div style="background: #ffffff; border: 0.8pt solid var(--color-border, #cbd5e1); border-radius: 2mm; padding: 1.5mm; text-align: center;">
    <div style="height: 24mm; background: #ffffff; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 1mm;">
      <img src="assets/illustrations/two-shot.jpg" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="2shot撮影会">
    </div>
    <div style="font-size: 8pt; font-weight: 800; color: var(--color-text-main, #1e293b);">② 2shot撮影会</div>
    <div style="font-size: 7.2pt; font-weight: 800; color: var(--color-secondary, #dc2626); margin: 0.5mm 0;">特典券 2枚</div>
    <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569);">スマホ・スタッフ撮影</div>
  </div>
  <!-- アイテム 3 -->
  <div style="background: #ffffff; border: 0.8pt solid var(--color-border, #cbd5e1); border-radius: 2mm; padding: 1.5mm; text-align: center;">
    <div style="height: 24mm; background: #ffffff; display: flex; align-items: center; justify-content: center; overflow: hidden; margin-bottom: 1mm;">
      <img src="assets/illustrations/group-shot.jpg" style="max-height: 100%; max-width: 100%; object-fit: contain;" alt="グループshot撮影会">
    </div>
    <div style="font-size: 8pt; font-weight: 800; color: #7e22ce; margin: 0.5mm 0;">特典券 3枚</div>
    <div style="font-size: 6.5pt; color: var(--color-text-sub, #475569);">全メンバーと記念撮影</div>
  </div>
</div>
```
