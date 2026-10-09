// static/script.js

document.addEventListener("DOMContentLoaded", function() {
    // 1. التحقق من المدخلات لمنع القيم السالبة أو الصفرية في الكميات والأسعار
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const numberInputs = form.querySelectorAll('input[type="number"]');
            let isValid = true;
            
            numberInputs.forEach(input => {
                if (parseFloat(input.value) <= 0 && input.name.includes('quantity')) {
                    alert("يرجى إدخال كميات موجبة أكبر من الصفر للحفاظ على دقة النمذجة الرياضية.");
                    isValid = false;
                }
            });

            if (!isValid) {
                event.preventDefault(); // إيقاف الإرسال
            }
        });
    });

    // 2. معالجة ورسم المبيان التفاعلي المحسن
    const vaElement = document.getElementById('va_value_hidden');
    const chartCanvas = document.getElementById('vaChart');
    
    if (vaElement && chartCanvas) {
        const vaValue = parseFloat(vaElement.value);
        const ctx = chartCanvas.getContext('2d');
        
        // إنشاء تدرج لوني (Gradient) احترافي للرسم البياني
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        
        if (vaValue >= 0) {
            // تدرج لوني للنمو الاقتصادي (أخضر)
            gradient.addColorStop(0, 'rgba(39, 174, 96, 0.9)');
            gradient.addColorStop(1, 'rgba(46, 204, 113, 0.3)');
        } else {
            // تدرج لوني للانكماش الاقتصادي (أحمر)
            gradient.addColorStop(0, 'rgba(192, 57, 43, 0.9)');
            gradient.addColorStop(1, 'rgba(231, 76, 60, 0.3)');
        }

        const borderColor = vaValue >= 0 ? '#27ae60' : '#c0392b';
        const chartLabel = vaValue >= 0 ? 'قيمة مضافة موجبة (مساهمة في النمو الاقتصادي)' : 'قيمة مقتطعة سالبة (عائق للنمو الاقتصادي)';

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['مؤشر الأثر الاقتصادي الكلي (VA)'],
                datasets: [{
                    label: chartLabel,
                    data: [vaValue],
                    backgroundColor: gradient,
                    borderColor: borderColor,
                    borderWidth: 2,
                    borderRadius: 8, // حواف دائرية احترافية
                    barPercentage: 0.4 // ضبط عرض العمود ليكون أكثر أناقة
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 1500, // حركة سلسة عند التحميل
                    easing: 'easeOutQuart'
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)',
                            borderDash: [5, 5] // خطوط شبكة خلفية منقطة
                        },
                        title: {
                            display: true,
                            text: 'القيمة النقدية (VA)',
                            font: {
                                family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                                size: 14,
                                weight: 'bold'
                            }
                        }
                    },
                    x: {
                        grid: {
                            display: false // إخفاء خطوط الشبكة العمودية لنظافة التصميم
                        },
                        ticks: {
                            font: {
                                family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                                size: 15,
                                weight: 'bold'
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: {
                                family: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                                size: 13
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(44, 62, 80, 0.95)',
                        titleFont: { size: 14, family: "'Segoe UI'" },
                        bodyFont: { size: 15, family: "'Segoe UI'", weight: 'bold' },
                        padding: 15,
                        displayColors: false,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                let value = context.parsed.y;
                                let prefix = value >= 0 ? ' المحصلة: +' : ' المحصلة: ';
                                return prefix + value + ' وحدة نقدية';
                            }
                        }
                    }
                }
            }
        });
    }
});