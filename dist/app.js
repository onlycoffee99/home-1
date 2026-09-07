const tasks=[
  {state:'now',label:'立即核實',title:'9/2 履約會議後續',detail:'確認議題說明書是否當場提出；會後 7 日內索取並核對會議紀錄。',date:'原期限 9/9'},
  {state:'now',label:'立即核實',title:'函 A｜七項不利因素揭露',detail:'確認 115北輕字第1150826001號是否已親送取戳；若未送，先核實佐證再決定補送。',date:'原建議 9/5'},
  {state:'now',label:'立即核實',title:'函 D｜評估區間與法源',detail:'確認 115北輕字第1150826002號是否已用印送達及 7 日回復期是否起算。',date:'待核實'},
  {state:'review',label:'待覆核',title:'12A｜票券履約保障方案',detail:'向平台取得信託／履約保障證明，並洽承作機構；發文時點依仲裁進度決定。',date:'評估會前備妥'},
  {state:'review',label:'待覆核',title:'函 11｜計畫書審查意見回復',detail:'逐項核實 8 項待確認資料；未補佐證者改寫為「另補送＋時程」。',date:'與 12A 銜接'},
  {state:'review',label:'待覆核',title:'函 C／文 07｜代墊繳納聲明',detail:'補行政執行命令與繳訖證明，修正原函正副本錯置及救濟敘述。',date:'附件待補'},
  {state:'review',label:'待覆核',title:'仲裁通知與求償資料',detail:'契約第 15 章以正本覆核；仲裁通知交律師、損害計算交會計師確認。',date:'不得逕送'},
  {state:'hold',label:'暫緩',title:'函 B、E 與票券方案發文',detail:'依函 D 回復期限、9/2 會後結果及仲裁提付時點排序，不提前假設完成。',date:'依前件結果'}
];
const list=document.querySelector('#task-list');
function render(filter='all'){
  const rows=filter==='all'?tasks:tasks.filter(t=>t.state===filter);
  list.innerHTML=rows.map(t=>`<article class="task"><span class="badge ${t.state}">${t.label}</span><div><h3>${t.title}</h3><p>${t.detail}</p></div><time>${t.date}</time></article>`).join('');
}
document.querySelectorAll('.filter').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('.filter').forEach(item=>item.classList.remove('active'));
  button.classList.add('active');render(button.dataset.filter);
}));
render();
