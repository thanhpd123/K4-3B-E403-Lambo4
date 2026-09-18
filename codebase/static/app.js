const $ = selector => document.querySelector(selector);
const lessons = JSON.parse($('#lessonData').textContent);
const notes = $('#notes'), reviewButton = $('#reviewButton'), loading = $('#loading');
const apiError = $('#apiError'), results = $('#results'), findingList = $('#findingList');
const draftArea = $('#draftArea'), draftNotes = $('#draftNotes'), slideViewer = $('#slideViewer');
const slideNumber = $('#slideNumber'), previousSlide = $('#previousSlide'), nextSlide = $('#nextSlide');
const labels = {correct_complete:['Đúng và đủ','correct_complete'],misconception:['Có điểm hiểu sai','misconception'],missing_boundary:['Thiếu điều kiện quan trọng','missing_boundary'],insufficient_evidence:['Chưa đủ căn cứ','insufficient_evidence']};
const noteStore = new Map();
let currentLesson = lessons[0], currentSlide = 1, currentFindings = [];
const escapeHtml = (value='') => value.replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const noteKey = () => `${currentLesson.id}:${currentSlide}`;

function setBusy(busy){reviewButton.disabled=busy;loading.classList.toggle('hidden',!busy)}
function showError(message){apiError.textContent=message;apiError.classList.remove('hidden')}
function saveCurrentNote(){noteStore.set(noteKey(),notes.value)}
function updateSlide(){
  currentSlide=Math.max(1,Math.min(currentLesson.slide_count,currentSlide));
  slideNumber.value=currentSlide;slideNumber.max=currentLesson.slide_count;$('#slideTotal').textContent=currentLesson.slide_count;
  $('#headerLesson').textContent=currentLesson.title;$('#headerProgress').textContent=`${currentSlide} / ${currentLesson.slide_count} slide`;
  $('#progressBar').style.width=`${(currentSlide/currentLesson.slide_count)*100}%`;
  $('#sourceStatus').textContent=`Slide ${currentSlide} + ${currentLesson.transcript_count} transcript của ${currentLesson.title}`;
  previousSlide.disabled=currentSlide===1;nextSlide.disabled=currentSlide===currentLesson.slide_count;
  slideViewer.src=`${currentLesson.slide_url}#page=${currentSlide}&toolbar=0&navpanes=0&view=FitH`;
  notes.value=noteStore.get(noteKey())||'';$('#saveState').textContent=notes.value?'Đã lưu cục bộ':'Chưa lưu';
  results.classList.add('hidden');draftArea.classList.add('hidden');apiError.classList.add('hidden');
}
function goToSlide(number){saveCurrentNote();currentSlide=number;updateSlide()}

previousSlide.addEventListener('click',()=>goToSlide(currentSlide-1));
nextSlide.addEventListener('click',()=>goToSlide(currentSlide+1));
slideNumber.addEventListener('change',()=>goToSlide(Number(slideNumber.value)||1));
document.querySelectorAll('.lesson-button').forEach(button=>button.addEventListener('click',()=>{
  saveCurrentNote();currentLesson=lessons.find(item=>item.id===button.dataset.lessonId);currentSlide=1;
  document.querySelectorAll('.lesson-button').forEach(item=>{item.classList.toggle('active',item===button);item.querySelector('small').textContent=item===button?'Đang học':''});
  updateSlide();
}));

function actionLabels(status){
  if(status==='misconception')return['Xem nguồn','Sửa nháp','Giữ nguyên','Bỏ qua'];
  if(status==='missing_boundary')return['Xem nguồn','Thêm vào ghi chú','Đã biết rồi','Bỏ qua'];
  if(status==='correct_complete')return['Xem nguồn','Giữ nguyên'];
  return['Bổ sung ghi chú','Chọn bài khác','Bỏ qua'];
}
function renderFinding(finding,index){
  const [label,css]=labels[finding.status]||labels.insufficient_evidence;
  const citations=finding.citations.map(c=>`<details class="citation" id="citation-${index}"><summary>${escapeHtml(c.source_id)} · ${escapeHtml(c.source_type)}</summary><blockquote>“${escapeHtml(c.quote)}”</blockquote></details>`).join('');
  const suggestion=finding.suggested_revision?`<div class="suggestion"><small>Bản sửa gợi ý — chưa áp dụng</small>${escapeHtml(finding.suggested_revision)}</div>`:'';
  const buttons=actionLabels(finding.status).map(action=>`<button class="${['Sửa nháp','Thêm vào ghi chú'].includes(action)?'apply':''}" data-action="${escapeHtml(action)}" data-index="${index}">${escapeHtml(action)}</button>`).join('');
  return `<article class="finding ${css}" data-card="${index}"><div class="finding-head"><span class="status">${label}</span><span class="confidence">Độ tin cậy: ${escapeHtml(finding.confidence)}</span></div><p class="excerpt">“${escapeHtml(finding.note_excerpt)}”</p><p><b>${escapeHtml(finding.finding)}</b></p><p>${escapeHtml(finding.explanation)}</p>${citations}${suggestion}${finding.review_question?`<p class="review-question">Tự kiểm: ${escapeHtml(finding.review_question)}</p>`:''}<div class="actions">${buttons}</div></article>`;
}

reviewButton.addEventListener('click',async()=>{
  apiError.classList.add('hidden');results.classList.add('hidden');
  if(notes.value.trim().length<3){showError('Hãy nhập ghi chú cho slide hiện tại trước khi review.');return}
  saveCurrentNote();const form=new FormData();form.append('notes',notes.value.trim());form.append('lesson_id',currentLesson.id);form.append('slide_number',String(currentSlide));setBusy(true);
  try{const response=await fetch('/api/review',{method:'POST',body:form});const data=await response.json();if(!response.ok)throw new Error(data.error||'Review thất bại.');currentFindings=data.findings;findingList.innerHTML=currentFindings.map(renderFinding).join('');$('#providerBadge').textContent=data.is_mock?'MOCK · KHÔNG PHẢI AI':`AI · ${data.provider}`;results.classList.remove('hidden')}
  catch(error){showError(error.message||'Không kết nối được dịch vụ AI.')}finally{setBusy(false)}
});

findingList.addEventListener('click',event=>{
  const button=event.target.closest('button[data-action]');if(!button)return;const index=Number(button.dataset.index),finding=currentFindings[index],action=button.dataset.action;
  if(action==='Xem nguồn'){const citation=$(`#citation-${index}`);if(citation){citation.open=true;citation.scrollIntoView({behavior:'smooth',block:'center'})}return}
  if(['Sửa nháp','Thêm vào ghi chú'].includes(action)){const original=notes.value;draftNotes.value=original.includes(finding.note_excerpt)?original.replace(finding.note_excerpt,finding.suggested_revision):`${original.trim()}\n\n${finding.suggested_revision}`.trim();draftArea.classList.remove('hidden');draftArea.scrollIntoView({behavior:'smooth'});return}
  if(action==='Bổ sung ghi chú'){notes.focus();return}if(action==='Chọn bài khác'){document.querySelector('.lesson-nav').scrollIntoView({behavior:'smooth'});return}button.closest('.finding').style.opacity='.5';
});
$('#confirmDraft').addEventListener('click',()=>{notes.value=draftNotes.value;saveCurrentNote();draftArea.classList.add('hidden');$('#saveState').textContent='Đã xác nhận'});
$('#cancelDraft').addEventListener('click',()=>draftArea.classList.add('hidden'));
notes.addEventListener('input',()=>{$('#saveState').textContent='Chưa lưu';saveCurrentNote()});
updateSlide();
