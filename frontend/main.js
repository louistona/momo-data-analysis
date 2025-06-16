function filterAndDisplay() {
    let filtered = window.transactions || [];
    const type = document.getElementById('filter').value;
    const date = document.getElementById('filterDate').value;
    const amount = parseInt(document.getElementById('filterAmount').value);
    if (type) filtered = filtered.filter(t => t.category === type);
    if (date) filtered = filtered.filter(t => t.date && t.date.slice(0, 10) === date);
    if (!isNaN(amount)) filtered = filtered.filter(t => t.amount >= amount);
    window.filteredTransactions = filtered;
    renderTable(filtered, window.currentPage, window.itemsPerPage);
    renderTypeChart(filtered);
    renderMonthlyChart(filtered);
}

function populateFilters(data) {
    const types = [...new Set(data.map(t => t.category))];
    const typeSelect = document.getElementById('filter');
    typeSelect.innerHTML = '<option value="">All</option>';
    types.forEach(type => {
        const opt = document.createElement('option');
        opt.value = type;
        opt.textContent = type.replace(/_/g, ' ');
        typeSelect.appendChild(opt);
    });
}

function renderTable(data, page = 1, perPage = null) {
    if (!perPage) perPage = window.itemsPerPage || 10;
    const tbody = document.querySelector('#transactionsTable tbody');
    tbody.innerHTML = '';
    const start = (page - 1) * perPage;
    const end = start + perPage;
    const paginated = data.slice(start, end);
    paginated.forEach(tr => {
        const sender = tr.sender && tr.sender.trim() ? tr.sender : '<span class="missing" title="Not provided for this type">&mdash;</span>';
        const receiver = tr.receiver && tr.receiver.trim() ? tr.receiver : '<span class="missing" title="Not provided for this type">&mdash;</span>';
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tr.id}</td>
            <td>${tr.category}</td>
            <td>${tr.amount}</td>
            <td>${sender}</td>
            <td>${receiver}</td>
            <td>${tr.date || ''}</td>
            <td>${tr.description || ''}</td>
        `;
        row.addEventListener('click', () => showDetails(tr));
        tbody.appendChild(row);
    });

    const pages = document.getElementById('pages');
    if (pages) {
        const totalPages = Math.ceil(data.length / perPage) || 1;
        page.innerHTML = `
            <button id="prevPage" ${page === 1 ? 'disabled' : ''}>Previous</button>
            <span>Page ${page} of ${totalPages}</span>
            <label>Items per page: <select id="itemsPerPage">
                <option value="10" ${perPage==10?'selected':''}>10</option>
                <option value="25" ${perPage==25?'selected':''}>25</option>
                <option value="50" ${perPage==50?'selected':''}>50</option>
                <option value="100" ${perPage==100?'selected':''}>100</option>
            </select></label>
            <button id="nextPage" ${page === totalPages ? 'disabled' : ''}>Next</button>
        `;
        document.getElementById('prevPage').onclick = () => {
            if (page > 1) window.currentPage = page - 1, renderTable(data, window.currentPage, perPage);
        };
        document.getElementById('nextPage').onclick = () => {
            if (page < totalPages) window.currentPage = page + 1, renderTable(data, window.currentPage, perPage);
        };
        document.getElementById('itemsPerPage').onchange = (e) => {
            window.itemsPerPage = parseInt(e.target.value);
            window.currentPage = 1;
            renderTable(data, window.currentPage, window.itemsPerPage);
        };
    }
}

const information = document.getElementById('details');
function showDetails(tr) {
    const content = `
        <div class="transaction-card">
            <h3>Transaction Details</h3>
            <dl>
                <dt>ID</dt><dd>${tr.id}</dd>
                <dt>Type</dt><dd>${tr.category.replace(/_/g, ' ')}</dd>
                <dt>Amount</dt><dd>${tr.amount.toLocaleString()} RWF</dd>
                <dt>Sender</dt><dd>${tr.sender ? tr.sender : '<span class="missing-info">N/A <span class="badge">Not provided for this type</span></span>'}</dd>
                <dt>Receiver</dt><dd>${tr.receiver ? tr.receiver : '<span class="missing-info">N/A <span class="badge">Not provided for this type</span></span>'}</dd>
                <dt>Date</dt><dd>${tr.date || '-'}</dd>
                <dt>Description</dt><dd>${tr.description || '-'}</dd>
            </dl>
        </div>
    `;
    document.getElementById('detailsContent').innerHTML = content;
    information.style.display = 'block';
}

document.addEventListener('DOMContentLoaded', function() {
    window.currentPage = 1;
    window.itemsPerPage = 10;
    fetch('http://localhost:8000/api/transactions')
        .then(res => res.json())
        .then(data => {
            window.transactions = data;
            window.filteredTransactions = data;
            populateFilters(data);
            renderTable(data);
            renderTypeChart(data);
            renderMonthlyChart(data);
        });

    document.getElementById('filter').addEventListener('change', filterAndDisplay);
    document.getElementById('filterDate').addEventListener('change', filterAndDisplay);
    document.getElementById('filterAmount').addEventListener('input', filterAndDisplay);
    document.getElementById('filtersReset').addEventListener('click', function() {
        document.getElementById('filter').value = '';
        document.getElementById('filterDate').value = '';
        document.getElementById('filterAmount').value = '';
        filterAndDisplay();
    });
    setupTabs();
    const close = document.querySelector('.close');
    close.onclick = () => information.style.display = 'none';
    window.onclick = function(event) { if (event.target == information) information.style.display = 'none'; };
});