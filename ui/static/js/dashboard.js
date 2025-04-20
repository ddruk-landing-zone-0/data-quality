// Global variables
let qaData = [];
let timeSeriesChart, ruleBreakdownChart, connectionComparisonChart;
let gaugeCharts = {};
const ruleTypes = ["accuracy", "completeness", "consistency", "validity", "timeliness"];
const colors = {
    accuracy: 'rgba(66, 133, 244, 1)',
    completeness: 'rgba(52, 168, 83, 1)',
    consistency: 'rgba(251, 188, 5, 1)',
    validity: 'rgba(234, 67, 53, 1)',
    timeliness: 'rgba(138, 78, 159, 1)'
};

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    initCharts();
    fetchData();
    
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('dashboard-theme');
    if (savedTheme) {
        document.body.className = savedTheme;
        document.getElementById('theme-switch').checked = savedTheme === 'dark-theme';
        updateThemeStylesheet(savedTheme);
    }
});

// Toggle between light and dark themes
function toggleTheme() {
    const isChecked = document.getElementById('theme-switch').checked;
    const newTheme = isChecked ? 'dark-theme' : 'light-theme';
    
    // Update body class
    document.body.className = newTheme;
    
    // Update stylesheet reference
    updateThemeStylesheet(newTheme);
    
    // Save preference to localStorage
    localStorage.setItem('dashboard-theme', newTheme);
}

// Update the theme stylesheet link
function updateThemeStylesheet(theme) {
    const stylesheetLink = document.getElementById('theme-stylesheet');
    if (stylesheetLink) {
        // Update the href with correct path
        const themeCssFile = theme === 'dark-theme' ? 'theme-dark-constraint.css' : 'theme-light-constraint.css';
        stylesheetLink.href = "{{ url_for('static', filename='css/" + themeCssFile + "') }}";
    }
}

// Fetch data from API endpoint
async function fetchData() {
    try {
        console.log('Fetching data from API... with payload:', {
            "type": "postgres",
            "database": "qa_db",
            "query": "SELECT * FROM qa_logs;"
        });
        const response = await fetch('http://127.0.0.1:9090/qa-results', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "type": "postgres",
                "database": "qa_db",
                "query": "SELECT * FROM qa_logs;"
            })
        });

        console.log('Response:', response);

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        // Transform the data from array of arrays to array of objects
        qaData = data.result.map(row => ({
            id: row[0],
            test_time: row[1],
            type: row[2],
            db: row[3],
            rule_type: row[4],
            rule_id: row[5],
            total_rows: row[6],
            total_rows_pass: row[7],
            pass_percentage: row[8]
        }));

        // Update last refresh time
        document.getElementById('last-update-time').textContent = 'Last updated: ' + new Date().toLocaleTimeString();
        
        // Process and display the data
        filterData();
    } catch (error) {
        console.error('Error fetching data:', error);
        
        // Use sample data if API fails (for development purposes)
        useSampleData();
    }
}

// Function to use sample data if API fails
function useSampleData() {
    // Sample data generation
    qaData = generateSampleData();
    filterData();
}

// Filter data based on user selections
function filterData() {
    const typeFilter = document.getElementById('type-filter').value;
    const dbFilter = document.getElementById('db-filter').value;
    const dateRange = document.getElementById('date-range').value;
    
    // Apply filters
    let filteredData = qaData.filter(item => {
        // Type filter
        if (typeFilter !== 'all' && item.type !== typeFilter) return false;
        
        // Database filter
        if (dbFilter !== 'all' && item.db !== dbFilter) return false;
        
        // Date filter
        const itemDate = new Date(item.test_time);
        const now = new Date();
        
        if (dateRange === 'day') {
            return itemDate >= new Date(now.setDate(now.getDate() - 1));
        } else if (dateRange === 'week') {
            return itemDate >= new Date(now.setDate(now.getDate() - 7));
        } else if (dateRange === 'month') {
            return itemDate >= new Date(now.setMonth(now.getMonth() - 1));
        }
        
        return true;
    });
    
    // Update all visualizations
    updateSummaryCards(filteredData);
    updateTimeSeriesChart(filteredData);
    updateRuleBreakdownChart(filteredData);
    updateConnectionComparisonChart(filteredData);
    updateDetailedTable(filteredData);
}

// Update time series chart with specified time interval
function updateTimeSeriesInterval() {
    updateTimeSeriesChart(qaData.filter(item => {
        // Apply current filters
        const typeFilter = document.getElementById('type-filter').value;
        const dbFilter = document.getElementById('db-filter').value;
        const dateRange = document.getElementById('date-range').value;
        
        // Type filter
        if (typeFilter !== 'all' && item.type !== typeFilter) return false;
        
        // Database filter
        if (dbFilter !== 'all' && item.db !== dbFilter) return false;
        
        // Date filter
        const itemDate = new Date(item.test_time);
        const now = new Date();
        
        if (dateRange === 'day') {
            return itemDate >= new Date(now.setDate(now.getDate() - 1));
        } else if (dateRange === 'week') {
            return itemDate >= new Date(now.setDate(now.getDate() - 7));
        } else if (dateRange === 'month') {
            return itemDate >= new Date(now.setMonth(now.getMonth() - 1));
        }
        
        return true;
    }));
}

// Initialize charts
function initCharts() {
    // Initialize gauge charts
    ruleTypes.forEach(type => {
        const ctx = document.getElementById(`gauge-${type}`).getContext('2d');
        gaugeCharts[type] = new Chart(ctx, createGaugeConfig(0, colors[type]));
    });
    
    // Initialize time series chart
    const timeSeriesCtx = document.getElementById('time-series-chart').getContext('2d');
    timeSeriesChart = new Chart(timeSeriesCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: ruleTypes.map((type, index) => ({
                label: type.charAt(0).toUpperCase() + type.slice(1),
                data: [],
                borderColor: colors[type],
                backgroundColor: colors[type].replace('1)', '0.1)'),
                tension: 0.4,
                pointRadius: 3
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Pass Percentage (%)'
                    }
                }
            }
        }
    });
    
    // Initialize rule breakdown chart
    const ruleBreakdownCtx = document.getElementById('rule-breakdown-chart').getContext('2d');
    ruleBreakdownChart = new Chart(ruleBreakdownCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Pass Percentage',
                data: [],
                backgroundColor: Object.values(colors),
                borderColor: Object.values(colors),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
    
    // Initialize connection comparison chart
    const connectionComparisonCtx = document.getElementById('connection-comparison-chart').getContext('2d');
    connectionComparisonChart = new Chart(connectionComparisonCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: ruleTypes.map((type, index) => ({
                label: type.charAt(0).toUpperCase() + type.slice(1),
                data: [],
                backgroundColor: colors[type],
                borderColor: colors[type],
                borderWidth: 1
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Pass Percentage (%)'
                    }
                }
            }
        }
    });
}

// Create gauge chart configuration
function createGaugeConfig(value, color) {
    return {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [value, 100 - value],
                backgroundColor: [
                    color,
                    'rgba(200, 200, 200, 0.2)'
                ],
                borderWidth: 0
            }]
        },
        options: {
            circumference: 180,
            rotation: -90,
            cutout: '75%',
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false
                }
            },
            maintainAspectRatio: false,
            responsive: true
        }
    };
}

// Update summary cards with gauge charts
function updateSummaryCards(data) {
    // Calculate average score by rule type
    const averages = {};
    
    ruleTypes.forEach(type => {
        const rules = data.filter(item => item.rule_type === type);
        if (rules.length > 0) {
            const sum = rules.reduce((acc, item) => acc + item.pass_percentage, 0);
            averages[type] = sum / rules.length;
        } else {
            averages[type] = 0;
        }
    });
    
    // Update each gauge chart and value
    ruleTypes.forEach(type => {
        const value = averages[type] || 0;
        const formattedValue = value.toFixed(1) + '%';
        
        // Update gauge chart
        gaugeCharts[type].data.datasets[0].data = [value, 100 - value];
        gaugeCharts[type].update();
        
        // Update text value
        document.getElementById(`${type}-value`).textContent = formattedValue;
    });
}

// Update time series chart
function updateTimeSeriesChart(data) {
    // Get time delta selection
    const deltaSelect = document.getElementById('time-delta').value;
    
    // Group data points based on selected time delta
    const groupedData = groupDataByTimeDelta(data, deltaSelect);
    
    // Update chart
    timeSeriesChart.data.labels = groupedData.labels;
    
    ruleTypes.forEach((type, index) => {
        timeSeriesChart.data.datasets[index].data = groupedData.series[type] || [];
    });
    
    timeSeriesChart.update();
}

// Group data by selected time delta
function groupDataByTimeDelta(data, deltaType) {
    // Sort data by test_time
    const sortedData = [...data].sort((a, b) => new Date(a.test_time) - new Date(b.test_time));
    
    // Initialize result object
    const result = {
        labels: [],
        series: {}
    };
    
    // Initialize series object for each rule type
    ruleTypes.forEach(type => {
        result.series[type] = [];
    });
    
    // If no data, return empty result
    if (sortedData.length === 0) {
        return result;
    }
    
    // Group data by selected time delta
    const timeGroups = {};
    
    sortedData.forEach(item => {
        const date = new Date(item.test_time);
        let groupKey;
        
        // Format date according to delta type
        switch (deltaType) {
            case 'minute':
                groupKey = moment(date).format('YYYY-MM-DD HH:mm');
                break;
            case 'hour':
                groupKey = moment(date).format('YYYY-MM-DD HH:00');
                break;
            case 'halfday':
                groupKey = moment(date).format('YYYY-MM-DD ') + (date.getHours() < 12 ? 'AM' : 'PM');
                break;
            case 'day':
                groupKey = moment(date).format('YYYY-MM-DD');
                break;
            case 'week':
                groupKey = moment(date).format('YYYY-[W]WW');
                break;
            case 'month':
                groupKey = moment(date).format('YYYY-MM');
                break;
            case 'year':
                groupKey = moment(date).format('YYYY');
                break;
            default:
                groupKey = moment(date).format('YYYY-MM-DD');
        }
        
        // Create group if it doesn't exist
        if (!timeGroups[groupKey]) {
            timeGroups[groupKey] = {};
            ruleTypes.forEach(type => {
                timeGroups[groupKey][type] = [];
            });
        }
        
        // Add data to appropriate group
        if (ruleTypes.includes(item.rule_type)) {
            timeGroups[groupKey][item.rule_type].push(item.pass_percentage);
        }
    });
    
    // Convert groups to arrays and calculate averages
    const groupKeys = Object.keys(timeGroups).sort();
    
    // Prepare labels and series data
    result.labels = groupKeys.map(key => {
        // Format display label based on delta type
        switch (deltaType) {
            case 'minute':
                return moment(key, 'YYYY-MM-DD HH:mm').format('HH:mm');
            case 'hour':
                return moment(key, 'YYYY-MM-DD HH:00').format('HH:00');
            case 'halfday':
                return key.split(' ')[1]; // Just show AM/PM
            case 'day':
                return moment(key, 'YYYY-MM-DD').format('MMM DD');
            case 'week':
                return key; // Already formatted as YYYY-WXX
            case 'month':
                return moment(key, 'YYYY-MM').format('MMM YYYY');
            case 'year':
                return key; // Already just the year
            default:
                return moment(key, 'YYYY-MM-DD').format('MMM DD');
        }
    });
    
    // Calculate averages for each group and rule type
    ruleTypes.forEach(type => {
        groupKeys.forEach(key => {
            const values = timeGroups[key][type];
            if (values.length > 0) {
                const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
                result.series[type].push(avg);
            } else {
                result.series[type].push(null); // No data for this time period
            }
        });
    });
    
    return result;
}

// Update rule breakdown chart
function updateRuleBreakdownChart(data) {
    // Get unique rule IDs
    const ruleIds = [...new Set(data.map(item => item.rule_id))];
    
    // Calculate average for each rule ID
    const ruleAverages = ruleIds.map(ruleId => {
        const ruleData = data.filter(item => item.rule_id === ruleId);
        const sum = ruleData.reduce((acc, item) => acc + item.pass_percentage, 0);
        const avg = sum / ruleData.length;
        
        // Get the rule type for color coding
        const ruleType = ruleData[0]?.rule_type || 'accuracy';
        
        return {
            ruleId,
            avg,
            ruleType
        };
    }).sort((a, b) => a.avg - b.avg); // Sort by average score
    
    // Update chart
    ruleBreakdownChart.data.labels = ruleAverages.map(item => item.ruleId);
    ruleBreakdownChart.data.datasets[0].data = ruleAverages.map(item => item.avg);
    ruleBreakdownChart.data.datasets[0].backgroundColor = ruleAverages.map(item => colors[item.ruleType]);
    
    ruleBreakdownChart.update();
}

// Update connection comparison chart
function updateConnectionComparisonChart(data) {
    // Get unique connection types
    const connectionTypes = [...new Set(data.map(item => item.type))];
    
    // Calculate average for each connection type and rule type
    const connectionAverages = {};
    
    connectionTypes.forEach(connType => {
        connectionAverages[connType] = {};
        
        ruleTypes.forEach(ruleType => {
            const filtered = data.filter(item => 
                item.type === connType && item.rule_type === ruleType
            );
            
            if (filtered.length > 0) {
                const sum = filtered.reduce((acc, item) => acc + item.pass_percentage, 0);
                connectionAverages[connType][ruleType] = sum / filtered.length;
            } else {
                connectionAverages[connType][ruleType] = 0;
            }
        });
    });
    
    // Update chart
    connectionComparisonChart.data.labels = connectionTypes;
    
    ruleTypes.forEach((type, index) => {
        connectionComparisonChart.data.datasets[index].data = 
            connectionTypes.map(connType => connectionAverages[connType][type]);
    });
    
    connectionComparisonChart.update();
}

// Update detailed table - show only the most recent 100 logs
function updateDetailedTable(data) {
    const tableBody = document.getElementById('detailed-scores-body');
    tableBody.innerHTML = '';
    
    // Sort by test_time (newest first)
    const sortedData = [...data].sort((a, b) => new Date(b.test_time) - new Date(a.test_time));
    
    // Limit to 100 most recent logs
    const recentLogs = sortedData.slice(0, 100);
    
    // Sort by pass percentage (lowest first) within the 100 most recent
    recentLogs.sort((a, b) => a.pass_percentage - b.pass_percentage);
    
    recentLogs.forEach(item => {
        const row = document.createElement('tr');
        
        // Add pass percentage class for styling
        if (item.pass_percentage < 50) {
            row.classList.add('fail');
        } else if (item.pass_percentage < 80) {
            row.classList.add('warning');
        } else {
            row.classList.add('pass');
        }
        
        // Format date
        const testDate = new Date(item.test_time);
        const formattedDate = testDate.toLocaleString();
        
        row.innerHTML = `
            <td>${item.rule_id}</td>
            <td>${item.rule_type}</td>
            <td>${item.type}</td>
            <td>${item.db}</td>
            <td>${item.total_rows}</td>
            <td>${item.total_rows_pass}</td>
            <td>${item.pass_percentage.toFixed(2)}%</td>
            <td>${formattedDate}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

// Generate sample data if API fails (for development)
function generateSampleData() {
    const sampleData = [];
    
    // Add sample data for different times and rule types
    const now = new Date();
    const connectionTypes = ["postgres", "mysql", "mongo"];
    const databases = ["test", "qa_db"];
    let idCounter = 1;
    
    // Generate samples for the past month
    for (let i = 30; i >= 0; i--) {
        const date = new Date(now);
        date.setDate(date.getDate() - i);
        
        // Add multiple data points per day to demonstrate time interval grouping
        for (let hour = 0; hour < 24; hour += 4) {
            date.setHours(hour);
            
            ruleTypes.forEach(ruleType => {
                connectionTypes.forEach(connType => {
                    // Skip some combinations to make data more realistic
                    if (Math.random() > 0.7) return;
                    
                    const db = databases[Math.floor(Math.random() * databases.length)];
                    const ruleId = `${ruleType}_check_${Math.floor(Math.random() * 3) + 1}`;
                    
                    // Create more realistic data patterns
                    let basePercentage;
                    
                    // Different databases have different baseline quality
                    if (db === "test") {
                        basePercentage = 85;
                    } else {
                        basePercentage = 70;
                    }
                    
                    // Different connection types have different reliability
                    if (connType === "postgres") {
                        basePercentage += 10;
                    } else if (connType === "mysql") {
                        basePercentage += 5;
                    } else {
                        basePercentage -= 5;
                    }
                    
                    // Add some randomness
                    const randomFactor = Math.floor(Math.random() * 30) - 15;
                    let finalPercentage = basePercentage + randomFactor;
                    
                    // Ensure percentage is within valid range
                    finalPercentage = Math.min(100, Math.max(0, finalPercentage));
                    
                    // Total rows is between 50 and 200
                    const totalRows = Math.floor(Math.random() * 150) + 50;
                    const passedRows = Math.floor(totalRows * (finalPercentage / 100));
                    
                    sampleData.push({
                        id: idCounter++,
                        test_time: date.toISOString(),
                        type: connType,
                        db: db,
                        rule_type: ruleType,
                        rule_id: ruleId,
                        total_rows: totalRows,
                        total_rows_pass: passedRows,
                        pass_percentage: finalPercentage
                    });
                });
            });
        }
    }
    
    return sampleData;
}