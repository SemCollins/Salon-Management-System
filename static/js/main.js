// Dark mode functionality
function initTheme() {
    const theme = localStorage.getItem('theme') || 'light';
    if (theme === 'dark') {
        document.documentElement.classList.add('dark');
    }
}

// Booking system
class BookingSystem {
    constructor() {
        this.currentStep = 1;
        this.selectedService = null;
        this.selectedStylist = null;
        this.selectedSlot = null;
    }

    async init() {
        await this.loadServices();
        this.renderStep();
    }

    async loadServices() {
        const response = await fetch('/api/services');
        this.services = await response.json();
    }

    renderStep() {
        const widget = document.getElementById('booking-widget');
        switch(this.currentStep) {
            case 1:
                widget.innerHTML = this.renderServiceSelection();
                break;
            case 2:
                widget.innerHTML = this.renderStylistSelection();
                break;
            case 3:
                widget.innerHTML = this.renderDateTimeSelection();
                break;
            case 4:
                widget.innerHTML = this.renderConfirmation();
                break;
        }
    }

    renderServiceSelection() {
        return `
            <h3 class="text-2xl font-playfair font-bold text-gray-800 dark:text-white mb-6">Select Service</h3>
            <div class="space-y-4">
                ${this.services.map(service => `
                    <div class="border-2 border-gray-200 dark:border-dark-600 rounded-xl p-4 cursor-pointer hover:border-primary-500 transition-colors" 
                         onclick="bookingSystem.selectService(${service.id})">
                        <div class="flex justify-between items-center">
                            <div>
                                <h4 class="font-semibold text-gray-800 dark:text-white">${service.name}</h4>
                                <p class="text-sm text-gray-600 dark:text-gray-400">${service.description}</p>
                            </div>
                            <div class="text-right">
                                <span class="text-primary-500 font-bold">$${service.price}</span>
                                <p class="text-sm text-gray-500">${service.duration}min</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
            ${this.selectedService ? `
                <button onclick="bookingSystem.nextStep()" class="w-full mt-6 bg-primary-500 hover:bg-primary-600 text-white py-3 rounded-lg transition-colors">
                    Continue to Stylist Selection
                </button>
            ` : ''}
        `;
    }

    selectService(serviceId) {
        this.selectedService = this.services.find(s => s.id === serviceId);
        this.renderStep();
    }

    nextStep() {
        this.currentStep++;
        this.renderStep();
    }

    previousStep() {
        this.currentStep--;
        this.renderStep();
    }
}

// Initialize booking system
const bookingSystem = new BookingSystem();

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    bookingSystem.init();
    
    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeIn');
            }
        });
    }, observerOptions);

    // Observe all sections for animation
    document.querySelectorAll('section').forEach(section => {
        observer.observe(section);
    });
});