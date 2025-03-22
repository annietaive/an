document.addEventListener('DOMContentLoaded', function() {
    console.log('Annie.py - English Learning Platform is ready!');

    // Audio pronunciation playback
    setupAudioPronunciation();
    
    // Form validation for exercises and quizzes
    setupFormValidation();
    
    // Progress chart if on progress page
    if (document.getElementById('progressChart')) {
        setupProgressChart();
    }
    
    // Navigation active state
    highlightCurrentNavItem();
});

// Function to handle audio pronunciation
function setupAudioPronunciation() {
    const audioButtons = document.querySelectorAll('.audio-btn');
    
    audioButtons.forEach(button => {
        button.addEventListener('click', function() {
            const word = this.dataset.word;
            
            // Use the Web Speech API for pronunciation
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';
                speechSynthesis.speak(utterance);
                
                // Visual feedback
                this.innerHTML = '<i class="fas fa-volume-up"></i> ';
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-volume-up"></i>';
                }, 1000);
            } else {
                alert('Trình duyệt của bạn không hỗ trợ phát âm. (Your browser does not support speech synthesis)');
            }
        });
    });
}

// Function to validate forms
function setupFormValidation() {
    const exerciseForm = document.getElementById('exerciseForm');
    const quizForm = document.getElementById('quizForm');
    
    if (exerciseForm) {
        exerciseForm.addEventListener('submit', function(e) {
            let valid = true;
            const requiredInputs = this.querySelectorAll('input[required]');
            
            requiredInputs.forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                document.getElementById('validationMessage').classList.remove('d-none');
            }
        });
    }
    
    if (quizForm) {
        quizForm.addEventListener('submit', function(e) {
            let valid = true;
            const questions = this.querySelectorAll('.quiz-question');
            
            questions.forEach(question => {
                const radioButtons = question.querySelectorAll('input[type="radio"]');
                const anyChecked = Array.from(radioButtons).some(radio => radio.checked);
                
                if (!anyChecked) {
                    valid = false;
                    question.classList.add('border-danger');
                } else {
                    question.classList.remove('border-danger');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                document.getElementById('validationMessage').classList.remove('d-none');
            }
        });
    }
}

// Function to setup progress chart
function setupProgressChart() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    
    // Get data from data attributes
    const exercisePercentage = parseFloat(document.getElementById('progressChart').dataset.exercisePercentage) || 0;
    const quizPercentage = parseFloat(document.getElementById('progressChart').dataset.quizPercentage) || 0;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Bài tập đã hoàn thành', 'Câu đố đã hoàn thành', 'Còn lại'],
            datasets: [{
                data: [
                    exercisePercentage, 
                    quizPercentage, 
                    100 - (exercisePercentage + quizPercentage)
                ],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(200, 200, 200, 0.2)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(200, 200, 200, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Function to highlight current navigation item
function highlightCurrentNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Function to toggle between light and dark themes if needed
function toggleTheme() {
    const body = document.body;
    body.dataset.bsTheme = body.dataset.bsTheme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', body.dataset.bsTheme);
}

// Vocabulary search functionality
const vocabularySearch = document.getElementById('vocabularySearch');
if (vocabularySearch) {
    vocabularySearch.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const vocabItems = document.querySelectorAll('.vocab-item');
        
        vocabItems.forEach(item => {
            const english = item.querySelector('.english-word').textContent.toLowerCase();
            const vietnamese = item.querySelector('.vietnamese-translation').textContent.toLowerCase();
            
            if (english.includes(searchTerm) || vietnamese.includes(searchTerm)) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Show correct answers for exercises
function showExerciseAnswers() {
    const answers = document.querySelectorAll('.answer');
    answers.forEach(answer => {
        answer.classList.remove('d-none');
    });
    document.getElementById('showAnswersBtn').classList.add('d-none');
}

// Show correct answers for quizzes
function showQuizAnswers() {
    const answers = document.querySelectorAll('.answer');
    answers.forEach(answer => {
        answer.classList.remove('d-none');
    });
    document.getElementById('showAnswersBtn').classList.add('d-none');
}
