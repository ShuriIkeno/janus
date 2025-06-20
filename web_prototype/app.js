// Janus Web Prototype - JavaScript

class JanusApp {
    constructor() {
        this.apiBaseUrl = 'http://127.0.0.1:8000';
        this.currentMode = 'past';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadInitialData();
    }

    bindEvents() {
        // Mode toggle
        document.getElementById('pastModeBtn').addEventListener('click', () => this.switchMode('past'));
        document.getElementById('futureModeBtn').addEventListener('click', () => this.switchMode('future'));

        // Past Mode events
        document.getElementById('captureBtn').addEventListener('click', () => this.captureContent());
        document.getElementById('refreshDigestBtn').addEventListener('click', () => this.loadDigest());

        // Future Mode events
        document.getElementById('refreshEventsBtn').addEventListener('click', () => this.loadUpcomingEvents());
        document.getElementById('generateBriefingBtn').addEventListener('click', () => this.generateBriefing());
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Update button states
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(`${mode}ModeBtn`).classList.add('active');

        // Update content visibility
        document.querySelectorAll('.mode-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${mode}Mode`).classList.add('active');

        // Load mode-specific data
        if (mode === 'past') {
            this.loadDigest();
        } else {
            this.loadUpcomingEvents();
        }
    }

    async loadInitialData() {
        await this.testApiConnection();
        this.loadDigest();
    }

    async testApiConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            const data = await response.json();
            console.log('API Health Check:', data);
        } catch (error) {
            console.error('API connection failed:', error);
            this.showMessage('APIサーバーに接続できません。バックエンドが起動していることを確認してください。', 'error');
        }
    }

    async captureContent() {
        const type = document.getElementById('captureType').value;
        const content = document.getElementById('captureContent').value;

        if (!content.trim()) {
            this.showMessage('内容を入力してください。', 'warning');
            return;
        }

        const button = document.getElementById('captureBtn');
        const originalText = button.textContent;
        button.innerHTML = '<span class="loading"></span> キャプチャ中...';
        button.disabled = true;

        try {
            const response = await fetch(`${this.apiBaseUrl}/test/capture`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: type,
                    content: content
                })
            });

            const data = await response.json();
            console.log('Capture result:', data);

            // Clear form
            document.getElementById('captureContent').value = '';
            
            this.showMessage('コンテンツがキャプチャされました！', 'success');
            this.loadDigest(); // Refresh digest
        } catch (error) {
            console.error('Capture failed:', error);
            this.showMessage('キャプチャに失敗しました。', 'error');
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }

    async loadDigest() {
        const digestList = document.getElementById('digestList');
        digestList.innerHTML = '<div class="loading"></div> ダイジェストを読み込み中...';

        try {
            // Mock digest data for demo
            const mockDigest = [
                {
                    id: '1',
                    title: 'AI技術の最新動向',
                    summary: 'Gemini 1.5 Proの新機能についての記事。マルチモーダル機能が大幅に向上し、テキスト、画像、音声を統合した処理が可能になった。',
                    source: 'https://example.com/ai-trends',
                    timestamp: '2024-01-20T09:00:00',
                    type: 'url'
                },
                {
                    id: '2',
                    title: 'UXデザインのベストプラクティス',
                    summary: 'モバイルファーストデザインの重要性について。ユーザー体験を向上させるための5つのポイントが解説されている。',
                    source: 'personal_note',
                    timestamp: '2024-01-19T14:30:00',
                    type: 'text'
                }
            ];

            this.renderDigest(mockDigest);
        } catch (error) {
            console.error('Failed to load digest:', error);
            digestList.innerHTML = '<p>ダイジェストの読み込みに失敗しました。</p>';
        }
    }

    renderDigest(digest) {
        const digestList = document.getElementById('digestList');
        
        if (digest.length === 0) {
            digestList.innerHTML = '<p>まだダイジェストがありません。コンテンツをキャプチャして明日の朝をお楽しみに！</p>';
            return;
        }

        const html = digest.map(item => `
            <div class="list-item">
                <h3>${item.title}</h3>
                <p>${item.summary}</p>
                <div class="meta">
                    <span>📅 ${new Date(item.timestamp).toLocaleDateString('ja-JP')}</span>
                    <span>📝 ${this.getTypeIcon(item.type)} ${item.type}</span>
                    ${item.source !== 'personal_note' ? `<a href="${item.source}" target="_blank">🔗 元記事</a>` : ''}
                </div>
            </div>
        `).join('');

        digestList.innerHTML = html;
    }

    async loadUpcomingEvents() {
        const eventsList = document.getElementById('upcomingEvents');
        eventsList.innerHTML = '<div class="loading"></div> 予定を読み込み中...';

        try {
            // Mock events data for demo
            const mockEvents = [
                {
                    id: '1',
                    title: 'プロジェクト進捗ミーティング',
                    start_time: '2024-01-22T10:00:00',
                    attendees: ['田中', '佐藤', '鈴木'],
                    description: 'Q1の進捗確認と課題の共有'
                },
                {
                    id: '2',
                    title: 'クライアント向けプレゼンテーション',
                    start_time: '2024-01-23T14:00:00',
                    attendees: ['田中', 'クライアントA社'],
                    description: '新機能のデモンストレーション'
                }
            ];

            this.renderEvents(mockEvents);
        } catch (error) {
            console.error('Failed to load events:', error);
            eventsList.innerHTML = '<p>予定の読み込みに失敗しました。</p>';
        }
    }

    renderEvents(events) {
        const eventsList = document.getElementById('upcomingEvents');
        
        if (events.length === 0) {
            eventsList.innerHTML = '<p>今後の予定がありません。</p>';
            return;
        }

        const html = events.map(event => `
            <div class="list-item">
                <h3>${event.title}</h3>
                <p>${event.description}</p>
                <div class="meta">
                    <span>📅 ${new Date(event.start_time).toLocaleDateString('ja-JP')}</span>
                    <span>🕒 ${new Date(event.start_time).toLocaleTimeString('ja-JP', {hour: '2-digit', minute: '2-digit'})}</span>
                    <span>👥 ${event.attendees.join(', ')}</span>
                </div>
            </div>
        `).join('');

        eventsList.innerHTML = html;
    }

    async generateBriefing() {
        const button = document.getElementById('generateBriefingBtn');
        const originalText = button.textContent;
        button.innerHTML = '<span class="loading"></span> 生成中...';
        button.disabled = true;

        try {
            // Mock briefing generation
            await new Promise(resolve => setTimeout(resolve, 2000)); // Simulate processing

            const mockBriefing = [
                {
                    id: '1',
                    event_title: 'プロジェクト進捗ミーティング',
                    briefing_content: '• 前回のアクションアイテムの確認\n• Q1目標達成率: 85%\n• 主要課題: リソース配分の最適化\n• 提案事項: 自動化ツールの導入検討',
                    created_at: new Date().toISOString()
                }
            ];

            this.renderBriefings(mockBriefing);
            this.showMessage('ブリーフィングが生成されました！', 'success');
        } catch (error) {
            console.error('Failed to generate briefing:', error);
            this.showMessage('ブリーフィング生成に失敗しました。', 'error');
        } finally {
            button.textContent = originalText;
            button.disabled = false;
        }
    }

    renderBriefings(briefings) {
        const briefingList = document.getElementById('briefingList');
        
        if (briefings.length === 0) {
            briefingList.innerHTML = '<p>ブリーフィングがありません。「ブリーフィング生成」ボタンをクリックしてください。</p>';
            return;
        }

        const html = briefings.map(briefing => `
            <div class="list-item">
                <h3>📋 ${briefing.event_title}</h3>
                <pre style="white-space: pre-wrap; font-family: inherit;">${briefing.briefing_content}</pre>
                <div class="meta">
                    <span>📅 ${new Date(briefing.created_at).toLocaleDateString('ja-JP')}</span>
                    <span>🕒 ${new Date(briefing.created_at).toLocaleTimeString('ja-JP')}</span>
                </div>
            </div>
        `).join('');

        briefingList.innerHTML = html;
    }

    getTypeIcon(type) {
        const icons = {
            'url': '🔗',
            'text': '📝',
            'voice': '🎤'
        };
        return icons[type] || '📄';
    }

    showMessage(message, type = 'info') {
        // Simple toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;

        const colors = {
            'success': '#48bb78',
            'error': '#f56565',
            'warning': '#ed8936',
            'info': '#4299e1'
        };

        toast.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }
}

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new JanusApp();
});