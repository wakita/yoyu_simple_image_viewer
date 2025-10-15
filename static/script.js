let currentPage = 1;
const pageSize = 20;
let totalPages = 1;

async function loadImages(page) {
    const gallery = document.getElementById('gallery');
    const pageInfo = document.getElementById('pageInfo');

    gallery.innerHTML = '<div class="loading">読み込み中...</div>';

    try {
        const response = await fetch(`/api/images?page=${page}&page_size=${pageSize}`);
        if (!response.ok) {
            throw new Error('Failed to load images');
        }

        const result = await response.json();
        const images = result.data;
        const pagination = result.pagination;

        currentPage = pagination.page;
        totalPages = pagination.total_pages;

        // Update page info
        pageInfo.textContent = `${pagination.total}件中 ${(currentPage-1)*pageSize + 1} - ${Math.min(currentPage*pageSize, pagination.total)}件目を表示（ページ ${currentPage}/${totalPages}）`;

        // Update buttons
        document.getElementById('prevBtn').disabled = currentPage <= 1;
        document.getElementById('nextBtn').disabled = currentPage >= totalPages;

        // Clear gallery
        gallery.innerHTML = '';

        // Render images
        if (images.length === 0) {
            gallery.innerHTML = '<div class="loading">画像がありません</div>';
            return;
        }

        images.forEach(img => {
            const pairDiv = document.createElement('div');
            pairDiv.className = 'image-pair';

            pairDiv.innerHTML = `
                <div class="image-container">
                    <h3>オリジナル</h3>
                    <img src="/images/original/${img.filename}" alt="${img.filename}" loading="lazy">
                    <div class="annotation">${escapeHtml(img.original)}</div>
                    <div class="filename">${escapeHtml(img.filename)}</div>
                </div>
                <div class="image-container">
                    <h3>第一色覚シミュレーション</h3>
                    <img src="/images/protanope/${img.filename}" alt="${img.filename}" loading="lazy">
                    <div class="annotation">${escapeHtml(img.protanope)}</div>
                    <div class="filename">${escapeHtml(img.filename)}</div>
                </div>
            `;

            gallery.appendChild(pairDiv);
        });

    } catch (error) {
        console.error('Error loading images:', error);
        gallery.innerHTML = '<div class="error">画像の読み込みに失敗しました</div>';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function prevPage() {
    if (currentPage > 1) {
        loadImages(currentPage - 1);
    }
}

function nextPage() {
    if (currentPage < totalPages) {
        loadImages(currentPage + 1);
    }
}

// Load initial page
loadImages(1);