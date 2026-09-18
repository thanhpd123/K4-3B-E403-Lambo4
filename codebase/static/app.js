const $ = (selector) => document.querySelector(selector);
const notes = $('#notes');
const source = $('#source');
const sourceFile = $('#sourceFile');
const reviewButton = $('#reviewButton');
const loading = $('#loading');
const apiError = $('#apiError');
const results = $('#results');
const findingList = $('#findingList');
const draftArea = $('#draftArea');
const draftNotes = $('#draftNotes');

const labels = {
  correct_complete: ['Đúng và đủ', 'correct_complete'],
  misconception: ['Có điểm hiểu sai', 'misconception'],
  missing_boundary: ['Thiếu điều kiện quan trọng', 'missing_boundary'],
  insufficient_evidence: ['Chưa đủ căn cứ', 'insufficient_evidence']
};

const escapeHtml = (value='') => value.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));

function setBusy(busy) {
  reviewButton.disabled = busy;
  loading.classList.toggle('hidden', !busy);
}

function showError(message) {
  apiError.textContent = message;
  apiError.classList.remove('hidden');
}

function actionLabels(status) {
  if (status === 'misconception') return ['Xem nguồn', 'Sửa nháp', 'Giữ nguyên', 'Bỏ qua'];
  if (status === 'missing_boundary') return ['Xem nguồn', 'Thêm vào ghi chú', 'Đã biết rồi', 'Bỏ qua'];
  if (status === 'correct_complete') return ['Xem nguồn', 'Giữ nguyên'];
  return ['Bổ sung ghi chú', 'Chọn lại nguồn', 'Bỏ qua'];
}

function renderFinding(finding, index) {
  const [label, css] = labels[finding.status] || labels.insufficient_evidence;
  const citations = finding.citations.map(c => `
    <details class="citation" id="citation-${index}">
      <summary>${escapeHtml(c.source_id)} · ${escapeHtml(c.source_type)}</summary>
      <blockquote>“${escapeHtml(c.quote)}”</blockquote>
    </details>`).join('');
  const suggestion = finding.suggested_revision ? `<div class="suggestion"><small>Bản sửa gợi ý — chưa áp dụng</small>${escapeHtml(finding.suggested_revision)}</div>` : '';
  const buttons = actionLabels(finding.status).map(action => {
    const apply = ['Sửa nháp', 'Thêm vào ghi chú'].includes(action);
    return `<button class="${apply ? 'apply' : ''}" data-action="${escapeHtml(action)}" data-index="${index}">${escapeHtml(action)}</button>`;
  }).join('');
  return `<article class="finding ${css}" data-card="${index}">
    <div class="finding-head"><span class="status">${label}</span><span class="confidence">Độ tin cậy: ${escapeHtml(finding.confidence)}</span></div>
    <p class="excerpt">“${escapeHtml(finding.note_excerpt)}”</p>
    <p><b>${escapeHtml(finding.finding)}</b></p>
    <p>${escapeHtml(finding.explanation)}</p>
    ${citations}${suggestion}
    ${finding.review_question ? `<p class="review-question">Tự kiểm: ${escapeHtml(finding.review_question)}</p>` : ''}
    <div class="actions">${buttons}</div>
  </article>`;
}

let currentFindings = [];

reviewButton.addEventListener('click', async () => {
  apiError.classList.add('hidden');
  results.classList.add('hidden');
  if (notes.value.trim().length < 3 || (!source.value.trim() && !sourceFile.files.length)) {
    showError('Hãy nhập ghi chú và dán hoặc tải lên nguồn sự thật trước khi review.');
    return;
  }
  const form = new FormData();
  form.append('notes', notes.value.trim());
  form.append('source_text', source.value.trim());
  form.append('source_type', document.querySelector('input[name="sourceType"]:checked').value);
  if (sourceFile.files[0]) form.append('source_file', sourceFile.files[0]);
  setBusy(true);
  try {
    const response = await fetch('/api/review', {method: 'POST', body: form});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Review thất bại.');
    currentFindings = data.findings;
    findingList.innerHTML = currentFindings.map(renderFinding).join('');
    $('#providerBadge').textContent = data.is_mock ? 'MOCK · KHÔNG PHẢI AI' : `AI · ${data.provider}`;
    results.classList.remove('hidden');
  } catch (error) {
    showError(error.message || 'Không kết nối được dịch vụ AI.');
  } finally {
    setBusy(false);
  }
});

findingList.addEventListener('click', event => {
  const button = event.target.closest('button[data-action]');
  if (!button) return;
  const index = Number(button.dataset.index);
  const finding = currentFindings[index];
  const action = button.dataset.action;
  if (action === 'Xem nguồn') {
    const citation = document.querySelector(`#citation-${index}`);
    if (citation) { citation.open = true; citation.scrollIntoView({behavior: 'smooth', block: 'center'}); }
    return;
  }
  if (['Sửa nháp', 'Thêm vào ghi chú'].includes(action)) {
    const original = notes.value;
    draftNotes.value = original.includes(finding.note_excerpt)
      ? original.replace(finding.note_excerpt, finding.suggested_revision)
      : `${original.trim()}\n\n${finding.suggested_revision}`.trim();
    draftArea.classList.remove('hidden');
    draftArea.scrollIntoView({behavior: 'smooth'});
    return;
  }
  if (action === 'Bổ sung ghi chú') { notes.focus(); return; }
  if (action === 'Chọn lại nguồn') { source.focus(); return; }
  button.closest('.finding').style.opacity = '.5';
});

$('#confirmDraft').addEventListener('click', () => {
  notes.value = draftNotes.value;
  draftArea.classList.add('hidden');
  $('#saveState').textContent = 'Đã xác nhận';
});
$('#cancelDraft').addEventListener('click', () => draftArea.classList.add('hidden'));
notes.addEventListener('input', () => $('#saveState').textContent = 'Chưa lưu');
sourceFile.addEventListener('change', () => {
  if (sourceFile.files[0]) sourceFile.closest('label').childNodes[0].textContent = sourceFile.files[0].name + ' ';
});

